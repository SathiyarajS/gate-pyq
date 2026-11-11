"""Dynamic-programming tables filled cell by cell.

Data: data/animations/dp.json. Each spec names a problem and its inputs:
  matrix-chain  dims d0..dn (matrix i is d(i−1) × d(i)), optional names;
                expect: cost, and/or pairs (the original adjacent matrices multiplied
                directly with each other, which must be the same in every optimal
                parenthesization)
  lcs           strings a and b; expect: length, distinct (number of different
                longest common subsequence strings), and optionally `answer` with
                `weights` {length: p, distinct: q} meaning p·length + q·distinct
  knapsack      0/1 knapsack: items [[weight, value], ...], capacity; expect: optimal,
                and with `greedy` (take items in decreasing value/weight order when
                they fit) also greedy and difference (optimal − greedy)
  nondecreasing  longest nondecreasing subsequence of an array; expect: length, and
                distance (entries to replace = n − length)
Everything is computed here, and the build stops on any difference.
"""
from itertools import product

from .common import _fmt, _list


def _check(qid, got, expect):
    for k, v in expect.items():
        if k not in got:
            raise SystemExit(f'{qid}: unknown dp expectation {k}')
        if got[k] != v:
            raise SystemExit(f'Animation for {qid} gives {k} = {got[k]}, not the expected {v}')


def _tab(short, title, rows, cols, corner, base, fill, steps, blank=None):
    return dict(short=short, title=title, rows=rows, cols=cols, corner=corner, base=base, fill=fill, blank=blank or [], steps=steps)


def matrix_chain(qid, spec):
    d = spec['dims']
    n = len(d) - 1
    names = spec.get('names') or [f'M{k}' for k in range(1, n + 1)]
    if len(names) != n:
        raise SystemExit(f'{qid}: {n} matrices need {n} names')
    m, best = {}, {}
    for i in range(1, n + 1):
        m[i, i] = 0
    fill, steps = [], [dict(at=-1, note=f"m[i, j] is the fewest scalar multiplications for {names[0]}…{names[-1]} from i to j. m[i, i] = 0; for i < j, m[i, j] = min over k of m[i, k] + m[k+1, j] + d(i−1)·d(k)·d(j), with d = {', '.join(map(str, d))}. Fill by chain length.")]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            opts = [(m[i, k] + m[k + 1, j] + d[i - 1] * d[k] * d[j], k) for k in range(i, j)]
            low = min(c for c, _ in opts)
            ks = [k for c, k in opts if c == low]
            m[i, j], best[i, j] = low, ks
            fill.append([i - 1, j - 1, str(low)])
            parts = [f"k = {k}: {m[i, k]} + {m[k + 1, j]} + {d[i - 1]}·{d[k]}·{d[j]} = {c}" for c, k in opts]
            note = f"m[{i}, {j}] ({names[i - 1]}…{names[j - 1]}): " + ('; '.join(parts) + f". The minimum is {low}" if len(opts) > 1 else parts[0]) + (f", at k = {ks[0]}." if len(opts) > 1 and len(ks) == 1 else f", at k = {_list([str(k) for k in ks])}." if len(opts) > 1 else '.')
            deps = [[i - 1, k - 1] for k in ks] + [[k, j - 1] for k in ks]
            alts = [[i - 1, k - 1] for _, k in opts if k not in ks] + [[k, j - 1] for _, k in opts if k not in ks]
            steps.append(dict(at=len(fill) - 1, deps=deps, alts=alts, note=note))

    def trees(i, j):
        if i == j:
            return [i]
        return [(a, b) for k in best[i, j] for a in trees(i, k) for b in trees(k + 1, j)]

    def show(t):
        return names[t - 1] if isinstance(t, int) else '(' + show(t[0]) + show(t[1]) + ')'

    def leafpairs(t, out):
        if isinstance(t, tuple):
            if isinstance(t[0], int) and isinstance(t[1], int):
                out.append(names[t[0] - 1] + names[t[1] - 1])
            leafpairs(t[0], out)
            leafpairs(t[1], out)
        return out
    all_t = trees(1, n)
    got = dict(cost=m[1, n])
    final = f"All done. The minimum is m[1, {n}] = {m[1, n]}, with " + ('the parenthesization ' + show(all_t[0]) if len(all_t) == 1 else 'parenthesizations ' + _list([show(t) for t in all_t])) + '.'
    if 'pairs' in spec['expect']:
        sets = {tuple(sorted(leafpairs(t, []))) for t in all_t}
        if len(sets) != 1:
            raise SystemExit(f'{qid}: optimal parenthesizations disagree on which matrices are multiplied directly')
        got['pairs'] = list(sets.pop())
        final += ' Two original matrices are multiplied directly only in ' + _list(got['pairs']) + '.'
    _check(qid, got, spec['expect'])
    path = []

    def mark(i, j):
        if i < j:
            path.append([i - 1, j - 1])
            k = best[i, j][0]
            mark(i, k)
            mark(k + 1, j)
    mark(1, n)
    steps.append(dict(at=len(fill) - 1, path=path, final=True, note=final))
    labels = [f'{k} {names[k - 1]}' for k in range(1, n + 1)]
    return [_tab('Matrix chain', 'm[i, j], rows i and columns j; dimensions ' + ' × '.join(map(str, d)), labels, labels, 'i \\ j',
                 [[k, k, '0'] for k in range(n)], fill, steps, blank=[[r, c] for r in range(n) for c in range(r)])]


