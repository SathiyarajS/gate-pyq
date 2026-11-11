"""Banker's algorithm and deadlock detection with given matrices.

Data: data/animations/banker.json. A spec states the resources, the processes,
the Allocation matrix, either Max (Need = Max − Allocation) or the outstanding
requests (`need`, for detection), and either Available or the total of each
resource. Each entry of `checks` is one tab:
  - a safety test of the state as given: expect {safe, sequence?, last?};
  - a resource request {process, vector}: expect {granted};
  - an abort of some processes before detection {abort: [...]}: expect {deadlock_free}.
Everything is computed here, and the build stops on any difference.

The safety (or detection) test repeatedly lets the first unfinished process, in
the listed order, whose Need fits in Work finish and return its Allocation.
Work only grows, so the order of choice cannot change whether every process
finishes. `sequence` is checked against that first-fit order; `last` is checked
against every possible completion order.
"""
from .common import _list


def vec(v):
    return '(' + ', '.join(str(x) for x in v) + ')' if len(v) > 1 else str(v[0])


def _le(a, b):
    return all(x <= y for x, y in zip(a, b))


def _matrix(qid, rows, procs, res, what):
    if len(rows) != len(procs) or any(len(r) != len(res) for r in rows):
        raise SystemExit(f'{qid}: {what} is not {len(procs)} × {len(res)}')
    if any(not isinstance(x, int) or x < 0 for r in rows for x in r):
        raise SystemExit(f'{qid}: {what} has a negative or non-integer entry')
    return [list(r) for r in rows]


class State:
    def __init__(self, qid, spec):
        self.qid, self.res, self.procs = qid, spec['resources'], spec['processes']
        self.alloc = _matrix(qid, spec['allocation'], self.procs, self.res, 'Allocation')
        if 'max' in spec:
            self.max = _matrix(qid, spec['max'], self.procs, self.res, 'Max')
            self.need = [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(self.max, self.alloc)]
            if any(x < 0 for r in self.need for x in r):
                raise SystemExit(f'{qid}: an allocation exceeds its maximum claim')
            self.label = 'Need'
        else:
            self.max = None
            self.need = _matrix(qid, spec['need'], self.procs, self.res, spec.get('need_label', 'Request'))
            self.label = spec.get('need_label', 'Request')
        held = [sum(r[k] for r in self.alloc) for k in range(len(self.res))]
        if 'available' in spec:
            self.avail = list(spec['available'])
            self.total = [a + b for a, b in zip(held, self.avail)]
        else:
            self.total = list(spec['total'])
            self.avail = [t - x for t, x in zip(self.total, held)]
            if any(x < 0 for x in self.avail):
                raise SystemExit(f'{qid}: more is allocated than exists')
        if len(self.avail) != len(self.res):
            raise SystemExit(f'{qid}: Available does not list every resource')
        # One instance of every resource: notes name the resources instead of giving counts.
        self.single = len(self.res) > 1 and all(t == 1 for t in self.total)

    def names(self, v):
        return _list([r for r, x in zip(self.res, v) if x]) or 'nothing'


def rows(st, alloc, need, done=(), now=None, waits=(), gone=(), asks=None):
    """One row per process: [name, allocation, max (or None), need, status]."""
    out = []
    for i, p in enumerate(st.procs):
        status = 'aborted' if p in gone else 'done' if p in done else 'finishes' if p == now else 'waits' if p in waits else 'asks' if p == asks else ''
        out.append([p, alloc[i][:], st.max[i][:] if st.max else None, need[i][:], status])
    return out


def safety(st, alloc, need, avail, alive, steps, head):
    """First-fit safety test. Appends one step per finishing process (and one if stuck)."""
    work, done, order = list(avail), [], []
    while len(done) < len(alive):
        waits, pick = [], None
        for i, p in enumerate(st.procs):
            if p not in alive or p in done:
                continue
            if _le(need[i], work):
                pick = i
                break
            waits.append(p)
        tried = []
        for p in waits:
            i = st.procs.index(p)
            short = [st.res[k] for k in range(len(st.res)) if need[i][k] > work[k]]
            if st.single:
                tried.append(f"{p} waits for {st.names(need[i])}, but {_list(short)} " + ('is' if len(short) == 1 else 'are') + ' still held')
            else:
                tried.append(f"{p} needs {vec(need[i])}: not enough {_list(short)}")
        if pick is None:
            left = [p for p in alive if p not in done]
            note = f"Work = {vec(work)}. " + ('; '.join(tried) + '. ' if tried else '') + f"No remaining process can finish: {_list(left)} " + ('is' if len(left) == 1 else 'are') + ' stuck.'
            steps.append(dict(head=head, work=work[:], rows=rows(st, alloc, need, done, None, waits, [p for p in st.procs if p not in alive]), note=note))
            return False, order, work
        p = st.procs[pick]
        new = [w + a for w, a in zip(work, alloc[pick])]
        note = f"Work = {vec(work)}. " + ('; '.join(tried) + '. ' if tried else '')
        if st.single:
            note += f"{p} waits for {st.names(need[pick])}, which " + ('is' if sum(need[pick]) == 1 else 'are') + f" free, so {p} can finish and release {st.names(alloc[pick])}: Work = {vec(new)}."
        else:
            note += f"{p} needs {vec(need[pick])}, which fits, so {p} can finish and return its allocation {vec(alloc[pick])}: Work = {vec(work)} + {vec(alloc[pick])} = {vec(new)}."
        steps.append(dict(head=head, work=work[:], next=new, rows=rows(st, alloc, need, done, p, waits, [q for q in st.procs if q not in alive]), now=p, note=note))
        work = new
        done.append(p)
        order.append(p)
    return True, order, work


