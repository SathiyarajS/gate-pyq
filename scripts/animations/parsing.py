"""Compiler parsing: FIRST and FOLLOW sets, LL(1) tables, LR item sets and
conflicts (LR(0), SLR(1), canonical LR(1), LALR(1)), shift-reduce and
predictive traces with translation actions, and derivations / parse trees.

Data: data/animations/parsing.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.

A grammar is a list of lines "A -> x B y | ε" with symbols separated by spaces
(the left sides are the nonterminals, the first one is the start symbol unless
`start` says otherwise). A line may instead be {"p": "A -> x B", "print": "2"}
or {"p": ..., "val": "$1 * $3"} for a translation action run when the
production is reduced ($k is the k-th symbol of the right side). A right side
may also hold embedded actions such as {print('+')} or {print(num.val)}, run
by a top-down parse when they reach the top of the stack.

`do` lists the work, one tab each: "sets" (FIRST and FOLLOW), "ll1" (the LL(1)
table), "lr0", "slr", "lr1", "lalr" (an item-set collection and its conflicts),
{"goto": [symbols]} (one GOTO chain from I0, or from `items`),
{"items": [...]} (which listed items share a state), {"sr": input} (a
shift-reduce trace), {"ll": input} (a predictive trace) and {"trees": input}
(every parse tree, or one derivation for `generated`). Input tokens are
separated by spaces; "id:20" is the token id with the lexeme 20. `parts` give
several grammars, each with its own `do` and `expect`.
"""
import re
from fractions import Fraction

from .common import _list

EPS = 'ε'
END = '$'
DOT = '·'


# ------------------------------------------------------------------ grammar

def _syms(text):
    text = text.strip()
    if text in ('', EPS):
        return []
    out = text.split()
    if EPS in out:
        raise SystemExit(f'ε inside a longer right side: {text!r}')
    return out


def _is_action(sym):
    return len(sym) > 2 and sym[0] == '{' and sym[-1] == '}'


class Grammar:
    def __init__(self, lines, start=None, augment=False, terminals=None):
        self.prods, self.marks, self.acts = [], [], []
        for line in lines:
            act = {}
            if isinstance(line, dict):
                act = {k: v for k, v in line.items() if k != 'p'}
                line = line['p']
            if not re.search(r'->|→', line):
                raise SystemExit(f'Bad production: {line!r}')
            lhs, rhs = re.split(r'\s*(?:->|→)\s*', line.strip(), maxsplit=1)
            alts = re.split(r'\s\|\s', ' ' + rhs + ' ')
            if act and len(alts) != 1:
                raise SystemExit(f'An action belongs to one production: {line!r}')
            for alt in alts:
                syms = _syms(alt)
                marks, body = [], []
                for s in syms:
                    if _is_action(s):
                        marks.append((len(body), s))
                    else:
                        body.append(s)
                self.prods.append((lhs.strip(), tuple(body)))
                self.marks.append(marks)
                self.acts.append(act)
        if len(set(self.prods)) != len(self.prods):
            raise SystemExit('A production is listed twice')
        self.nts = list(dict.fromkeys(a for a, _ in self.prods))
        self.start = start or self.nts[0]
        if self.start not in self.nts:
            raise SystemExit(f'Start symbol {self.start} has no production')
        if augment:
            new = self.start + '′'
            if new in self.nts:
                raise SystemExit(f'{new} is already a nonterminal')
            self.prods.insert(0, (new, (self.start,)))
            self.marks.insert(0, [])
            self.acts.insert(0, {})
            self.nts.insert(0, new)
            self.start = new
        self.ntset = set(self.nts)
        self.terms = list(dict.fromkeys(s for _, r in self.prods for s in r if s not in self.ntset))
        if terminals:
            if sorted(terminals) != sorted(self.terms):
                raise SystemExit(f'The terminals {terminals} are not those of the grammar: {self.terms}')
            self.terms = list(terminals)
        elif all(len(t) == 1 and t.isalpha() and t.islower() for t in self.terms):
            self.terms.sort()
        if END in self.terms:
            raise SystemExit('$ is the end marker, not a grammar symbol')
        allsyms = self.nts + self.terms
        self.spaced = any(len(s.rstrip('′')) > 1 for s in allsyms)
        self.sep = ' ' if self.spaced else ''
        self.by = {a: [i for i, (l, _) in enumerate(self.prods) if l == a] for a in self.nts}
        self.order = {t: k for k, t in enumerate(self.terms + [END, EPS])}
        self.minlen = self._minlen()
        self._first = None

    def _minlen(self):
        INF = 10 ** 9
        m = {a: INF for a in self.nts}
        changed = True
        while changed:
            changed = False
            for a, r in self.prods:
                v = sum(1 if s not in self.ntset else m[s] for s in r)
                if v < m[a]:
                    m[a], changed = v, True
        for a in self.nts:
            if m[a] >= INF:
                raise SystemExit(f'{a} derives no terminal string')
        return m

    def seqmin(self, seq):
        return sum(1 if s not in self.ntset else self.minlen[s] for s in seq)

    # text
    def rt(self, rhs):
        return self.sep.join(rhs) if rhs else EPS

    def pt(self, i, arrow=' → '):
        a, r = self.prods[i]
        return f'{a}{arrow}{self.rt(r)}'

    def full(self, i, arrow=' → '):
        """A production with its embedded actions, as written."""
        a, r = self.prods[i]
        out = list(r)
        for pos, m in reversed(self.marks[i]):
            out.insert(pos, m)
        return f'{a}{arrow}{" ".join(out) if self.marks[i] else self.rt(r)}' if out else f'{a}{arrow}{EPS}'

    def find(self, text):
        """The production index for 'A -> x y'."""
        lhs, rhs = re.split(r'\s*(?:->|→)\s*', text.strip(), maxsplit=1)
        key = (lhs, tuple(_syms(rhs)))
        if key not in self.prods:
            raise SystemExit(f'No production {text!r}')
        return self.prods.index(key)

    def ordered(self, s):
        return sorted(s, key=lambda t: self.order.get(t, -1))

    def fmt(self, s):
        return '{' + ', '.join(self.ordered(s)) + '}'

    def first(self):
        if self._first is None:
            self._first = first_sets(self, None)
        return self._first

    def first_seq(self, seq, first=None):
        first = first or self.first()
        out = set()
        for x in seq:
            if x in self.ntset:
                out |= first[x] - {EPS}
                if EPS not in first[x]:
                    return out, False
            else:
                out.add(x)
                return out, False
        return out, True


def _num(text):
    x = Fraction(text)
    return x


def _show(x):
    """A value as a student writes it: 6, −2, 2.375 or 1/3."""
    x = Fraction(x)
    neg = x < 0
    x = abs(x)
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if x.denominator == 1:
        s = str(x.numerator)
    elif d == 1:
        k = 0
        while (x * 10 ** k).denominator != 1:
            k += 1
        s = f'{x.numerator * 10 ** k // x.denominator}'.rjust(k + 1, '0')
        s = s[:-k] + '.' + s[-k:]
    else:
        s = f'{x.numerator}/{x.denominator}'
    return ('−' if neg else '') + s


# ------------------------------------------------------------ FIRST / FOLLOW

def _sets_rows(g, first, follow):
    return [[a, g.ordered(first[a]), g.ordered(follow[a]) if follow is not None else []] for a in g.nts]


