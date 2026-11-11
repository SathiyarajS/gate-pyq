"""Build-time step data for the 'Step through it' players (data/animations.json).

Each animation is simulated here; the build stops if a result differs from the
recorded expectation, so a player can never show a different answer from the key.
"""
import json
from fractions import Fraction

POLICIES = {
    'fcfs': ('FCFS', 'First come, first served'),
    'sjf': ('SJF', 'Shortest job first (non-preemptive)'),
    'srtf': ('SRTF', 'Shortest remaining time first (preemptive)'),
    'rr': ('Round robin', 'Round robin, time slice {q}'),
    'priority': ('Priority', 'Priority (non-preemptive), {high} number = higher priority'),
    'priority-p': ('Priority', 'Priority (preemptive), {high} number = higher priority'),
}
NON_PREEMPTIVE = {'fcfs', 'sjf', 'priority'}


def _fmt(x):
    x = Fraction(x).limit_denominator(1000)
    return str(x.numerator) if x.denominator == 1 else ('%.2f' % float(x)).rstrip('0').rstrip('.')


def _list(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]


def cpu_schedule(processes, policy, quantum=None, high='lower'):
    """Simulate one CPU-scheduling policy and return the Gantt segments and decision steps.

    processes: [name, arrival, burst] or [name, arrival, burst, priority], in table order.
    Ties go to the running process, then the earlier arrival, then table order.
    Round robin: processes arriving when a time slice ends join the queue before
    the preempted process.
    """
    if policy not in POLICIES:
        raise SystemExit('Unknown scheduling policy: ' + policy)
    if policy == 'rr' and not quantum:
        raise SystemExit('Round robin needs a time slice (quantum)')
    procs = [dict(name=p[0], arrival=p[1], burst=p[2], prio=p[3] if len(p) > 3 else None, left=p[2], done=None, i=i)
             for i, p in enumerate(processes)]
    if policy.startswith('priority') and any(p['prio'] is None for p in procs):
        raise SystemExit('Priority scheduling needs a priority for every process')
    rank = (lambda p: p['prio']) if high == 'lower' else (lambda p: -p['prio'])
    arrivals = sorted({p['arrival'] for p in procs})
    t, running, used, queue, segs, steps = 0, None, 0, [], [], []

    def pr(p):
        return f"{p['name']} (priority {p['prio']})"

    while any(p['done'] is None for p in procs):
        notes = []
        if running is not None and running['left'] == 0:
            notes.append(f"{running['name']} finishes.")
            running = None
        arrived = [p for p in procs if p['arrival'] == t]
        if arrived:
            notes.append(_list([f"{p['name']} arrives needing {p['burst']}" + (f", priority {p['prio']}" if policy.startswith('priority') else '') for p in arrived]) + '.')
        queue += arrived
        expired = None
        if policy == 'rr' and running is not None and used == quantum:
            if queue:
                expired, running = running, None
                queue.append(expired)
            else:
                used = 0
                notes.append(f"{running['name']}'s time slice ends, but nothing else is waiting, so it carries on.")
        if running is None and not queue:
            nxt = min(p['arrival'] for p in procs if p['arrival'] > t)
            notes.append(f'The CPU is idle until {nxt}.')
            steps.append(dict(t=t, run=None, rem=[p['left'] for p in procs], ready=[], note=' '.join(notes)))
            t = nxt
            continue
        # Choose who runs next.
        if policy in NON_PREEMPTIVE or policy == 'rr':
            if running is not None:
                choice = running
            elif policy in ('fcfs', 'rr'):
                choice = queue[0]
            elif policy == 'sjf':
                choice = min(queue, key=lambda p: (p['burst'], p['arrival'], p['i']))
            else:
                choice = min(queue, key=lambda p: (rank(p), p['arrival'], p['i']))
        else:
            measure = (lambda p: p['left']) if policy == 'srtf' else rank
            choice = min(queue + ([running] if running else []), key=lambda p: (measure(p), 0 if p is running else 1, p['arrival'], p['i']))
        others = [p for p in queue if p is not choice]
        # Explain the choice.
        if choice is running:
            if arrived and policy in NON_PREEMPTIVE:
                notes.append(f"{running['name']} keeps the CPU: this policy never interrupts a running process.")
            elif arrived and policy == 'rr':
                notes.append(f"{_list([p['name'] for p in arrived])} {'joins' if len(arrived) == 1 else 'join'} the back of the queue; {running['name']} carries on with its time slice.")
            elif arrived and policy == 'srtf':
                cmp = 'less than' if all(choice['left'] < p['left'] for p in arrived) else 'no more than'
                notes.append(f"{choice['name']} has {choice['left']} left, {cmp} " + _list([f"{p['name']}'s {p['left']}" for p in arrived]) + f", so {choice['name']} keeps running.")
            elif arrived and policy == 'priority-p':
                notes.append(f"{pr(choice)} still has the highest priority, so it keeps running.")
        elif running is not None:
            if policy == 'srtf':
                notes.append(f"{running['name']} has {running['left']} left, but {choice['name']} needs only {choice['left']}, so {choice['name']} takes the CPU.")
            else:
                notes.append(f"{pr(choice)} outranks {pr(running)}, so {choice['name']} takes the CPU; {running['name']} waits with {running['left']} left.")
            queue.append(running)
        else:
            if expired is not None:
                notes.append(f"{expired['name']} has used its time slice of {quantum} and goes to the back of the queue" + (' after the new arrival' + ('s' if len(arrived) > 1 else '') if arrived else '') + f". {choice['name']} is at the front, so it runs.")
            elif not others:
                notes.append(f"{choice['name']} is the only process waiting, so it runs.")
            elif policy == 'fcfs':
                notes.append(f"{choice['name']} arrived first among those waiting, so it runs.")
            elif policy == 'rr':
                notes.append(f"{choice['name']} is at the front of the queue, so it runs for up to {quantum}.")
            elif policy == 'sjf':
                notes.append('Waiting jobs and their bursts: ' + ', '.join(f"{p['name']} {p['burst']}" for p in sorted(queue, key=lambda p: p['i'])) + f". {choice['name']} is shortest, so it runs.")
            elif policy == 'srtf':
                notes.append('Remaining times: ' + ', '.join(f"{p['name']} {p['left']}" for p in sorted(queue, key=lambda p: p['i'])) + f". {choice['name']} is shortest, so it runs.")
            else:
                notes.append('Priorities of those waiting: ' + ', '.join(f"{p['name']} {p['prio']}" for p in sorted(queue, key=lambda p: p['i'])) + f". {choice['name']} has the highest, so it runs.")
        if choice is not running:
            used = 0
        if choice in queue:
            queue.remove(choice)
        # Run until the next event: completion, an arrival, or the end of the time slice.
        end = t + choice['left']
        future = [a for a in arrivals if a > t]
        if future:
            end = min(end, future[0])
        if policy == 'rr':
            end = min(end, t + quantum - used)
        steps.append(dict(t=t, run=choice['name'], rem=[p['left'] for p in procs], ready=[p['name'] for p in queue], note=' '.join(notes)))
        if segs and segs[-1][0] == choice['name'] and segs[-1][2] == t:
            segs[-1][2] = end
        else:
            segs.append([choice['name'], t, end])
        choice['left'] -= end - t
        used += end - t
        if choice['left'] == 0:
            choice['done'] = end
        running, t = choice, end
    short, title = POLICIES[policy]
    if policy == 'rr':
        short = f'Round robin ({quantum})'
    return dict(policy=policy, short=short, title=title.format(q=quantum, high=high), segs=segs, steps=steps, end=t,
                queue_label='Queue (front first)' if policy in ('fcfs', 'rr') else 'Waiting'), procs


