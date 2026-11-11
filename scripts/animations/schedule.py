"""Database transaction schedules: precedence graphs, serializability, recoverability.

Data: data/animations/schedule.json. A spec lists one or more schedules (tabs),
each a list of operations written as in the question: r1(X) / R1(X) read,
w1(X) / W1(X) write, c1 commit, a1 abort (an optional underscore after the
letter is allowed). Each tab's `expect` may give:
  conflict_serializable, view_serializable   true or false
  orders       the correct serial orders among the tab's `candidates`
  recoverable, cascadeless, strict           true or false
  rollback     the transactions that must roll back when the aborts happen
  equivalent   true or false, with `compare_to` naming another tab: are the two
               schedules conflict equivalent?
Everything is computed here, and the build stops on any difference.

Two operations conflict when they belong to different transactions, use the
same item and at least one writes; each conflict adds an edge from the earlier
transaction to the later one. A read reads from the last earlier write of that
item by a transaction that has not aborted (or the initial value).
"""
import re
from itertools import permutations

from .common import _list

OP = re.compile(r'^([RrWw])_?(\d+)\(\s*([A-Za-z][\w′]*)\s*\)$')
END = re.compile(r'^([CcAa])_?(\d+)$')
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')


def parse(qid, ops):
    out = []
    for s in ops:
        plain = s.translate(SUB)
        m, e = OP.match(plain), END.match(plain)
        if m:
            out.append(dict(t='T' + m.group(2), a=m.group(1).lower(), x=m.group(3), label=s))
        elif e:
            out.append(dict(t='T' + e.group(2), a=e.group(1).lower(), x=None, label=s))
        else:
            raise SystemExit(f'{qid}: cannot read the operation {s!r}')
    for t in {o['t'] for o in out}:
        ends = [k for k, o in enumerate(out) if o['t'] == t and o['a'] in 'ca']
        if len(ends) > 1 or (ends and any(o['t'] == t for o in out[ends[0] + 1:])):
            raise SystemExit(f'{qid}: {t} acts after it has committed or aborted')
    return out


def txns(ops):
    return sorted({o['t'] for o in ops}, key=lambda t: int(t[1:]))


def conflicts(ops):
    """Every conflicting pair (earlier index, later index)."""
    return [(i, j) for j, b in enumerate(ops) for i, a in enumerate(ops[:j])
            if a['x'] and b['x'] and a['x'] == b['x'] and a['t'] != b['t'] and 'w' in (a['a'], b['a'])]


def edges(ops):
    seen = {}
    for i, j in conflicts(ops):
        seen.setdefault((ops[i]['t'], ops[j]['t']), (i, j))
    return seen


def cycle(nodes, es):
    """A directed cycle as a list of nodes (first repeated at the end), or None."""
    out = {n: [v for (u, v) in es if u == n] for n in nodes}
    state, stack = {}, []

    def go(u):
        state[u] = 1
        stack.append(u)
        for v in out[u]:
            if state.get(v) == 1:
                return stack[stack.index(v):] + [v]
            if not state.get(v):
                c = go(v)
                if c:
                    return c
        state[u] = 2
        stack.pop()
        return None
    for n in nodes:
        if not state.get(n):
            c = go(n)
            if c:
                return c
    return None


def topo_orders(nodes, es):
    return [list(p) for p in permutations(nodes) if all(p.index(u) < p.index(v) for u, v in es)]


def reads_from(ops):
    """For each read index: the index of the write it reads (None = initial value or its own write)."""
    out, aborted = {}, set()
    for j, o in enumerate(ops):
        if o['a'] == 'a':
            aborted.add(o['t'])
        if o['a'] != 'r':
            continue
        src = None
        for i in range(j - 1, -1, -1):
            p = ops[i]
            if p['a'] == 'w' and p['x'] == o['x'] and p['t'] not in aborted:
                src = i
                break
        out[j] = None if src is None or ops[src]['t'] == o['t'] else src
    return out


def _view(ops, order):
    """Reads-from (by transaction) and final writers of the serial schedule `order`."""
    serial = [o for t in order for o in ops if o['t'] == t]
    return _view_of(serial)