def first_sets(g, steps):
    """FIRST by passes over the productions; one step per production that adds something."""
    first = {a: set() for a in g.nts}
    head = 'FIRST sets'

    def snap(note, rule=None, new=()):
        if steps is not None:
            steps.append(dict(head=head, note=note, rule=rule, sets=_sets_rows(g, first, None),
                              new=dict(first={k: g.ordered(v) for k, v in new}, follow={}), view='sets'))

    snap('FIRST(X) is the set of terminals that can begin a string derived from X, plus ε if X can derive ε. '
         'Go through the productions again and again until a whole pass adds nothing.')
    pas, changed = 0, True
    while changed:
        pas += 1
        changed = False
        for i, (a, r) in enumerate(g.prods):
            add, scanned = set(), []
            nullable = True
            for x in r:
                scanned.append(x)
                if x in g.ntset:
                    add |= first[x] - {EPS}
                    if EPS not in first[x]:
                        nullable = False
                        break
                else:
                    add.add(x)
                    nullable = False
                    break
            if nullable:
                add.add(EPS)
            new = add - first[a]
            if not new:
                continue
            first[a] |= new
            changed = True
            p = g.pt(i)
            if not r:
                note = f'{p}: {a} can derive ε, so ε goes into FIRST({a}).'
            elif r[0] not in g.ntset:
                note = f'{p} starts with the terminal {r[0]}, so add {r[0]} to FIRST({a}).'
            else:
                gain = g.ordered(new - {EPS})
                if len(scanned) == 1:
                    note = f'{p} starts with {r[0]}, so whatever begins {r[0]} also begins {a}' + (f': add {_list(gain)}.' if gain else '.')
                else:
                    begins = lambda x: f'whatever begins {x}' if x in g.ntset else x
                    note = (f'{p} can begin with {begins(scanned[0])}, and since {_list(scanned[:-1])} can derive ε, '
                            f'also with {_list([begins(x) for x in scanned[1:]])}.')
                    if gain:
                        note += f' This adds {_list(gain)} to FIRST({a}).'
                if EPS in new:
                    note += (f' Every symbol of the right side can derive ε, so ε is in FIRST({a}) too.' if len(r) > 1
                             else f' {r[0]} can derive ε, so ε is in FIRST({a}) too.')
            snap(f'Pass {pas}. ' + note, i, [(a, new)])
    snap(f'Pass {pas} adds nothing new, so the FIRST sets are final.')
    return first


def follow_sets(g, first, steps):
    follow = {a: set() for a in g.nts}
    head = 'FOLLOW sets'

    def snap(note, rule=None, new=()):
        if steps is not None:
            steps.append(dict(head=head, note=note, rule=rule, sets=_sets_rows(g, first, follow),
                              new=dict(first={}, follow={k: g.ordered(v) for k, v in new}), view='sets'))

    follow[g.start] = {END}
    snap(f'FOLLOW(X) is the set of terminals that can come right after X in some sentential form. '
         f'{g.start} is the start symbol, so the end marker $ follows it: FOLLOW({g.start}) = {{$}}.', None, [(g.start, {END})])
    pas, changed = 0, True
    while changed:
        pas += 1
        changed = False
        for i, (a, r) in enumerate(g.prods):
            for k, b in enumerate(r):
                if b not in g.ntset:
                    continue
                beta = r[k + 1:]
                f, nullable = g.first_seq(beta, first)
                add = f | (follow[a] if nullable else set())
                new = add - follow[b]
                if not new:
                    continue
                follow[b] |= new
                changed = True
                p = g.pt(i)
                if not beta:
                    note = f'{b} is at the end of {p}, so whatever follows {a} also follows {b}: add {_list(g.ordered(new))}.'
                elif len(beta) == 1 and beta[0] not in g.ntset:
                    note = f'In {p}, {b} is followed by {beta[0]}: add {beta[0]} to FOLLOW({b}).'
                elif not nullable:
                    note = f'In {p}, {b} is followed by {g.rt(beta)}, which begins with {_list(g.ordered(f))}: add {_list(g.ordered(new))}.'
                elif a == b:
                    note = f'In {p}, {b} is followed by {g.rt(beta)}, which begins with {_list(g.ordered(f))}: add {_list(g.ordered(new))}.'
                else:
                    lead = f'which begins with {_list(g.ordered(f))} and can also derive ε' if f else 'which can only derive ε'
                    note = (f'In {p}, {b} is followed by {g.rt(beta)}, {lead}, so whatever follows {a} also follows {b}. '
                            f'Add {_list(g.ordered(new))}.')
                snap(f'Pass {pas}. ' + note, i, [(b, new)])
    snap(f'Pass {pas} adds nothing new, so the FOLLOW sets are final.')
    return follow


def do_sets(g, steps, out):
    first = first_sets(g, steps)
    follow = follow_sets(g, first, steps)
    out['first'], out['follow'] = first, follow
    return first, follow


# ------------------------------------------------------------------ LL(1)

def do_ll1(g, steps, out, first=None, follow=None):
    first = first or first_sets(g, None)
    follow = follow or follow_sets(g, first, None)
    cols = g.terms + [END]
    table = {}
    head = 'LL(1) table'

    def grid(new=()):
        return dict(rows=list(g.nts), cols=cols,
                    cells=[[[g.pt(i, '→') for i in table.get((a, t), [])] for t in cols] for a in g.nts],
                    new=[[g.nts.index(a), cols.index(t)] for a, t in new])

    steps.append(dict(head=head, note='Fill the table one production A → α at a time: put it under every terminal in FIRST(α); '
                                      'if α can derive ε, also put it under every symbol in FOLLOW(A).',
                      rule=None, grid=grid(), view='ll1', sets=_sets_rows(g, first, follow)))
    for i, (a, r) in enumerate(g.prods):
        f, nullable = g.first_seq(r, first)
        where = g.ordered(f) + [t for t in g.ordered(follow[a]) if nullable and t not in f]
        p = g.pt(i)
        clash = []
        for t in where:
            if table.get((a, t)):
                clash.append(t)
            table.setdefault((a, t), []).append(i)
        cells = lambda ts: (f'M[{a}, {ts[0]}]' if len(ts) == 1 else f'row {a} under {_list(ts)}')
        if not r:
            note = f'{p}: put it under FOLLOW({a}) = {g.fmt(follow[a])}, in {cells(g.ordered(follow[a]))}.' if follow[a] else f'{p}: FOLLOW({a}) is empty, so it goes nowhere.'
        elif not nullable:
            note = f'FIRST({g.rt(r)}) = {g.fmt(f)}, so {p} goes in {cells(g.ordered(f))}.'
        else:
            fs = g.fmt(f | {EPS})
            rest = [t for t in g.ordered(follow[a]) if t not in f]
            note = (f'FIRST({g.rt(r)}) = {fs}. It can derive ε, so besides ' + (f'{_list(g.ordered(f))} ' if f else '')
                    + f'{p} also goes under FOLLOW({a}) = {g.fmt(follow[a])}'
                    + (f': {cells(g.ordered(set(where)))}.' if where else '.'))
            del rest
        if clash:
            note += ' ' + ' '.join(f'M[{a}, {t}] now holds two productions: a conflict.' for t in clash)
        steps.append(dict(head=head, note=note, rule=i, grid=grid([(a, t) for t in where]), view='ll1',
                          sets=_sets_rows(g, first, follow), bad=[[g.nts.index(a), cols.index(t)] for t in clash]))
    multi = [(a, t) for (a, t), v in table.items() if len(v) > 1]
    multi.sort(key=lambda x: (g.nts.index(x[0]), cols.index(x[1])))
    if multi:
        note = (f'{_list([f"M[{a}, {t}]" for a, t in multi])} {"holds" if len(multi) == 1 else "hold"} more than one production, '
                'so the grammar is not LL(1).')
    else:
        note = 'No cell holds more than one production, so the grammar is LL(1).'
    steps.append(dict(head=head, note=note, rule=None, grid=grid(), view='ll1', sets=_sets_rows(g, first, follow),
                      bad=[[g.nts.index(a), cols.index(t)] for a, t in multi]))
    out['table'] = {k: [g.prods[i][1] for i in v] for k, v in table.items()}
    out['ll1'] = not multi
    return table