def _result(procs, metric, process):
    """The value the question asks for, the final note and the final table columns."""
    by = {p['name']: p for p in procs}
    tat = {p['name']: p['done'] - p['arrival'] for p in procs}
    wait = {n: tat[n] - by[n]['burst'] for n in tat}
    if metric == 'order':
        order = [p['name'] for p in sorted(procs, key=lambda p: (p['done'], p['i']))]
        return order, 'All done. Completion order: ' + ', '.join(order) + '.', None
    if metric == 'completion':
        p = by[process]
        return p['done'], f"{process} finishes its CPU burst at {p['done']}.", None
    values = tat if metric == 'turnaround' else wait
    formula = 'completion − arrival' if metric == 'turnaround' else 'completion − arrival − burst'
    if process:
        p = by[process]
        parts = [p['done'], p['arrival']] + ([p['burst']] if metric == 'waiting' else [])
        return values[process], f"All done. {process}'s {metric} time = {formula} = {' − '.join(map(str, parts))} = {values[process]}.", metric
    avg = Fraction(sum(values.values()), len(values))
    return avg, f"All done. {metric.capitalize()} time = {formula}. Average = ({' + '.join(str(values[p['name']]) for p in procs)}) / {len(procs)} = {_fmt(avg)}.", metric


def _final(procs, metric, process, has_prio):
    cols = ['Process', 'Arrival', 'Burst'] + (['Priority'] if has_prio else []) + ['Done at']
    if metric in ('turnaround', 'waiting'):
        cols.append(metric.capitalize())
    rows = []
    for p in procs:
        r = [p['name'], p['arrival'], p['burst']] + ([p['prio']] if has_prio else []) + [p['done']]
        if metric == 'turnaround':
            r.append(p['done'] - p['arrival'])
        elif metric == 'waiting':
            r.append(p['done'] - p['arrival'] - p['burst'])
        rows.append(r)
    return dict(cols=cols, rows=rows, highlight=process, metric=metric in ('turnaround', 'waiting'))


