"""Graph algorithms on an explicitly given graph.

Breadth- and depth-first orders, Dijkstra, edge-bounded Bellman-Ford, best paths
in a DAG, Kruskal (total weight, the tree, the number of minimum trees, a forced
leaf, a path in the tree, possible acceptance orders) and topological orders.

Data: data/animations/graph.json. A spec states the graph (`nodes` and `edges` as
[u, v] or [u, v, weight], or `nodes` and a weight `matrix`), `directed`, an
optional drawing position for each node (`pos`, or "layers" for a DAG), the
question's other inputs, and `expect`. Everything else is computed here, and the
build stops on any difference from `expect`.

Ties: where the outcome could depend on how ties are broken, the simulator either
stops the build or, when the spec says the question leaves ties open
(`"ties": "any"`), tries every tie order and stops unless they all give the
expected answer. Equal-weight edges in Kruskal are taken in the listed order;
the notes say when the choice does not matter, and only facts that hold for every
choice are checked.
"""
from collections import deque
from fractions import Fraction
from itertools import combinations
from math import comb

from .common import _fmt, _list


def fw(x):
    """A weight or distance for a note: exact, with a real minus sign; None is infinity."""
    return '∞' if x is None else _fmt(x).replace('-', '−')


def plus(a, w):
    return f"{fw(a)} − {fw(-w)}" if w < 0 else f"{fw(a)} + {fw(w)}"


def total(ws):
    s = ' + '.join(fw(w) for w in ws).replace('+ −', '− ')
    return s if len(ws) < 2 else s + ' = ' + fw(sum(ws, Fraction(0)))


def _num(x, what):
    if isinstance(x, bool) or not isinstance(x, (int, float, str)):
        raise SystemExit(f'{what}: weight {x!r} is not a number')
    return Fraction(str(x))


class Graph:
    def __init__(self, qid, spec):
        self.qid, self.directed = qid, bool(spec.get('directed'))
        if 'matrix' in spec:
            nodes, m = [str(n) for n in spec['nodes']], spec['matrix']
            if len(m) != len(nodes) or any(len(r) != len(nodes) for r in m):
                raise SystemExit(f'{qid}: the weight matrix is not {len(nodes)} × {len(nodes)}')
            raw = []
            for i in range(len(nodes)):
                if m[i][i] != 0:
                    raise SystemExit(f'{qid}: the weight matrix has a nonzero diagonal')
                for j in range(len(nodes)):
                    if i == j or (not self.directed and j < i):
                        continue
                    if not self.directed and m[i][j] != m[j][i]:
                        raise SystemExit(f'{qid}: the weight matrix of an undirected graph is not symmetric')
                    if m[i][j] == 0:
                        raise SystemExit(f'{qid}: a zero off the diagonal is ambiguous (no edge, or weight 0?)')
                    raw.append([nodes[i], nodes[j], m[i][j]])
        else:
            raw = spec['edges']
            nodes = [str(n) for n in spec.get('nodes') or dict.fromkeys(str(x) for e in raw for x in e[:2])]
        if len(set(nodes)) != len(nodes):
            raise SystemExit(f'{qid}: a vertex is listed twice')
        self.nodes, self.edges, seen = nodes, [], set()
        for e in raw:
            u, v = str(e[0]), str(e[1])
            if u not in nodes or v not in nodes:
                raise SystemExit(f'{qid}: edge {u}-{v} uses an unlisted vertex')
            if u == v:
                raise SystemExit(f'{qid}: self-loop at {u}')
            key = (u, v) if self.directed else frozenset((u, v))
            if key in seen:
                raise SystemExit(f'{qid}: edge {u}-{v} is listed twice')
            seen.add(key)
            self.edges.append((u, v, _num(e[2], qid) if len(e) > 2 and e[2] is not None else None))
        self.out = {n: [] for n in nodes}
        self.inn = {n: [] for n in nodes}
        for i, (u, v, w) in enumerate(self.edges):
            self.out[u].append((v, w, i))
            self.inn[v].append((u, w, i))
            if not self.directed:
                self.out[v].append((u, w, i))
                self.inn[u].append((v, w, i))
        self.pos = spec.get('pos')
        if self.pos == 'layers':
            self.pos = self.layers()
        if self.pos is not None and set(self.pos) != set(nodes):
            raise SystemExit(f'{qid}: pos must give every vertex exactly once')

    def weighted(self):
        if any(w is None for *_, w in self.edges):
            raise SystemExit(f'{self.qid}: every edge needs a weight')

    def arrow(self, u, v):
        return f"{u}{'→' if self.directed else '–'}{v}"

    def name(self, i):
        u, v, _ = self.edges[i]
        return self.arrow(u, v)

    def topo(self, pick=None):
        """Kahn's algorithm; ties go to the earliest listed vertex unless pick chooses."""
        deg = {v: len(self.inn[v]) for v in self.nodes}
        order = []
        while len(order) < len(self.nodes):
            ready = [v for v in self.nodes if v not in order and deg[v] == 0]
            if not ready:
                raise SystemExit(f'{self.qid}: the graph has a directed cycle')
            v = pick(ready) if pick else ready[0]
            order.append(v)
            for x, _, _ in self.out[v]:
                deg[x] -= 1
        return order

    def layers(self):
        """Left-to-right layers for a DAG: each vertex one column right of its furthest predecessor."""
        if not self.directed:
            raise SystemExit(f'{self.qid}: layered drawing needs a directed graph')
        col = {}
        for v in self.topo():
            col[v] = max((col[u] + 1 for u, _, _ in self.inn[v]), default=0)
        pos = {}
        for c in sorted(set(col.values())):
            vs = [v for v in self.nodes if col[v] == c]
            for k, v in enumerate(vs):
                pos[v] = [c, k - (len(vs) - 1) / 2]
        return pos

    def data(self):
        return dict(nodes=self.nodes, edges=[[u, v, None if w is None else fw(w)] for u, v, w in self.edges],
                    directed=self.directed, pos=self.pos)


def step(note, head=None, n=None, e=None, tag=None, table=None, line=None, final=False):
    s = dict(note=note)
    for k, v in (('head', head), ('n', n), ('e', e), ('tag', tag), ('table', table), ('line', line)):
        if v:
            s[k] = v
    if final:
        s['final'] = True
    return s


def schedule(short, title, steps, legend):
    steps[-1]['final'] = True
    return dict(short=short, title=title, steps=steps, legend=legend)


def out(kind, g, schedules, **extra):
    return dict(kind=kind, **g.data(), schedules=schedules, count=sum(len(s['steps']) for s in schedules), **extra)


def check(qid, what, got, want):
    if got != want:
        raise SystemExit(f'Animation for {qid}: {what} is {got}, not the expected {want}')


def spec_order(g, seq, what):
    seq = [str(x) for x in seq]
    if sorted(seq) != sorted(g.nodes):
        raise SystemExit(f'{g.qid}: {what} {seq} does not list every vertex exactly once')
    return seq


# ---------------------------------------------------------------- shortest paths