def lcs(qid, spec):
    a, b = spec['a'], spec['b']
    p, q = len(a), len(b)
    L = [[0] * (q + 1) for _ in range(p + 1)]
    S = [[{''} for _ in range(q + 1)] for _ in range(p + 1)]
    fill = []
    steps = [dict(at=-1, note=f"L[i, j] is the length of a longest common subsequence of the first i letters of {a} and the first j letters of {b}. Row 0 and column 0 are 0. If the letters match, L[i, j] = L[i−1, j−1] + 1; otherwise L[i, j] = max(L[i−1, j], L[i, j−1]).")]
    for i, j in product(range(1, p + 1), range(1, q + 1)):
        x, y = a[i - 1], b[j - 1]
        if x == y:
            L[i][j] = L[i - 1][j - 1] + 1
            S[i][j] = {s + x for s in S[i - 1][j - 1]}
            note, deps = f"{a[:i]} and {b[:j]}: both end in {x}, so L[{i}, {j}] = L[{i - 1}, {j - 1}] + 1 = {L[i][j]}.", [[i - 1, j - 1]]
        else:
            up, left = L[i - 1][j], L[i][j - 1]
            L[i][j] = max(up, left)
            S[i][j] = (S[i - 1][j] if up == L[i][j] else set()) | (S[i][j - 1] if left == L[i][j] else set())
            note = f"{a[:i]} and {b[:j]}: {x} ≠ {y}, so L[{i}, {j}] = max(L[{i - 1}, {j}], L[{i}, {j - 1}]) = max({up}, {left}) = {L[i][j]}."
            deps = [c for c, v in (([i - 1, j], up), ([i, j - 1], left)) if v == L[i][j]]
        fill.append([i, j, str(L[i][j])])
        steps.append(dict(at=len(fill) - 1, deps=deps, note=note))
    best = sorted(S[p][q])
    got = dict(length=L[p][q], distinct=len(best))
    final = f"All done. The longest common subsequences have length L[{p}, {q}] = {L[p][q]}. Following every way back through the table gives {len(best)} different strings: {_list(best)}."
    if 'answer' in spec['expect']:
        w = spec['weights']
        got['answer'] = sum(w[k] * got[k] for k in w)
        final += ' So ' + ' + '.join(f"{w[k]}·{got[k]}" if w[k] != 1 else str(got[k]) for k in w) + f" = {got['answer']}."
    _check(qid, got, spec['expect'])
    path, i, j = [], p, q
    while i and j:
        path.append([i, j])
        if a[i - 1] == b[j - 1]:
            i, j = i - 1, j - 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    steps.append(dict(at=len(fill) - 1, path=path, final=True, note=final))
    rows, cols = ['ε'] + [f'{k} {c}' for k, c in enumerate(a, 1)], ['ε'] + [f'{k} {c}' for k, c in enumerate(b, 1)]
    base = [[0, j, '0'] for j in range(q + 1)] + [[i, 0, '0'] for i in range(1, p + 1)]
    return [_tab('LCS table', f'L[i, j] for {a} (rows) and {b} (columns)', rows, cols, '', base, fill, steps)]