def _same(value, expect):
    if isinstance(expect, list):
        return value == expect
    if isinstance(expect, str):
        return str(value) == expect
    return abs(float(value) - float(expect)) < 1e-9


def cpu_animation(qid, spec):
    metric, process = spec['metric'], spec.get('process')
    if metric not in ('turnaround', 'waiting', 'completion', 'order'):
        raise SystemExit(f'Unknown metric for {qid}: {metric}')
    has_prio = any(len(p) > 3 for p in spec['processes'])
    schedules, values = [], []
    for s in spec['schedules']:
        data, procs = cpu_schedule(spec['processes'], s['policy'], s.get('quantum'), spec.get('high', 'lower'))
        value, note, _ = _result(procs, metric, process)
        if not _same(value, s['expect']):
            raise SystemExit(f"Animation for {qid} ({s['policy']}) gives {value if isinstance(value, list) else float(value)}, not the expected {s['expect']}")
        if spec.get('then'):
            note += ' ' + spec['then']
        data['steps'].append(dict(t=data['end'], run=None, rem=[0] * len(procs), ready=[], final=True, note=note))
        data['final'] = _final(procs, metric, process, has_prio)
        schedules.append(data)
        values.append(value)
    compare = spec.get('compare')
    if compare:
        label = [f"{d['short']} {_fmt(v)}" for d, v in zip(schedules, values)]
        if compare == 'difference':
            got = abs(values[0] - values[1])
            line = f"Averages: {label[0]} and {label[1]}. Difference = {_fmt(got)}."
        elif compare == 'lowest':
            best = min(range(len(values)), key=lambda k: values[k])
            got = spec['schedules'][best]['policy']
            line = 'Averages: ' + ', '.join(label) + f". Lowest: {schedules[best]['short']}."
        else:
            raise SystemExit(f'Unknown comparison for {qid}: {compare}')
        if not _same(got, spec['expect_compare']):
            raise SystemExit(f'Animation for {qid} compares to {got}, not the expected {spec["expect_compare"]}')
        for d in schedules:
            d['steps'][-1]['note'] += ' ' + line
    names = [p[0] for p in spec['processes']]
    colors = spec.get('colors') or list(range(len(names)))
    if len(set(colors)) > 6 or any(not 0 <= c < 6 for c in colors):
        raise SystemExit(f'Animation for {qid} needs more than the six series colours; group processes with "colors"')
    out = dict(kind='cpu-schedule', processes=names, arrival=[p[1] for p in spec['processes']],
               burst=[p[2] for p in spec['processes']], colors=colors, schedules=schedules,
               count=sum(len(s['steps']) for s in schedules))
    if has_prio:
        out['priority'] = [p[3] for p in spec['processes']]
    return out