def _view_of(ops):
    rf, last = [], {}
    count = {}
    for o in ops:
        if o['a'] == 'r':
            k = count[(o['t'], o['x'])] = count.get((o['t'], o['x']), 0) + 1
            rf.append((o['t'], o['x'], k, last.get(o['x'])))
        elif o['a'] == 'w':
            last[o['x']] = o['t']
    return sorted(rf, key=str), sorted(last.items())


def ended(ops, upto):
    """Transactions that have committed (c) or aborted (a) before index `upto`."""
    return {o['t']: o['a'] for o in ops[:upto] if o['a'] in 'ca'}


def recovery(ops):
    rf = reads_from(ops)
    deps = [(j, i) for j, i in rf.items() if i is not None]
    commit = {o['t']: k for k, o in enumerate(ops) if o['a'] == 'c'}
    recoverable = all(not (ops[j]['t'] in commit and not (ops[i]['t'] in commit and commit[ops[i]['t']] < commit[ops[j]['t']])) for j, i in deps)
    cascadeless = all(ended(ops, j).get(ops[i]['t']) == 'c' for j, i in deps)
    strict = True
    for j, o in enumerate(ops):
        if o['a'] not in 'rw':
            continue
        for i in range(j - 1, -1, -1):
            p = ops[i]
            if p['a'] == 'w' and p['x'] == o['x']:
                if p['t'] != o['t'] and p['t'] not in ended(ops, j):
                    strict = False
                break
    return rf, recoverable, cascadeless, strict


def rollback(ops):
    """Transactions that must roll back because of the aborts in the schedule."""
    rf = reads_from(ops)
    out = []
    for k, o in enumerate(ops):
        if o['a'] != 'a':
            continue
        bad = {o['t']}
        changed = True
        while changed:
            changed = False
            for j, i in rf.items():
                if i is not None and ops[i]['t'] in bad and ops[j]['t'] not in bad and j < k:
                    bad.add(ops[j]['t'])
                    changed = True
        out += [t for t in sorted(bad - {o['t']}, key=lambda t: int(t[1:])) if t not in out]
    return out


def arrow(u, v):
    return f'{u} → {v}'


