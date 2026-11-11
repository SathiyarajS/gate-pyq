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


def heap_ops(spec):
    """Binary or d-ary heap: insert (sift up), delete the root (sift down) and bottom-up build.

    Each step records the array, the indices being compared or swapped, and a note.
    """
    d, kind = spec.get('arity', 2), spec.get('kind_of_heap', 'max')
    better = (lambda a, b: a > b) if kind == 'max' else (lambda a, b: a < b)
    word = 'larger' if kind == 'max' else 'smaller'
    a = list(spec.get('start', []))
    steps = [dict(arr=list(a), hi=[], note=(f"Start: the {kind}-heap " + str(a) + '.') if a else f"Start with an empty {kind}-heap.")]
    parent = lambda i: (i - 1) // d
    kids = lambda i: [c for c in range(d * i + 1, d * i + d + 1) if c < len(a)]

    def sift_down(i, n_note=''):
        while True:
            cs = kids(i)
            if not cs:
                steps.append(dict(arr=list(a), hi=[i], note=f"{a[i]} is now a leaf at index {i}, so it stops." if n_note else f"{a[i]} at index {i} has no children, so it stays."))
                return
            best = cs[0]
            for c in cs[1:]:
                if better(a[c], a[best]):
                    best = c
            listing = ', '.join(str(a[c]) for c in cs)
            if better(a[best], a[i]):
                steps.append(dict(arr=list(a), hi=[i, best], note=f"{a[i]} at index {i} has children {listing}; the {word} child {a[best]} beats it, so they swap."))
                a[i], a[best] = a[best], a[i]
                i, n_note = best, 'moved'
            else:
                steps.append(dict(arr=list(a), hi=[i], note=f"{a[i]} at index {i} has children {listing}; none beats it, so it stays."))
                return

    for op in spec['ops']:
        if op[0] == 'insert':
            for k in op[1]:
                a.append(k)
                i = len(a) - 1
                if i == 0:
                    steps.append(dict(arr=list(a), hi=[0], note=f"Insert {k}: it becomes the root."))
                    continue
                steps.append(dict(arr=list(a), hi=[i], note=f"Insert {k}: append it at index {i}, below {a[parent(i)]} at index {parent(i)}."))
                while i > 0 and better(a[i], a[parent(i)]):
                    q = parent(i)
                    a[i], a[q] = a[q], a[i]
                    steps.append(dict(arr=list(a), hi=[q, i], note=f"{k} beats its parent {a[i]}, so they swap; {k} moves up to index {q}."))
                    i = q
                if i > 0:
                    steps[-1]['note'] += f" {k} does not beat its parent {a[parent(i)]}, so it stops."
                else:
                    steps[-1]['note'] += f" {k} is now the root."
        elif op[0] == 'delete':
            for _ in range(op[1]):
                top, last = a[0], a.pop()
                if not a:
                    steps.append(dict(arr=[], hi=[], note=f"Remove {top}; the heap is now empty."))
                    continue
                a[0] = last
                steps.append(dict(arr=list(a), hi=[0], note=f"Remove the root {top}. Move the last element {last} to the root."))
                sift_down(0)
        elif op[0] == 'build':
            a = list(op[1])
            last_parent = parent(len(a) - 1)
            steps.append(dict(arr=list(a), hi=[], note=f"Build a {kind}-heap bottom-up: sift down each node that has children, from index {last_parent} back to 0."))
            for i in range(last_parent, -1, -1):
                sift_down(i)
        else:
            raise SystemExit('Unknown heap operation: ' + op[0])
    return steps, a


def heap_animation(qid, spec):
    steps, a = heap_ops(spec)
    want = spec['expect']
    got = a[:len(want)] if spec.get('prefix') else a
    if got != want:
        raise SystemExit(f'Animation for {qid} ends with {a}, not {want}')
    note = 'All done. Level order: ' + ', '.join(map(str, a)) + '.'
    if spec.get('prefix'):
        note += ' The first ' + str(len(want)) + ' entries: ' + ', '.join(map(str, want)) + '.'
    steps.append(dict(arr=list(a), hi=[], final=True, note=note))
    d = spec.get('arity', 2)
    title = ('Ternary ' if d == 3 else '') + ('max' if spec.get('kind_of_heap', 'max') == 'max' else 'min') + '-heap' + (f', children of i at {d}i+1 to {d}i+{d}' if d != 2 else '')
    return dict(kind='heap', arity=d, schedules=[dict(short='Heap', title=title[0].upper() + title[1:], steps=steps)], count=len(steps))


