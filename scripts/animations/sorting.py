"""Sorting traces: quicksort partitions, insertion, selection, merge sort, adjacent-swap passes.

Data: data/animations/sorting.json. A spec gives one or more runs (tabs), each
with an input array and an algorithm:
  quicksort   pivot 'first' or 'last'. The partition compares every other element
              of the subarray with the pivot once and moves the smaller ones to
              the front in the order met (Lomuto's scheme); comparisons counted
              are element-versus-pivot comparisons.
  insertion   comparisons of the key with the element to its left, stopping at the
              first that is not larger.
  selection   comparisons of each remaining element with the current minimum.
  merge       top-down merge sort, halves of sizes ⌊n/2⌋ and ⌈n/2⌉; a merge compares
              the two front elements until one side is empty.
  merge-passes  bottom-up (straight two-way) merging: pass k merges neighbouring
              runs of length 2^(k−1); a run with no partner is carried over.
  passes      the question's own loop of adjacent compare-and-swap passes, repeated
              until a whole round makes no swap.
Each run may expect: comparisons, swaps, array (final), after_pass {pass, array},
void_merges, value_at {index, value}. A question-level `expect` may give
`fewest` (the run with strictly the fewest comparisons) or `relation`
[run, '>' or '<' or '=', run] on comparison counts. The build stops on any difference.
"""
from .common import _list


def _s(a):
    return '[' + ', '.join(map(str, a)) + ']'


class Trace:
    def __init__(self, a):
        self.a, self.steps, self.comps, self.swaps = list(a), [], 0, 0
        self.fixed = set()

    def add(self, note, **kw):
        st = dict(arr=list(self.a), comps=self.comps, swaps=self.swaps, fixed=sorted(self.fixed), note=note)
        st.update({k: v for k, v in kw.items() if v is not None})
        self.steps.append(st)

    def swap(self, i, j):
        self.a[i], self.a[j] = self.a[j], self.a[i]
        self.swaps += 1


def quicksort(t, pivot):
    a = t.a

    def part(lo, hi):
        if lo > hi:
            return
        if lo == hi:
            t.fixed.add(lo)
            return
        if pivot == 'first':
            p = a[lo]
            t.add(f"Partition {_s(a[lo:hi + 1])} around its first element, {p}.", rng=[lo, hi], piv=lo)
            i = lo
            for j in range(lo + 1, hi + 1):
                t.comps += 1
                if a[j] < p:
                    i += 1
                    if i != j:
                        t.swap(i, j)
                        t.add(f"{a[i]} < {p}: it joins the smaller part; swap it with {a[j]}.", rng=[lo, hi], piv=lo, cmp=[lo, i], sw=[i, j])
                    else:
                        t.add(f"{a[j]} < {p}: it joins the smaller part, already in place.", rng=[lo, hi], piv=lo, cmp=[lo, j])
                else:
                    t.add(f"{a[j]} > {p}: it stays in the larger part.", rng=[lo, hi], piv=lo, cmp=[lo, j])
            if i != lo:
                t.swap(lo, i)
            t.fixed.add(i)
            t.add(f"Put the pivot {p} between the parts" + (f" by swapping it with {a[lo]}" if i != lo else '') + f": {_s(a[lo:i])} | {p} | {_s(a[i + 1:hi + 1])}. That took {hi - lo} comparison" + ("" if hi - lo == 1 else "s") + f".", rng=[lo, hi], piv=i)
        else:
            p = a[hi]
            t.add(f"Partition {_s(a[lo:hi + 1])} around its last element, {p}.", rng=[lo, hi], piv=hi)
            i = lo - 1
            for j in range(lo, hi):
                t.comps += 1
                if a[j] <= p:
                    i += 1
                    if i != j:
                        t.swap(i, j)
                        t.add(f"{a[i]} < {p}: it joins the smaller part; swap it with {a[j]}.", rng=[lo, hi], piv=hi, cmp=[hi, i], sw=[i, j])
                    else:
                        t.add(f"{a[j]} < {p}: it joins the smaller part, already in place.", rng=[lo, hi], piv=hi, cmp=[hi, j])
                else:
                    t.add(f"{a[j]} > {p}: it stays in the larger part.", rng=[lo, hi], piv=hi, cmp=[hi, j])
            i += 1
            if i != hi:
                t.swap(i, hi)
            t.fixed.add(i)
            t.add(f"Put the pivot {p} between the parts" + (f" by swapping it with {a[hi]}" if i != hi else '') + f": {_s(a[lo:i])} | {p} | {_s(a[i + 1:hi + 1])}. That took {hi - lo} comparison" + ("" if hi - lo == 1 else "s") + f".", rng=[lo, hi], piv=i)
        part(lo, i - 1)
        part(i + 1, hi)
    part(0, len(a) - 1)