PAGE_POLICIES = {
    'fifo': ('FIFO', 'First in, first out'),
    'lru': ('LRU', 'Least recently used'),
    'optimal': ('Optimal', 'Optimal: replace the page used farthest in the future'),
    'optimal-window': ('Optimal (window {w})', 'Optimal, looking only {w} references ahead (including the current one)'),
}


def page_replace(refs, frames, policy, window=None):
    """Simulate demand paging with `frames` initially empty frames.

    A new page fills the first empty frame, else the victim's frame. Where the
    optimal policy has several pages it never needs again, the one loaded first goes
    (the fault count is the same whichever goes).
    """
    if policy not in PAGE_POLICIES:
        raise SystemExit('Unknown page-replacement policy: ' + policy)
    if policy == 'optimal-window' and not window:
        raise SystemExit('Windowed optimal needs a window')
    slots, loaded, used = [None] * frames, {}, {}
    steps = [dict(i=-1, frames=list(slots), fault=None, note=f"Start: {frames} empty frames. References: {', '.join(map(str, refs))}.")]
    faults = []
    for i, page in enumerate(refs):
        n = i + 1
        if page in slots:
            used[page] = i
            note = f"Reference {n}: page {page} is already in a frame, a hit."
            if policy == 'lru':
                note += f' It becomes the most recently used.'
            elif policy == 'fifo':
                note += ' FIFO order does not change on a hit.'
            steps.append(dict(i=i, frames=list(slots), fault=False, note=note, order=_page_order(policy, slots, loaded, used)))
            continue
        faults.append(n)
        note = f"Reference {n}: page {page} is not in memory, a fault."
        if None in slots:
            k = slots.index(None)
            note += ' It goes into an empty frame.'
            victim = None
        else:
            resident = [x for x in slots]
            if policy == 'fifo':
                victim = min(resident, key=lambda x: loaded[x])
                note += f" Load order (oldest first): {', '.join(str(x) for x in sorted(resident, key=lambda x: loaded[x]))}. Page {victim} was loaded first, so it is replaced."
            elif policy == 'lru':
                victim = min(resident, key=lambda x: used[x])
                note += ' Last used: ' + ', '.join(f"{x} at {used[x] + 1}" for x in sorted(resident, key=lambda x: used[x])) + f". Page {victim} is the least recently used, so it is replaced."
            else:
                ahead = refs[i:i + window] if policy == 'optimal-window' else refs[i:]
                nxt = {x: (i + ahead.index(x) + 1 if x in ahead else None) for x in resident}
                absent = [x for x in resident if nxt[x] is None]
                if absent:
                    victim = min(absent, key=lambda x: loaded[x])
                else:
                    victim = max(resident, key=lambda x: nxt[x])
                where = 'in the window ' + '[' + ', '.join(map(str, ahead)) + ']' if policy == 'optimal-window' else 'from here on'
                uses = ', '.join(f"{x} at {nxt[x]}" for x in sorted(resident, key=lambda x: (nxt[x] is None, nxt[x] or 0)) if nxt[x] is not None)
                gone = [x for x in sorted(absent, key=lambda x: loaded[x])]
                text = f" Next use {where}: " + (uses if uses else 'none of the resident pages')
                if gone:
                    text += ('; ' if uses else '') + ('page ' + str(gone[0]) + ' is' if len(gone) == 1 else 'pages ' + _list([str(x) for x in gone]) + ' are') + (' not used in it' if policy == 'optimal-window' else ' never used again')
                text += '.'
                if len(gone) > 1:
                    text += f" Any of them can go; page {victim}, loaded first, is replaced."
                elif gone:
                    text += f" So page {victim} is replaced."
                else:
                    text += f" Page {victim} is needed latest, so it is replaced."
                note += text
            k = slots.index(victim)
            del loaded[victim]
            used.pop(victim, None)
        slots[k] = page
        loaded[page] = i
        used[page] = i
        steps.append(dict(i=i, frames=list(slots), fault=True, slot=k, victim=victim, note=note, order=_page_order(policy, slots, loaded, used)))
    short, title = PAGE_POLICIES[policy]
    return dict(policy=policy, short=short.format(w=window), title=title.format(w=window), steps=steps), faults