# ---------------------------------------------------------------- LR items

def _closure0(g, kernel):
    items = list(dict.fromkeys(kernel))
    k = 0
    while k < len(items):
        p, d = items[k]
        r = g.prods[p][1]
        if d < len(r) and r[d] in g.ntset:
            for q in g.by[r[d]]:
                if (q, 0) not in items:
                    items.append((q, 0))
        k += 1
    return items


def _closure1(g, kernel):
    items = list(dict.fromkeys(kernel))
    k = 0
    while k < len(items):
        p, d, la = items[k]
        r = g.prods[p][1]
        if d < len(r) and r[d] in g.ntset:
            f, nullable = g.first_seq(r[d + 1:])
            looks = g.ordered(f | ({la} if nullable else set()))
            for q in g.by[r[d]]:
                for b in looks:
                    if (q, 0, b) not in items:
                        items.append((q, 0, b))
        k += 1
    return items


def _q(x):
    """A symbol inside running text; brackets and commas get quotes."""
    return f"'{x}'" if x in ('(', ')', ',') else x


def _core(items):
    return frozenset((it[0], it[1]) for it in items)


def _item_text(g, p, d):
    a, r = g.prods[p]
    syms = list(r[:d]) + [DOT] + list(r[d:])
    if g.spaced:
        body = ' '.join(syms)
    else:
        body = ''.join(syms)
    return f'{a} → {body}'


def _texts(g, items):
    """Item lines; LR(1) items with one core share a line: 'S → (·S), )/$'."""
    if items and len(items[0]) == 2:
        return [_item_text(g, p, d) for p, d in items]
    cores = {}
    for p, d, la in items:
        cores.setdefault((p, d), []).append(la)
    return [f'{_item_text(g, p, d)}, {"/".join(g.ordered(set(las)))}' for (p, d), las in cores.items()]


def _goto(g, items, x, lr1):
    kernel = []
    for it in items:
        p, d = it[0], it[1]
        r = g.prods[p][1]
        if d < len(r) and r[d] == x:
            kernel.append((p, d + 1) + tuple(it[2:]))
    if not kernel:
        return None, None
    return kernel, (_closure1 if lr1 else _closure0)(g, kernel)


def _symbols_after_dot(g, items):
    out = []
    for it in items:
        p, d = it[0], it[1]
        r = g.prods[p][1]
        if d < len(r) and r[d] not in out:
            out.append(r[d])
    return out


class State:
    def __init__(self, name, kernel, items):
        self.name, self.kernel, self.items, self.go = name, kernel, items, []


def _cards(g, states, show=(), src=None, cur=None):
    """Item-set cards: every line, with the first k the kernel; only the shown ones are drawn in full."""
    out = []
    for s in states:
        c = dict(name=s.name, items=_texts(g, s.items), k=len(_texts(g, s.kernel)), go=[[x, t] for x, t in s.go])
        flags = dict(full=s.name in show, cur=s.name == cur, src=s.name == src, bad=getattr(s, 'bad', None))
        c.update({k: v for k, v in flags.items() if v})
        out.append(c)
    return out


def _compact(sched):
    """Store what every step shares once per tab: trace rows, item-set cards and the sets beside an LL(1) table."""
    steps = sched['steps']
    if any('rows' in st for st in steps):
        rows = steps[-1]['rows']
        sched['cols'] = steps[-1]['cols']
        for st in steps:
            if st['rows'] != rows[:len(st['rows'])]:
                raise SystemExit('Trace rows changed after they were written')
            st['n'] = len(st.pop('rows'))
            st.pop('cols')
        sched['rows'] = rows
    if any('cards' in st for st in steps):
        bodies, index = [], {}
        for st in steps:
            refs = []
            for c in st.pop('cards', []):
                body = {k: c[k] for k in ('name', 'items', 'k', 'go')}
                key = repr(body)
                if key not in index:
                    index[key] = len(bodies)
                    bodies.append(body)
                refs.append(dict({'c': index[key]}, **{k: c[k] for k in ('full', 'cur', 'src', 'bad') if k in c}))
            st['cards'] = refs
        sched['cards'] = bodies
    if steps and all('sets' in st for st in steps) and steps[0].get('view') == 'll1':
        if any(st['sets'] != steps[0]['sets'] for st in steps):
            raise SystemExit('FIRST/FOLLOW changed while the table was filled')
        sched['sets'] = steps[0]['sets']
        for st in steps:
            del st['sets']


def _added(g, kernel, items, lr1):
    extra = items[len(kernel):]
    if not extra:
        return 'no nonterminal follows a dot, so closure adds nothing'
    heads = list(dict.fromkeys(g.prods[it[0]][0] for it in extra))
    n = len(_texts(g, items)) - len(_texts(g, kernel))
    return f'closure adds the productions of {_list(heads)} with the dot at the start ({n} more item{"s" if n != 1 else ""})'


def build_collection(g, lr1, steps, head):
    """The canonical collection, states numbered as they are found."""
    k0 = [(0, 0, END)] if lr1 else [(0, 0)]
    i0 = (_closure1 if lr1 else _closure0)(g, k0)
    states = [State('I0', k0, i0)]
    key = (lambda items: frozenset(items)) if lr1 else _core
    index = {key(i0): 0}
    kinds = 'LR(1)' if lr1 else 'LR(0)'
    steps.append(dict(head=head, view='lr', rule=0, note=(
        f'Build the {kinds} item sets. I0 is the closure of {_texts(g, k0)[0]}: whenever a nonterminal follows the dot, '
        f'add its productions with the dot at the start' + (', each with the terminals that can follow it as lookaheads' if lr1 else '')
        + f'. I0 has {len(_texts(g, i0))} items.'), cards=_cards(g, states, show={'I0'}, cur='I0')))
    k = 0
    while k < len(states):
        s = states[k]
        again = []
        for x in _symbols_after_dot(g, s.items):
            kernel, items = _goto(g, s.items, x, lr1)
            kk = key(items)
            if kk in index:
                t = states[index[kk]]
                s.go.append((x, t.name))
                again.append((x, t.name))
                continue
            t = State(f'I{len(states)}', kernel, items)
            index[kk] = len(states)
            states.append(t)
            s.go.append((x, t.name))
            moved = _list(_texts(g, kernel))
            note = (f'GOTO({s.name}, {_q(x)}): move the dot over {_q(x)}, giving {moved}; '
                    f'{_added(g, kernel, items, lr1)}. This is a new state, {t.name}.')
            steps.append(dict(head=head, view='lr', note=note, cards=_cards(g, states, show={s.name, t.name}, src=s.name, cur=t.name)))
        if again:
            bits = [f'{_q(x)} leads to {n}' for x, n in again]
            steps.append(dict(head=head, view='lr', note=f'From {s.name}, {_list(bits)}, {"a state" if len(again) == 1 else "states"} already found.',
                              cards=_cards(g, states, show={s.name}, cur=s.name)))
        k += 1
    steps[-1]['note'] += f' Every GOTO has been tried: {len(states)} states in all.'
    return states


