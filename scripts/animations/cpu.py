"""CPU scheduling: FCFS, SJF, SRTF, round robin and priority.

Data: data/animations/cpu.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from fractions import Fraction

from .common import _fmt, _list, _same


POLICIES = {
    'fcfs': ('FCFS', 'First come, first served'),
    'sjf': ('SJF', 'Shortest job first (non-preemptive)'),
    'srtf': ('SRTF', 'Shortest remaining time first (preemptive)'),
    'rr': ('Round robin', 'Round robin, time slice {q}'),
    'priority': ('Priority', 'Priority (non-preemptive), {high} number = higher priority'),
    'priority-p': ('Priority', 'Priority (preemptive), {high} number = higher priority'),
}


NON_PREEMPTIVE = {'fcfs', 'sjf', 'priority'}


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



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'cpu-schedule': cpu_animation}
PLAYER = 'cpu'
TABS = 'schedules'