def analyse(qid, tab, others):
    ops = parse(qid, tab['ops'])
    ts, expect = txns(ops), tab['expect']
    want_graph = any(k in expect for k in ('conflict_serializable', 'view_serializable', 'orders', 'two_phase_locking'))
    want_rec = any(k in expect for k in ('recoverable', 'cascadeless', 'strict', 'rollback'))
    if 'equivalent' in expect:
        return equivalence(qid, tab, ops, others)
    rf = reads_from(ops)
    steps, es = [], {}
    rules = []
    if want_graph:
        rules.append('Two operations conflict when different transactions use the same item and at least one of them writes; the earlier one\'s transaction gets an edge to the later one\'s.')
    if want_rec:
        rules.append('Track which write each read sees, and when each transaction commits or aborts.')
    steps.append(dict(i=-1, edges=[], note=' '.join(rules)))
    for j, o in enumerate(ops):
        note, cmp, new = o['label'] + ':', [], []
        if o['a'] in 'rw' and want_graph:
            hits = [i for i, jj in conflicts(ops) if jj == j]
            cmp = hits
            if hits:
                by = {}
                for i in hits:
                    labels = by.setdefault(ops[i]['t'], [])
                    if ops[i]['label'] not in labels:
                        labels.append(ops[i]['label'])
                parts = []
                for t, labels in by.items():
                    e = (t, o['t'])
                    parts.append(f"{_list(labels)} of {t}, so {arrow(*e)}" + (' (already there)' if e in es else ''))
                    if e not in es:
                        es[e] = True
                        new.append(list(e))
                note += ' conflicts with the earlier ' + '; and '.join(parts) + '.'
            else:
                note += ' no conflict with an earlier operation of another transaction.'
        src = None
        if o['a'] == 'r' and want_rec:
            src = rf[j]
            if src is None:
                own = any(p['a'] == 'w' and p['x'] == o['x'] and p['t'] == o['t'] for p in ops[:j])
                note += f" {o['t']} reads its own write of {o['x']}." if own else f" {o['t']} reads the initial value of {o['x']}."
            else:
                w = ops[src]['t']
                state = ended(ops, j).get(w)
                note += f" {o['t']} reads {o['x']} written by {w}, " + ('which has already committed.' if state == 'c' else f'which has not committed yet: a dirty read.')
        elif o['a'] == 'w' and want_rec:
            prev = next((ops[i] for i in range(j - 1, -1, -1) if ops[i]['a'] == 'w' and ops[i]['x'] == o['x'] and ops[i]['t'] != o['t']), None)
            if prev and prev['t'] not in ended(ops, j):
                note += f" {o['t']} overwrites {o['x']} written by {prev['t']}, which has not finished yet."
            elif not want_graph:
                note += f" {o['t']} writes {o['x']}."
        elif o['a'] == 'c':
            readers = [(jj, i) for jj, i in rf.items() if i is not None and jj < j and ops[jj]['t'] == o['t']]
            note = f"{o['label']}: {o['t']} commits."
            if want_rec:
                bad = sorted({ops[i]['t'] for jj, i in readers if ended(ops, j).get(ops[i]['t']) != 'c'})
                good = sorted({ops[i]['t'] for jj, i in readers} - set(bad))
                if bad:
                    note += f" It read from {_list(bad)}, which " + ('has' if len(bad) == 1 else 'have') + ' not committed: this breaks recoverability.'
                elif good:
                    note += f" Everything it read came from {_list(good)}, already committed."
        elif o['a'] == 'a':
            note = f"{o['label']}: {o['t']} aborts and its writes are undone."
            if want_rec:
                hit = sorted({ops[jj]['t'] for jj, i in rf.items() if i is not None and ops[i]['t'] == o['t'] and jj < j})
                done = ended(ops, j)
                late = [t for t in hit if done.get(t) == 'c']
                live = [t for t in hit if t not in done]
                if live:
                    note += f" {_list(live)} read data it wrote, so " + ('it' if len(live) == 1 else 'they') + ' must roll back too.'
                if late:
                    note += f" {_list(late)} read data it wrote but " + ('has' if len(late) == 1 else 'have') + ' already committed, so ' + ('it' if len(late) == 1 else 'they') + ' cannot be rolled back.'
                if not hit:
                    note += ' No other transaction read anything it wrote.'
        steps.append(dict(i=j, cmp=cmp, src=src, edges=[list(e) for e in es], new=new, note=note))
    got, final = {}, ['All done.']
    tag = None
    if want_graph:
        cyc = cycle(ts, list(es))
        got['conflict_serializable'] = cyc is None
        if cyc:
            tag = dict(cycle=cyc)
            final.append(f"The precedence graph has the cycle {' → '.join(cyc)}, so the schedule is not conflict serializable.")
        else:
            orders = topo_orders(ts, list(es))
            tag = dict(order=orders[0])
            final.append('The precedence graph has no cycle, so the schedule is conflict serializable. ' +
                         ('Its only equivalent serial order is ' + ', '.join(orders[0]) + '.' if len(orders) == 1 else
                          'Equivalent serial orders: ' + '; '.join(', '.join(o) for o in orders) + '.'))
        if 'two_phase_locking' in expect:
            if cyc is None:
                raise SystemExit(f'{qid}: whether two-phase locking allows a conflict-serializable schedule is not modelled')
            got['two_phase_locking'] = False
            final.append('Two-phase locking only lets through conflict-serializable schedules, so it could not have produced this one.')
        if 'view_serializable' in expect:
            if any(o['a'] == 'a' for o in ops):
                raise SystemExit(f'{qid}: view serializability with aborts is not modelled')
            mine = _view_of(ops)
            views = [list(p) for p in permutations(ts) if _view(ops, p) == mine]
            got['view_serializable'] = bool(views)
            final.append(('It is view serializable, like ' + ', '.join(views[0]) + '.') if views else
                         'It is not view serializable either: no serial order has the same reads and final writes.')
        if 'orders' in expect:
            cands = [[t if str(t).startswith('T') else 'T' + str(t) for t in c] for c in tab['candidates']]
            good = [c for c in cands if cyc is None and all(c.index(u) < c.index(v) for u, v in es)]
            got['orders'] = good
            for c in cands:
                if c in good:
                    continue
                if cyc:
                    break
                u, v = next((u, v) for u, v in es if c.index(u) > c.index(v))
                final.append(f"{', '.join(c)} puts {v} before {u}, against the edge {arrow(u, v)}.")
            if good:
                final.append('Listed orders that respect every edge: ' + '; '.join(', '.join(c) for c in good) + '.')
    if want_rec:
        _, rec, aca, strict = recovery(ops)
        got.update(recoverable=rec, cascadeless=aca, strict=strict)
        if 'recoverable' in expect:
            final.append('It is recoverable: every transaction commits only after those it read from.' if rec else
                         'It is not recoverable: a transaction committed after reading from one that had not committed.')
        if 'cascadeless' in expect:
            final.append('No read sees uncommitted data, so no abort can cascade.' if aca else 'Some read sees uncommitted data, so an abort can cascade.')
        if 'strict' in expect:
            final.append('It is strict: nothing reads or overwrites an item while its last writer is still running.' if strict else
                         'It is not strict: an item is read or overwritten while the transaction that wrote it is still running.')
        if 'rollback' in expect:
            rb = rollback(ops)
            got['rollback'] = rb
            final.append(('Transactions that must roll back as well: ' + _list(rb) + '.') if rb else 'No other transaction has to roll back.')
    for k, v in expect.items():
        if k not in got:
            raise SystemExit(f'{qid}: unknown schedule expectation {k}')
        if k == 'orders':
            v = [[t if str(t).startswith('T') else 'T' + str(t) for t in c] for c in v]
        if got[k] != v:
            raise SystemExit(f'Animation for {qid} ({tab.get("name")}) gives {k} = {got[k]}, not the expected {v}')
    steps.append(dict(i=len(ops), edges=[list(e) for e in es], final=True, note=' '.join(final), **(tag or {})))
    return ops, ts, steps, want_graph