def insertion(t):
    a = t.a
    t.fixed.add(0)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            t.comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                a[j] = key
                t.swaps += 1
                t.add(f"Insert {key}: {a[j + 1]} > {key}, so {a[j + 1]} shifts right.", cmp=[j, j + 1], sw=[j, j + 1], rng=[0, i])
                j -= 1
            else:
                t.add(f"Insert {key}: {a[j]} is not larger than {key}, so {key} stays" + (' where it is.' if j == i - 1 else ' in place here.'), cmp=[j, j + 1], rng=[0, i])
                break
        else:
            t.add(f"{key} is the smallest so far and reaches the front.", rng=[0, i])
        t.fixed.add(i)


def selection(t):
    a, n = t.a, len(t.a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            t.comps += 1
            if a[j] < a[m]:
                old, m = a[m], j
                t.add(f"Pass {i + 1}: {a[j]} < {old}, so {a[j]} is the smallest so far.", cmp=[m, j], rng=[i, n - 1], piv=m)
            else:
                t.add(f"Pass {i + 1}: {a[j]} > {a[m]}, so {a[m]} stays the smallest.", cmp=[m, j], rng=[i, n - 1], piv=m)
        if m != i:
            t.swap(i, m)
            t.fixed.add(i)
            t.add(f"Swap the smallest, {a[i]}, into position {i + 1}.", sw=[i, m], rng=[i, n - 1])
        else:
            t.fixed.add(i)
            t.add(f"The smallest, {a[i]}, is already in position {i + 1}; no swap.", rng=[i, n - 1])
    t.fixed.add(n - 1)


def _merge(t, lo, mid, hi, runs):
    a = t.a
    left, right = a[lo:mid], a[mid:hi]
    out, i, j, c = [], 0, 0, 0
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out += left[i:] + right[j:]
    t.comps += c
    a[lo:hi] = out
    void = out == left + right
    return left, right, out, c, void


def merge_sort(t, counter):
    n = len(t.a)
    runs = [[k, k + 1] for k in range(n)]

    def sort(lo, hi):
        if hi - lo < 2:
            return
        mid = lo + (hi - lo) // 2
        sort(lo, mid)
        sort(mid, hi)
        left, right, out, c, void = _merge(t, lo, mid, hi, runs)
        counter['merges'] += 1
        counter['void'] += void
        runs[:] = [r for r in runs if not (lo <= r[0] and r[1] <= hi)] + [[lo, hi]]
        runs.sort()
        why = (f"{max(left)} ≤ {min(right)}, so the output is just the left half followed by the right: a void merge." if void else
               f"{max(left)} > {min(right)}, so the halves interleave.")
        t.add(f"Merge {_s(left)} and {_s(right)} into {_s(out)} with {c} comparison" + ('' if c == 1 else 's') + f". {why}", rng=[lo, hi - 1], runs=[list(r) for r in runs], void=void)
    sort(0, n)


def merge_passes(t, stop):
    n, width, k = len(t.a), 1, 0
    runs = [[x, x + 1] for x in range(n)]
    after = {}
    while width < n and (stop is None or k < stop):
        k += 1
        new = []
        for lo in range(0, n, 2 * width):
            mid, hi = min(lo + width, n), min(lo + 2 * width, n)
            if mid >= hi:
                new.append([lo, hi])
                t.add(f"Pass {k}: {_s(t.a[lo:hi])} has no partner and is carried over.", rng=[lo, hi - 1], runs=[list(r) for r in sorted(new + [r for r in runs if r[0] >= hi])], pass_=k)
                continue
            left, right, out, c, _ = _merge(t, lo, mid, hi, runs)
            new.append([lo, hi])
            t.add(f"Pass {k}: merge {_s(left)} and {_s(right)} into {_s(out)}.", rng=[lo, hi - 1], runs=[list(r) for r in sorted(new + [r for r in runs if r[0] >= hi])], pass_=k)
        runs, width = new, width * 2
        after[k] = list(t.a)
        t.steps[-1]['note'] += f" After pass {k}: {_s(t.a)}."
    return after


def passes(t, loops):
    """The question's loop: repeat its passes until a whole round makes no swap."""
    a, rnd = t.a, 0
    while True:
        rnd += 1
        if rnd > 100:
            raise SystemExit('Adjacent-swap passes do not terminate')
        swapped = False
        for p in loops:
            frm, to, d, op = p['from'], p['to'], p['other'], p['swap_if']
            rng = range(frm, to + 1) if frm <= to else range(frm, to - 1, -1)
            for i in rng:
                j = i + d
                t.comps += 1
                hit = a[i] < a[j] if op == '<' else a[i] > a[j]
                label = f"Round {rnd}, {p['name']}: i = {i}."
                if hit:
                    x, y = a[i], a[j]
                    t.swap(i, j)
                    swapped = True
                    t.add(f"{label} a[{i}] = {x} {op} a[{j}] = {y}, so swap them.", cmp=[i, j], sw=[i, j], idx=True)
                else:
                    t.add(f"{label} a[{i}] = {a[i]} {op} a[{j}] = {a[j]} is false; no swap.", cmp=[i, j], idx=True)
        t.steps[-1]['note'] += f" End of round {rnd}: {_s(a)}" + (', with swaps, so the loop goes round again.' if swapped else ', with no swap, so the loop stops.')
        if not swapped:
            return rnd


NAMES = {'quicksort': 'Quicksort', 'insertion': 'Insertion sort', 'selection': 'Selection sort', 'merge': 'Merge sort',
         'merge-passes': 'Bottom-up merge sort', 'passes': 'The given loop'}


def run(qid, r):
    alg, a = r['algorithm'], r['array']
    if alg not in NAMES:
        raise SystemExit(f'{qid}: unknown sorting algorithm {alg}')
    t = Trace(a)
    counter = dict(merges=0, void=0)
    title = r.get('title')
    t.add(f"Start: {_s(a)}.", idx=alg == 'passes' or None)
    after = {}
    if alg == 'quicksort':
        if r.get('pivot') not in ('first', 'last'):
            raise SystemExit(f'{qid}: quicksort needs pivot first or last')
        if len(set(a)) != len(a):
            raise SystemExit(f'{qid}: quicksort traces need distinct keys')
        quicksort(t, r['pivot'])
        title = title or f"Quicksort, {r['pivot']} element as pivot; each partition compares the pivot with every other element once"
    elif alg == 'insertion':
        insertion(t)
    elif alg == 'selection':
        selection(t)
    elif alg == 'merge':
        merge_sort(t, counter)
    elif alg == 'merge-passes':
        after = merge_passes(t, r.get('stop_after'))
    else:
        passes(t, r['loops'])
    got = dict(comparisons=t.comps, swaps=t.swaps, array=t.a, void_merges=counter['void'])
    exp = r.get('expect', {})
    note = 'All done. ' + (f"Array: {_s(t.a)}." if alg != 'merge-passes' or r.get('stop_after') is None else f"Stopped after pass {r['stop_after']}: {_s(t.a)}.")
    if alg in ('quicksort', 'insertion', 'selection', 'merge') or 'comparisons' in exp:
        note += f" Comparisons: {t.comps}."
    if 'swaps' in exp:
        note += f" Swaps: {t.swaps}."
    if 'void_merges' in exp:
        note += f" Void merges: {counter['void']} of {counter['merges']}."
    if 'after_pass' in exp:
        k = exp['after_pass']['pass']
        if k not in after:
            raise SystemExit(f'{qid}: no pass {k}')
        got['after_pass'] = dict(**{'pass': k}, array=after[k])
    if 'value_at' in exp:
        k = exp['value_at']['index']
        got['value_at'] = dict(index=k, value=t.a[k])
        note += f" a[{k}] = {t.a[k]}."
    for k, v in exp.items():
        if k not in got:
            raise SystemExit(f'{qid}: unknown sorting expectation {k}')
        if got[k] != v:
            raise SystemExit(f'Animation for {qid} ({r.get("name", alg)}) gives {k} = {got[k]}, not the expected {v}')
    t.fixed = set(range(len(a))) if alg != 'merge-passes' and alg != 'passes' else t.fixed
    t.add(note, final=True, idx=alg == 'passes' or None, runs=[[0, len(a)]] if alg in ('merge',) else (t.steps[-1].get('runs') if alg == 'merge-passes' else None))
    return dict(short=r.get('name', NAMES[alg]), title=title or NAMES[alg], steps=t.steps, alg=alg), t.comps


def sorting_animation(qid, spec):
    tabs, comps = [], {}
    for r in spec['runs']:
        tab, c = run(qid, r)
        tabs.append(tab)
        comps[tab['short']] = c
    exp = spec.get('expect', {})
    line = None
    if 'fewest' in exp:
        best = min(comps.values())
        who = [k for k, v in comps.items() if v == best]
        if who != [exp['fewest']]:
            raise SystemExit(f'Animation for {qid}: fewest comparisons by {who}, not {exp["fewest"]}')
        line = 'Comparisons: ' + ', '.join(f"{k} {v}" for k, v in comps.items()) + f". {who[0]} uses the fewest."
    if 'relation' in exp:
        a, op, b = exp['relation']
        x, y = comps[a], comps[b]
        ok = {'>': x > y, '<': x < y, '=': x == y}[op]
        if not ok:
            raise SystemExit(f'Animation for {qid}: {a} = {x} and {b} = {y}, so not {a} {op} {b}')
        line = f"{a} = {x} and {b} = {y}, so {a} {op} {b}."
    for k in exp:
        if k not in ('fewest', 'relation'):
            raise SystemExit(f'{qid}: unknown sorting expectation {k}')
    if line:
        for tab in tabs:
            tab['steps'][-1]['note'] += ' ' + line
    return dict(kind='sort-trace', schedules=tabs, count=sum(len(t['steps']) for t in tabs))


KINDS = {'sort-trace': sorting_animation}
PLAYER = 'sorting'
TABS = 'runs'