LEGEND_SP = [['n-now', 'being settled'], ['n-done', 'settled'], ['e-now', 'edge being relaxed'], ['e-tree', 'best path so far']]


def dijkstra(g, src, script=()):
    """Dijkstra from src. At the k-th tie for the smallest distance, take candidate script[k] (default the first listed).

    Returns the settle order, distances, predecessors, steps, tie sizes and the vertices whose
    distance was matched (not improved) by a later edge.
    """
    g.weighted()
    dist, pred, done, ties, matched, steps = {src: Fraction(0)}, {}, [], [], set(), []

    def snap(note, head, now=None, edge=None, row=None):
        n = {v: 'done' if v in done else 'seen' for v in dist}
        if now:
            n[now] = 'now'
        e = {str(i): 'tree' for _, i in pred.values()}
        if edge is not None:
            e[str(edge)] = 'now'
        rows = [[v, fw(dist.get(v)), pred[v][0] if v in pred else '', str(done.index(v) + 1) if v in done else ''] for v in g.nodes]
        table = dict(head=['Vertex', 'Distance', 'Via', 'Settled'], rows=rows, now=[g.nodes.index(row)] if row else [])
        steps.append(step(note, head, n, e, {v: fw(dist.get(v)) for v in g.nodes}, table))

    snap(f"Start at {src} with distance 0; every other vertex starts at ∞.", 'Start', row=src)
    while True:
        cand = [v for v in g.nodes if v not in done and v in dist]
        if not cand:
            break
        m = min(dist[v] for v in cand)
        tied = [v for v in cand if dist[v] == m]
        c = 0
        if len(tied) > 1:
            c = script[len(ties)] if len(ties) < len(script) else 0
            ties.append(len(tied))
        u = tied[c]
        done.append(u)
        if len(tied) > 1:
            others = [v for v in tied if v != u]
            note = f"Settle {u}: {_list(tied)} are tied at {fw(m)}, the smallest tentative distance; take {u} (taking {_list(others)} first ends with the same distances)."
        elif len(done) == 1:
            note = f"Settle {u}: its distance {fw(m)} is final."
        else:
            note = f"Settle {u}: at {fw(m)} it has the smallest tentative distance, so {fw(m)} is final."
        snap(note, f'Settle {u}', u, row=u)
        for v, w, i in g.out[u]:
            alt, arc = dist[u] + w, g.arrow(u, v)
            if v in done:
                if alt < dist[v]:
                    raise SystemExit(f'{g.qid}: Dijkstra would lower the settled vertex {v}; the question must say what happens then')
                note = f"Edge {arc}: {v} is already settled at {fw(dist[v])}, and {plus(dist[u], w)} = {fw(alt)} is no smaller."
            elif v not in dist or alt < dist[v]:
                old = dist.get(v)
                dist[v], pred[v] = alt, (u, i)
                note = f"Relax {arc}: {plus(dist[u], w)} = {fw(alt)} < {fw(old)}, so {v} becomes {fw(alt)}."
            elif alt == dist[v]:
                matched.add(v)
                note = f"Relax {arc}: {plus(dist[u], w)} = {fw(alt)} only equals {v}'s {fw(dist[v])}, so {v} keeps its path through {pred[v][0]}."
            else:
                note = f"Relax {arc}: {plus(dist[u], w)} = {fw(alt)} is not less than {fw(dist[v])}, so {v} stays at {fw(dist[v])}."
            snap(note, f'Edges out of {u}', u, i, v)
    return dict(order=done, dist=dist, pred=pred, steps=steps, ties=ties, matched=matched)


def every_tie_order(run):
    """Run with every sequence of tie choices; returns [(script, result)]."""
    found, stack = [], [()]
    while stack:
        sc = stack.pop()
        res = run(sc)
        found.append((sc, res))
        for k in range(len(sc), len(res['ties'])):
            for c in range(1, res['ties'][k]):
                stack.append(tuple(sc) + (0,) * (k - len(sc)) + (c,))
    return found


def true_distances(g, src):
    """Bellman-Ford over every edge (both ways if undirected); stops the build on a reachable negative cycle."""
    arcs = [(u, v, w) for u, v, w in g.edges] + ([] if g.directed else [(v, u, w) for u, v, w in g.edges])
    d = {src: Fraction(0)}
    for _ in range(len(g.nodes)):
        changed = False
        for u, v, w in arcs:
            if u in d and (v not in d or d[u] + w < d[v]):
                d[v], changed = d[u] + w, True
        if not changed:
            return d
    raise SystemExit(f'{g.qid}: a negative cycle is reachable from {src}')


def path_to(pred, src, t):
    path = [t]
    while path[-1] != src:
        if path[-1] not in pred:
            raise SystemExit(f'{t} cannot be reached from {src}')
        path.append(pred[path[-1]][0])
    return path[::-1]


def dijkstra_animation(qid, spec, g):
    src, want = str(spec['source']), spec['expect']
    ties = spec.get('ties', 'none')
    if ties not in ('none', 'any'):
        raise SystemExit(f'{qid}: unknown tie rule {ties}')
    if not set(want) <= {'order', 'dist', 'path', 'correct'} or not want:
        raise SystemExit(f'{qid}: Dijkstra expects some of order, dist, path, correct')
    truth = true_distances(g, src) if 'correct' in want else None

    def facts(r):
        f = {}
        if 'order' in want:
            f['order'] = r['order']
        if 'dist' in want:
            f['dist'] = {v: fw(r['dist'].get(v)) for v in expected['dist']}
        if 'path' in want:
            f['path'] = {t: path_to(r['pred'], src, t) for t in expected['path']}
        if 'correct' in want:
            f['correct'] = [v for v in g.nodes if v in truth and r['dist'].get(v) == truth[v]]
        return f

    expected = {}
    if 'order' in want:
        expected['order'] = [str(x) for x in want['order']]
    if 'dist' in want:
        expected['dist'] = {str(t): fw(_num(x, qid)) for t, x in want['dist'].items()}
    if 'path' in want:
        expected['path'] = {str(t): [str(x) for x in p] for t, p in want['path'].items()}
    if 'correct' in want:
        expected['correct'] = [str(x) for x in want['correct']]
    runs = every_tie_order(lambda sc: dijkstra(g, src, sc))
    if len(runs) > 1 and ties != 'any':
        raise SystemExit(f'{qid}: Dijkstra meets a tie; say "ties": "any" if the question leaves ties open')
    res = runs[0][1]
    for sc, r in runs:
        # Every tie order must give the expected answer, or the answer depends on the ties.
        check(qid, f'Dijkstra (tie choices {list(sc)})', facts(r), expected)
        if spec.get('update') != 'strict' and 'path' in want and any(v in r['matched'] for p in expected['path'].values() for v in p):
            raise SystemExit(f'{qid}: an equal-length path reached a vertex on the expected path; the question must state the update rule')
        if r['dist'] != res['dist']:
            raise SystemExit(f'{qid}: tie order changes the distances, so the settle note would be wrong')
    final = []
    if 'order' in want:
        final.append(f"Done: the vertices were settled in the order {', '.join(res['order'])}.")
    for t in expected.get('path', {}):
        p = path_to(res['pred'], src, t)
        ws = [g.edges[res['pred'][v][1]][2] for v in p[1:]]
        final.append(f"The path to {t} is {('→' if g.directed else '–').join(p)}, of length {total(ws)}.")
    listing = ', '.join(f"{v} {fw(res['dist'].get(v))}" for v in g.nodes)
    if 'correct' in want:
        ok = facts(res)['correct']
        final.append(f"Final distances: {listing}. " + ("Each equals the true shortest distance, so Dijkstra is right at every vertex here despite the negative edges."
                                                         if len(ok) == len(g.nodes) else f"Only {_list(ok)} match the true shortest distances."))
    elif 'dist' in want and 'path' not in want:
        final.append(f"Final distances: {listing}.")
    steps = res['steps']
    last = dict(steps[-1])
    last.update(note=' '.join(final), head='Finished')
    last['n'] = {v: 'done' for v in res['order']}
    last['e'] = {str(i): 'tree' for _, i in res['pred'].values()}
    for t in want.get('path', {}):
        for v in path_to(res['pred'], src, t)[1:]:
            last['e'][str(res['pred'][v][1])] = 'path'
    last['table'] = dict(last['table'], now=[])
    steps.append(last)
    legend = LEGEND_SP + ([['e-path', 'answer path']] if 'path' in want else [])
    return out('graph-paths', g, [schedule('Dijkstra', f'Dijkstra from {src}' + (', replacing a path only when a strictly shorter one is found' if spec.get('update') == 'strict' else ''), steps, legend)])