def _page_order(policy, slots, loaded, used):
    pages = [x for x in slots if x is not None]
    if policy == 'fifo':
        return 'Load order (oldest first): ' + ', '.join(str(x) for x in sorted(pages, key=lambda x: loaded[x]))
    if policy == 'lru':
        return 'Recency (least recent first): ' + ', '.join(str(x) for x in sorted(pages, key=lambda x: used[x]))
    return ''


def page_animation(qid, spec):
    refs, frames, metric = spec['refs'], spec['frames'], spec.get('metric', 'faults')
    if metric not in ('faults', 'rate'):
        raise SystemExit(f'Unknown metric for {qid}: {metric}')
    out, counts = [], []
    for s in spec['policies']:
        data, faults = page_replace(refs, frames, s['policy'], s.get('window'))
        count = len(faults)
        value = Fraction(count, len(refs)) if metric == 'rate' else count
        if not _same(value, s['expect']):
            raise SystemExit(f"Animation for {qid} ({s['policy']}) gives {float(value)}, not the expected {s['expect']}")
        if 'positions' in s and s['positions'] != faults:
            raise SystemExit(f"Animation for {qid} ({s['policy']}) faults at {faults}, not {s['positions']}")
        note = f"All done. {count} faults in {len(refs)} references, at references {', '.join(map(str, faults))}."
        if metric == 'rate':
            note += f" Fault rate = {count} / {len(refs)} = {_fmt(value)}."
        data['steps'].append(dict(i=len(refs), frames=data['steps'][-1]['frames'], fault=None, final=True, note=note))
        out.append(data)
        counts.append(count)
    compare = spec.get('compare')
    if compare:
        label = [f"{d['short']} {c}" for d, c in zip(out, counts)]
        if compare == 'difference':
            got = abs(counts[0] - counts[1])
            line = f"Faults: {label[0]} and {label[1]}. Difference = {got}."
        elif compare == 'rank':
            ranked = sorted(range(len(counts)), key=lambda k: counts[k])
            if len(set(counts)) < len(counts):
                raise SystemExit(f'Animation for {qid}: equal fault counts cannot be ranked strictly')
            got = [spec['policies'][k]['policy'] for k in ranked]
            line = 'Faults: ' + ' < '.join(label[k] for k in ranked) + '.'
        else:
            raise SystemExit(f'Unknown comparison for {qid}: {compare}')
        if not _same(got, spec['expect_compare']):
            raise SystemExit(f'Animation for {qid} compares to {got}, not the expected {spec["expect_compare"]}')
        for d in out:
            d['steps'][-1]['note'] += ' ' + line
    return dict(kind='page-replace', refs=refs, frames=frames, schedules=out, count=sum(len(d['steps']) for d in out))