def _actions(g, s, method, follow):
    """ACTION entries of one state: {terminal: [('s', None) | ('r', prod) | ('acc', None)]}."""
    acts = {}
    for it in s.items:
        p, d = it[0], it[1]
        r = g.prods[p][1]
        if d < len(r):
            if r[d] not in g.ntset:
                acts.setdefault(r[d], [])
                if ('s', None) not in acts[r[d]]:
                    acts[r[d]].append(('s', None))
            continue
        if p == 0:
            acts.setdefault(END, []).append(('acc', None))
            continue
        if method == 'lr0':
            looks = g.terms + [END]
        elif method == 'slr':
            looks = g.ordered(follow[g.prods[p][0]])
        else:
            looks = [it[2]]
        for t in looks:
            acts.setdefault(t, [])
            if ('r', p) not in acts[t]:
                acts[t].append(('r', p))
    return acts


def check_conflicts(g, states, method, steps, head, follow=None):
    """One step per state that has a completed item next to a shift or another completed item."""
    names = {'lr0': 'LR(0)', 'slr': 'SLR(1)', 'lr1': 'LR(1)', 'lalr': 'LALR(1)'}
    rule = {'lr0': 'In LR(0), a completed item reduces on every input symbol.',
            'slr': 'In SLR(1), a completed item A → α· reduces only on the symbols in FOLLOW(A).',
            'lr1': 'In LR(1), a completed item reduces only on its own lookahead.',
            'lalr': 'In LALR(1), a completed item reduces only on its (merged) lookaheads.'}[method]
    sr, rr, cells = 0, 0, []
    steps.append(dict(head=head, view='lr', note=f'Now look for conflicts. {rule} A state clashes if a symbol gets a shift and a reduce, or two reduces.',
                      cards=_cards(g, states)))
    for s in states:
        done = [it for it in s.items if it[1] == len(g.prods[it[0]][1]) and it[0] != 0]
        shifts = [x for x in _symbols_after_dot(g, s.items) if x not in g.ntset]
        if not done or (len(done) == 1 and not shifts and method != 'lr0') or (len(_core(done)) == 1 and not shifts):
            s.bad = None
            continue
        acts = _actions(g, s, method, follow)
        bad = {t: v for t, v in acts.items() if len(v) > 1}
        if any(x[0] == 'acc' for v in bad.values() for x in v):
            raise SystemExit(f'{s.name}: accept clashes with another action')
        red = list(dict.fromkeys(it[0] for it in done))
        why = []
        for p in red:
            if method == 'lr0':
                on = 'every symbol'
            elif method == 'slr':
                a = g.prods[p][0]
                on = f'FOLLOW({a}) = {g.fmt(follow[a])}'
            else:
                las = [it[2] for it in done if it[0] == p]
                on = '/'.join(g.ordered(set(las)))
            why.append(f'{_item_text(g, p, len(g.prods[p][1]))} reduces on {on}')
        txt = f'{s.name}: ' + '; '.join(why)
        if shifts:
            txt += f'; it shifts {_list([_q(x) for x in shifts])}'
        if bad:
            kinds = []
            for t in [t for t in g.terms + [END] if t in bad]:
                v = bad[t]
                nr = sum(1 for x in v if x[0] == 'r')
                if any(x[0] == 's' for x in v):
                    sr += 1
                    kinds.append(f'shift-reduce on {t}')
                if nr > 1:
                    rr += 1
                    kinds.append(f'reduce-reduce on {t}')
                cells.append((s.name, t))
            txt += '. Conflict: ' + _list(kinds) + '.'
            s.bad = [t for t in g.terms + [END] if t in bad]
        else:
            txt += '. These symbols do not overlap, so there is no conflict.'
            s.bad = None
        steps.append(dict(head=head, view='lr', note=txt, cards=_cards(g, states, show={s.name}, cur=s.name)))
    if sr + rr:
        parts = []
        if sr:
            parts.append(f'{sr} shift-reduce conflict{"s" if sr != 1 else ""}')
        if rr:
            parts.append(f'{rr} reduce-reduce conflict{"s" if rr != 1 else ""}')
        verdict = f'In all: {_list(parts)} in the ACTION table, so the grammar is not {names[method]}.'
    else:
        verdict = f'No ACTION entry gets two actions, so the grammar is {names[method]}.'
    steps.append(dict(head=head, view='lr', note=verdict, cards=_cards(g, states)))
    return dict(sr=sr, rr=rr, ok=not (sr + rr), cells=cells)


def merge_lalr(g, states, steps, head):
    groups = {}
    for s in states:
        groups.setdefault(_core(s.items), []).append(s)
    merged, name_of = [], {}
    for core, members in groups.items():
        name = 'I' + ''.join(m.name[1:] for m in members) if len(members) > 1 else members[0].name
        items, kernel = [], []
        for m in members:
            items += [it for it in m.items if it not in items]
            kernel += [it for it in m.kernel if it not in kernel]
        # keep the first member's item order, with every lookahead
        order = list(dict.fromkeys((it[0], it[1]) for it in members[0].items))
        items.sort(key=lambda it: order.index((it[0], it[1])))
        korder = list(dict.fromkeys((it[0], it[1]) for it in members[0].kernel))
        kernel.sort(key=lambda it: korder.index((it[0], it[1])))
        st = State(name, kernel, items)
        st.members = members
        merged.append(st)
        for m in members:
            name_of[m.name] = name
    for st in merged:
        go = []
        for x, t in st.members[0].go:
            go.append((x, name_of[t]))
        st.go = go
    steps.append(dict(head=head, view='lr', note=f'Start from the {len(states)} canonical LR(1) states. LALR(1) merges states whose items are the same apart from the lookaheads.',
                      cards=_cards(g, states)))
    for st in merged:
        if len(st.members) > 1:
            steps.append(dict(head=head, view='lr', note=(f'{_list([m.name for m in st.members])} have the same items apart from the lookaheads, '
                                                          f'so they merge into {st.name}, which keeps every lookahead.'),
                              cards=_cards(g, merged, show={st.name}, cur=st.name)))
    n = sum(1 for st in merged if len(st.members) > 1)
    steps[-1]['note'] += f' That leaves {len(merged)} states.' if n else ''
    if not n:
        steps[-1]['note'] = f'No two of the {len(states)} states share their items apart from the lookaheads, so nothing merges: LALR(1) has {len(merged)} states too.'
    return merged


def do_lr(g, method, steps, out):
    """method: lr0, slr, lr1 or lalr; needs an augmented grammar."""
    head = {'lr0': 'LR(0) items', 'slr': 'SLR(1)', 'lr1': 'Canonical LR(1)', 'lalr': 'LALR(1)'}[method]
    if method == 'lalr':
        sub = []
        canon = build_collection(g, True, sub, head)
        states = merge_lalr(g, canon, steps, head)
    else:
        states = build_collection(g, method in ('lr1',), steps, head)
    follow = None
    if method == 'slr':
        first = first_sets(g, None)
        follow = follow_sets(g, first, None)
        steps.append(dict(head=head, view='lr', note='SLR(1) uses these LR(0) states and FOLLOW sets: '
                          + '; '.join(f'FOLLOW({a}) = {g.fmt(follow[a])}' for a in g.nts[1:]) + '.', cards=_cards(g, states)))
    res = check_conflicts(g, states, method, steps, head, follow)
    out.setdefault('states', {})[method] = len(states)
    out.setdefault('ok', {})[method] = res['ok']
    out.setdefault('sr_conflicts', {})[method] = res['sr']
    out.setdefault('rr_conflicts', {})[method] = res['rr']
    out.setdefault('collections', {})[method] = states
    return states


