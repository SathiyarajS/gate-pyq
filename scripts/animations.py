"""Build-time step data for the 'Step through it' players (data/animations.json).

Each animation is simulated here; the build stops if a result differs from the
recorded expectation, so a player can never show a different answer from the key.
"""
import json
from fractions import Fraction

POLICY_NAMES = {'srtf': 'Shortest remaining time first (preemptive)', 'sjf': 'Shortest job first (non-preemptive)'}


def _fmt(x):
    x = Fraction(x).limit_denominator(1000)
    return str(x.numerator) if x.denominator == 1 else ('%.2f' % float(x)).rstrip('0').rstrip('.')


def _list(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]


def cpu_schedule(processes, policy, metric):
    """Simulate SRTF or non-preemptive SJF. Ties keep the running process, then the earlier arrival."""
    procs = [dict(name=n, arrival=a, burst=b, left=b, done=None) for n, a, b in processes]
    order = {p['name']: i for i, p in enumerate(procs)}
    events = sorted({p['arrival'] for p in procs})
    t, running, segs, steps = 0, None, [], []
    while any(p['done'] is None for p in procs):
        arrived = [p for p in procs if p['arrival'] == t]
        finished = [p for p in procs if p['done'] == t and p['left'] == 0 and p.get('_noted') is None]
        for p in finished: p['_noted'] = True
        ready = [p for p in procs if p['arrival'] <= t and p['left'] > 0]
        notes = []
        if finished: notes.append(_list([p['name'] for p in finished]) + ' finishes.')
        if arrived: notes.append(_list([f"{p['name']} arrives needing {p['burst']}" for p in arrived]) + '.')
        if not ready:
            nxt = min(p['arrival'] for p in procs if p['left'] > 0)
            notes.append(f'The CPU is idle until {nxt}.')
            steps.append(dict(t=t, run=None, rem=[p['left'] for p in procs], ready=[], note=' '.join(notes)))
            t = nxt; running = None; continue
        key = lambda p: (p['left'] if policy == 'srtf' else p['burst'], 0 if p is running else 1, p['arrival'], order[p['name']])
        if policy == 'sjf' and running is not None and running['left'] > 0:
            choice = running
            if arrived: notes.append(f"{running['name']} keeps the CPU: this policy never interrupts a running job.")
        else:
            choice = min(ready, key=key)
            others = [p for p in ready if p is not choice]
            measure = 'left' if policy == 'srtf' else 'burst'
            if running is not None and running['left'] > 0 and choice is not running:
                notes.append(f"{running['name']} has {running['left']} left, but {choice['name']} needs only {choice['left']}, so {choice['name']} takes the CPU.")
            elif running is not None and running['left'] > 0 and arrived:
                rivals = [p for p in arrived if p is not choice]
                cmp = 'less than' if all(choice['left'] < p[measure] for p in rivals) else 'no more than'
                notes.append(f"{choice['name']} has {choice['left']} left, {cmp} " + _list([f"{p['name']}'s {p[measure]}" for p in rivals]) + f", so {choice['name']} keeps running.")
            elif others:
                notes.append(('Remaining times: ' if policy == 'srtf' else 'Ready jobs and their bursts: ') + ', '.join(f"{p['name']} {p[measure]}" for p in sorted(ready, key=lambda p: order[p['name']])) + f". {choice['name']} is shortest, so it runs.")
            else:
                notes.append(f"{choice['name']} is the only process ready, so it runs.")
        # Run until the next decision point: completion, or (SRTF) the next arrival.
        future = [a for a in events if a > t]
        end = t + choice['left']
        if policy == 'srtf' and future:
            end = min(end, future[0])
        steps.append(dict(t=t, run=choice['name'], rem=[p['left'] for p in procs], ready=[p['name'] for p in ready if p is not choice], note=' '.join(notes)))
        if segs and segs[-1][0] == choice['name'] and segs[-1][2] == t:
            segs[-1][2] = end
        else:
            segs.append([choice['name'], t, end])
        choice['left'] -= end - t
        if choice['left'] == 0: choice['done'] = end
        running, t = choice, end
    rows = []
    for p in procs:
        tat = p['done'] - p['arrival']; wait = tat - p['burst']
        rows.append([p['name'], p['arrival'], p['burst'], p['done'], tat, wait])
    col = 4 if metric == 'turnaround' else 5
    values = [r[col] for r in rows]
    avg = Fraction(sum(values), len(values))
    formula = 'completion − arrival' if metric == 'turnaround' else 'completion − arrival − burst'
    steps.append(dict(t=t, run=None, rem=[0] * len(procs), ready=[], final=True,
                      note=f"All done. {metric.capitalize()} time = {formula}. Average = ({' + '.join(map(str, values))}) / {len(values)} = {_fmt(avg)}."))
    return dict(policy=policy, title=POLICY_NAMES[policy], segs=segs, steps=steps, rows=rows, metric=metric, average=_fmt(avg), end=t), avg


def load(root, question_ids):
    path = root / 'data/animations.json'
    if not path.exists():
        return {}
    out = {}
    for qid, spec in json.loads(path.read_text())['questions'].items():
        if qid not in question_ids:
            raise SystemExit('data/animations.json names an unknown question: ' + qid)
        if spec['kind'] != 'cpu-schedule':
            raise SystemExit('Unknown animation kind for ' + qid)
        schedules = []
        for s in spec['schedules']:
            data, avg = cpu_schedule(spec['processes'], s['policy'], spec['metric'])
            if abs(float(avg) - float(s['expect'])) > 1e-9:
                raise SystemExit(f"Animation for {qid} ({s['policy']}) gives {float(avg)}, not the expected {s['expect']}")
            schedules.append(data)
        out[qid] = dict(kind=spec['kind'], processes=[p[0] for p in spec['processes']], schedules=schedules,
                        count=sum(len(s['steps']) for s in schedules))
    return out