def equivalence(qid, tab, ops, others):
    ref = others.get(tab['compare_to'])
    if ref is None:
        raise SystemExit(f'{qid}: compare_to names no earlier tab')
    base = parse(qid, ref['ops'])
    if sorted(o['label'] for o in base) != sorted(o['label'] for o in ops):
        raise SystemExit(f'{qid}: {tab["name"]} does not have the same operations')
    pos = {o['label']: k for k, o in enumerate(ops)}
    if len(pos) != len(ops):
        raise SystemExit(f'{qid}: repeated operations are not modelled in an equivalence check')
    steps = [dict(i=-1, note=f"Two schedules are conflict equivalent when each transaction keeps its own order and every conflicting pair of {ref['name']} stays in the same order.")]
    same = True
    for t in txns(base):
        if [o['label'] for o in base if o['t'] == t] != [o['label'] for o in ops if o['t'] == t]:
            same = False
            steps.append(dict(i=-1, note=f"{t}'s operations are in a different order, so the schedules cannot be equivalent."))
    for i, j in conflicts(base):
        a, b = base[i]['label'], base[j]['label']
        kept = pos[a] < pos[b]
        same = same and kept
        steps.append(dict(i=-1, cmp=[pos[a], pos[b]], bad=not kept, note=f"{ref['name']} has {a} before {b}. Here {a} is operation {pos[a] + 1} and {b} is operation {pos[b] + 1}: " + ('the same order.' if kept else 'the order is reversed.')))
    if same != tab['expect']['equivalent']:
        raise SystemExit(f'Animation for {qid} ({tab["name"]}) gives equivalent = {same}, not the expected {tab["expect"]["equivalent"]}')
    steps.append(dict(i=-1, final=True, note='All done. ' + (f"Every conflicting pair keeps its order, so this schedule is conflict equivalent to {ref['name']}." if same else
                                                         f"At least one conflicting pair is reversed, so this schedule is not conflict equivalent to {ref['name']}.")))
    return ops, txns(ops), steps, False


def schedule_animation(qid, spec):
    tabs, seen = [], {}
    for tab in spec['schedules']:
        ops, ts, steps, graph = analyse(qid, tab, seen)
        seen[tab['name']] = tab
        tabs.append(dict(short=tab['name'], title=tab.get('title', tab['name'] + ': ' + ', '.join(tab['ops'])), steps=steps, graph=graph,
                         ops=[[o['t'], o['label']] for o in ops], txns=ts))
    return dict(kind='txn-schedule', schedules=tabs, count=sum(len(t['steps']) for t in tabs))


KINDS = {'txn-schedule': schedule_animation}
PLAYER = 'schedule'
TABS = 'schedules'