def _parse_item(g, text, lr1=False):
    lhs, rhs = re.split(r'\s*(?:->|→)\s*', text.strip(), maxsplit=1)
    syms = rhs.split()
    if syms.count('.') != 1:
        raise SystemExit(f'An item needs one dot: {text!r}')
    d = syms.index('.')
    body = tuple(s for s in syms if s != '.')
    if (lhs, body) not in g.prods:
        raise SystemExit(f'No production for item {text!r}')
    return (g.prods.index((lhs, body)), d)


def do_goto(g, task, steps, out):
    head = 'GOTO'
    if 'from' in task:
        kernel = [_parse_item(g, t) for t in task['from']]
        items = _closure0(g, kernel)
        start = 'I'
        note = (f'Start from the item set {{{", ".join(_texts(g, kernel))}}}. '
                + ('Its closure adds nothing: no nonterminal follows a dot.' if len(items) == len(kernel)
                   else f'Its closure adds {len(items) - len(kernel)} items.'))
    else:
        kernel = [(0, 0)]
        items = _closure0(g, kernel)
        start = 'I0'
        note = (f'I0 is the closure of {_texts(g, kernel)[0]}: whenever a nonterminal follows the dot, add its productions '
                f'with the dot at the start. I0 has {len(items)} items.')
    states = [State(start, kernel, items)]
    steps.append(dict(head=head, view='lr', rule=0 if 'from' not in task else None, note=note, cards=_cards(g, states, show={start}, cur=start)))
    cur = states[0]
    name = start
    for x in task['goto']:
        kernel, items = _goto(g, cur.items, x, False)
        if kernel is None:
            raise SystemExit(f'GOTO({name}, {x}) is empty')
        name = f'GOTO({name}, {_q(x)})'
        nxt = State(name, kernel, items)
        cur.go.append((x, name))
        states.append(nxt)
        moved = _list(_texts(g, kernel))
        steps.append(dict(head=head, view='lr', note=(f'{name}: the items with {_q(x)} right after the dot are moved past it, giving {moved}. '
                                                      f'{_added(g, kernel, items, False)[0].upper() + _added(g, kernel, items, False)[1:]}.'),
                          cards=_cards(g, states, show={cur.name, nxt.name}, src=cur.name, cur=nxt.name)))
        cur = nxt
    n = len(cur.items)
    steps.append(dict(head=head, view='lr', note=f'{name} holds {n} items.', cards=_cards(g, states, show={cur.name}, cur=cur.name)))
    out['items'] = n


def do_together(g, task, steps, out):
    """Which of the listed items occur in one LR(0) state."""
    sub = []
    states = build_collection(g, False, sub, 'LR(0) items')
    steps.extend(sub)
    want = [(_parse_item(g, t), t) for t in task['items']]
    where = []
    for it, text in want:
        homes = [s.name for s in states if it in s.items]
        where.append(homes)
    bits = [f'{_item_text(g, *it)} is in {_list(h) if h else "no state"}' for (it, _), h in zip(want, where)]
    res = {}
    for a in range(len(want)):
        for b in range(a + 1, len(want)):
            res[(a + 1, b + 1)] = bool(set(where[a]) & set(where[b]))
    pairs = [f'{a} and {b}' for (a, b), v in res.items() if v]
    verdict = ('No two of them share a state.' if not pairs else f'Items {_list(pairs)} share a state.')
    steps.append(dict(head='LR(0) items', view='lr', note='; '.join(bits) + '. ' + verdict, cards=_cards(g, states, show={n for h in where for n in h})))
    out['together'] = res


# ----------------------------------------------------------- parse trees

class Trees:
    """Parse trees of a token string. A tree is (production, [children]); a leaf is the token index."""

    def __init__(self, g, toks):
        self.g, self.toks = g, toks
        self.cmemo, self.tmemo, self.busy = {}, {}, set()

    def count(self, a, i, j):
        key = (a, i, j)
        if key in self.cmemo:
            return self.cmemo[key]
        if key in self.busy:
            raise SystemExit(f'{a} can derive itself, so some strings have infinitely many parse trees')
        self.busy.add(key)
        n = sum(self._cseq(self.g.prods[p][1], 0, i, j) for p in self.g.by[a])
        self.busy.discard(key)
        self.cmemo[key] = n
        return n

    def _cseq(self, r, k, i, j):
        g = self.g
        if k == len(r):
            return 1 if i == j else 0
        x, rest = r[k], g.seqmin(r[k + 1:])
        if x not in g.ntset:
            return self._cseq(r, k + 1, i + 1, j) if i < j and self.toks[i] == x else 0
        total = 0
        for m in range(i + g.minlen[x], j - rest + 1):
            c = self.count(x, i, m)
            if c:
                total += c * self._cseq(r, k + 1, m, j)
        return total

    def trees(self, a, i, j, cap=12):
        key = (a, i, j)
        if key in self.tmemo:
            return self.tmemo[key]
        if self.count(a, i, j) > cap:
            raise SystemExit(f'Too many parse trees to show for {a}')
        out = []
        for p in self.g.by[a]:
            for kids in self._tseq(self.g.prods[p][1], 0, i, j, cap):
                out.append((p, kids))
        self.tmemo[key] = out
        return out

    def _tseq(self, r, k, i, j, cap):
        g = self.g
        if k == len(r):
            return [[]] if i == j else []
        x, rest = r[k], g.seqmin(r[k + 1:])
        if x not in g.ntset:
            if i < j and self.toks[i] == x:
                return [[i] + t for t in self._tseq(r, k + 1, i + 1, j, cap)]
            return []
        out = []
        for m in range(i + g.minlen[x], j - rest + 1):
            if not self.count(x, i, m):
                continue
            tails = self._tseq(r, k + 1, m, j, cap)
            for t in self.trees(x, i, m, cap):
                for tail in tails:
                    out.append([t] + tail)
        return out


def smallest_tree(g, toks):
    """One parse tree with the fewest nodes (works even when the grammar has cycles), or None."""
    n = len(toks)
    best = {}
    changed = True

    def seq(r, k, i, j):
        if k == len(r):
            return (0, []) if i == j else None
        x = r[k]
        if x not in g.ntset:
            if i < j and toks[i] == x:
                t = seq(r, k + 1, i + 1, j)
                return (t[0], [i] + t[1]) if t else None
            return None
        res = None
        for m in range(i, j + 1):
            b = best.get((x, i, m))
            if not b:
                continue
            t = seq(r, k + 1, m, j)
            if t and (res is None or b[0] + t[0] < res[0]):
                res = (b[0] + t[0], [b[1]] + t[1])
        return res

    while changed:
        changed = False
        for i in range(n + 1):
            for j in range(i, n + 1):
                for a in g.nts:
                    for p in g.by[a]:
                        t = seq(g.prods[p][1], 0, i, j)
                        if t and ((a, i, j) not in best or t[0] + 1 < best[(a, i, j)][0]):
                            best[(a, i, j)] = (t[0] + 1, (p, t[1]))
                            changed = True
    b = best.get((g.start, 0, n))
    smallest_tree.spans = set(best)
    return b[1] if b else None


def _pieces_step(g, lex, word, head):
    """Which pieces of the input each nonterminal can derive (from the search that found no derivation)."""
    rows = []
    for a in g.nts:
        got = sorted({(j - i, i, j) for (x, i, j) in smallest_tree.spans if x == a and j > i})
        seen, pieces = set(), []
        for _, i, j in got:
            w = _word(g, lex[i:j])
            if w not in seen:
                seen.add(w)
                pieces.append(w)
        rows.append([a, pieces])
    return dict(head=head, view='pieces', rows=rows, rule=None,
                note=f'Work out, for every piece of {word}, which nonterminals can derive it, from the shortest pieces up. '
                     f'{g.start} derives the pieces listed beside it, but never all of {word}, so {word} is not generated.')