def bounded_animation(qid, spec, g):
    """Shortest paths with at most k edges: k rounds, each using only the previous round's values."""
    g.weighted()
    src, t, k = str(spec['source']), str(spec['target']), spec['rounds']
    rounds = [{v: None for v in g.nodes}]
    rounds[0][src] = Fraction(0)
    via = [{}]
    steps, ambiguous = [], set()
    cols = ['Vertex', '0'] + [f'≤{r}' for r in range(1, k + 1)]

    def snap(note, head, r, now=None, edge=None):
        rows = [[v] + [fw(rounds[j][v]) if j < len(rounds) and (j < r or (j == r and v in rounds[j])) else '' for j in range(k + 1)] for v in g.nodes]
        cur = {v: rounds[-1].get(v, rounds[-2][v] if len(rounds) > 1 else None) for v in g.nodes}
        n = {v: 'seen' for v in g.nodes if cur[v] is not None}
        n[src] = 'done'
        if now:
            n[now] = 'now'
        e = {}
        for v in g.nodes:
            for j in range(len(via) - 1, 0, -1):
                if v in via[j] and via[j][v] is not None and (j < len(via) - 1 or v in rounds[-1]):
                    e[str(via[j][v][1])] = 'tree'
                    break
        if edge is not None:
            e[str(edge)] = 'now'
        steps.append(step(note, head, n, e, {v: fw(cur[v]) for v in g.nodes}, dict(head=cols, rows=rows, now=[g.nodes.index(now)] if now else []),
                          ['Columns: the best distance from ' + src + ' using at most that many edges.']))

    snap(f"Start: {src} is 0 away using no edges and every other vertex is ∞; each round allows one more edge and uses only the previous round's values.", 'Start', 0)
    for r in range(1, k + 1):
        prev, cur, choice = rounds[-1], {}, {}
        rounds.append(cur)
        via.append(choice)
        for v in g.nodes:
            cands = [(prev[u] + w, u, i, w) for u, w, i in g.inn[v] if prev[u] is not None]
            best = min([c[0] for c in cands] + ([prev[v]] if prev[v] is not None else []), default=None)
            offers = [f"{plus(prev[u], w)} = {fw(a)} from {u}" for a, u, i, w in cands]
            parts = ', '.join(([f"keep {fw(prev[v])}"] + (['or ' + offers[0]] + offers[1:] if offers else [])) if prev[v] is not None else offers)
            winners = [c for c in cands if c[0] == best]
            within = f"With up to {r} edge{'s' if r > 1 else ''}, vertex {v}"
            if best is None:
                cur[v], choice[v] = None, None
                snap(f"{within} stays ∞: none of its neighbours was reachable yet.", f'Round {r}', r, v)
                continue
            if prev[v] is not None and prev[v] == best:
                cur[v], choice[v] = best, None
                if v == src:
                    continue
                snap(f"{within}: {parts}; nothing beats {fw(best)}, so it stays.", f'Round {r}', r, v)
                continue
            if len(winners) > 1:
                ambiguous.add((r, v))
            a, u, i, w = winners[0]
            cur[v], choice[v] = best, (u, i)
            snap(f"{within}: {parts}; it becomes {fw(best)}, from {u}." if len(cands) > 1 or prev[v] is not None else f"{within}: {parts}, so it becomes {fw(best)}.", f'Round {r}', r, v, i)
    # Walk the answer back through the rounds.
    path, ws, v, r = [t], [], t, k
    if rounds[k][t] is None:
        raise SystemExit(f'{qid}: {t} cannot be reached within {k} edges')
    while r > 0:
        if (r, v) in ambiguous:
            raise SystemExit(f'{qid}: two paths tie for {v} in round {r}, so the path is not determined')
        if via[r].get(v):
            u, i = via[r][v]
            ws.append(g.edges[i][2])
            path.append(u)
            v = u
        r -= 1
    path, ws = path[::-1], ws[::-1]
    if path[0] != src:
        raise SystemExit(f'{qid}: internal error walking back the path')
    want = spec['expect']
    check(qid, f'the best weight to {t} within {k} edges', fw(rounds[k][t]), fw(_num(want['dist'], qid)))
    if 'path' in want:
        check(qid, 'the path', path, [str(x) for x in want['path']])
    note = f"With at most {k} edges the cheapest {src}-to-{t} path is {('→' if g.directed else '–').join(path)}, of weight {total(ws)}."
    free = true_distances(g, src)[t]
    if free < rounds[k][t]:
        note += f" Without the limit, vertex {t} is only {fw(free)} away, but that needs more than {k} edges."
    last = dict(steps[-1])
    last.update(note=note, head='Finished', table=dict(last['table'], now=[]))
    last['n'] = {x: 'done' for x in path}
    last['e'] = {}
    v, r = t, k
    while r > 0:
        if via[r].get(v):
            last['e'][str(via[r][v][1])] = 'path'
            v = via[r][v][0]
        r -= 1
    steps.append(last)
    legend = [['n-now', 'being updated'], ['n-done', 'source'], ['e-now', 'best edge into it'], ['e-path', 'answer path']]
    return out('graph-paths', g, [schedule('Rounds', f'Shortest paths from {src} with at most {k} edges (Bellman-Ford rounds)', steps, legend)])