def all_orders(st, alloc, need, work, alive):
    """Every order in which all processes can finish (small inputs only)."""
    out = []

    def go(work, done):
        if len(done) == len(alive):
            out.append(list(done))
            return
        for i, p in enumerate(st.procs):
            if p in alive and p not in done and _le(need[i], work):
                go([w + a for w, a in zip(work, alloc[i])], done + [p])
    go(list(work), [])
    return out


def banker_animation(qid, spec):
    st = State(qid, spec)
    detect = st.max is None
    tabs = []
    for chk in spec['checks']:
        alloc, need, avail = [r[:] for r in st.alloc], [r[:] for r in st.need], st.avail[:]
        alive = list(st.procs)
        steps, expect = [], chk['expect']
        if detect:
            intro = (f"Every resource has one instance and all are held, so Available = {vec(avail)}." if st.single and not any(avail) else
                     f"Available = {vec(avail)} (total {vec(st.total)} minus everything allocated).")
            intro += f" The {st.label} column shows what each process is still waiting for. A process can finish once that fits in Work, and then it releases what it holds."
        else:
            intro = f"Need = Max − Allocation. Available = {vec(avail)}" + ('' if 'available' in spec else f" (total {vec(st.total)} minus everything allocated)") + '. Start the safety test with Work = Available.'
        if 'request' in chk:
            p, r = chk['request']['process'], chk['request']['vector']
            i = st.procs.index(p)
            steps.append(dict(head='Start', work=avail[:], rows=rows(st, alloc, need), note=intro.replace(' Start the safety test with Work = Available.', '')))
            if not _le(r, need[i]):
                raise SystemExit(f'{qid}: the request exceeds {p}\'s need; that is an error, not a wait')
            if not _le(r, avail):
                raise SystemExit(f'{qid}: the request exceeds Available; it simply waits (not modelled)')
            avail = [a - x for a, x in zip(avail, r)]
            alloc[i] = [a + x for a, x in zip(alloc[i], r)]
            need[i] = [a - x for a, x in zip(need[i], r)]
            steps.append(dict(head=f'{p} asks for {vec(r)}', work=avail[:], rows=rows(st, alloc, need, asks=p), now=p,
                              note=f"{p} asks for {vec(r)}. It is within {p}'s need and within Available, so pretend to grant it: Available = {vec(avail)}, {p}'s allocation = {vec(alloc[i])}, its need = {vec(need[i])}. Now test whether this state is safe."))
        elif 'abort' in chk:
            gone = chk['abort']
            for p in gone:
                i = st.procs.index(p)
                avail = [a + x for a, x in zip(avail, alloc[i])]
            alive = [p for p in st.procs if p not in gone]
            steps.append(dict(head='Abort ' + _list(gone), work=avail[:], rows=rows(st, alloc, need, gone=gone),
                              note=f"Abort {_list(gone)}: " + _list([f"{p} releases " + (st.names(alloc[st.procs.index(p)]) if st.single else vec(alloc[st.procs.index(p)])) for p in gone]) + f", so Available = {vec(avail)}. Then run the detection test on the processes left."))
        else:
            steps.append(dict(head='Start', work=avail[:], rows=rows(st, alloc, need), note=intro))
        ok, order, work = safety(st, alloc, need, avail, alive, steps, 'Safety test' if not detect else 'Detection')
        word = ('safe' if ok else 'unsafe') if not detect else ('deadlock-free' if ok else 'deadlocked')
        if ok:
            note = f"All done. Every process can finish, in the order {', '.join(order)}, so the state is {word}."
        else:
            note = f"All done. Not every process can finish, so the state is {word}."
        got = dict(safe=ok, deadlock_free=ok)
        if 'request' in chk:
            got['granted'] = ok
            note += f" The request is granted." if ok else f" The request is not granted: {chk['request']['process']} must wait, and the pretend grant is undone."
        if 'last' in expect:
            orders = all_orders(st, alloc, need, avail, alive)
            lasts = sorted({o[-1] for o in orders})
            if not orders or lasts != [expect['last']]:
                raise SystemExit(f'Animation for {qid}: the last process can be {lasts}, not only {expect["last"]}')
            got['last'] = expect['last']
            note += f" The order is forced: {', '.join(orders[0])} is the only one." if len(orders) == 1 else f" In every possible order {expect['last']} finishes last."
        if 'sequence' in expect:
            got['sequence'] = order
        if 'deadlocked' in expect:
            if not ok and not detect:
                raise SystemExit(f'{qid}: an unsafe state need not be deadlocked; this test cannot tell')
            got['deadlocked'] = not ok
            if ok and not detect:
                note += ' A safe state is not deadlocked: the processes can all finish in that order.'
        for k, v in expect.items():
            if k not in got:
                raise SystemExit(f'{qid}: unknown banker expectation {k}')
            if got[k] != v:
                raise SystemExit(f'Animation for {qid} gives {k} = {got[k]}, not the expected {v}')
        steps.append(dict(head='Finished', work=work, rows=rows(st, alloc, need, order, gone=[p for p in st.procs if p not in alive]), final=True, note=note))
        tabs.append(dict(short=chk.get('short', 'Safety'), title=chk.get('title', "Banker's safety test" if not detect else 'Deadlock detection'), steps=steps,
                         cols=['Process', 'Allocation'] + ([] if detect else ['Max']) + [st.label, '']))
    return dict(kind='banker', resources=st.res, label=st.label, schedules=tabs, count=sum(len(t['steps']) for t in tabs))


KINDS = {'banker': banker_animation}
PLAYER = 'banker'
TABS = 'checks'