def _tokens(text):
    toks, lex = [], []
    for t in text.split():
        if ':' in t and len(t) > 1:
            c, v = t.split(':', 1)
            toks.append(c)
            lex.append(v)
        else:
            toks.append(t)
            lex.append(t)
    return toks, lex


def _word(g, lex):
    return (' ' if g.spaced else '').join(lex) if lex else EPS


def _derivation(g, tree, lex, rightmost, head, tabsteps):
    """Sentential forms of a leftmost (or rightmost) derivation of the tree."""
    form = [('n', tree)]

    def text(form):
        return [(g.prods[x[1][0]][0] if x[0] == 'n' else lex[x[1]]) for x in form]

    lines = [dict(syms=text(form), hi=[0], new=[])]
    tabsteps.append(dict(head=head, view='derive', note=f'Start from {g.start}.', lines=[dict(l) for l in lines], rule=None))
    count = 0
    while any(x[0] == 'n' for x in form):
        idx = [k for k, x in enumerate(form) if x[0] == 'n']
        k = idx[-1] if rightmost else idx[0]
        p, kids = form[k][1]
        rep = [('n', c) if isinstance(c, tuple) else ('t', c) for c in kids]
        form = form[:k] + rep + form[k + 1:]
        count += 1
        a = g.prods[p][0]
        which = 'rightmost' if rightmost else 'leftmost'
        many = len(idx) > 1
        note = f'Expand the {which} {a} by {g.pt(p)}.' if many else f'Expand {a} by {g.pt(p)}.'
        if not kids:
            note = (f'The {which} {a} derives ε here: use {g.pt(p)}.' if many else f'{a} derives ε here: use {g.pt(p)}.')
        lines[-1]['hi'] = [k]
        lines.append(dict(syms=text(form), hi=[], new=list(range(k, k + len(rep)))))
        tabsteps.append(dict(head=head, view='derive', note=note, rule=p, lines=[dict(l) for l in lines]))
    return count


def do_trees(g, task, steps_by_tab, out, rightmost=False):
    toks, lex = _tokens(task['trees'])
    word = _word(g, lex)
    for t in toks:
        if t not in g.terms:
            raise SystemExit(f'{t} is not a terminal of the grammar')
    if task.get('generated_only'):
        tree = smallest_tree(g, toks)
        out.setdefault('generated', {})[task['trees']] = tree is not None
        tab = []
        if tree is None:
            tab.append(dict(head=word, view='derive', note=f'Is {word} generated? Look for a derivation from {g.start}.', lines=[dict(syms=[g.start], hi=[], new=[])], rule=None))
            tab.append(_pieces_step(g, lex, word, word))
        else:
            n = _derivation(g, tree, lex, rightmost, word, tab)
            tab[-1]['note'] += f' That is {word}, so it is generated ({n} steps).'
        steps_by_tab.append((word, f'Is {word} generated?', tab))
        return
    tr = Trees(g, toks)
    n = tr.count(g.start, 0, len(toks))
    out.setdefault('trees', {})[task['trees']] = n
    if n == 0:
        if smallest_tree(g, toks) is not None:
            raise SystemExit(f'The tree count and the search disagree for {word}')
        tab = [dict(head=word, view='derive', note=f'Try to derive {word} from {g.start}.', lines=[dict(syms=[g.start], hi=[], new=[])], rule=None),
               _pieces_step(g, lex, word, word)]
        steps_by_tab.append((word, f'{word}: no parse tree', tab))
        return
    which = 'rightmost' if rightmost else 'leftmost'
    trees = tr.trees(g.start, 0, len(toks))
    for k, t in enumerate(trees):
        tab = []
        name = f'{word}: tree {k + 1}' if n > 1 else word
        _derivation(g, t, lex, rightmost, name, tab)
        if n == 1:
            tab[-1]['note'] += f' This is the only parse tree of {word}, so it has exactly one {which} derivation.'
        else:
            tab[-1]['note'] += f' That is {word}: parse tree {k + 1} of {n}.'
            if k == n - 1:
                tab[-1]['note'] += f' {word} has {n} different parse trees ({n} {which} derivations), so the grammar is ambiguous.'
            elif k == 0:
                tab[-1]['note'] += ' The next tab shows another.'
        steps_by_tab.append((f'Tree {k + 1}' if n > 1 else word, f'{word}, {which} derivation' + (f' {k + 1} of {n}' if n > 1 else ''), tab))


# ----------------------------------------------------- translation actions

def _eval(expr, vals):
    """Arithmetic over $k (values of the right-side symbols) with + − * × / and brackets."""
    toks = re.findall(r'\$\d+|\d+(?:\.\d+)?|[-+*/×−()]', expr)
    if ''.join(toks) != re.sub(r'\s+', '', expr):
        raise SystemExit(f'Bad action expression {expr!r}')
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def atom():
        t = take()
        if t == '(':
            v, s = add()
            if take() != ')':
                raise SystemExit(f'Bad action expression {expr!r}')
            return v, f'({s})'
        if t in ('-', '−'):
            v, s = atom()
            return -v, f'−{s}'
        if t.startswith('$'):
            k = int(t[1:]) - 1
            if k >= len(vals) or vals[k] is None:
                raise SystemExit(f'{t} has no value in {expr!r}')
            v = vals[k]
            return v, (f'({_show(v)})' if v < 0 else _show(v))
        return Fraction(t), _show(Fraction(t))

    def mul():
        v, s = atom()
        while peek() in ('*', '×', '/'):
            op = take()
            w, t = atom()
            if op == '/':
                if w == 0:
                    raise SystemExit('Division by zero in an action')
                v, s = v / w, f'{s} / {t}'
            else:
                v, s = v * w, f'{s} × {t}'
        return v, s

    def add():
        v, s = mul()
        while peek() in ('+', '-', '−'):
            op = take()
            w, t = mul()
            v, s = (v + w, f'{s} + {t}') if op == '+' else (v - w, f'{s} − {t}')
        return v, s

    v, s = add()
    if pos[0] != len(toks):
        raise SystemExit(f'Bad action expression {expr!r}')
    return v, s


def _lexval(x):
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError):
        return None