def dag_animation(qid, spec, g):
    """Best path scores in a DAG, in topological order: score(v) = best over edges u→v of score(u) (× or +) weight."""
    g.weighted()
    if not g.directed:
        raise SystemExit(f'{qid}: a DAG must be directed')
    src, op, best = str(spec['source']), spec['combine'], spec['best']
    if op not in ('product', 'sum') or best not in ('max', 'min'):
        raise SystemExit(f'{qid}: unknown DAG rule {op}/{best}')
    order = g.topo()
    score, came = {src: _num(spec['start_score'], qid)}, {}
    sym = '×' if op == 'product' else '+'
    steps = []

    def snap(note, head, now=None, edge=None):
        rows = [[v, fw(score[v]) if v in score else '', came[v][0] if v in came else ''] for v in order]
        n = {v: 'done' for v in score}
        if now:
            n[now] = 'now'
        e = {str(i): 'tree' for _, i in came.values()}
        if edge is not None:
            e[str(edge)] = 'now'
        steps.append(step(note, head, n, e, {v: fw(score[v]) for v in score}, dict(head=['Vertex', 'Score', 'From'], rows=rows, now=[order.index(now)] if now else [])))

    snap(f"score({src}) = {fw(score[src])}; take the vertices in the topological order {', '.join(order)}, so every predecessor is done first.", 'Start', src)
    for v in order:
        if v == src:
            continue
        cands = [((score[u] * w) if op == 'product' else score[u] + w, u, w, i) for u, w, i in g.inn[v] if u in score]
        if not cands:
            raise SystemExit(f'{qid}: {v} cannot be reached from {src}')
        pick = (max if best == 'max' else min)(cands, key=lambda c: c[0])
        score[v], came[v] = pick[0], (pick[1], pick[3])
        parts = [f"score({u}) {sym} {fw(w)} = {fw(a)}" for a, u, w, i in cands]
        note = (f"score({v}) = {parts[0]}, from {pick[1]}." if len(parts) == 1 else
                f"score({v}) = {best}({', '.join(parts)}) = {fw(pick[0])}, from {pick[1]}.")
        snap(note, f'Vertex {v}', v, pick[3])
    want = spec['expect']
    if 'scores' in want:
        check(qid, 'the scores', {v: fw(score[v]) for v in want['scores']}, {v: fw(_num(x, qid)) for v, x in want['scores'].items()})
    s = sum(score.values(), Fraction(0))
    check(qid, 'the sum of all scores', fw(s), fw(_num(want['total'], qid)))
    last = dict(steps[-1])
    last.update(note=f"Sum of all scores: {total([score[v] for v in order])}.", head='Finished', table=dict(last['table'], now=[]))
    last['n'] = {v: 'done' for v in order}
    last['e'] = {str(i): 'tree' for _, i in came.values()}
    steps.append(last)
    legend = [['n-now', 'being scored'], ['n-done', 'scored'], ['e-now', 'best incoming edge'], ['e-tree', 'best edges so far']]
    word = {'product': 'product', 'sum': 'sum'}[op]
    return out('graph-paths', g, [schedule('DAG', f'{"Largest" if best == "max" else "Smallest"} path {word} from {src}, in topological order', steps, legend)])


def paths_animation(qid, spec):
    g = Graph(qid, spec)
    algo = spec.get('algo')
    if algo == 'dijkstra':
        return dijkstra_animation(qid, spec, g)
    if algo == 'bounded':
        return bounded_animation(qid, spec, g)
    if algo == 'dag':
        return dag_animation(qid, spec, g)
    raise SystemExit(f'{qid}: unknown shortest-path algorithm {algo}')


# ---------------------------------------------------------------- minimum spanning trees

class DSU:
    def __init__(self, nodes):
        self.p = {v: v for v in nodes}

    def find(self, v):
        while self.p[v] != v:
            self.p[v] = self.p[self.p[v]]
            v = self.p[v]
        return v

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[b] = a
        return True


def spanning_trees(g, nodes):
    """Every spanning tree of the subgraph on nodes, as (weight, edge indices). Small graphs only."""
    idx = [i for i, (u, v, _) in enumerate(g.edges) if u in nodes and v in nodes]
    if comb(len(idx), len(nodes) - 1) > 300000:
        raise SystemExit(f'{g.qid}: too many edge subsets to check every spanning tree')
    found = []
    for sub in combinations(idx, len(nodes) - 1):
        d = DSU(nodes)
        if all(d.union(g.edges[i][0], g.edges[i][1]) for i in sub):
            found.append((sum((g.edges[i][2] for i in sub), Fraction(0)), sub))
    if not found:
        raise SystemExit(f'{g.qid}: the graph is not connected')
    return found


def comp_name(g, d, x, nodes):
    members = [v for v in nodes if d.find(v) == d.find(x)]
    return members[0] if len(members) == 1 else '{' + ', '.join(members) + '}'


def weight_class(g, d, cls, nodes):
    """For the equal-weight edges cls, given the components d so far: how many ways they can be used, and a note."""
    cand = [i for i in cls if d.find(g.edges[i][0]) != d.find(g.edges[i][1])]
    if not cand:
        return 1, None
    roots = lambda i: (d.find(g.edges[i][0]), d.find(g.edges[i][1]))
    # The rank: how many of these edges any minimum tree uses.
    t = DSU({r for i in cand for r in roots(i)})
    rank = sum(t.union(*roots(i)) for i in cand)
    ways = 0
    for sub in combinations(cand, rank):
        s = DSU({r for i in cand for r in roots(i)})
        ways += all(s.union(*roots(i)) for i in sub)
    if ways == 1:
        return 1, None
    w = fw(g.edges[cand[0]][2])
    groups = {}
    for i in cand:
        groups.setdefault(frozenset(roots(i)), []).append(i)
    if len(groups) == rank:  # the joined components form a forest: one independent choice per pair
        parts, sizes = [], []
        for key, es in groups.items():
            a, b = (g.edges[es[0]][0], g.edges[es[0]][1])
            names = [g.name(i) for i in es]
            joined = f"join {comp_name(g, d, a, nodes)} and {comp_name(g, d, b, nodes)}"
            parts.append(f"{', '.join(names[:-1]) + ' or ' + names[-1] if len(names) > 1 else names[0]} {'can ' if len(names) > 1 else 'must '}{joined}")
            sizes.append(len(es))
        many = [str(s) for s in sizes if s > 1]
        note = f"Weight {w}: " + '; '.join(parts) + f", so there are {' × '.join(many) + ' = ' if len(many) > 1 else ''}{ways} equally good ways to use this weight."
    else:
        note = f"Weight {w}: {rank} of {_list([g.name(i) for i in cand])} are needed, and they can be chosen in {ways} ways."
    return ways, note


LEGEND_MST = [['e-now', 'edge being considered'], ['e-tree', 'taken'], ['e-bad', 'skipped'], ['n-done', 'in the tree so far']]