DISK_POLICIES = {
    'fcfs': ('FCFS', 'First come, first served'),
    'sstf': ('SSTF', 'Shortest seek time first'),
    'scan': ('SCAN', 'SCAN: sweep to the end of the disk, then reverse'),
    'look': ('LOOK', 'LOOK: sweep to the last request, then reverse'),
    'cscan': ('C-SCAN', 'C-SCAN: sweep up to the end, return to the start, sweep up again'),
    'clook': ('C-LOOK', 'C-LOOK: sweep up to the last request, jump to the lowest request, sweep up again'),
}


def disk_schedule(start, requests, policy, direction='up', lo=0, hi=None):
    """Simulate disk-head scheduling. Returns the moves [from, to, served] and the steps.

    The circular policies sweep upwards; their return jump counts as head movement.
    SSTF stops the build on a distance tie, since the question must then state a rule.
    """
    if policy not in DISK_POLICIES:
        raise SystemExit('Unknown disk-scheduling policy: ' + policy)
    if policy in ('scan', 'cscan') and hi is None:
        raise SystemExit('SCAN and C-SCAN need the last cylinder')
    pending, pos, up = list(requests), start, direction == 'up'
    moves, steps, total = [], [], 0
    steps.append(dict(pos=start, pending=list(pending), note=f"The head starts at {start}" + ('' if policy in ('fcfs', 'sstf') else f", moving {'up' if up else 'down'}") + f". Pending: {', '.join(map(str, pending))}."))

    def go(target, why, served=True):
        nonlocal pos, total
        d = abs(target - pos)
        total += d
        moves.append([pos, target, served])
        if served:
            pending.remove(target)
        steps.append(dict(pos=target, pending=list(pending), note=f"{why} Move {pos} → {target}: {d}. Total so far {total}."))
        pos = target

    if policy == 'fcfs':
        while pending:
            go(pending[0], f"Next in arrival order is {pending[0]}.")
    elif policy == 'sstf':
        while pending:
            dist = sorted((abs(r - pos), r) for r in pending)
            if len(dist) > 1 and dist[0][0] == dist[1][0] and dist[0][1] != dist[1][1]:
                raise SystemExit(f'SSTF tie at {pos} between {dist[0][1]} and {dist[1][1]}')
            nearest = dist[0][1]
            go(nearest, ('Distances: ' + ', '.join(f"{r} is {abs(r - pos)} away" for r in pending) + f". Nearest is {nearest}.") if len(pending) > 1 else f"Only {nearest} is left.")
    else:
        def ahead(upwards):
            return sorted([r for r in pending if (r >= pos if upwards else r <= pos)], reverse=not upwards)
        while pending:
            nxt = ahead(up)
            if nxt:
                go(nxt[0], f"Moving {'up' if up else 'down'}, the next request is {nxt[0]}.")
                continue
            if policy in ('scan', 'cscan') and pos != (hi if up else lo):
                end = hi if up else lo
                go(end, f"No more requests {'above' if up else 'below'}; {DISK_POLICIES[policy][0]} still runs to the end of the disk.", served=False)
                continue
            if policy in ('scan', 'look'):
                up = not up
                steps[-1]['note'] += f" The head now reverses and moves {'up' if up else 'down'}."
                continue
            # Circular: return to the lowest point and continue upwards.
            target = lo if policy == 'cscan' else min(pending)
            what = f"returns to cylinder {lo}" if policy == 'cscan' else f"jumps to the lowest pending request, {target}"
            go(target, f"No more requests above; {DISK_POLICIES[policy][0]} {what}. The jump counts as head movement.", served=policy == 'clook')
    short, title = DISK_POLICIES[policy]
    return dict(policy=policy, short=short, title=title, moves=moves, steps=steps, total=total)