def do_sr(g, task, steps, out):
    """Shift-reduce parse of the input; the unique parse tree fixes every move."""
    toks, lex = _tokens(task['sr'])
    for t in toks:
        if t not in g.terms:
            raise SystemExit(f'{t} is not a terminal of the grammar')
    tr = Trees(g, toks)
    n = tr.count(g.start, 0, len(toks))
    if n != 1:
        raise SystemExit(f'{task["sr"]!r} has {n} parse trees, not exactly one')
    tree = tr.trees(g.start, 0, len(toks))[0]
    events = []

    def walk(node):
        p, kids = node
        for c in kids:
            if isinstance(c, tuple):
                walk(c)
            else:
                events.append(('s', c))
        events.append(('r', p))
    walk(tree)
    printing = any('print' in a for a in g.acts)
    valued = any('val' in a for a in g.acts)
    cols = ['Stack', 'Input', 'Action'] + (['Printed'] if printing else [])
    rows, stack, printed, handles, reductions = [], [], [], [], 0
    pos = 0
    head = 'Shift-reduce parse'

    def row(action):
        r = dict(stack=[[s, _show(v) if v is not None else None] for s, v, _ in stack], input=lex[pos:] + [END], action=action)
        if printing:
            r['out'] = ''.join(printed)
        rows.append(r)

    row('start')
    steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None,
                      note='Start with an empty stack and the whole input. Shift tokens onto the stack; when the top of the stack is a handle '
                           '(the right side the parse reduces next), replace it by the production\'s left side.'))
    for kind, x in events:
        if kind == 's':
            top = [s for s, _, _ in stack]
            match = None
            for i, (a, r) in enumerate(g.prods):
                if r and len(top) >= len(r) and tuple(top[len(top) - len(r):]) == r:
                    match = i
                    break
            stack.append((toks[x], _lexval(lex[x]) if toks[x] != lex[x] else None, lex[x]))
            pos = x + 1
            row(f'shift {lex[x]}')
            if match is not None:
                note = f'{g.rt(g.prods[match][1])} on top matches {g.pt(match)}, but it is not the handle here, so shift {lex[x]}.'
            elif not top:
                note = f'The stack is empty: shift {lex[x]}.'
            else:
                note = f'No handle on top of the stack yet, so shift {lex[x]}.'
            steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None, note=note))
            continue
        p = x
        a, r = g.prods[p]
        k = len(r)
        popped = stack[len(stack) - k:] if k else []
        del stack[len(stack) - k:]
        act = g.acts[p]
        note = (f'The top of the stack, {g.rt(r)}, is the handle: reduce it to {a} by {g.pt(p)}.' if k
                else f'The handle here is empty: reduce by {g.pt(p)}, pushing {a} without popping anything.')
        value = None
        if 'val' in act:
            vals = [v for _, v, _ in popped]
            value, shown = _eval(act['val'], vals)
            simple = re.fullmatch(r'\s*-?\d+(\.\d+)?\s*', act['val']) is not None
            note += f' {a}.val = {_show(value)}.' if simple or shown == _show(value) else f' {a}.val = {shown} = {_show(value)}.'
        if 'print' in act:
            s = act['print']
            s = re.sub(r'\$(\d+)', lambda m: popped[int(m.group(1)) - 1][2], s)
            printed.append(s)
            note += f' Print {s}.'
        stack.append((a, value, None))
        handles.append(r)
        reductions += 1
        row(f'reduce {g.pt(p, "→")}')
        steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=p, note=note))
    row('accept')
    final = f'Only {g.start} is left on the stack and the input is used up, so accept after {reductions} reductions.'
    if printing:
        final += f' The printed output is {"".join(printed)}.'
    if valued:
        final += f' The value is {g.start}.val = {_show(stack[-1][1])}.'
    steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None, note=final))
    out['output'] = ''.join(printed)
    out['value'] = stack[-1][1]
    out['handles'] = [list(h) for h in handles]
    out['reductions'] = reductions


def _short_mark(m):
    """{print('+')} as {print +}, {print(num.val)} as {print num}, to keep the stack narrow."""
    body = m[1:-1].strip().rstrip(';').strip()
    lit = re.fullmatch(r"print\(\s*'(.*)'\s*\)", body) or re.fullmatch(r'print\(\s*(\w+)\.\w+\s*\)', body)
    return '{print ' + lit.group(1) + '}' if lit else m


def _run_mark(g, m, node, lex):
    """{print('+')} prints +, {print(num.val)} prints the lexeme of num in this production."""
    body = m[1:-1].strip().rstrip(';').strip()
    lit = re.fullmatch(r"print\(\s*'(.*)'\s*\)", body)
    if lit:
        return lit.group(1)
    ref = re.fullmatch(r'print\(\s*(\w+)\.\w+\s*\)', body)
    if ref:
        p, kids = node
        r = g.prods[p][1]
        if r.count(ref.group(1)) != 1:
            raise SystemExit(f'{m}: {ref.group(1)} must occur once in {g.pt(p)}')
        return lex[kids[r.index(ref.group(1))]]
    raise SystemExit(f'Unknown action {m}')


def do_ll(g, task, steps, out):
    """Predictive (top-down) parse with embedded actions; the unique parse tree picks each production."""
    toks, lex = _tokens(task['ll'])
    for t in toks:
        if t not in g.terms:
            raise SystemExit(f'{t} is not a terminal of the grammar')
    tr = Trees(g, toks)
    n = tr.count(g.start, 0, len(toks))
    if n != 1:
        raise SystemExit(f'{task["ll"]!r} has {n} parse trees, not exactly one')
    tree = tr.trees(g.start, 0, len(toks))[0]
    first = first_sets(g, None)
    follow = follow_sets(g, first, None)
    table = {}
    for i, (a, r) in enumerate(g.prods):
        f, nullable = g.first_seq(r, first)
        for t in f | (follow[a] if nullable else set()):
            table.setdefault((a, t), []).append(i)
    cols = ['Stack', 'Input', 'Action', 'Printed']
    rows, printed = [], []
    head = 'Predictive parse'
    # stack entries: ('n', node, span) | ('t', token index) | ('a', mark text, (prod, kids)) | ('$',)
    spans = {}

    def span(node, i):
        p, kids = node
        j = i
        for c in kids:
            if isinstance(c, tuple):
                j = span(c, j)
            else:
                j = c + 1
        spans[id(node)] = (i, j)
        return j
    span(tree, 0)
    stack = [('n', tree), ('$',)]
    pos = 0

    def show(e):
        if e[0] == 'n':
            return g.prods[e[1][0]][0]
        if e[0] == 't':
            return toks[e[1]]
        if e[0] == 'a':
            return _short_mark(e[1])
        return END

    def row(action):
        rows.append(dict(stack=[[show(e), None] for e in stack], input=lex[pos:] + [END], action=action, out=''.join(printed)))

    row('start')
    steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None, top=True,
                      note=f'The stack starts with {g.start} above $ (top first). Expand the nonterminal on top, match a terminal on top '
                           'with the next input token, and run an action when it reaches the top.'))
    while stack[0][0] != '$':
        e = stack.pop(0)
        if e[0] == 't':
            pos = e[1] + 1
            row(f'match {lex[e[1]]}')
            steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None, top=True,
                              note=f'{toks[e[1]]} is on top and is the next input token' + (f' ({lex[e[1]]})' if lex[e[1]] != toks[e[1]] else '') + ': match it and move on.'))
            continue
        if e[0] == 'a':
            s = _run_mark(g, e[1], e[2], lex)
            printed.append(s)
            row(f'print {s}')
            steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=e[2][0], top=True,
                              note=f'The action {e[1]} is on top: run it, printing {s}.'))
            continue
        node = e[1]
        p, kids = node
        a, r = g.prods[p]
        i, j = spans[id(node)]
        look = toks[pos] if pos < len(toks) else END
        cell = table.get((a, look), [])
        if cell == [p]:
            why = f'M[{a}, {look}] is {g.full(p)}'
        else:
            sub = _word(g, lex[i:j])
            why = f'{a} has to derive {sub} here' if j > i else f'{a} has to derive ε here'
            alts = [q for q in g.by[a] if q != p]
            why += (f', and only {g.full(p)} can do that' if alts else '')
        new = []
        for k, c in enumerate(kids):
            new.append(('n', c) if isinstance(c, tuple) else ('t', c))
        # embedded actions go in at their positions
        body = list(new)
        for pos_m, m in reversed(g.marks[p]):
            body.insert(pos_m, ('a', m, (p, kids)))
        stack[0:0] = body
        row(f'{g.full(p, "→")}')
        note = f'{why}: replace {a} by ' + (' '.join(show(x) for x in body) if body else 'nothing') + '.'
        steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=p, top=True, note=note))
    row('accept')
    steps.append(dict(head=head, view='sr', cols=cols, rows=[dict(r) for r in rows], rule=None, top=True,
                      note=f'Only $ is left and the input is used up, so accept. The printed output is {"".join(printed)}.'))
    out['output'] = ''.join(printed)