def kruskal(g, nodes=None, script_note=None):
    """Kruskal on the subgraph on nodes, equal weights in the listed order. Returns accepted edges, steps and the ways per weight."""
    g.weighted()
    nodes = nodes or g.nodes
    order = sorted((i for i, (u, v, _) in enumerate(g.edges) if u in nodes and v in nodes), key=lambda i: (g.edges[i][2], i))
    d, taken, skipped, rows, steps, ways = DSU(nodes), [], [], [], [], []
    off = {str(i): 'off' for i, (u, v, _) in enumerate(g.edges) if u not in nodes or v not in nodes}

    def snap(note, head, now=None):
        n = {x: 'done' for i in taken for x in g.edges[i][:2]}
        for x in g.nodes:
            if x not in nodes:
                n[x] = 'off'
        e = dict(off)
        e.update({str(i): 'tree' for i in taken})
        e.update({str(i): 'bad' for i in skipped})
        if now is not None:
            e[str(now)] = 'now'
            for x in g.edges[now][:2]:
                n[x] = 'now'
        steps.append(step(note, head, n, e, None, dict(head=['Edge', 'Weight', 'Result'], rows=[list(r) for r in rows], now=[len(rows) - 1] if now is not None else [])))

    snap(script_note or f"Sort the {len(order)} edges by weight and take them in that order, skipping any that would close a cycle; equal weights go in the listed order.", 'Start')
    k = 0
    while k < len(order) and len(taken) < len(nodes) - 1:
        w = g.edges[order[k]][2]
        cls = [i for i in order[k:] if g.edges[i][2] == w]
        m, note = weight_class(g, d, cls, nodes)
        ways.append((w, m))
        if note:
            snap(note, f'Weight {fw(w)}')
        for i in cls:
            if len(taken) == len(nodes) - 1:
                break
            u, v, _ = g.edges[i]
            if d.union(u, v):
                taken.append(i)
                rows.append([g.name(i), fw(w), 'taken'])
                snap(f"Take {g.name(i)} ({fw(w)}): {u} and {v} are not yet connected.", f'Edge {g.name(i)}', i)
            else:
                skipped.append(i)
                rows.append([g.name(i), fw(w), 'skipped'])
                snap(f"Skip {g.name(i)} ({fw(w)}): {u} and {v} are already connected, so it would close a cycle.", f'Edge {g.name(i)}', i)
        k += len(cls)
    if len(taken) != len(nodes) - 1:
        raise SystemExit(f'{g.qid}: the graph is not connected')
    weight = sum((g.edges[i][2] for i in taken), Fraction(0))
    return dict(taken=taken, steps=steps, ways=ways, weight=weight, d=d, snap=snap)


def finish(steps, note, e=None, n=None):
    last = dict(steps[-1])
    last.update(note=note, head='Finished')
    if 'table' in last:
        last['table'] = dict(last['table'], now=[])
    if e is not None:
        last['e'] = e
    if n is not None:
        last['n'] = n
    steps.append(last)
    return steps


def mst_animation(qid, spec):
    g = Graph(qid, spec)
    q, want = spec.get('query'), spec.get('expect', {})
    if g.directed:
        raise SystemExit(f'{qid}: spanning trees need an undirected graph')
    if q == 'check':
        return mst_check(qid, spec, g)
    if q == 'leaf':
        return mst_leaf(qid, spec, g)
    if q not in ('weight', 'edges', 'count', 'path'):
        raise SystemExit(f'{qid}: unknown MST query {q}')
    r = kruskal(g)
    trees = spanning_trees(g, g.nodes)
    best = min(t[0] for t in trees)
    minimal = [t for t in trees if t[0] == best]
    if r['weight'] != best:
        raise SystemExit(f'{qid}: internal error, Kruskal gives {r["weight"]} but the lightest tree weighs {best}')
    count = 1
    for _, m in r['ways']:
        count *= m
    if count != len(minimal):
        raise SystemExit(f'{qid}: internal error, {count} ways by weight but {len(minimal)} minimum trees')
    if 'weight' in want:
        check(qid, 'the MST weight', fw(best), fw(_num(want['weight'], qid)))
    ws = [g.edges[i][2] for i in r['taken']]
    tree_e = {str(i): 'tree' for i in r['taken']}
    steps = r['steps']
    if q == 'weight':
        note = f"Done: {len(ws)} edges with total weight {total(ws)}" + (". Other choices among equal weights give other trees of the same weight." if count > 1 else ".")
    elif q == 'edges':
        exp = {frozenset(map(str, e)) for e in want['edges']}
        check(qid, 'the tree drawn', {frozenset(g.edges[i][:2]) for i in r['taken']}, exp)
        note = f"Done: {_list([g.name(i) for i in r['taken']])}, total {total(ws)}" + (
            f"; {'one other minimum tree uses' if count == 2 else f'{count - 1} other minimum trees use'} a different edge of the same weight." if count > 1 else ".")
    elif q == 'count':
        check(qid, 'the number of minimum spanning trees', len(minimal), want['count'])
        many = [(w, m) for w, m in r['ways'] if m > 1]
        if len(many) == 1:
            how = f"The {count} ways at weight {fw(many[0][0])} give {count} minimum spanning trees"
        else:
            how = f"Multiplying the choices at each weight, {' × '.join(str(m) for _, m in many)} = {count} minimum spanning tree{'s' if count != 1 else ''}"
        note = f"{how}, each of weight {total(ws)}."
    else:
        if count != 1:
            raise SystemExit(f'{qid}: the minimum spanning tree is not unique, so its paths are not determined')
        a, b = str(spec['from']), str(spec['to'])
        adj = {}
        for i in r['taken']:
            u, v, _ = g.edges[i]
            adj.setdefault(u, []).append((v, i))
            adj.setdefault(v, []).append((u, i))
        prev, queue = {a: None}, deque([a])
        while queue:
            x = queue.popleft()
            for y, i in adj.get(x, []):
                if y not in prev:
                    prev[y] = (x, i)
                    queue.append(y)
        path, pe, x = [b], [], b
        while prev[x]:
            x, i = prev[x]
            path.append(x)
            pe.append(i)
        path, pe = path[::-1], pe[::-1]
        pw = [g.edges[i][2] for i in pe]
        check(qid, f'the tree path weight from {a} to {b}', fw(sum(pw, Fraction(0))), fw(_num(want['path_weight'], qid)))
        if 'path' in want:
            check(qid, 'the tree path', path, [str(x) for x in want['path']])
        e = dict(tree_e)
        e.update({str(i): 'path' for i in pe})
        last = dict(steps[-1])
        last.update(note=f"The tree is complete with {len(ws)} edges and is the only minimum tree; its path from {a} to {b} is {'–'.join(path)}.",
                    head=f'Path {a} to {b}', e=e, n={x: 'done' for x in g.nodes}, table=dict(last['table'], now=[]))
        steps.append(last)
        note = f"Its weight is {total(pw)}."
        finish(steps, note, e)
        legend = LEGEND_MST + [['e-path', 'path in the tree']]
        return out('graph-mst', g, [schedule('Kruskal', 'Kruskal: lightest edges first, skipping any that close a cycle', steps, legend)])
    finish(steps, note, tree_e, {x: 'done' for x in g.nodes})
    return out('graph-mst', g, [schedule('Kruskal', 'Kruskal: lightest edges first, skipping any that close a cycle', steps, LEGEND_MST)])