def bst_build(keys):
    """Insert keys in order into an unbalanced BST. Returns parent links, depths and steps."""
    root, left, right, depth, parent = None, {}, {}, {}, {}
    steps = [dict(shown=[], path=[], note='Start with an empty tree. Smaller keys go left, larger keys go right.')]
    for k in keys:
        if k in depth:
            raise SystemExit(f'Duplicate BST key {k}')
        if root is None:
            root, depth[k] = k, 0
            steps.append(dict(shown=list(depth), path=[k], key=k, note=f"Insert {k}: the tree is empty, so {k} is the root."))
            continue
        node, path, moves = root, [], []
        while True:
            path.append(node)
            side = left if k < node else right
            moves.append(f"{k} {'<' if k < node else '>'} {node}, go {'left' if k < node else 'right'}")
            if node in side:
                node = side[node]
            else:
                side[node] = k
                parent[k], depth[k] = node, depth[node] + 1
                break
        steps.append(dict(shown=list(depth), path=path + [k], key=k, note=f"Insert {k}: " + '; '.join(moves) + f". It becomes the {'left' if k < node else 'right'} child of {node}."))
    return dict(root=root, left=left, right=right, depth=depth, parent=parent), steps


def bst_animation(qid, spec):
    keys = spec['keys']
    tree, steps = bst_build(keys)
    if spec.get('from_preorder'):
        steps[0]['note'] = 'Inserting the keys in preorder rebuilds the same tree: each key arrives after its ancestors. ' + steps[0]['note']
    left, right, depth = tree['left'], tree['right'], tree['depth']
    order = []

    def walk(n, kind):
        if n is None:
            return
        if kind == 'preorder':
            order.append(n)
        walk(left.get(n), kind)
        if kind == 'inorder':
            order.append(n)
        walk(right.get(n), kind)
        if kind == 'postorder':
            order.append(n)

    q, want = spec['query'], spec['expect']
    note = 'All done.'
    traversal = None
    if q in ('inorder', 'preorder', 'postorder'):
        walk(tree['root'], q)
        got = order
        traversal = order
        # Show the traversal one node at a time.
        rule = {'inorder': 'left subtree, node, right subtree', 'preorder': 'node, left subtree, right subtree', 'postorder': 'left subtree, right subtree, node'}[q]
        steps.append(dict(shown=list(depth), path=[], out=[], note=f"Now the {q} traversal: {rule}."))
        for i, n in enumerate(order):
            steps.append(dict(shown=list(depth), path=[n], out=order[:i + 1], note=f"Visit {n} (position {i + 1})."))
        note += f" {q.capitalize()}: " + ', '.join(map(str, order)) + '.'
        if spec.get('position_of') is not None:
            got = order.index(spec['position_of']) + 1
            note += f" {spec['position_of']} is at position {got}."
    elif q == 'height':
        got = max(depth.values())
        deepest = [k for k in keys if depth[k] == got]
        note += f" The deepest node{'s are' if len(deepest) > 1 else ' is'} {_list([str(x) for x in deepest])}, {got} edges below the root, so the height is {got}."
    elif q == 'deepest':
        h = max(depth.values())
        got = [k for k in keys if depth[k] == h]
        note += f" The deepest level is {h} edges below the root: {_list([str(x) for x in got])}."
    elif q == 'depth':
        got = depth[spec['node']]
        path, n = [spec['node']], spec['node']
        while n in tree['parent']:
            n = tree['parent'][n]
            path.append(n)
        note += f" The path from {spec['node']} to the root is {' → '.join(map(str, path))}: {got} edges."
    elif q == 'subtrees':
        r = tree['root']

        def size(n):
            return 0 if n is None else 1 + size(left.get(n)) + size(right.get(n))
        got = [size(left.get(r)), size(right.get(r))]
        note += f" The root {r} has {got[0]} nodes in its left subtree and {got[1]} in its right."
    else:
        raise SystemExit(f'Unknown BST query for {qid}: {q}')
    if got != want:
        raise SystemExit(f'Animation for {qid} gives {got}, not {want}')
    steps.append(dict(shown=list(depth), path=[], out=traversal, final=True, note=note))
    rank = {k: i for i, k in enumerate(sorted(keys))}
    nodes = [[k, rank[k], depth[k], tree['parent'].get(k)] for k in keys]
    return dict(kind='bst', nodes=nodes, schedules=[dict(short='BST', title='Binary search tree' + (', built from its preorder' if spec.get('from_preorder') else ''), steps=steps)], count=len(steps))