# ------------------------------------------------------------------ checks

def _set(text):
    return set(text.split())


def _check(qid, name, g, expect, out):
    if not expect:
        raise SystemExit(f'Animation for {qid} ({name}) has no expectation')
    for k, want in expect.items():
        if k in ('first', 'follow'):
            got = {a: out[k][a] for a in want}
            want = {a: _set(v) for a, v in want.items()}
        elif k in ('cells', 'table'):
            got, w2 = {}, {}
            for a, t, rhs in want:
                w2[(a, t)] = sorted(tuple(_syms(x)) for x in rhs)
                got[(a, t)] = sorted(out['table'].get((a, t), []))
            if k == 'table':
                got = {key: sorted(v) for key, v in out['table'].items()}
                w2 = {key: v for key, v in w2.items() if v}
            want = w2
        elif k == 'll1':
            got = out.get('ll1')
        elif k in ('lr0', 'slr1', 'lr1', 'lalr1'):
            got = out.get('ok', {}).get({'lr0': 'lr0', 'slr1': 'slr', 'lr1': 'lr1', 'lalr1': 'lalr'}[k])
        elif k == 'states':
            got = {m: out.get('states', {}).get(m) for m in want}
        elif k == 'sr_conflicts':
            got = {m: out.get('sr_conflicts', {}).get(m) for m in want}
        elif k == 'relation':
            vals = {n: out['states'][m] for n, m in want['names'].items()}
            parts = re.split(r'(<=|>=|=|<|>)', want['holds'])
            ok = True
            for x in range(1, len(parts) - 1, 2):
                l, op, r = vals[parts[x - 1]], parts[x], vals[parts[x + 1]]
                ok &= {'=': l == r, '<': l < r, '>': l > r, '<=': l <= r, '>=': l >= r}[op]
            got, want = ok, True
        elif k == 'items':
            got = out.get('items')
        elif k == 'together':
            got = {tuple(map(int, key.split(','))): out['together'].get(tuple(map(int, key.split(',')))) for key in want}
            want = {tuple(map(int, key.split(','))): v for key, v in want.items()}
        elif k == 'output':
            got = out.get('output')
        elif k == 'value':
            got, want = out.get('value'), Fraction(want)
        elif k == 'reductions':
            got = out.get('reductions')
        elif k == 'handles':
            got, want = out.get('handles'), [x.split() for x in want]
        elif k in ('trees', 'generated'):
            got = {s: out.get(k, {}).get(s) for s in want}
        elif k == 'code':
            got = out.get('code')
        else:
            raise SystemExit(f'Animation for {qid}: unknown expectation {k}')
        if got != want:
            raise SystemExit(f'Animation for {qid} ({name}): {k} is {got}, not {want}')


TITLES = {'sets': 'FIRST and FOLLOW', 'll1': 'LL(1) table', 'lr0': 'LR(0)', 'slr': 'SLR(1)', 'lr1': 'LR(1)', 'lalr': 'LALR(1)'}


def _grammar_view(g):
    return [g.full(i) for i in range(len(g.prods))]


def parse_animation(qid, spec):
    schedules = []
    parts = spec.get('parts', [spec])
    for part in parts:
        name = part.get('name', '')
        lines = part.get('grammar', spec.get('grammar'))
        start = part.get('start', spec.get('start'))
        terms = part.get('terminals', spec.get('terminals'))
        g = Grammar(lines, start, terminals=terms)
        if part.get('augmented', spec.get('augmented')):
            # The question gives S' -> S itself.
            if len(g.prods[0][1]) != 1 or len(g.by[g.start]) != 1 or g.prods[0][1][0] not in g.ntset:
                raise SystemExit(f'Animation for {qid}: the first production is not of the form S′ → S')
            ga = g
        else:
            lr = any(t in ('lr0', 'slr', 'lr1', 'lalr') or (isinstance(t, dict) and ('goto' in t or 'items' in t)) for t in part['do'])
            ga = Grammar(lines, start, augment=True, terminals=terms) if lr else None
        out = {}
        sets = None
        pre = f'{name}: ' if name else ''
        for task in part['do']:
            steps, tabs = [], None
            gv = ga if task in ('lr0', 'slr', 'lr1', 'lalr') or (isinstance(task, dict) and ('goto' in task or 'items' in task)) else g
            if task == 'sets':
                sets = do_sets(g, steps, out)
                short, title = 'FIRST/FOLLOW', 'FIRST and FOLLOW sets'
                if 'code' in part:
                    c = part['code']
                    which, a = c['of'].split()
                    members = out[which][a]
                    ix = sorted((c['index'][t] for t in members), reverse=True)
                    out['code'] = ''.join(str(x) for x in ix)
                    steps[-1]['note'] += (f' That gives {which.upper()}({a}) = {g.fmt(members)}. Their indices in descending order are '
                                          f'{_list([str(x) for x in ix])}, which concatenate to {out["code"]}.')
            elif task == 'll1':
                sets = sets or (lambda f: (f, follow_sets(g, f, None)))(first_sets(g, None))
                do_ll1(g, steps, out, *sets)
                short, title = 'LL(1) table', 'LL(1) parsing table'
            elif task in ('lr0', 'slr', 'lr1', 'lalr'):
                do_lr(ga, task, steps, out)
                short = TITLES[task]
                title = {'lr0': 'LR(0) item sets', 'slr': 'SLR(1): LR(0) item sets with FOLLOW', 'lr1': 'Canonical LR(1) item sets',
                         'lalr': 'LALR(1): LR(1) states merged'}[task]
            elif isinstance(task, dict) and 'goto' in task:
                do_goto(ga, task, steps, out)
                short, title = 'GOTO', 'LR(0) closure and GOTO'
            elif isinstance(task, dict) and 'items' in task:
                do_together(ga, task, steps, out)
                short, title = 'LR(0) items', 'LR(0) item sets'
            elif isinstance(task, dict) and 'sr' in task:
                do_sr(g, task, steps, out)
                short, title = 'Shift-reduce', f'Shift-reduce parse of {_word(g, _tokens(task["sr"])[1])}'
            elif isinstance(task, dict) and 'll' in task:
                do_ll(g, task, steps, out)
                short, title = 'Predictive parse', f'Top-down parse of {_word(g, _tokens(task["ll"])[1])}'
            elif isinstance(task, dict) and 'trees' in task:
                tabs = []
                do_trees(g, task, tabs, out, task.get('rightmost', False))
            else:
                raise SystemExit(f'Animation for {qid}: unknown task {task}')
            if tabs is None:
                tabs = [(short, title, steps)]
            for short, title, st in tabs:
                if len(st) < 2:
                    raise SystemExit(f'Animation for {qid} has a tab with fewer than two steps')
                schedules.append(dict(dict(short=pre + short, title=pre + title, grammar=_grammar_view(gv), steps=st), **({'spaced': True} if gv.spaced else {})))
        _check(qid, name or 'grammar', g, part.get('expect'), out)
    for s in schedules:
        s['steps'][-1]['final'] = True
        _compact(s)
    data = dict(kind=spec['kind'], schedules=schedules, count=sum(len(s['steps']) for s in schedules))
    if spec['kind'] == 'parse-trees':
        data['tabs_label'] = 'derivations'
    return data


# Animation kinds this family provides, and the player file that draws them.
KINDS = {k: parse_animation for k in ('parse-sets', 'parse-ll1', 'parse-lr', 'parse-sr', 'parse-ll', 'parse-trees')}
PLAYER = 'parsing'
TABS = 'parts'