def mst_leaf(qid, spec, g):
    leaf = str(spec['leaf'])
    rest = [v for v in g.nodes if v != leaf]
    r = kruskal(g, rest, f"Vertex {leaf} must be a leaf, so it joins by exactly one edge: build a minimum tree on the other vertices first, then attach {leaf} by its cheapest edge.")
    steps = r['steps']
    near = sorted(((w, i) for _, w, i in g.out[leaf]), key=lambda x: (x[0], x[1]))
    w0, i0 = near[0]
    same = [g.name(i) for w, i in near[1:] if w == w0]
    e = {str(i): 'tree' for i in r['taken']}
    e[str(i0)] = 'now'
    last = dict(steps[-1])
    last.update(head=f'Attach {leaf}', e=e, n={x: 'done' for x in g.nodes} | {leaf: 'now'},
                note=f"Attach {leaf} by its cheapest edge, {g.name(i0)} ({fw(w0)})" + (f"; {_list(same)} is just as cheap." if same else "."),
                table=dict(head=last['table']['head'], rows=last['table']['rows'] + [[g.name(i0), fw(w0), 'attach']], now=[len(last['table']['rows'])]))
    steps.append(last)
    ws = [g.edges[i][2] for i in r['taken']]
    weight = r['weight'] + w0
    best = min(t for t, sub in spanning_trees(g, g.nodes) if sum(leaf in g.edges[i][:2] for i in sub) == 1)
    if best != weight:
        raise SystemExit(f'{qid}: internal error, the leaf construction gives {weight} but the best is {best}')
    check(qid, f'the lightest tree with {leaf} as a leaf', fw(weight), fw(_num(spec['expect']['weight'], qid)))
    e = dict(e)
    e[str(i0)] = 'tree'
    finish(steps, f"Total: {total(ws)} for the other vertices, plus {fw(w0)} for {leaf}, giving {fw(weight)}.", e, {x: 'done' for x in g.nodes})
    return out('graph-mst', g, [schedule('Kruskal', f'Kruskal on the vertices other than {leaf}, then attach {leaf}', steps, LEGEND_MST)])


def mst_check(qid, spec, g):
    """Is each listed sequence a possible order in which Kruskal accepts edges (any tie order)?"""
    g.weighted()
    lookup = {}
    for i, (u, v, _) in enumerate(g.edges):
        lookup[(u, v)] = lookup[(v, u)] = i
    scheds = []
    for opt in spec['orders']:
        seq = []
        for e in opt['seq']:
            e = [str(x) for x in e]
            if tuple(e) not in lookup:
                raise SystemExit(f'{qid}: option {opt["label"]} uses {e}, which is not an edge')
            seq.append(lookup[tuple(e)])
        d, taken, rows, steps, ok = DSU(g.nodes), [], [], [], True

        def snap(note, head, now=None, bad=False, first=None):
            n = {x: 'done' for i in taken for x in g.edges[i][:2]}
            e = {str(i): 'tree' for i in taken}
            if now is not None:
                e[str(now)] = 'bad' if bad else 'now'
                for x in g.edges[now][:2]:
                    n[x] = 'now'
            if first is not None:
                e[str(first)] = 'path'
            steps.append(step(note, head, n, e, None, dict(head=['Edge', 'Weight', 'Check'], rows=[list(r) for r in rows], now=[len(rows) - 1] if rows and now is not None else [])))

        names = ', '.join(g.name(i) for i in seq)
        snap(f"Check {opt['label']}: {names}. Kruskal may take an edge only if no lighter edge still joins two separate parts.", f"Option {opt['label']}")
        for i in seq:
            u, v, w = g.edges[i]
            lighter = [j for j in range(len(g.edges)) if j not in taken and g.edges[j][2] < w and d.find(g.edges[j][0]) != d.find(g.edges[j][1])]
            if d.find(u) == d.find(v):
                rows.append([g.name(i), fw(w), 'closes a cycle'])
                snap(f"{g.name(i)} ({fw(w)}) cannot come next: {u} and {v} are already connected, so it would close a cycle.", f'Edge {g.name(i)}', i, True)
                ok = False
                break
            if lighter:
                j = min(lighter, key=lambda j: (g.edges[j][2], j))
                rows.append([g.name(i), fw(w), f'{g.name(j)} ({fw(g.edges[j][2])}) first'])
                snap(f"{g.name(i)} ({fw(w)}) cannot come next: {g.name(j)} ({fw(g.edges[j][2])}) is lighter and still joins two separate parts, so Kruskal takes it first.", f'Edge {g.name(i)}', i, True, j)
                ok = False
                break
            d.union(u, v)
            taken.append(i)
            rows.append([g.name(i), fw(w), 'possible'])
            snap(f"{g.name(i)} ({fw(w)}) can come next: {u} and {v} are in different parts and no lighter edge still joins two parts.", f'Edge {g.name(i)}', i)
        if ok and len(taken) != len(g.nodes) - 1:
            raise SystemExit(f'{qid}: option {opt["label"]} does not list a whole spanning tree')
        check(qid, f'whether option {opt["label"]} is a possible Kruskal order', ok, opt['expect'])
        finish(steps, f"So {names} {'is' if ok else 'is not'} a possible Kruskal order.")
        legend = [['e-now', 'edge being checked'], ['e-tree', 'accepted so far'], ['e-bad', 'not possible here']] + ([] if ok else [['e-path', 'lighter edge Kruskal takes first']])
        scheds.append(schedule(opt['label'], f"Option {opt['label']}: could Kruskal accept the edges in this order?", steps, legend))
    return out('graph-mst', g, scheds)


# ---------------------------------------------------------------- searches

def bfs_check(g, seq, label):
    """Is seq a possible queue-based BFS order from seq[0], for some neighbour order?"""
    seq = spec_order(g, seq, f'option {label}')
    start, pos, queue, found, tree, steps = seq[0], 1, deque([seq[0]]), {seq[0]: 0}, [], []
    level = {start: 0}

    def snap(note, head, now=None):
        n = {v: 'done' for v in seq[:pos] if v not in queue}
        n.update({v: 'seen' for v in queue})
        if now:
            n[now] = 'now'
        steps.append(step(note, head, n, {str(i): 'tree' for i in tree}, {v: str(seq.index(v) + 1) for v in seq[:pos]}, None,
                          [f"Order to check: {', '.join(seq)}", 'Queue: ' + (', '.join(queue) if queue else 'empty')]))

    snap(f"Start at {start}: it is visited first and goes into the queue.", f'Start at {start}', start)
    ok = True
    while queue:
        u = queue.popleft()
        new = []
        for v, _, i in g.out[u]:
            if v not in found and v not in new:
                new.append(v)
        nxt = seq[pos:pos + len(new)]
        if not new:
            snap(f"Dequeue {u}: all its neighbours are already discovered, so nothing joins the queue.", f'Dequeue {u}', u)
            continue
        if set(nxt) != set(new):
            snap(f"Dequeue {u}: its undiscovered neighbour{'s are' if len(new) > 1 else ' is'} {_list(sorted(new, key=g.nodes.index))}, but the order lists {_list(nxt)} next, so this is not a BFS order.", f'Dequeue {u}', u)
            ok = False
            break
        for v in nxt:
            found[v] = len(found)
            level[v] = level[u] + 1
            tree.append(next(i for x, _, i in g.out[u] if x == v))
            queue.append(v)
        pos += len(nxt)
        snap(f"Dequeue {u}: its undiscovered neighbour{'s' if len(new) > 1 else ''} {_list(nxt)} come{'' if len(new) > 1 else 's'} next in the order and join{'' if len(new) > 1 else 's'} the queue.", f'Dequeue {u}', u)
    if ok and pos != len(seq):
        raise SystemExit(f'{g.qid}: option {label} visits vertices BFS from {start} cannot reach')
    return ok, steps


