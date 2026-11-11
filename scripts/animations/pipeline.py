"""Instruction pipelines: a stage-by-cycle grid for a given instruction sequence.

Data: data/animations/pipeline.json. A spec states the stages, the instructions
(with their registers when data dependencies matter), how many cycles each stage
takes, forwarding, a taken branch, and the expected answer. Everything else is
computed here, and the build stops on any difference.

Timing model. Cycles are numbered from 1. Each stage holds one instruction at a
time and instructions stay in program order. Two ways of handing work on are
simulated:
  - 'blocking': an instruction that has finished a stage waits in it until the
    next stage is free, so the stage behind it stays occupied (no buffers);
  - 'buffered': a finished instruction leaves its stage for a buffer, freeing the
    stage at once.
A spec names the model the player shows, and the other one is simulated too: if
the two give different totals the build stops, because the answer would then
depend on a convention the question does not state.

With forwarding {from: F, to: U}, a dependent instruction may start stage U in
the cycle after its producer finishes stage F. A taken branch {at, target,
resolve: R} stops fetching until the branch has finished stage R.
In 'hazards' mode the instructions run one per cycle with no stalls, and every
true dependency is checked against the register timing (reads in the second
half of the read stage, writes in the first half of the write stage).
"""
from .common import _fmt, _list


def _range(a, b):
    return str(a) if a == b else f'{a}–{b}'


def _parse(qid, spec):
    stages = spec['stages']
    if len(set(stages)) != len(stages):
        raise SystemExit(f'{qid}: a stage is listed twice')
    instrs = []
    for k, ins in enumerate(spec['instructions']):
        name = ins.get('name') or f'I{k + 1}'
        if 'cycles' in ins:
            dur = ins['cycles']
            if len(dur) != len(stages):
                raise SystemExit(f'{qid}: {name} gives {len(dur)} stage times for {len(stages)} stages')
        else:
            op = ins.get('op')
            dur = []
            for s in stages:
                table = spec.get('stage_cycles', {}).get(s, {})
                if isinstance(table, int):
                    dur.append(table)
                elif op in table:
                    dur.append(table[op])
                elif '*' in table:
                    dur.append(table['*'])
                elif table:
                    raise SystemExit(f'{qid}: no {s} time for {op}')
                else:
                    dur.append(1)
        if any(not isinstance(d, int) or d < 1 for d in dur):
            raise SystemExit(f'{qid}: stage times must be positive whole cycles')
        instrs.append(dict(name=name, text=ins.get('text', name), dest=ins.get('dest'), src=ins.get('src', []), dur=dur))
    if len({i['name'] for i in instrs}) != len(instrs):
        raise SystemExit(f'{qid}: an instruction name is repeated')
    return stages, instrs


def executed(qid, instrs, branch):
    """The instructions that run, in order: a taken branch skips to its target."""
    if not branch:
        return instrs, None
    names = [i['name'] for i in instrs]
    if branch['at'] not in names or branch['target'] not in names:
        raise SystemExit(f'{qid}: the branch names an unknown instruction')
    a, t = names.index(branch['at']), names.index(branch['target'])
    if t <= a:
        raise SystemExit(f'{qid}: only forward branches are modelled')
    return instrs[:a + 1] + instrs[t:], instrs[a + 1:t]


def deps(instrs):
    """True (read-after-write) dependencies: (producer index, consumer index, register)."""
    out = []
    for c, ins in enumerate(instrs):
        for r in ins['src']:
            for p in range(c - 1, -1, -1):
                if instrs[p]['dest'] == r:
                    out.append((p, c, r))
                    break
    return out


def schedule(stages, instrs, model, forward=None, branch=None):
    """Start cycle of every (instruction, stage), and why each start is when it is."""
    if model not in ('blocking', 'buffered'):
        raise SystemExit('Unknown pipeline model: ' + model)
    n, m = len(instrs), len(stages)
    start = [[0] * m for _ in range(n)]
    why = [[None] * m for _ in range(n)]
    dd = deps(instrs) if forward else []
    fi = stages.index(forward['from']) if forward else None
    # 'at': 'end' means the value is latched into stage `to` as the producer finishes, so the
    # dependent's following stage is the one that waits; otherwise stage `to` itself waits.
    ui = stages.index(forward['to']) + (forward.get('at') == 'end') if forward else None
    bi = stages.index(branch['resolve']) if branch else None
    for i, ins in enumerate(instrs):
        d = ins['dur']
        for j in range(m):
            cands = []
            if j == 0:
                cands.append((1, 'first'))
            else:
                cands.append((start[i][j - 1] + d[j - 1], 'work'))
            if i > 0:
                if model == 'buffered' or j == m - 1:
                    free = start[i - 1][j] + instrs[i - 1]['dur'][j]
                else:
                    free = start[i - 1][j + 1]
                cands.append((free, ('busy', i - 1)))
                if j == 0 and branch and instrs[i - 1]['name'] == branch['at']:
                    cands.append((start[i - 1][bi] + instrs[i - 1]['dur'][bi], ('branch', i - 1)))
            if forward and j == ui:
                for p, c, r in dd:
                    if c == i:
                        cands.append((start[p][fi] + instrs[p]['dur'][fi], ('data', p, r)))
            best = max(c for c, _ in cands)
            start[i][j] = best
            # Why the stage starts when it does: every constraint that is binding and later than the
            # instruction's own readiness (end of its previous stage, or the cycle after the previous fetch).
            ready = start[i][j - 1] + d[j - 1] if j else (start[i - 1][0] + 1 if i else 1)
            why[i][j] = [w for c, w in cands if c == best and isinstance(w, tuple)] if best > ready else []
    return start, why