def disk_animation(qid, spec):
    metric = spec.get('metric', 'movement')
    if metric not in ('movement', 'cost'):
        raise SystemExit(f'Unknown metric for {qid}: {metric}')
    out, totals = [], []
    for s in spec['policies']:
        data = disk_schedule(spec['start'], spec['requests'], s['policy'], spec.get('direction', 'up'), spec.get('lo', 0), spec.get('hi'))
        parts = [abs(b - a) for a, b, _ in data['moves']]
        note = f"All done. Total head movement = {' + '.join(map(str, parts))} = {data['total']} cylinders."
        value = data['total']
        if metric == 'cost':
            c = spec['cost']
            up = spec.get('direction', 'up') == 'up'
            reversals = 0
            for a, b, _ in data['moves']:
                if b != a and (b > a) != up:
                    reversals += 1
                    up = b > a
            value = Fraction(data['total'] * c['per'], c['cylinders']) + reversals * c['reversal']
            note += f" The head changes direction {reversals} times. Cost = {data['total']}/{c['cylinders']} × {c['per']} + {reversals} × {c['reversal']} = {_fmt(value)}."
        if not _same(value, s['expect']):
            raise SystemExit(f"Animation for {qid} ({s['policy']}) gives {float(value)}, not the expected {s['expect']}")
        if s.get('path') and [m[1] for m in data['moves']] != s['path']:
            raise SystemExit(f"Animation for {qid} ({s['policy']}) visits {[m[1] for m in data['moves']]}, not {s['path']}")
        if spec.get('then'):
            note += ' ' + spec['then']
        data['steps'].append(dict(pos=data['steps'][-1]['pos'], pending=[], final=True, note=note))
        out.append(data)
        totals.append(data['total'])
    if spec.get('compare') == 'difference':
        got = abs(totals[0] - totals[1])
        if not _same(got, spec['expect_compare']):
            raise SystemExit(f'Animation for {qid} compares to {got}, not the expected {spec["expect_compare"]}')
        for d in out:
            d['steps'][-1]['note'] += f" {out[0]['short']} {totals[0]}, {out[1]['short']} {totals[1]}: difference {got}."
    elif spec.get('compare'):
        raise SystemExit(f'Unknown comparison for {qid}')
    marks = [spec['start']] + spec['requests'] + [x for x in (spec.get('lo', 0), spec.get('hi')) if x is not None]
    return dict(kind='disk-schedule', start=spec['start'], requests=spec['requests'], lo=spec.get('lo', 0),
                hi=spec.get('hi') if spec.get('hi') is not None else max(marks), schedules=out,
                count=sum(len(d['steps']) for d in out))


HASH_METHODS = {'chaining': 'Separate chaining', 'linear': 'Open addressing, linear probing',
                'quadratic': 'Open addressing, quadratic probing', 'double': 'Open addressing, double hashing'}


def _hash_text(spec):
    a, b, m = spec.get('a', 1), spec.get('b', 0), spec['size']
    inner = ('k' if a == 1 else f'{a}k') + (f' + {b}' if b else '')
    return (f'({inner}) mod {m}' if b or a != 1 else f'k mod {m}'), (lambda k: (a * k + b) % m)