def dfs_check(g, seq, label):
    """Is seq a possible recursive DFS discovery order from seq[0], for some neighbour order?"""
    seq = spec_order(g, seq, f'option {label}')
    stack, seen, tree, steps = [seq[0]], {seq[0]}, [], []

    def snap(note, head, now=None, edge=None):
        n = {v: 'done' for v in seen if v not in stack}
        n.update({v: 'seen' for v in stack})
        if now:
            n[now] = 'now'
        e = {str(i): 'tree' for i in tree}
        steps.append(step(note, head, n, e, {v: str(seq.index(v) + 1) for v in seen}, None,
                          [f"Order to check: {', '.join(seq)}", 'Stack: ' + ', '.join(stack)]))

    snap(f"Start at {seq[0]}.", f'Start at {seq[0]}', seq[0])
    for x in seq[1:]:
        while stack and not [v for v, _, _ in g.out[stack[-1]] if v not in seen]:
            done = stack.pop()
            if not stack:
                raise SystemExit(f'{g.qid}: option {label} needs a vertex DFS from {seq[0]} cannot reach')
            snap(f"{done} has no unvisited neighbours left, so DFS backs up to {stack[-1]}.", f'Back to {stack[-1]}', stack[-1])
        top = stack[-1]
        free = [v for v, _, _ in g.out[top] if v not in seen]
        if x not in free:
            snap(f"{top} still has unvisited neighbour{'s' if len(free) > 1 else ''} {_list(sorted(free, key=g.nodes.index))}, so DFS cannot go to {x} next; this is not a DFS order.", f'{top} → {x}?', top)
            return False, steps
        i = next(i for v, _, i in g.out[top] if v == x)
        stack.append(x)
        seen.add(x)
        tree.append(i)
        snap(f"Go from {top} to {x}: {x} is an unvisited neighbour of {top}.", f'Visit {x}', x)
    return True, steps


def search_animation(qid, spec):
    g = Graph(qid, spec)
    algo = spec.get('algo')
    if algo in ('bfs', 'dfs'):
        scheds = []
        for opt in spec['orders']:
            ok, steps = (bfs_check if algo == 'bfs' else dfs_check)(g, opt['seq'], opt['label'])
            check(qid, f'whether option {opt["label"]} is a possible {algo.upper()} order', ok, opt['expect'])
            seq = ', '.join(map(str, opt['seq']))
            finish(steps, f"Every step fits, so {seq} is a possible {algo.upper()} order." if ok else f"So {seq} is not a possible {algo.upper()} order.")
            legend = [['n-now', 'current vertex'], ['n-seen', 'in the queue' if algo == 'bfs' else 'on the stack'], ['n-done', 'finished'], ['e-tree', 'tree edge']]
            scheds.append(schedule(opt['label'], f"Option {opt['label']}: could {'breadth' if algo == 'bfs' else 'depth'}-first search visit the vertices in this order?", steps, legend))
        return out('graph-search', g, scheds)
    if algo == 'double-bfs':
        return double_bfs(qid, spec, g)
    raise SystemExit(f'{qid}: unknown search {algo}')