def total(start, instrs):
    return start[-1][-1] + instrs[-1]['dur'][-1] - 1


def grid_row(stages, start, instrs, i, model):
    """One instruction's cells: (cycle, stage, kind) with kind work or stall (held in a stage)."""
    cells, d = [], instrs[i]['dur']
    for j, s in enumerate(stages):
        a = start[i][j]
        for c in range(a, a + d[j]):
            cells.append([c, s, 'work'])
        if j + 1 < len(stages) and model == 'blocking':
            for c in range(a + d[j], start[i][j + 1]):
                cells.append([c, s, 'stall'])
    return cells


def _row_note(stages, start, why, instrs, i, model):
    ins, d = instrs[i], instrs[i]['dur']
    parts = []
    for j, s in enumerate(stages):
        a, b = start[i][j], start[i][j] + d[j] - 1
        text = f"{s} {_range(a, b)}"
        reasons = []
        for w in why[i][j]:
            if w[0] == 'busy':
                reasons.append(f"{s} is busy with {instrs[w[1]]['name']} until cycle {a - 1}")
            elif w[0] == 'data':
                reasons.append(f"it needs {w[2]} from {instrs[w[1]]['name']}, forwarded at the end of cycle {a - 1}")
            elif w[0] == 'branch':
                reasons.append(f"fetching waits until {instrs[w[1]]['name']} is resolved in cycle {a - 1}")
        if reasons:
            text += ' (' + '; '.join(reasons) + ')'
        parts.append(text)
    held = []
    if model == 'blocking':
        for j in range(len(stages) - 1):
            a, b = start[i][j] + d[j], start[i][j + 1] - 1
            if b >= a:
                held.append(f"waits in {stages[j]} during {_range(a, b)}")
    elif i:
        for j in range(1, len(stages)):
            a, b = start[i][j - 1] + d[j - 1], start[i][j] - 1
            if b >= a:
                held.append(f"waits in a buffer before {stages[j]} during {_range(a, b)}")
    note = f"{ins['name']}" + (f" ({ins['text']})" if ins['text'] != ins['name'] else '') + ': ' + ', '.join(parts) + '.'
    if held:
        note += ' It ' + _list(held) + '.'
    return note


