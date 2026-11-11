"""Page replacement: FIFO, LRU, optimal and windowed optimal.

Data: data/animations/paging.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from fractions import Fraction

from .common import _fmt, _list, _same


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
                note += ' It becomes the most recently used.'
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



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'page-replace': page_animation}
PLAYER = 'paging'