def hash_insert(spec):
    """Insert keys in order. Returns the table after each key and a note on the probes."""
    m, method, keys = spec['size'], spec['method'], spec['keys']
    if method not in HASH_METHODS:
        raise SystemExit('Unknown hashing method: ' + method)
    text, h = _hash_text(spec)
    if method == 'double':
        c, d = spec['h2']['c'], spec['h2']['d']
        h2 = lambda k: c + k % d
    table = [[] for _ in range(m)] if method == 'chaining' else [None] * m
    steps = [dict(key=None, table=_copy(table), slot=None, probed=[], note=f"Empty table with {m} slots (0 to {m - 1}). h(k) = {text}; {HASH_METHODS[method].lower()}." + (f" Probe i uses (h(k) + i·h2(k)) mod {m}, with h2(k) = {c} + (k mod {d})." if method == 'double' else ''))]
    for k in keys:
        home = h(k)
        if method == 'chaining':
            table[home].append(k)
            steps.append(dict(key=k, table=_copy(table), slot=home, probed=[], note=f"h({k}) = {home}. {k} joins the chain at slot {home}" + (f", which now holds {len(table[home])} keys." if len(table[home]) > 1 else '.')))
            continue
        probed, note = [], f"h({k}) = {home}."
        if method == 'double':
            step2 = h2(k)
            note += f" h2({k}) = {c} + ({k} mod {d}) = {step2}."
        for i in range(m):
            slot = (home + (i if method == 'linear' else i * i if method == 'quadratic' else i * step2)) % m
            if table[slot] is None:
                break
            probed.append(slot)
        else:
            raise SystemExit(f'No free slot for {k}')
        if probed:
            hits = _list([f"slot {x} holds {table[x]}" for x in probed])
            note += ' ' + hits[0].upper() + hits[1:] + (', a collision.' if len(probed) == 1 else ': collisions.')
        note += f" Slot {slot} is empty, so {k} goes there."
        table[slot] = k
        steps.append(dict(key=k, table=_copy(table), slot=slot, probed=probed, note=note))
    return steps, table


def _copy(table):
    return [list(x) if isinstance(x, list) else x for x in table]


def hash_animation(qid, spec):
    steps, table = hash_insert(spec)
    expect, m = spec['expect'], spec['size']
    note = 'All done.'
    if 'table' in expect:
        if table != expect['table']:
            raise SystemExit(f'Animation for {qid} ends with {table}, not {expect["table"]}')
        note += ' Final table: ' + ', '.join(f"{i}: {v}" for i, v in enumerate(table) if v not in (None, [])) + '.'
    if 'slot_of' in expect:
        for k, slot in expect['slot_of'].items():
            if table.index(int(k)) != slot:
                raise SystemExit(f'Animation for {qid} puts {k} in slot {table.index(int(k))}, not {slot}')
            note += f' {k} ends up in slot {slot}.'
    if 'empty' in expect:
        empty = [i for i, v in enumerate(table) if v is None]
        if empty != expect['empty']:
            raise SystemExit(f'Animation for {qid} leaves {empty} empty, not {expect["empty"]}')
        note += ' Empty slots: ' + ', '.join(map(str, empty)) + '.'
    if 'chains' in expect:
        lens = [len(x) for x in table]
        got = dict(max=max(lens), min=min(lens), avg=float(Fraction(sum(lens), m)))
        for k, v in expect['chains'].items():
            if abs(got[k] - v) > 1e-9:
                raise SystemExit(f'Animation for {qid}: chain {k} is {got[k]}, not {v}')
        note += f" Chain lengths: {', '.join(map(str, lens))}. Longest {got['max']}, shortest {got['min']}, average {sum(lens)}/{m} = {_fmt(Fraction(sum(lens), m))}."
    steps.append(dict(key=None, table=_copy(table), slot=None, probed=[], final=True, note=note))
    return dict(kind='hash-insert', size=m, chaining=spec['method'] == 'chaining', keys=spec['keys'],
                schedules=[dict(short=HASH_METHODS[spec['method']], title=HASH_METHODS[spec['method']] + ', h(k) = ' + _hash_text(spec)[0], steps=steps)],
                count=len(steps))


def load(root, question_ids):
    path = root / 'data/animations.json'
    if not path.exists():
        return {}
    out = {}
    for qid, spec in json.loads(path.read_text())['questions'].items():
        if qid not in question_ids:
            raise SystemExit('data/animations.json names an unknown question: ' + qid)
        kinds = {'cpu-schedule': cpu_animation, 'page-replace': page_animation, 'disk-schedule': disk_animation, 'hash-insert': hash_animation}
        if spec['kind'] not in kinds:
            raise SystemExit('Unknown animation kind for ' + qid)
        out[qid] = kinds[spec['kind']](qid, spec)
    return out
