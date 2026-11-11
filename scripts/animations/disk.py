"""Disk scheduling: FCFS, SSTF, SCAN, LOOK, C-SCAN and C-LOOK.

Data: data/animations/disk.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from fractions import Fraction

from .common import _fmt, _same


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



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'disk-schedule': disk_animation}
PLAYER = 'disk'
TABS = 'schedules'