def _log2(n, what):
    if n <= 0 or n & (n - 1):
        raise SystemExit(f'{what} = {n} is not a power of two')
    return n.bit_length() - 1


def _size(n, unit='B'):
    """2^k units in binary prefixes: 32768 B -> '32 KB'."""
    for p, name in ((60, 'E'), (50, 'P'), (40, 'T'), (30, 'G'), (20, 'M'), (10, 'K')):
        if n >= 1 << p and n % (1 << p) == 0:
            return f'{n >> p} {name}{unit}'
    return f'{n}{unit}' if unit.startswith(' ') else f'{n} {unit}'


def address_fields(spec):
    """Derive address fields (tag/index/offset, page number/offset) and related sizes.

    Every value is computed from the stated parameters; sizes are in addressable
    units unless the spec says otherwise.
    """
    mode, unit = spec['mode'], spec.get('unit', 'byte')
    U = 'B' if unit == 'byte' else ' words'
    rows, steps, fields, out = [], [], [], {}

    def step(name, value, how, note, field=None):
        if field:
            fields.insert(0, field)
        rows.append([name, value, how])
        steps.append(dict(fields=[list(f) for f in fields], rows=[list(r) for r in rows], note=note))

    steps.append(dict(fields=[], rows=[], note=spec.get('intro', 'Work out each field from the right: the offset first, then the index, and the tag is what is left.' if mode in ('cache', 'tlb') else 'Split the address into page number and offset, then size the tables.')))
    if 'address_bits' in spec:
        A = spec['address_bits']
        step('Address bits', A, 'given', f'Addresses are {A} bits.')
    elif 'memory' in spec:
        A = _log2(spec['memory'], 'memory size')
        step('Address bits', A, f'log₂({_size(spec["memory"], U)})', f'{_size(spec["memory"], U)} of {unit}-addressable memory needs {A}-bit addresses, since 2^{A} = {spec["memory"]}.')
    else:
        A = None
    out['address'] = A
    if mode == 'cache':
        cache, ways = spec['cache'], spec.get('ways', 1)
        block = spec.get('block')
        if block:
            off = _log2(block, 'block size')
            step('Offset bits', off, f'log₂({block})', f"A block holds {spec.get('block_text', _size(block, U))}" + (f' = {block} {unit}s' if spec.get('block_text') else '') + f", so the offset needs {off} bits.", ['Offset', off])
            out['offset'] = off
            lines = cache // block
            step('Lines', lines, f'{_size(cache, U)} ÷ {_size(block, U)}', f'The cache holds {_size(cache, U)} in blocks of {_size(block, U)}: {lines} lines.')
            out['lines'] = lines
            if ways == 'full':
                sets, idx = 1, 0
                step('Index bits', 0, 'fully associative', 'Fully associative: any block can go in any line, so there is no index field.')
            else:
                sets = lines // ways
                idx = _log2(sets, 'number of sets')
                how = f'{lines} ÷ {ways}' if ways > 1 else 'one line per set'
                word = 'line' if ways == 1 else 'set'
                step('Sets' if ways > 1 else 'Index bits', sets if ways > 1 else idx, how if ways > 1 else f'log₂({lines})',
                     (f'{ways}-way: {lines} lines in sets of {ways} gives {sets} sets.' if ways > 1 else f'Direct-mapped: each of the {lines} lines is its own set, so the index needs {idx} bits.'),
                     None if ways > 1 else ['Index', idx])
                if ways > 1:
                    step('Index bits', idx, f'log₂({sets})', f'Choosing one of {sets} sets needs {idx} bits.', ['Index', idx])
            out['sets'], out['index'] = sets, idx
            low = off + idx
        else:
            low = _log2(cache // ways, 'cache size ÷ ways')
            step('Index + offset bits', low, f'log₂({_size(cache, U)} ÷ {ways})', f'Each way holds {_size(cache // ways, U)}, and the index and offset together address one byte of a way: {low} bits, whatever the block size.', ['Index + offset', low])
        if A is not None:
            tag = A - low
            parts = ' − '.join(str(x) for x in [A] + [f[1] for f in fields])
            step('Tag bits', tag, parts, f'The tag is what is left: {parts} = {tag} bits.', ['Tag', tag])
            out['tag'] = tag
            if 'extra_bits' in spec:
                per = tag + spec['extra_bits']
                total = per * out['lines']
                step('Bits per line', per, f'{tag} + {spec["extra_bits"]}', f'Each line stores the {tag}-bit tag plus {spec["extra_bits"]} bits ({spec.get("extra_text", "status bits")}): {per} bits.')
                step('Directory bits', total, f'{per} × {out["lines"]}', f'Over {out["lines"]} lines: {per} × {out["lines"]} = {total} bits = {_size(total, " bits")}.')
                out['directory_bits'] = total
            if spec.get('tag_store'):
                total = tag * out['lines']
                step('Tag storage', total, f'{tag} × {out["lines"]}', f'All tags together: {tag} × {out["lines"]} = {total} bits = {_size(total // 8)}.' if total % 8 == 0 else f'All tags together: {tag} × {out["lines"]} = {total} bits.')
                out['tag_store_bits'] = total
            if 'split' in spec:
                addr = int(spec['split'], 16)
                bits = format(addr, f'0{A}b')
                vals, pos = {}, 0
                for name, w in fields:
                    chunk = bits[pos:pos + w]
                    vals[name] = int(chunk, 2) if chunk else 0
                    pos += w
                text = ', '.join(f'{n} {vals[n]:X}H' for n, _ in fields)
                step('Split of ' + spec['split'].upper() + 'H', text, 'cut the binary into fields', f'{spec["split"].upper()}H in binary is {bits}. Cutting it into fields: {text}.')
                out['split'] = {n: format(v, 'X') for n, v in vals.items()}
    elif mode == 'tlb':
        page, entries, ways = spec['page'], spec['entries'], spec.get('ways', 'full')
        off = _log2(page, 'page size')
        step('Page offset bits', off, f'log₂({_size(page)})', f'Pages are {_size(page)}, so the offset is {off} bits.', ['Offset', off])
        vpn = A - off
        step('Page number bits', vpn, f'{A} − {off}', f'The virtual page number is {A} − {off} = {vpn} bits.')
        sets = 1 if ways == 'full' else entries // ways
        idx = _log2(sets, 'TLB sets')
        if ways != 'full':
            step('TLB sets', sets, f'{entries} ÷ {ways}', f'{entries} entries, {ways}-way: {sets} sets, chosen by the low {idx} bits of the page number.', ['Index', idx])
        tag = vpn - idx
        step('Tag bits', tag, f'{vpn} − {idx}', f'The TLB tag is the rest of the page number: {vpn} − {idx} = {tag} bits.', ['Tag', tag])
        out.update(offset=off, vpn=vpn, sets=sets, index=idx, tag=tag)
    elif mode == 'page':
        page = spec['page']
        off = _log2(page, 'page size')
        step('Offset bits', off, f'log₂({_size(page)})', f'Pages are {_size(page)}, so the offset is {off} bits.', ['Offset', off])
        vpn = A - off
        step('Page number bits', vpn, f'{A} − {off}', f'The page number is the rest: {A} − {off} = {vpn} bits.', ['Page number', vpn])
        out.update(offset=off, vpn=vpn, entries=1 << vpn)
        step('Page-table entries', f'2^{vpn}', f'one per page', f'A one-level table has one entry per virtual page: 2^{vpn} entries.')
        if 'pte' in spec:
            pte = spec['pte']
            size = (1 << vpn) * pte
            step('Table size', _size(size), f'2^{vpn} × {pte} B', f'Each entry is {pte} bytes, so the table takes 2^{vpn} × {pte} = {_size(size)}.')
            out['table_bytes'] = size
            per = page // pte
            if spec.get('levels'):
                k = _log2(per, 'entries per page')
                levels = -(-vpn // k)
                step('Entries per page', per, f'{_size(page)} ÷ {pte} B', f'One page holds {per} entries, so each level resolves {k} bits.')
                step('Levels', levels, f'⌈{vpn} ÷ {k}⌉', f'{vpn} page-number bits at {k} per level need ⌈{vpn}/{k}⌉ = {levels} levels.')
                out['levels'] = levels
            if spec.get('per_page'):
                step('Entries per page', per, f'{_size(page)} ÷ {pte} B', f'One page holds {_size(page)} ÷ {pte} = {per} entries.')
                out['entries_per_page'] = per
            if 'physical_bits' in spec:
                frame = spec['physical_bits'] - off
                spare = pte * 8 - frame
                step('Frame number bits', frame, f'{spec["physical_bits"]} − {off}', f'Physical addresses are {spec["physical_bits"]} bits, so a frame number is {frame} bits.')
                step('Spare bits per entry', spare, f'{pte * 8} − {frame}', f'A {pte * 8}-bit entry has {spare} bits left for protection and other flags.')
                out['spare_bits'] = spare
    elif mode == 'translate':
        page, va, frames = spec['page'], spec['virtual'], spec['frames']
        pg, off = divmod(va, page)
        step('Page', pg, f'⌊{va} ÷ {page}⌋', f'{va} ÷ {page} = page {pg}, remainder {off}.')
        step('Offset', off, f'{va} mod {page}', f'The offset within the page is {off}.')
        fr = frames[pg]
        step('Frame', fr, f'page {pg} → frame {fr}', f'Page {pg} is in frame {fr}.')
        pa = fr * page + off
        step('Physical address', pa, f'{fr} × {page} + {off}', f'Physical address = {fr} × {page} + {off} = {pa}.')
        out['physical'] = pa
    elif mode == 'tlb-size':
        page, reach = spec['page'], spec['reach']
        entries = reach // page
        off = _log2(page, 'page size')
        step('Entries', entries, f'{_size(reach)} ÷ {_size(page)}', f'The TLB covers {_size(reach)} with {_size(page)} pages: {entries} entries.')
        vpn = _log2(spec['virtual'], 'virtual space') - off
        pfn = _log2(spec['physical'], 'physical space') - off
        step('Page number bits', vpn, f'log₂({_size(spec["virtual"])}) − {off}', f'{_size(spec["virtual"])} of virtual space in {_size(page)} pages: {vpn}-bit page numbers.')
        step('Frame number bits', pfn, f'log₂({_size(spec["physical"])}) − {off}', f'{_size(spec["physical"])} of physical memory: {pfn}-bit frame numbers.')
        extra = spec.get('extra_bits', 0)
        bits = vpn + pfn + extra
        step('Bits per entry', bits, f'{vpn} + {pfn} + {extra}', f'Each entry holds the page number, frame number and {extra} other bits ({spec.get("extra_text", "")}): {bits} bits = {bits // 8} bytes.' if bits % 8 == 0 else f'Each entry holds {bits} bits.')
        total = entries * bits // 8
        step('TLB size', total, f'{entries} × {bits // 8} B', f'{entries} entries × {bits // 8} bytes = {total} bytes.')
        out['tlb_bytes'] = total
    else:
        raise SystemExit('Unknown address mode: ' + mode)
    return steps, out, A


def fields_animation(qid, spec):
    steps, out, A = address_fields(spec)
    for k, v in spec['expect'].items():
        if out.get(k) != v:
            raise SystemExit(f'Animation for {qid}: {k} is {out.get(k)}, not {v}')
    steps[-1] = dict(steps[-1], final=True)
    titles = {'cache': 'Cache address fields', 'tlb': 'TLB tag', 'page': 'Paging', 'translate': 'Address translation', 'tlb-size': 'TLB size'}
    return dict(kind='address-fields', bits=A, schedules=[dict(short='Fields', title=titles[spec['mode']], steps=steps)], count=len(steps))


def load(root, question_ids):
    path = root / 'data/animations.json'
    if not path.exists():
        return {}
    out = {}
    for qid, spec in json.loads(path.read_text())['questions'].items():
        if qid not in question_ids:
            raise SystemExit('data/animations.json names an unknown question: ' + qid)
        kinds = {'cpu-schedule': cpu_animation, 'page-replace': page_animation, 'disk-schedule': disk_animation, 'hash-insert': hash_animation, 'heap': heap_animation, 'bst': bst_animation, 'address-fields': fields_animation}
        if spec['kind'] not in kinds:
            raise SystemExit('Unknown animation kind for ' + qid)
        out[qid] = kinds[spec['kind']](qid, spec)
    return out