def knapsack(qid, spec):
    items, W = spec['items'], spec['capacity']
    n = len(items)
    K = [[0] * (W + 1) for _ in range(n + 1)]
    fill, steps = [], [dict(at=-1, note=f"K[i, c] is the best value using only the first i items with capacity c. Row 0 is 0. If item i weighs more than c, K[i, c] = K[i−1, c]; otherwise K[i, c] = max(K[i−1, c], K[i−1, c − w] + v).")]
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(W + 1):
            if w > c:
                K[i][c] = K[i - 1][c]
                note, deps = f"Item {i} ({w} kg, value {v}) does not fit in {c} kg: K[{i}, {c}] = K[{i - 1}, {c}] = {K[i][c]}.", [[i - 1, c]]
            else:
                skip, take = K[i - 1][c], K[i - 1][c - w] + v
                K[i][c] = max(skip, take)
                note = f"Item {i} ({w} kg, value {v}), capacity {c}: skip it for K[{i - 1}, {c}] = {skip}, or take it for K[{i - 1}, {c - w}] + {v} = {take}. Best: {K[i][c]}."
                deps = [cell for cell, val in (([i - 1, c], skip), ([i - 1, c - w], take)) if val == K[i][c]]
            fill.append([i, c, str(K[i][c])])
            steps.append(dict(at=len(fill) - 1, deps=deps, note=note))
    opt = K[n][W]
    chosen, c = [], W
    path = []
    for i in range(n, 0, -1):
        path.append([i, c])
        if K[i][c] != K[i - 1][c]:
            chosen.append(i)
            c -= items[i - 1][0]
    chosen.reverse()
    got = dict(optimal=opt)
    final = f"All done. The best value is K[{n}, {W}] = {opt}, taking item" + ('s ' if len(chosen) > 1 else ' ') + _list([str(k) for k in chosen]) + '.'
    tabs = []
    rows, cols = ['none'] + [f'{k} ({w}, {v})' for k, (w, v) in enumerate(items, 1)], [str(c) for c in range(W + 1)]
    gsteps = None
    if spec.get('greedy'):
        ratio = [(v / w, k) for k, (w, v) in enumerate(items, 1)]
        if len({r for r, _ in ratio}) != n:
            raise SystemExit(f'{qid}: equal value/weight ratios make the greedy order ambiguous')
        order = [k for _, k in sorted(ratio, reverse=True)]
        left, val, took = W, 0, []
        gsteps = [dict(at=-1, note='Greedy order, by value per kg: ' + ', '.join(f"item {k} ({_fmt(items[k - 1][1] / items[k - 1][0])})" for k in order) + f'. Capacity {W} kg.')]
        for k in order:
            w, v = items[k - 1]
            if w <= left:
                left -= w
                val += v
                took.append(k)
                gsteps.append(dict(at=-1, took=list(took), note=f"Item {k} ({w} kg, value {v}) fits: take it. {left} kg left, value so far {val}."))
            else:
                gsteps.append(dict(at=-1, took=list(took), note=f"Item {k} ({w} kg) does not fit in the {left} kg left: skip it."))
        got['greedy'] = val
        got['difference'] = opt - val
        line = f" Greedy gets {val}, so the difference is {opt} − {val} = {opt - val}."
        final += line
        gsteps.append(dict(at=-1, took=list(took), final=True, note=f"All done. Greedy takes item" + ('s ' if len(took) > 1 else ' ') + _list([str(k) for k in took]) + f" for a value of {val}. The table's optimum is {opt}, so the difference is {opt - val}."))
    _check(qid, got, spec['expect'])
    steps.append(dict(at=len(fill) - 1, path=path, final=True, note=final))
    tabs.append(_tab('DP table', f'K[i, c]: rows are items (weight, value), columns capacity in kg', rows, cols, 'item \\ c', [[0, c, '0'] for c in range(W + 1)], fill, steps))
    if gsteps:
        tabs.append(_tab('Greedy', 'Greedy: highest value per kg first, take it if it fits', [f'{k} ({w}, {v})' for k, (w, v) in enumerate(items, 1)], ['value/kg'], 'item', [[k - 1, 0, _fmt(items[k - 1][1] / items[k - 1][0])] for k in range(1, n + 1)], [], gsteps))
    return tabs


def nondecreasing(qid, spec):
    a = spec['array']
    n = len(a)
    Lv = [1] * n
    fill, steps = [], [dict(at=-1, note=f"L[i] is the length of the longest nondecreasing subsequence ending at position i: 1 + the largest L[j] over earlier j with A[j] ≤ A[i], or 1 if there is none.")]
    for i in range(n):
        prev = [j for j in range(i) if a[j] <= a[i]]
        if prev:
            top = max(Lv[j] for j in prev)
            Lv[i] = top + 1
            best = [j for j in prev if Lv[j] == top]
            note = f"A[{i + 1}] = {a[i]}: earlier entries ≤ {a[i]} are at " + _list([str(j + 1) for j in prev]) + f", with the largest L = {top}, so L[{i + 1}] = {Lv[i]}."
        else:
            best = []
            note = f"A[{i + 1}] = {a[i]}: no earlier entry is ≤ {a[i]}, so L[{i + 1}] = 1."
        fill.append([1, i, str(Lv[i])])
        steps.append(dict(at=len(fill) - 1, deps=[[0, j] for j in best], alts=[[0, j] for j in prev if j not in best], note=note))
    length = max(Lv)
    got = dict(length=length, distance=n - length)
    _check(qid, got, spec['expect'])
    path, want, end = [], length, None
    for i in range(n - 1, -1, -1):
        if Lv[i] == want and (end is None or a[i] <= a[end]):
            path.append([1, i])
            want, end = want - 1, i
    steps.append(dict(at=len(fill) - 1, path=path, final=True, note=f"All done. At most {length} entries can stay unchanged (for example " + ', '.join(str(a[c]) for _, c in reversed(path)) + f"), so at least {n} − {length} = {n - length} must be replaced."))
    return [_tab('Table', 'A and L, position by position', ['A', 'L'], [str(k) for k in range(1, n + 1)], 'i', [[0, k, str(v)] for k, v in enumerate(a)], fill, steps)]


PROBLEMS = {'matrix-chain': matrix_chain, 'lcs': lcs, 'knapsack': knapsack, 'nondecreasing': nondecreasing}


def dp_animation(qid, spec):
    if spec.get('problem') not in PROBLEMS:
        raise SystemExit(f'{qid}: unknown dp problem {spec.get("problem")}')
    tabs = PROBLEMS[spec['problem']](qid, spec)
    return dict(kind='dp-table', schedules=tabs, count=sum(len(t['steps']) for t in tabs))


KINDS = {'dp-table': dp_animation}
PLAYER = 'dp'
TABS = 'tables'