def bfs_levels(g, s):
    dist, order = {s: 0}, [s]
    for u in order:
        for v, _, _ in g.out[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                order.append(v)
    return dist, order


def double_bfs(qid, spec, g):
    """BFS from v, take a farthest vertex u, BFS from u, report the largest distance. Checked for every v and every choice of u."""
    results = set()
    for v in g.nodes:
        dist, _ = bfs_levels(g, v)
        if len(dist) != len(g.nodes):
            raise SystemExit(f'{qid}: the graph is not connected')
        far = max(dist.values())
        for u in [x for x in g.nodes if dist[x] == far]:
            results.add(max(bfs_levels(g, u)[0].values()))
    if len(results) != 1:
        raise SystemExit(f'{qid}: the reported distance depends on the start or on the farthest vertex chosen: {sorted(results)}')
    check(qid, 'the reported distance', results.pop(), spec['expect'])
    steps, start = [], str(spec['show_from'])

    def run(s, other=None):
        dist, order = bfs_levels(g, s)
        tree = {}
        for u in order:
            for v, _, i in g.out[u]:
                if dist.get(v) == dist[u] + 1 and v not in tree:
                    tree[v] = i
        far = max(dist.values())
        for d in range(far + 1):
            layer = [v for v in order if dist[v] == d]
            n = {v: 'done' for v in order if dist[v] < d}
            n.update({v: 'now' for v in layer})
            if other:
                n.setdefault(other, 'seen')
            e = {str(tree[v]): 'tree' for v in order if v in tree and dist[v] <= d}
            tag = {v: str(dist[v]) for v in order if dist[v] <= d}
            if d == 0:
                note = f"First pass: run BFS from {s}; any starting vertex would do." if other is None else f"Second pass: run BFS again, now from {s}."
            else:
                note = f"Distance {d} from {s}: {_list(layer)}."
            steps.append(step(note, f'BFS from {s}', n, e, tag, None, [f"Distance {d}: {', '.join(layer)}"]))
        return dist, [v for v in order if dist[v] == far], far

    dist, far_set, far = run(start)
    u = far_set[0]
    steps[-1]['note'] = (f"Distance {far} from {start}: {_list(far_set)}. These are the farthest" + (f"; take {u} (any of them gives the same final answer)." if len(far_set) > 1 else f", so take {u}."))
    dist2, far2, d2 = run(u, start)
    steps[-1]['note'] = f"Distance {d2} from {u}: {_list(far2)}, the farthest, so the algorithm reports {d2}."
    path = [far2[0]]
    while path[-1] != u:
        x = path[-1]
        path.append(next(y for y, _, _ in g.out[x] if dist2.get(y) == dist2[x] - 1))
    e = {}
    for a, b in zip(path, path[1:]):
        e[str(next(i for y, _, i in g.out[a] if y == b))] = 'path'
    last = dict(steps[-1])
    last.update(head='Finished', note=f"The path {'–'.join(path[::-1])} has {d2} edges, so the reported distance is {d2}.", e=e, n={x: 'done' for x in path}, line=None)
    last.pop('line', None)
    steps.append(last)
    legend = [['n-now', 'this distance'], ['n-done', 'closer'], ['e-tree', 'BFS tree edge'], ['e-path', 'longest path found']]
    return out('graph-search', g, [schedule('Two BFS', 'BFS from one vertex, then BFS again from a farthest vertex', steps, legend)])


# ---------------------------------------------------------------- topological orders

def all_topo(g, cap=5000):
    deg0 = {v: len(g.inn[v]) for v in g.nodes}
    found = []

    def go(order, deg):
        if len(found) > cap:
            raise SystemExit(f'{g.qid}: too many topological orders to list')
        if len(order) == len(g.nodes):
            found.append(list(order))
            return
        for v in g.nodes:
            if v not in order and deg[v] == 0:
                nd = dict(deg)
                for x, _, _ in g.out[v]:
                    nd[x] -= 1
                go(order + [v], nd)
    go([], deg0)
    if not found:
        raise SystemExit(f'{g.qid}: the graph has a directed cycle')
    return found


def kahn_trace(g, order):
    deg = {v: len(g.inn[v]) for v in g.nodes}
    placed, steps = [], []

    def snap(note, head, now=None):
        n = {v: 'done' for v in placed}
        n.update({v: 'seen' for v in g.nodes if v not in placed and deg[v] == 0})
        if now:
            n[now] = 'now'
        e = {str(i): 'off' for v in placed for _, _, i in g.out[v]}
        if now:
            e.update({str(i): 'now' for _, _, i in g.out[now]})
        rows = [[v, str(deg[v]) if v not in placed or v == now else '', str(placed.index(v) + 1) if v in placed else ''] for v in g.nodes]
        steps.append(step(note, head, n, e, {v: str(placed.index(v) + 1) for v in placed}, dict(head=['Vertex', 'In-degree left', 'Position'], rows=rows, now=[g.nodes.index(now)] if now else []),
                          ['Order so far: ' + (', '.join(placed) if placed else '(none)')]))

    ready = [v for v in g.nodes if deg[v] == 0]
    snap(f"Count incoming edges; {_list(ready)} {'have' if len(ready) > 1 else 'has'} none, so {'either' if len(ready) == 2 else 'any of them' if len(ready) > 2 else 'it'} can go first.", 'Start')
    for v in order:
        ready = [x for x in g.nodes if x not in placed and deg[x] == 0]
        if v not in ready:
            raise SystemExit(f'{g.qid}: internal error, {v} is not ready')
        lowered = []
        for x, _, _ in g.out[v]:
            deg[x] -= 1
            lowered.append(f"{x} to {deg[x]}")
        placed.append(v)
        why = f"Take {v}, the only vertex with no incoming edge left" if len(ready) == 1 else f"{_list(ready)} have no incoming edge left; take {v}"
        snap(why + (f", and removing its edges lowers {_list(lowered)}." if lowered else "."), f'Take {v}', v)
    return steps


def topo_animation(qid, spec):
    g = Graph(qid, spec)
    if not g.directed:
        raise SystemExit(f'{qid}: topological order needs a directed graph')
    algo, want = spec.get('algo'), spec.get('expect')
    legend = [['n-now', 'just placed'], ['n-seen', 'ready (no incoming edge left)'], ['n-done', 'placed'], ['e-now', 'edges removed now']]
    if algo == 'check':
        scheds = []
        for opt in spec['orders']:
            seq = spec_order(g, opt['seq'], f'option {opt["label"]}')
            placed, steps, ok = [], [], True

            def snap(note, head, now=None, bad=None):
                n = {v: 'done' for v in placed}
                e = {}
                if now:
                    n[now] = 'now'
                    for u, _, i in g.inn[now]:
                        e[str(i)] = 'now' if u in (bad or []) else 'tree'
                steps.append(step(note, head, n, e, {v: str(placed.index(v) + 1) for v in placed}, None, [f"Order to check: {', '.join(seq)}"]))

            snap(f"Check {', '.join(seq)}: every edge must point from an earlier vertex to a later one.", f"Option {opt['label']}")
            for v in seq:
                preds = [u for u, _, _ in g.inn[v]]
                missing = [u for u in preds if u not in placed]
                if missing:
                    snap(f"{v} cannot come next: {_list([g.arrow(u, v) for u in missing])} need{'s' if len(missing) == 1 else ''} {_list(missing)} before {v}, and {'it has' if len(missing) == 1 else 'they have'} not been placed yet.", f'Place {v}?', v, missing)
                    ok = False
                    break
                placed.append(v)
                snap(f"Place {v}: " + (f"{'its predecessor' if len(preds) == 1 else 'its predecessors'} {_list(preds)} {'is' if len(preds) == 1 else 'are'} already placed." if preds else "it has no incoming edges."), f'Place {v}', v)
            check(qid, f'whether option {opt["label"]} is a topological order', ok, opt['expect'])
            finish(steps, f"Every edge points forward, so {', '.join(seq)} is a topological order." if ok else f"So {', '.join(seq)} is not a topological order.")
            scheds.append(schedule(opt['label'], f"Option {opt['label']}: is this a topological order?", steps, [['n-now', 'vertex being placed'], ['n-done', 'placed'], ['e-tree', 'edge already satisfied'], ['e-now', 'edge that fails']]))
        return out('graph-topo', g, scheds)
    if algo != 'kahn':
        raise SystemExit(f'{qid}: unknown topological algorithm {algo}')
    orders = all_topo(g)
    if 'orders' in want:
        check(qid, 'the topological orders', sorted(orders), sorted([str(x) for x in o] for o in want['orders']))
    if 'count' in want:
        check(qid, 'the number of topological orders', len(orders), want['count'])
    scheds = []
    shown = orders if len(orders) <= 4 else orders[:1]
    for o in shown:
        steps = kahn_trace(g, o)
        if len(orders) == 1:
            note = f"Done: {', '.join(o)} is the only topological order."
        elif len(shown) > 1:
            note = f"Done: {', '.join(o)}. Choosing differently when several vertices were ready gives the other order{'s' if len(orders) > 2 else ''}, {_list([', '.join(x) for x in orders if x != o])}; these {len(orders)} are all the topological orders."
        else:
            sep = '' if all(len(v) == 1 for v in g.nodes) else ' '
            note = f"Done: {', '.join(o)}. Choosing differently whenever several vertices are ready gives {len(orders)} orders in all: " + ', '.join(sep.join(x) for x in orders) + '.'
        finish(steps, note)
        scheds.append(schedule(''.join(o) if len(''.join(o)) <= 8 else ' '.join(o), "Kahn's algorithm: repeatedly take a vertex with no incoming edge left", steps, legend))
    return out('graph-topo', g, scheds, tabs_label='orders')


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'graph-paths': paths_animation, 'graph-mst': mst_animation, 'graph-search': search_animation, 'graph-topo': topo_animation}
PLAYER = 'graph'
TABS = 'options'  # several tabs are the options being checked; Kahn's orders set their own label