def pipeline_animation(qid, spec):
    stages, instrs = _parse(qid, spec)
    mode, expect = spec.get('mode', 'timing'), spec['expect']
    if mode == 'hazards':
        return hazard_animation(qid, spec, stages, instrs)
    branch, forward, model = spec.get('branch'), spec.get('forward'), spec.get('model', 'blocking')
    for st in ([forward['from'], forward['to']] if forward else []) + ([branch['resolve']] if branch else []):
        if st not in stages:
            raise SystemExit(f'{qid}: unknown stage {st}')
    if forward and forward.get('at') == 'end' and forward['to'] == stages[-1]:
        raise SystemExit(f'{qid}: nothing follows {forward["to"]}')
    run, skipped = executed(qid, instrs, branch)
    start, why = schedule(stages, run, model, forward, branch)
    other = 'buffered' if model == 'blocking' else 'blocking'
    alt, _ = schedule(stages, run, other, forward, branch)
    cycles = total(start, run)
    if total(alt, run) != cycles:
        raise SystemExit(f'{qid}: the {model} and {other} pipeline models give {cycles} and {total(alt, run)} cycles; the answer depends on an unstated convention')
    steps = []
    intro = f"{len(run)} instructions, stages {', '.join(stages)}. Each stage holds one instruction at a time, in program order."
    if skipped:
        intro += f" {branch['at']} is a taken branch to {branch['target']}, so {_list([x['name'] for x in skipped])} never run" + ('s' if len(skipped) == 1 else '') + '.'
    if forward and forward.get('at') == 'end':
        nxt = stages[stages.index(forward['to']) + 1]
        intro += f" A result is forwarded from the end of {forward['from']} into a dependent instruction's {forward['to']}, so the dependent can start {nxt} in the next cycle."
    elif forward:
        intro += f" A result is forwarded from the end of {forward['from']} to the start of a dependent instruction's {forward['to']}."
    if model == 'blocking':
        intro += ' An instruction that cannot move on waits in its stage.'
    steps.append(dict(row=-1, rows=[], note=intro))
    rows = []
    for i in range(len(run)):
        rows.append(grid_row(stages, start, run, i, model))
        note = _row_note(stages, start, why, run, i, model)
        if branch and run[i]['name'] == branch['at']:
            note += f" The branch is resolved at the end of {branch['resolve']} in cycle {start[i][stages.index(branch['resolve'])] + run[i]['dur'][stages.index(branch['resolve'])] - 1}; with no prediction nothing more is fetched before then."
        steps.append(dict(row=i, rows=[list(map(list, r)) for r in rows], note=note))
    final = f"All done. The last instruction, {run[-1]['name']}, finishes {stages[-1]} in cycle {cycles}, so the sequence takes {cycles} cycles."
    got = dict(cycles=cycles)
    if 'stage_ns' in spec:
        ns = spec['stage_ns']
        if len(ns) != len(stages):
            raise SystemExit(f'{qid}: stage_ns does not match the stages')
        clock = max(ns) + spec.get('buffer_ns', 0)
        got['clock_ns'] = clock
        got['time_ns'] = cycles * clock
        final += f" The clock period is the slowest stage plus the buffer delay: {_fmt(max(ns))} + {_fmt(spec.get('buffer_ns', 0))} = {_fmt(clock)} ns, so the time is {cycles} × {_fmt(clock)} = {_fmt(cycles * clock)} ns."
    for k, v in expect.items():
        if k not in got:
            raise SystemExit(f'{qid}: unknown pipeline expectation {k}')
        if abs(got[k] - v) > 1e-9:
            raise SystemExit(f'Animation for {qid} gives {k} = {got[k]}, not the expected {v}')
    steps.append(dict(row=len(run), rows=[list(map(list, r)) for r in rows], final=True, note=final))
    title = ('Instructions wait in their stage when the next stage is busy' if model == 'blocking'
             else 'Finished work waits in a buffer between stages')
    return dict(kind='pipeline', stages=stages, names=[x['name'] for x in run], texts=[x['text'] for x in run], cycles=cycles,
                schedules=[dict(short='Pipeline', title=title, steps=steps)], count=len(steps))


def hazard_animation(qid, spec, stages, instrs):
    read, write = spec['read_stage'], spec['write_stage']
    ri, wi = stages.index(read), stages.index(write)
    if any(d != 1 for x in instrs for d in x['dur']):
        raise SystemExit(f'{qid}: hazard mode needs one cycle per stage')
    cyc = lambda i, j: i + j + 1
    found, steps = [], [dict(row=-1, rows=[], note=f"With no stalls, instruction k is in stage j in cycle k + j − 1. Registers are read in the second half of {read} and written in the first half of {write}, so a value written in a cycle can be read in that same cycle.")]
    rows = []
    for c, ins in enumerate(instrs):
        rows.append([[cyc(c, j), s, 'work'] for j, s in enumerate(stages)])
        parts = []
        for p, cc, r in deps(instrs):
            if cc != c:
                continue
            rc, wc = cyc(c, ri), cyc(p, wi)
            if rc < wc:
                found.append([instrs[p]['name'], ins['name'], r])
                parts.append(f"it reads {r} in {read} in cycle {rc}, but {instrs[p]['name']} writes {r} only in {write} in cycle {wc}: a read-after-write hazard")
            else:
                parts.append(f"it reads {r} in cycle {rc}, " + ('the same cycle' if rc == wc else 'after the cycle') + f" {instrs[p]['name']} writes it in {write}" + (' (write first, then read)' if rc == wc else '') + ': no hazard')
        note = f"{ins['name']} ({ins['text']}): " + ('; '.join(parts) if parts else 'it uses no register written by an earlier instruction') + '.'
        steps.append(dict(row=c, rows=[list(map(list, r)) for r in rows], note=note[0].upper() + note[1:]))
    want = spec['expect']['hazards']
    if sorted(found) != sorted(want):
        raise SystemExit(f'Animation for {qid} finds hazards {found}, not {want}')
    final = 'All done. Read-after-write hazards without forwarding: ' + _list([f"{a}→{b} on {r}" for a, b, r in found]) + '.'
    steps.append(dict(row=len(instrs), rows=[list(map(list, r)) for r in rows], final=True, note=final))
    return dict(kind='pipeline', stages=stages, names=[x['name'] for x in instrs], texts=[x['text'] for x in instrs], cycles=len(instrs) + len(stages) - 1,
                schedules=[dict(short='Hazards', title=f'No stalls; reads in the second half of {read}, writes in the first half of {write}', steps=steps)], count=len(steps))


KINDS = {'pipeline': pipeline_animation}
PLAYER = 'pipeline'
