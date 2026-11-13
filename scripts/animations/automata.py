"""Finite automata stated in the question text.

Runs of a DFA, NFA or ε-NFA on given strings, counting the accepted strings of a
given shape, the subset construction, minimisation by partition refinement (DFAs,
product DFAs and Mealy machines), the minimal DFA of a precisely stated language,
claims about a machine's language, and Mealy output traces.

Data: data/animations/automata.json. A machine is stated as `states`, `start`,
`final`, `alphabet` and `edges` [from, labels, to], where labels are symbols
separated by commas ("0,1"), ε for a move without input, or input/output pairs
("1/01") for a Mealy machine. A language is {"regex": ...} in the question's
notation (+ is union, ε the empty string, ⁺ one or more), {"member": a Python
expression in w}, {"machine": ...}, or {"rule": ...} (states built by an update
rule) together with "member". Everything else is computed here, and the build
stops on any difference from `expect`.

Language facts are decided exactly with DFAs whenever both sides are regular, and
are also checked on every string up to a length set by the alphabet size. A
"member" predicate alone can supply a counterexample, never a universal proof. A minimal-DFA count whose machine needs a
dead state is accepted only when the spec says the question counts it
(`"dead": "counted"`, for a question that asks for a complete DFA).
"""
import math
import re
from collections import deque
from itertools import product as _cartesian

from .common import _list

EPS = 'ε'
SAFE = {'__builtins__': {}, 'len': len, 'int': int, 'all': all, 'any': any, 'range': range, 'sum': sum,
        'min': min, 'max': max, 'set': set, 'format': format, 'zip': zip, 'str': str, 'abs': abs, 'tuple': tuple,
        'prod': math.prod}


def fail(qid, msg):
    raise SystemExit(f'Animation for {qid}: {msg}')


def check(qid, what, got, want):
    if got != want:
        fail(qid, f'{what} is {got!r}, not the expected {want!r}')


def show(w):
    return w if w else 'ε'


_COMPILED = {}


def _ev(qid, expr, **env):
    try:
        # Expressions come from the repository's own spec file; each is compiled once and reused.
        code = _COMPILED.get(expr)
        if code is None:
            code = _COMPILED[expr] = compile(expr, '<spec>', 'eval')
        return eval(code, dict(SAFE, **env))
    except Exception as e:  # noqa: BLE001
        fail(qid, f'cannot evaluate {expr!r}: {e}')


def maxlen(k):
    """Brute-force checks cover every string up to this length (about 16,000 strings)."""
    return 30 if k == 1 else max(5, int(14 / math.log2(k)))


def words(alphabet, n):
    """Every string of length 0..n, shortest first, in alphabet order."""
    for k in range(n + 1):
        for t in _cartesian(alphabet, repeat=k):
            yield ''.join(t)


# ---------------------------------------------------------------- machines

class FA:
    """A DFA, NFA, ε-NFA or Mealy machine exactly as the question states it."""

    def __init__(self, qid, spec, name='the machine'):
        self.qid, self.name = qid, name
        self.states = [str(s) for s in spec['states']]
        if len(set(self.states)) != len(self.states):
            fail(qid, f'{name} lists a state twice')
        self.start = None if spec.get('start') is None else str(spec['start'])  # a Mealy table may have none
        self.final = [str(s) for s in spec.get('final', [])]
        for s in ([self.start] if self.start else []) + self.final:
            if s not in self.states:
                fail(qid, f'{name}: {s} is not a listed state')
        self.delta, self.out, groups, syms = {}, {}, {}, []
        for e in spec['edges']:
            if len(e) != 3:
                fail(qid, f'{name}: edge {e} is not [from, labels, to]')
            u, lab, v = str(e[0]), str(e[1]), str(e[2])
            if u not in self.states or v not in self.states:
                fail(qid, f'{name}: edge {e} uses an unlisted state')
            g = groups.setdefault((u, v), [])
            for item in [x.strip() for x in lab.split(',')]:
                if not item:
                    fail(qid, f'{name}: empty label on {e}')
                c, o = (item.split('/', 1) + [None])[:2]
                if o is not None:
                    if (u, c) in self.out:
                        fail(qid, f'{name}: two outputs for {u} on {c}')
                    self.out[(u, c)] = o
                tg = self.delta.setdefault((u, c), [])
                if v in tg:
                    fail(qid, f'{name}: {u} --{c}--> {v} is listed twice')
                tg.append(v)
                g.append(item)
                if c != EPS and c not in syms:
                    syms.append(c)
        self.alphabet = [str(c) for c in spec['alphabet']] if 'alphabet' in spec else sorted(syms)
        for c in syms:
            if c not in self.alphabet:
                fail(qid, f'{name}: symbol {c} is not in the alphabet')
        self.edges = [[u, v, ','.join(lab)] for (u, v), lab in groups.items()]
        self.eidx = {(u, v): i for i, (u, v, _) in enumerate(self.edges)}
        self.mealy = bool(self.out)
        self.eps = any(c == EPS for (_, c) in self.delta)
        self.det = not self.eps and all(len(t) == 1 for t in self.delta.values())
        self.complete = self.det and all((s, c) in self.delta for s in self.states for c in self.alphabet)
        if self.mealy:
            if not self.complete or len(self.out) != len(self.delta):
                fail(qid, f'{name}: a Mealy machine needs one next state and one output for every state and input')
        self.pos = spec.get('pos')
        self.numeric = all(x.isdigit() for x in self.states)

    def who(self, xs):
        """State names for a note: 'state 3' or 'states 2 and 5' when the states are numbers."""
        xs = list(xs)
        return (('state ' if len(xs) == 1 else 'states ') if self.numeric else '') + _list(xs)

    def order(self, S):
        return [s for s in self.states if s in S]

    def fmt(self, S):
        return '{' + ', '.join(self.order(S)) + '}' if S else '∅'

    def nxt(self, s, c):
        return self.delta[(s, c)][0]

    def closure(self, S):
        """ε-closure, and the ε-edges it follows."""
        seen, todo, used = set(S), list(self.order(S)), []
        while todo:
            s = todo.pop(0)
            for t in self.delta.get((s, EPS), []):
                used.append(self.eidx[(s, t)])
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        return frozenset(seen), used

    def move(self, S, c):
        T, used = set(), []
        for s in self.order(S):
            for t in self.delta.get((s, c), []):
                T.add(t)
                used.append(self.eidx[(s, t)])
        return frozenset(T), used

    def run_from(self, S, w):
        S = self.closure(S)[0]
        for c in w:
            S = self.closure(self.move(S, c)[0])[0]
        return S

    def accepts(self, w):
        return bool(self.run_from({self.start}, w) & set(self.final))

    def subsets(self):
        """The subset construction from the start state: subsets in the order found, and their moves."""
        S0 = self.closure({self.start})[0]
        order, trans, todo = [S0], {}, deque([S0])
        while todo:
            S = todo.popleft()
            for c in self.alphabet:
                T = self.closure(self.move(S, c)[0])[0]
                trans[(S, c)] = T
                if T not in order:
                    order.append(T)
                    todo.append(T)
        return order, trans

    def dfa(self):
        order, trans = self.subsets()
        F = set(self.final)
        return DFA(order, self.alphabet, order[0], {S for S in order if S & F}, trans)

    def reachable(self):
        seen, todo = [self.start], [self.start]
        while todo:
            s = todo.pop(0)
            for c in self.alphabet + [EPS]:
                for t in self.delta.get((s, c), []):
                    if t not in seen:
                        seen.append(t)
                        todo.append(t)
        return self.order(seen)

    def outputs(self, w, s=None):
        s, outs, path = s or self.start, [], [s or self.start]
        for c in w:
            outs.append(self.out[(s, c)])
            s = self.nxt(s, c)
            path.append(s)
        return outs, path

    def draw(self, pos=None):
        return dict(states=self.states, start=self.start, final=self.final, edges=self.edges,
                    pos=layout(self.qid, self.states, self.start, self.edges, pos or self.pos))


class DFA:
    """A complete DFA over hashable states, used to decide language facts exactly."""

    def __init__(self, states, alphabet, start, final, delta):
        self.states, self.alphabet, self.start, self.final, self.delta = list(states), list(alphabet), start, set(final), delta

    def run(self, w, s=None):
        s = self.start if s is None else s
        for c in w:
            s = self.delta[(s, c)]
        return s

    def accepts(self, w):
        return self.run(w) in self.final

    def complement(self):
        return DFA(self.states, self.alphabet, self.start, set(self.states) - self.final, self.delta)

    def witness(self, other, bad):
        """A shortest string (alphabet order among equals) with bad(self accepts, other accepts), or None."""
        if self.alphabet != other.alphabet:
            raise SystemExit('Comparing languages over different alphabets')
        start = (self.start, other.start)
        seen, todo = {start: ''}, deque([start])
        while todo:
            p = todo.popleft()
            if bad(p[0] in self.final, p[1] in other.final):
                return seen[p]
            for c in self.alphabet:
                q = (self.delta[(p[0], c)], other.delta[(p[1], c)])
                if q not in seen:
                    seen[q] = seen[p] + c
                    todo.append(q)
        return None

    def minimal_size(self):
        reach = reach_order(self.start, self.alphabet, lambda s, c: self.delta[(s, c)])
        hist = refine(reach, self.alphabet, lambda s, c: self.delta[(s, c)], lambda s: s in self.final)
        return len(hist[-1]['blocks'])


def reach_order(start, alphabet, nxt):
    seen, todo = [start], deque([start])
    while todo:
        s = todo.popleft()
        for c in alphabet:
            t = nxt(s, c)
            if t not in seen:
                seen.append(t)
                todo.append(t)
    return seen


def refine(states, alphabet, nxt, key):
    """Moore's partition refinement. key(s) gives the first grouping (acceptance, or a Mealy
    machine's outputs). A group that splits keeps its number for the part holding its first
    state; the other parts get new numbers. Returns one entry per round."""
    blocks, keys = [], []
    for s in states:
        k = key(s)
        if k not in keys:
            keys.append(k)
            blocks.append([])
        blocks[keys.index(k)].append(s)
    hist = [dict(blocks=[list(b) for b in blocks], keys=keys, sig=None, splits=[])]
    while True:
        bid = {s: i for i, b in enumerate(blocks) for s in b}
        sig = {s: tuple(bid[nxt(s, c)] for c in alphabet) for s in states}
        new, splits = [list(b) for b in blocks], []
        for i, b in enumerate(blocks):
            parts = {}
            for s in b:
                parts.setdefault(sig[s], []).append(s)
            if len(parts) > 1:
                ps = list(parts.values())
                new[i] = ps[0]
                for p in ps[1:]:
                    new.append(p)
                splits.append((i, ps))
        hist[-1]['sig'] = sig
        if not splits:
            return hist
        hist.append(dict(blocks=new, sig=None, splits=splits, prev=blocks))
        blocks = new


def separate(states_nxt, alphabet, p, q, differ):
    """A shortest suffix on which states p and q behave differently. differ(a, b, c) says whether
    the states a, b already differ (c None: acceptance; else the output on symbol c)."""
    seen, todo = {(p, q): ''}, deque([(p, q)])
    while todo:
        a, b = todo.popleft()
        w = seen[(a, b)]
        if differ(a, b, None):
            return w
        for c in alphabet:
            if differ(a, b, c):
                return w + c
            n = (states_nxt(a, c), states_nxt(b, c))
            if n not in seen:
                seen[n] = w + c
                todo.append(n)
    return None


# ---------------------------------------------------------------- regular expressions

def parse_regex(qid, text, alphabet):
    toks = [ch for ch in text if not ch.isspace()]
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat(ch=None):
        c = peek()
        if ch is not None and c != ch:
            fail(qid, f'regex {text!r}: expected {ch!r} at position {pos[0]}')
        pos[0] += 1
        return c

    def union():
        node = concat()
        while peek() in ('+', '|'):
            eat()
            node = ('|', node, concat())
        return node

    def concat():
        parts = []
        while peek() is not None and peek() not in '+|)':
            parts.append(postfix())
        if not parts:
            fail(qid, f'regex {text!r}: empty operand at position {pos[0]}')
        node = parts[0]
        for p in parts[1:]:
            node = ('.', node, p)
        return node

    def postfix():
        node = atom()
        while peek() in ('*', '⁺'):
            node = ('*' if eat() == '*' else '⁺', node)
        return node

    def atom():
        c = peek()
        if c == '(':
            eat()
            node = union()
            eat(')')
            return node
        if c == EPS:
            eat()
            return ('e',)
        if c is not None and c in alphabet:
            eat()
            return ('c', c)
        fail(qid, f'regex {text!r}: unexpected {c!r}')

    node = union()
    if peek() is not None:
        fail(qid, f'regex {text!r}: unexpected {peek()!r}')
    return node


def thompson(qid, node, alphabet):
    edges, n = [], [0]

    def new():
        n[0] += 1
        return str(n[0] - 1)

    def build(t):
        a, b = new(), new()
        if t[0] == 'e':
            edges.append([a, EPS, b])
        elif t[0] == 'c':
            edges.append([a, t[1], b])
        elif t[0] == '|':
            for sub in t[1:]:
                x, y = build(sub)
                edges.extend([[a, EPS, x], [y, EPS, b]])
        elif t[0] == '.':
            x1, y1 = build(t[1])
            x2, y2 = build(t[2])
            edges.extend([[a, EPS, x1], [y1, EPS, x2], [y2, EPS, b]])
        else:
            x, y = build(t[1])
            edges.extend([[a, EPS, x], [y, EPS, b], [y, EPS, x]])
            if t[0] == '*':
                edges.append([a, EPS, b])
        return a, b

    s, f = build(node)
    return FA(qid, dict(states=[str(i) for i in range(n[0])], start=s, final=[f], alphabet=alphabet, edges=edges), 'the expression')


class Lang:
    """A language from the spec: membership for brute-force checks, and a DFA when it is regular by construction."""

    def __init__(self, qid, src, alphabet):
        self.qid, self.alphabet, self.dfa = qid, list(alphabet), None
        self.text = src.get('text')
        if 'regex' in src:
            raw = src['regex']
            self.dfa = thompson(qid, parse_regex(qid, raw, self.alphabet), self.alphabet).dfa()
            pat = re.compile(raw.replace(' ', '').replace('+', '|').replace('⁺', '+').replace(EPS, '(?:)'))
            self.member = lambda w: pat.fullmatch(w) is not None
            for w in words(self.alphabet, maxlen(len(self.alphabet))):
                if self.dfa.accepts(w) != self.member(w):
                    fail(qid, f'the construction of {raw} disagrees with Python re on {show(w)}')
            self.text = self.text or raw
            if 'member' in src:  # the regex is our construction; the member test transcribes the question
                expr = src['member']
                self.member = lambda w: bool(_ev(qid, expr, w=w))
        elif 'machine' in src:
            fa = FA(qid, src['machine'], src.get('text', 'the other machine'))
            if fa.alphabet != self.alphabet:
                fail(qid, 'machines over different alphabets')
            self.dfa = fa.dfa()
            self.member = fa.accepts
        elif 'member' in src:
            expr = src['member']
            self.member = lambda w: bool(_ev(qid, expr, w=w))
        else:
            fail(qid, f'unknown language {src}')
        if 'rule' in src:
            self.rule = RuleDFA(qid, src['rule'], self.alphabet)
            self.dfa = self.rule.dfa
        if src.get('complement'):
            m = self.member
            self.member = lambda w: not m(w)
            if self.dfa:
                self.dfa = self.dfa.complement()
        if not self.text:
            fail(qid, f'language {src} needs a "text" to show')
        if self.dfa:  # the construction and the independent membership test must agree
            for w in words(self.alphabet, maxlen(len(self.alphabet))):
                if self.dfa.accepts(w) != self.member(w):
                    fail(qid, f'the construction of {self.text} disagrees with its membership test on {show(w)}')


class RuleDFA:
    """States built by an update rule: start, next (in s and c), accept (in s), name and pos (in s)."""

    def __init__(self, qid, rule, alphabet):
        start = _ev(qid, rule['start'])
        nxt = lambda s, c: _ev(qid, rule['next'], s=s, c=c)
        self.order = reach_order(start, alphabet, nxt)
        if len(self.order) > 60:
            fail(qid, 'the rule gives too many states to draw')
        self.delta = {(s, c): nxt(s, c) for s in self.order for c in alphabet}
        self.final = {s for s in self.order if _ev(qid, rule['accept'], s=s)}
        self.dfa = DFA(self.order, alphabet, start, self.final, self.delta)
        names = [str(_ev(qid, rule['name'], s=s)) if 'name' in rule else f'q{i}' for i, s in enumerate(self.order)]
        if len(set(names)) != len(names):
            fail(qid, 'the rule gives two states the same name')
        self.name = dict(zip(self.order, names))
        self.pos = {self.name[s]: list(_ev(qid, rule['pos'], s=s)) for s in self.order} if 'pos' in rule else rule.get('layout')

    def fa(self, qid, alphabet):
        edges = [[self.name[s], c, self.name[self.delta[(s, c)]]] for s in self.order for c in alphabet]
        return FA(qid, dict(states=[self.name[s] for s in self.order], start=self.name[self.order[0]],
                            final=[self.name[s] for s in self.order if s in self.final], alphabet=alphabet,
                            edges=edges, pos=self.pos))


def dfa_to_fa(qid, dfa, names=None):
    order = reach_order(dfa.start, dfa.alphabet, lambda s, c: dfa.delta[(s, c)])
    names = names or {s: f'q{i}' for i, s in enumerate(order)}
    edges = [[names[s], c, names[dfa.delta[(s, c)]]] for s in order for c in dfa.alphabet]
    return FA(qid, dict(states=[names[s] for s in order], start=names[order[0]], final=[names[s] for s in order if s in dfa.final],
                        alphabet=dfa.alphabet, edges=edges))


def minimal_dfa(qid, dfa):
    """The minimal DFA as an FA, its states named q0, q1, … in breadth-first order."""
    order = reach_order(dfa.start, dfa.alphabet, lambda s, c: dfa.delta[(s, c)])
    hist = refine(order, dfa.alphabet, lambda s, c: dfa.delta[(s, c)], lambda s: s in dfa.final)
    blocks = hist[-1]['blocks']
    bid = {s: i for i, b in enumerate(blocks) for s in b}
    q = DFA(range(len(blocks)), dfa.alphabet, bid[dfa.start], {bid[s] for s in dfa.final if s in bid},
            {(bid[b[0]], c): bid[dfa.delta[(b[0], c)]] for b in blocks for c in dfa.alphabet})
    return dfa_to_fa(qid, q)


def compare(qid, fa_or_dfa, member, lang, rel):
    """Decide L(machine) rel L for rel in eq, sub (⊆), sup (⊇), psub (⊊). Returns (holds, witness, side)
    where the witness is a shortest string breaking the relation and side says which language has it."""
    dfa = fa_or_dfa if isinstance(fa_or_dfa, DFA) else fa_or_dfa.dfa()
    bads = {'eq': lambda a, b: a != b, 'sub': lambda a, b: a and not b, 'sup': lambda a, b: b and not a}
    n = maxlen(len(dfa.alphabet))

    def brute(bad):
        for w in words(dfa.alphabet, n):
            if bad(member(w), lang.member(w)):
                return w
        return None

    def decide(bad):
        w = dfa.witness(lang.dfa, bad) if lang.dfa else brute(bad)
        if w is None and lang.dfa is None:
            fail(qid, 'bounded enumeration cannot prove a language relation; supply an exact construction')
        if lang.dfa and (w is None) != (brute(bad) is None) and len(w or '') <= n:
            fail(qid, 'the exact and brute-force language checks disagree')
        return w

    if rel == 'psub':
        w = decide(bads['sub'])
        if w is not None:
            return False, w, 'machine'
        extra = decide(lambda a, b: b and not a)
        return extra is not None, extra, 'other'
    w = decide(bads[rel])
    return w is None, w, (None if w is None else ('machine' if member(w) else 'other'))


# ---------------------------------------------------------------- layout

def layout(qid, states, start, edges, pos):
    """Drawing positions: given, on a circle, or in breadth-first columns from the start (folded after five)."""
    if isinstance(pos, dict):
        if set(pos) != set(states):
            fail(qid, 'pos must place every state exactly once')
        return {s: list(map(float, pos[s])) for s in states}
    if pos == 'circle':
        n = len(states)
        return {s: [round(math.sin(2 * math.pi * k / n), 3), round(-math.cos(2 * math.pi * k / n), 3)] for k, s in enumerate(states)}
    if pos not in (None, 'layers'):
        fail(qid, f'unknown layout {pos}')
    start = start or states[0]
    depth, todo = {start: 0}, deque([start])
    while todo:
        s = todo.popleft()
        for u, v, _ in edges:
            if u == s and v not in depth:
                depth[v] = depth[s] + 1
                todo.append(v)
    last = max(depth.values()) + 1
    for s in states:
        depth.setdefault(s, last)
    cols = sorted(set(depth.values()))
    col = {d: i for i, d in enumerate(cols)}
    tall = max(sum(1 for s in states if depth[s] == d) for d in cols)
    out, width = {}, 5
    for d in cols:
        members = [s for s in states if depth[s] == d]
        k = col[d]
        band, x = divmod(k, width)
        if band % 2:
            x = width - 1 - x
        for j, s in enumerate(members):
            out[s] = [float(x), band * (tall + 0.6) + j - (len(members) - 1) / 2]
    return out


# ---------------------------------------------------------------- steps

def step(note, head=None, **kw):
    s = dict(note=note)
    if head:
        s['head'] = head
    for k, v in kw.items():
        if v is not None and v != {} and v != []:
            s[k] = v
    return s


def schedule(short, title, fa, steps, legend=None):
    steps[-1]['final'] = True
    out = dict(short=short, title=title, fa=fa, steps=steps)
    if legend:
        out['legend'] = legend
    return out


def done(kind, schedules, **extra):
    return dict(kind=kind, schedules=schedules, count=sum(len(s['steps']) for s in schedules), **extra)


def tape(w, pos, out=None):
    t = dict(sym=list(w) if w else [], pos=pos)
    if out is not None:
        t['out'] = out
    return t


LEGEND_RUN = [['n-now', 'current state'], ['e-now', 'move just taken'], ['n-acc', 'accepting (double ring)']]


def run_steps(fa, w, frm=None, verdict=True, extra_note=''):
    """Step through fa on w, one symbol at a time. Returns (steps, final set)."""
    steps = []
    S0 = {frm or fa.start}
    S, eps = fa.closure(S0)
    rows = [['start', '', fa.fmt(S)]]

    def table():
        return dict(head=['Read', 'Symbol', 'Now in' if not fa.det else 'State'], rows=[list(r) for r in rows], now=[len(rows) - 1])

    who = fa.who([next(iter(S0))])
    if S == frozenset(S0):
        note = f"Start in {who}." if fa.det or not fa.eps else f"Start in {who}; it has no ε-moves."
    else:
        note = f"Start in {who}. Its ε-moves also reach {fa.who(fa.order(S - S0))}, so the machine can be in {fa.fmt(S)}."
    steps.append(step(note + (f" Input: {show(w)}." if w else ''), 'Start', n={s: 'now' for s in S}, e={str(i): 'eps' for i in eps}, tape=tape(w, -1), table=table()))
    for i, c in enumerate(w):
        T, used = fa.move(S, c)
        C, eps = fa.closure(T)
        parts = []
        for s in fa.order(S):
            ts = fa.delta.get((s, c), [])
            parts.append(f"{fa.who([s])} goes to {fa.who(ts)}" if ts else f"{fa.who([s])} has no move on {c}")
        if fa.det:
            note = f"Read {c}: " + (f"{fa.who(fa.order(S))} goes to {fa.who(fa.order(C))}." if C else f"{parts[0]}, so the machine is stuck and the input is rejected.") if S else f"Read {c}: no state is active."
        else:
            note = f"Read {c}: " + '; '.join(parts) + '.'
            if C != T:
                note += f" ε-moves add {_list(fa.order(C - T))}."
            note += f" Now {fa.fmt(C)}." if C else " No state is active any more, so the input is rejected."
        rows.append([str(i + 1), c, fa.fmt(C) if not fa.det else (fa.order(C)[0] if C else '∅')])
        ecls = {str(j): 'now' for j in used}
        ecls.update({str(j): 'eps' for j in eps if str(j) not in ecls})
        steps.append(step(note, f'Symbol {i + 1} of {len(w)}', n={s: 'now' for s in C}, e=ecls, tape=tape(w, i), table=table()))
        S = C
        if not S:
            break
    acc = [s for s in fa.order(S) if s in fa.final]
    if verdict:
        if fa.det or len(S) <= 1:
            v = (f"It ends in {fa.who(fa.order(S))}, " + ("an accepting state, so " + show(w) + " is accepted." if acc else "which is not accepting, so " + show(w) + " is rejected.")) if S else f"So {show(w)} is rejected."
        else:
            v = f"It ends in {fa.fmt(S)}, " + (f"which includes the accepting {_list(acc)}, so {show(w)} is accepted." if acc else f"with no accepting state, so {show(w)} is rejected.")
        steps[-1]['note'] += ' ' + v + extra_note
    return steps, S


# ---------------------------------------------------------------- kinds

def run_animation(qid, spec):
    """Run a machine on given strings; each run checks the final set of states or acceptance."""
    fa = FA(qid, spec['machine'])
    if fa.mealy:
        fail(qid, 'use fa-mealy for a Mealy machine')
    draw = fa.draw()
    scheds = []
    for r in spec['runs']:
        w, frm = r['input'], r.get('from')
        if frm is not None and frm not in fa.states:
            fail(qid, f'run from unknown state {frm}')
        steps, S = run_steps(fa, w, frm, verdict=frm is None)
        want = r['expect']
        if 'states' in want:
            check(qid, f'the states after {show(w)}', fa.order(S), fa.order(set(want['states'])))
            if not set(want['states']) <= set(fa.states):
                fail(qid, 'expected states contain an unknown state')
            if len(set(want['states'])) != len(want['states']):
                fail(qid, 'expected states repeat')
        if 'accept' in want:
            check(qid, f'acceptance of {show(w)}', bool(S & set(fa.final)), want['accept'])
        if frm is not None:
            steps[-1]['note'] += f" So from {frm}, reading {show(w)} can end in exactly {fa.fmt(S)}."
        title = f"Reading {show(w)}" + (f" from {frm}" if frm else '') + (" (sets of states, as for an NFA)" if not fa.det else '')
        scheds.append(schedule(show(w), title, draw, steps, LEGEND_RUN))
    return done('fa-run', scheds)


def count_animation(qid, spec):
    """Count the strings of one length (some positions fixed) that a DFA accepts, by counting how many reach each state."""
    fa = FA(qid, spec['machine'])
    if not fa.det:
        fail(qid, 'counting needs a DFA')
    n = int(spec['length'])
    fixed = {int(k): str(v) for k, v in spec.get('fixed', {}).items()}
    for k, v in fixed.items():
        if not 1 <= k <= n or v not in fa.alphabet:
            fail(qid, f'bad fixed position {k}={v}')
    cnt = {fa.start: 1}
    rows = [['0', ''] + [str(cnt.get(s, 0)) for s in fa.states]]
    head = ['After', 'Symbol'] + fa.states

    def tbl():
        return dict(head=head, rows=[list(r) for r in rows], now=[len(rows) - 1])

    steps = [step(f"One string, the empty one, is in {fa.start} before anything is read. "
                  f"We follow all {math.prod(1 if k in fixed else len(fa.alphabet) for k in range(1, n + 1))} strings at once, counting how many are in each state.",
                  'Start', n={fa.start: 'now'}, tag={fa.start: '1'}, table=tbl())]
    for k in range(1, n + 1):
        allowed = [fixed[k]] if k in fixed else fa.alphabet
        new, used = {}, set()
        for s in fa.states:
            if cnt.get(s):
                for c in allowed:
                    if (s, c) in fa.delta:
                        t = fa.nxt(s, c)
                        new[t] = new.get(t, 0) + cnt[s]
                        used.add(fa.eidx[(s, t)])
        cnt = new
        rows.append([str(k), '/'.join(allowed)] + [str(cnt.get(s, 0)) for s in fa.states])
        live = [f"{cnt[s]} in {s}" for s in fa.states if cnt.get(s)]
        what = f"Symbol {k} must be {allowed[0]}" if k in fixed else f"Symbol {k} can be {' or '.join(allowed)}"
        steps.append(step(f"{what}. Each count moves along its {'edge' if len(allowed) == 1 else 'edges'}: now {_list(live)}.",
                          f'Symbol {k} of {n}', n={s: 'now' for s in cnt if cnt[s]}, e={str(i): 'now' for i in sorted(used)},
                          tag={s: str(v) for s, v in cnt.items() if v}, table=tbl()))
    total = sum(v for s, v in cnt.items() if s in fa.final)
    # Independent check: run every string of the shape.
    shape = [[fixed[k]] if k in fixed else fa.alphabet for k in range(1, n + 1)]
    acc = [''.join(t) for t in _cartesian(*shape) if fa.accepts(''.join(t))]
    check(qid, 'the brute-force count', len(acc), total)
    check(qid, 'the number of accepted strings', total, spec['expect']['count'])
    fin = [s for s in fa.final if cnt.get(s)]
    note = f"The accepting {'state' if len(fa.final) == 1 else 'states'} {_list(fa.final)} {'holds' if len(fin) <= 1 else 'hold'} {total} of the strings, so {total} are accepted."
    line = [f"Accepted: {', '.join(acc)}"] if len(acc) <= 16 else None
    steps[-1]['note'] += ' ' + note
    if line:
        steps[-1]['line'] = line
    return done('fa-count', [schedule('count', f"Count the accepted strings of length {n}", fa.draw(), steps,
                                      [['n-now', 'reached by some strings'], ['e-now', 'edges used'], ['n-acc', 'accepting (double ring)']])])


def subset_animation(qid, spec):
    """The subset construction for an NFA, then a check of the language it shows."""
    fa = FA(qid, spec['machine'])
    order, trans = fa.subsets()
    F = set(fa.final)
    names = {S: fa.fmt(S) for S in order}
    rows, steps = [], []
    head = ['DFA state'] + [f'on {c}' for c in fa.alphabet] + ['Accepting?']
    S0, eps = fa.closure({fa.start})
    note = f"The DFA starts in the set of states the NFA can be in before reading anything: {names[S0]}" + \
        (f" ({fa.start} and what its ε-moves reach)." if len(S0) > 1 else '.')
    steps.append(step(note, 'Start', n={s: 'now' for s in S0}, e={str(i): 'eps' for i in eps},
                      table=dict(head=head, rows=[[names[S0]] + [''] * len(fa.alphabet) + ['']], now=[0])))
    seen = [S0]
    for S in order:
        parts, ecls = [], {}
        for c in fa.alphabet:
            T = trans[(S, c)]
            _, used = fa.move(S, c)
            _, eu = fa.closure(fa.move(S, c)[0])
            for i in used:
                ecls[str(i)] = 'now'
            for i in eu:
                ecls.setdefault(str(i), 'eps')
            fresh = T not in seen
            if fresh:
                seen.append(T)
            parts.append(f"on {c} to {names[T]}" + (' (new)' if fresh else ''))
        rows.append([names[S]] + [names[trans[(S, c)]] for c in fa.alphabet] + ['yes' if S & F else 'no'])
        pend = [[names[T]] + [''] * len(fa.alphabet) + [''] for T in seen if T not in order[:len(rows)]]
        acc = f"It contains the accepting {_list(fa.order(S & F))}, so it is accepting." if S & F else "It contains no accepting state."
        steps.append(step(f"From {names[S]}: " + ', '.join(parts) + '. ' + acc, f'Row {len(rows)}',
                          n={s: 'now' for s in S}, e=ecls, table=dict(head=head, rows=[list(r) for r in rows] + pend, now=[len(rows) - 1])))
    want = spec['expect']
    dfa = DFA(order, fa.alphabet, order[0], {S for S in order if S & F}, trans)
    if 'count' in want:
        check(qid, 'the number of subset states', len(order), want['count'])
    msg = f"The DFA has {len(order)} states."
    for key in ('language', 'complement'):
        if key in want:
            lang = Lang(qid, want[key], fa.alphabet)
            target = dfa if key == 'language' else dfa.complement()
            ok, w, _ = compare(qid, target, target.accepts, lang, 'eq')
            if not ok:
                fail(qid, f'the {key} is not {lang.text}: {show(w)} differs')
            rej = [names[S] for S in order if not S & F]
            if key == 'language':
                msg += (" Every one of them is accepting, so every string is accepted" if not rej else
                        f" Only {_list(rej)} {'is' if len(rej) == 1 else 'are'} not accepting") + f": the language is {lang.text}."
            else:
                msg += (f" Only {_list(rej)} {'is' if len(rej) == 1 else 'are'} not accepting" if rej else " All of them are accepting") + \
                    f", so the complement (the strings that end there) is {lang.text}."
    steps[-1]['note'] += ' ' + msg
    return done('fa-subset', [schedule('subsets', 'Subset construction: each DFA state is a set of NFA states', fa.draw(), steps,
                                       [['n-now', 'states in the current set'], ['e-now', 'moves on a symbol'], ['e-eps', 'ε-moves']])])


def roman(i):
    """Group numbers as Roman numerals, so they never look like state names."""
    n, out = i + 1, ''
    for v, r in ((50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v:
            out, n = out + r, n - v
    return out


def cap(text):
    return text[:1].upper() + text[1:]


def group_name(states):
    return '{' + ', '.join(states) + '}'


def refine_steps(fa, steps, label='DFA'):
    """Partition refinement on a complete DFA or Mealy machine; appends steps, returns the final groups."""
    if not fa.complete:
        fail(fa.qid, 'minimisation needs a complete machine')
    states = fa.states if fa.mealy else fa.reachable()
    if not fa.mealy and len(states) < len(fa.states):
        gone = [s for s in fa.states if s not in states]
        steps.append(step(f"{_list(gone)} cannot be reached from the start state {fa.start}, so {'it is' if len(gone) == 1 else 'they are'} dropped first.",
                          'Unreachable', n={s: 'off' for s in gone}))
    key = (lambda s: tuple(fa.out[(s, c)] for c in fa.alphabet)) if fa.mealy else (lambda s: s in fa.final)
    hist = refine(states, fa.alphabet, fa.nxt, key)
    syms = fa.alphabet

    def table(h, now=()):
        blocks = h['blocks']
        bid = {s: i for i, b in enumerate(blocks) for s in b}
        sig = h['sig']
        head = ['State', 'Group'] + [f'on {c}' for c in syms] + (['Outputs'] if fa.mealy else [])
        rows, cls = [], []
        for b in blocks:
            for s in b:
                r = [s, roman(bid[s])] + ([f'→ {fa.nxt(s, c)} ({roman(sig[s][k])})' for k, c in enumerate(syms)] if sig else [''] * len(syms))
                if fa.mealy:
                    r.append(', '.join(fa.out[(s, c)] for c in syms))
                rows.append(r)
                cls.append(bid[s] % 6)
        return dict(head=head, rows=rows, group=cls, now=[k for k, r in enumerate(rows) if r[0] in now])

    def colours(blocks):
        return {s: f'g{i % 6}' for i, b in enumerate(blocks) for s in b}

    h0 = hist[0]
    if fa.mealy:
        parts = [f"outputs ({', '.join(k)}) for {_list(b)}" for k, b in zip(h0['keys'], h0['blocks'])]
        note = f"Start by grouping states with the same outputs on inputs {', '.join(syms)}: " + '; '.join(parts) + '.'
    else:
        acc = [b for b, k in zip(h0['blocks'], h0['keys']) if k]
        rej = [b for b, k in zip(h0['blocks'], h0['keys']) if not k]
        note = "Start with two groups: " + (f"accepting {group_name(acc[0])}" if acc else "no accepting state") + ' and ' + \
            (f"non-accepting {group_name(rej[0])}" if rej else "no non-accepting state") + '.'
        if not acc or not rej:
            note = "Every reachable state is " + ('accepting' if acc else 'non-accepting') + ", so they all start in one group."
    steps.append(step(note, 'Round 0', n=colours(h0['blocks']), table=table(dict(blocks=h0['blocks'], sig=h0['sig']))))
    for r in range(1, len(hist)):
        h, prev = hist[r], hist[r - 1]
        texts = []
        for i, ps in h['splits'][:3]:
            sig = prev['sig']
            c = next(k for k in range(len(syms)) if len({sig[p[0]][k] for p in ps}) > 1)
            into = lambda p: f"{fa.who(p)} {'goes' if len(p) == 1 else 'go'} into group {roman(sig[p[0]][c])} {group_name(prev['blocks'][sig[p[0]][c]])}"
            texts.append(f"Group {roman(i)} {group_name(prev['blocks'][i])} splits: on {syms[c]}, " + ', but '.join(into(p) for p in ps))
        more = len(h['splits']) - 3
        note = ' '.join(t + '.' for t in texts) + (f" {more} more {'group splits' if more == 1 else 'groups split'} the same way." if more > 0 else '')
        moved = [s for _, ps in h['splits'] for p in ps[1:] for s in p]
        steps.append(step(note, f'Round {r}', n=colours(h['blocks']), table=table(dict(blocks=h['blocks'], sig=prev['sig']), moved)))
    last = hist[-1]
    blocks = last['blocks']
    steps.append(step(f"Check again with the new groups: every state in a group still moves to the same groups and "
                      f"{'gives the same outputs' if fa.mealy else 'agrees on acceptance'}, so nothing splits. "
                      f"The minimal {label} has {len(blocks)} state{'s' if len(blocks) != 1 else ''}" +
                      (': ' + ', '.join(group_name(b) for b in sorted(blocks, key=lambda b: states.index(b[0]))) + '.' if len(blocks) < len(states) else
                       ', one for each state: no two states can merge.'),
                      'Stable', n=colours(blocks), table=table(last)))
    return blocks


LEGEND_REFINE = [['n-g0', 'colour = group'], ['n-acc', 'accepting (double ring)']]


def _differ(fa):
    if fa.mealy:
        return lambda a, b, c: c is not None and fa.out[(a, c)] != fa.out[(b, c)]
    return lambda a, b, c: c is None and ((a in fa.final) != (b in fa.final))


def product_fa(qid, spec):
    ms = [FA(qid, m, f'machine {k + 1}') for k, m in enumerate(spec['machines'])]
    if len(ms) != 2 or ms[0].alphabet != ms[1].alphabet or not all(m.complete for m in ms):
        fail(qid, 'a product needs two complete DFAs over one alphabet')
    op = spec['op']
    if op not in ('and', 'or'):
        fail(qid, f'unknown product {op}')
    a, b = ms
    start = (a.start, b.start)
    order = reach_order(start, a.alphabet, lambda p, c: (a.nxt(p[0], c), b.nxt(p[1], c)))
    nm = lambda p: f'{p[0]}{p[1]}' if all(len(x) == 1 for x in p) else f'{p[0]},{p[1]}'
    fin = [nm(p) for p in order if (p[0] in a.final and p[1] in b.final) if op == 'and'] if op == 'and' else \
        [nm(p) for p in order if p[0] in a.final or p[1] in b.final]
    edges = [[nm(p), c, nm((a.nxt(p[0], c), b.nxt(p[1], c)))] for p in order for c in a.alphabet]
    fa = FA(qid, dict(states=[nm(p) for p in order], start=nm(start), final=fin, alphabet=a.alphabet, edges=edges, pos=spec.get('pos')), 'the product')
    return fa, ms, order, nm


def refine_animation(qid, spec):
    """Minimise a DFA, a product of two DFAs, or a Mealy machine by partition refinement."""
    steps = []
    if 'product' in spec:
        fa, ms, order, nm = product_fa(qid, spec['product'])
        op, names = spec['product']['op'], spec['product']['names']
        steps.append(step(f"Run {names[0]} and {names[1]} together. A product state such as {fa.start} means {names[0]} is in {order[0][0]} and {names[1]} is in {order[0][1]}; it is the start. "
                          f"It is accepting when {'both are' if op == 'and' else 'either is'} accepting.", 'Product', n={fa.start: 'now'}))
        for p in order:
            parts = [f"on {c} to {nm((ms[0].nxt(p[0], c), ms[1].nxt(p[1], c)))}" for c in fa.alphabet]
            steps.append(step(f"From {nm(p)} ({names[0]} in {p[0]}, {names[1]} in {p[1]}): " + ', '.join(parts) + '.',
                              f'Product state {order.index(p) + 1} of {len(order)}', n={nm(p): 'now'},
                              e={str(fa.eidx[(nm(p), nm((ms[0].nxt(p[0], c), ms[1].nxt(p[1], c))))]): 'now' for c in fa.alphabet}))
        steps[-1]['note'] += ' ' + (f"Only {_list(fa.final)} {'is' if len(fa.final) == 1 else 'are'} accepting." if fa.final else
                                    f"No reachable pair has both {names[0]} and {names[1]} accepting, so no string is accepted." if op == 'and' else "No reachable pair is accepting.")
    else:
        fa = FA(qid, spec['machine'])
    blocks = refine_steps(fa, steps, label='Mealy machine' if fa.mealy else 'DFA')
    want = spec['expect']
    if 'count' in want:
        check(qid, 'the number of states after minimising', len(blocks), want['count'])
    if 'blocks' in want:
        check(qid, 'the groups of equivalent states', sorted(sorted(b) for b in blocks), sorted(sorted(map(str, b)) for b in want['blocks']))
    bid = {s: i for i, b in enumerate(blocks) for s in b}
    bname = [''.join(b) if all(len(s) == 1 for s in b) else group_name(b) for b in blocks]
    extra = []
    if 'quotient' in want:
        got = {bname[i]: [f"{bname[bid[fa.nxt(b[0], c)]]}/{fa.out[(b[0], c)]}" if fa.mealy else bname[bid[fa.nxt(b[0], c)]] for c in fa.alphabet]
               for i, b in enumerate(blocks)}
        check(qid, 'the reduced table', got, want['quotient'])
        extra.append(dict(head=['State'] + [f'on {c}' for c in fa.alphabet], rows=[[k] + v for k, v in got.items()]))
        steps[-1]['note'] += " Naming each group by its members and replacing every next state by its group gives the reduced table."
    if 'equivalent' in want:
        other = FA(qid, want['equivalent'], 'the offered machine')
        ok, w, _ = compare(qid, fa, fa.accepts, Lang(qid, dict(machine=want['equivalent'], text='the offered machine'), fa.alphabet), 'eq')
        if not ok:
            fail(qid, f'the offered machine differs on {show(w)}')
        n_other = DFA(*_complete(other)).minimal_size()
        check(qid, 'the size of the offered machine', (len(other.states), n_other), (len(blocks), len(blocks)))
        steps[-1]['note'] += f" The offered machine with {len(other.states)} states accepts the same strings, so it is an equivalent minimal DFA."
    if extra:
        steps[-1]['table2'] = extra[0]
    title = ('Minimise the product machine' if 'product' in spec else 'Minimise the Mealy machine' if fa.mealy else 'Minimise the DFA') + ' by splitting groups until stable'
    return done('fa-refine', [schedule('groups', title, fa.draw(), steps, LEGEND_REFINE)])


def _walk(fa, s, w):
    for c in w:
        s = fa.nxt(s, c)
    return s


def _complete(fa):
    """A machine with missing moves sent to a dead state, as DFA arguments."""
    if not fa.det:
        d = fa.dfa()
        return d.states, d.alphabet, d.start, d.final, d.delta
    dead = '∅'
    delta = {(s, c): fa.delta[(s, c)][0] if (s, c) in fa.delta else dead for s in fa.states for c in fa.alphabet}
    states = list(fa.states)
    if dead in delta.values():
        states.append(dead)
        delta.update({(dead, c): dead for c in fa.alphabet})
    return states, fa.alphabet, fa.start, set(fa.final), delta


def has_dead(fa):
    return any(s not in fa.final and all(fa.nxt(s, c) == s for c in fa.alphabet) for s in fa.states)


def language_animation(qid, spec):
    """The minimal DFA of a stated language: build it state by state, then confirm no two states merge."""
    alphabet = [str(c) for c in spec['alphabet']]
    lang = Lang(qid, spec['lang'], alphabet)
    want = spec['expect']
    if hasattr(lang, 'rule'):
        fa = lang.rule.fa(qid, alphabet)
    elif lang.dfa:
        fa = minimal_dfa(qid, lang.dfa)
        if spec.get('pos'):
            fa.pos = spec['pos']
    else:
        fail(qid, 'a language needs a regex or a rule to build its DFA')
    ok, w, _ = compare(qid, fa, fa.accepts, lang, 'eq')
    if not ok:
        fail(qid, f'the DFA does not accept exactly {lang.text}: {show(w)} differs')
    if 'dfa' in want:
        offered = Lang(qid, dict(machine=want['dfa'], text='the recorded DFA'), alphabet)
        if lang.dfa.witness(offered.dfa, lambda a, b: a != b) is not None:
            fail(qid, 'the computed DFA differs from the recorded DFA')
    # Breadth-first: name each state by the first string that reaches it.
    reach = {fa.start: ''}
    order, todo = [fa.start], deque([fa.start])
    build, rows = [], []
    head = ['State', 'Reached by'] + [f'on {c}' for c in alphabet] + ['Accepting?']
    tbl = lambda now: dict(head=head, rows=[list(r) for r in rows], now=now)
    build.append(step(f"Start in {fa.start}, the state for the empty string. " +
                      ("It is accepting: ε is in the language." if fa.start in fa.final else "It is not accepting: ε is not in the language."),
                      'Start', n={fa.start: 'now'}, table=dict(head=head, rows=[[fa.start, 'ε'] + [''] * len(alphabet) + ['yes' if fa.start in fa.final else 'no']], now=[0])))
    while todo:
        s = todo.popleft()
        parts, ecls = [], {}
        for c in alphabet:
            t = fa.nxt(s, c)
            ecls[str(fa.eidx[(s, t)])] = 'now'
            x = reach[s] + c
            if t not in reach:
                reach[t] = x
                order.append(t)
                todo.append(t)
                parts.append(f"{c} leads to a new state {t} (first reached by {x})")
            elif t == s:
                parts.append(f"{c} stays in {s}")
            else:
                parts.append(f"{c} leads to {t}, since {x} behaves like {show(reach[t])}")
        rows.append([s, show(reach[s])] + [fa.nxt(s, c) for c in alphabet] + ['yes' if s in fa.final else 'no'])
        pend = [[t, show(reach[t])] + [''] * len(alphabet) + ['yes' if t in fa.final else 'no'] for t in order[len(rows):]]
        build.append(step(f"From {s} ({'the start' if s == fa.start else 'after ' + reach[s]}): " + '; '.join(parts) + '.', f'State {len(rows)} of {len(fa.states)}',
                          n={s: 'now'}, e=ecls, table=dict(head=head, rows=[list(r) for r in rows] + pend, now=[len(rows) - 1])))
    unreach = [s for s in fa.states if s not in reach]
    if unreach:
        fail(qid, f'the DFA has unreachable states {unreach}')
    build[-1]['note'] += f" Every move is now filled in: {len(fa.states)} states."
    check_steps = []
    blocks = refine_steps(fa, check_steps)
    n = len(blocks)
    if 'count' in want:
        if has_dead(fa) and n == len(fa.states) and spec.get('dead') != 'counted':
            fail(qid, 'the minimal DFA has a dead state; say "dead": "counted" only if the question asks for a complete DFA')
        check(qid, 'the number of states of the minimal DFA', n, want['count'])
        check(qid, 'the minimal-DFA size from the exact construction', lang.dfa.minimal_size() if lang.dfa else n, n)
    dead = [s for s in fa.states if s not in fa.final and all(fa.nxt(s, c) == s for c in alphabet)]
    check_steps[-1]['note'] += (f" This count includes the dead state {dead[0]}, which the question's complete DFA must have." if dead and 'count' in want else '')
    title = f"Build a DFA for {lang.text}"
    return done('fa-language', [schedule('build', title, fa.draw(), build, [['n-now', 'state being filled in'], ['e-now', 'its moves'], ['n-acc', 'accepting (double ring)']]),
                                schedule('minimal?', 'Can any two states merge? Split groups until stable', fa.draw(), check_steps, LEGEND_REFINE)],
                tabs_label='parts')


def pick(alphabet, pred):
    """A short example: the first string of length 3 or more with pred, else the first nonempty one."""
    xs = [x for x in words(alphabet, 6 if len(alphabet) <= 2 else 4) if x and pred(x)]
    return next((x for x in xs if len(x) >= 3), xs[0] if xs else None)


def claims_animation(qid, spec):
    """Statements about a machine: language comparisons (with a shortest counterexample traced),
    minimality and distinguishability (by partition refinement)."""
    base = FA(qid, spec['machine']) if 'machine' in spec else None
    scheds = []
    for cl in spec['claims']:
        test, label = cl['test'], cl['label']
        if 'machine' in test:
            fa = FA(qid, test['machine'], f'machine {label}')
        elif 'add' in test:
            m = dict(spec['machine'])
            m['edges'] = list(m['edges']) + test['add']
            fa = FA(qid, m, f'machine {label}')
        else:
            fa = base
        draw = fa.draw()
        text = cl['text']
        if 'lang' in test:
            lang = Lang(qid, test['lang'], fa.alphabet)
            rel = test.get('rel', 'eq')
            ok, w, side = compare(qid, fa, fa.accepts, lang, rel)
            told = lang.text.startswith('the ')  # a language described in words, not an expression
            isin = lambda x, yes: f"{show(x)} is {'' if yes else 'not '}{'one of' if told else 'in'} {lang.text}"
            how = '' if lang.dfa else f" (checked on every string up to length {maxlen(len(fa.alphabet))})"
            if ok:
                sample = pick(fa.alphabet, lang.member if rel == 'sup' else fa.accepts)
                steps, _ = run_steps(fa, sample) if sample is not None else ([step('The machine accepts no nonempty string.', 'Start', n={fa.start: 'now'})], None)
                if sample is not None:
                    steps[0]['note'] = f"For example, {isin(sample, True)}. " + steps[0]['note']
                concl = {'eq': (f"The machine accepts exactly {lang.text}{how}." if told else
                                f"No string separates the machine from {lang.text}{how}: they describe the same language."),
                         'sub': f"Every string the machine accepts is {'one of' if told else 'in'} {lang.text}{how}.",
                         'sup': f"Every string {'that is one of' if told else 'in'} {lang.text} is accepted{how}.",
                         'psub': f"Every accepted string is {'one of' if told else 'in'} {lang.text}, and {isin(w, True)} but is not accepted."}[rel]
                steps.append(step(concl + f" So statement {label} is true.", 'Verdict'))
            elif w is None:  # a proper-subset claim between equal languages
                steps, _ = run_steps(fa, pick(fa.alphabet, fa.accepts) or '')
                steps.append(step(f"The machine accepts exactly {lang.text}, so it is not a proper subset. Statement {label} is false.", 'Verdict'))
            else:
                steps, _ = run_steps(fa, w)
                acc, inl = fa.accepts(w), lang.member(w)
                steps.append(step(f"The machine {'accepts' if acc else 'rejects'} {show(w)}, but {isin(w, inl)}. So statement {label} is false.", 'Verdict'))
            check(qid, f'statement {label}', ok, cl['expect'])
            scheds.append(schedule(label, text, draw, steps, LEGEND_RUN))
            continue
        if 'minimal' in test or 'distinct' in test:
            steps = []
            blocks = refine_steps(fa, steps)
            bid = {s: i for i, b in enumerate(blocks) for s in b}
            if 'minimal' in test:
                ok = len(blocks) == len(fa.states)
                steps[-1]['note'] += f" The machine has {len(fa.states)} states, so it {'is' if ok else 'is not'} minimal. Statement {label} is {'true' if ok == test['minimal'] else 'false'}."
                ok = ok == test['minimal']
            else:
                p, q = map(str, test['distinct'])
                d = bid[p] != bid[q]
                if d:
                    w = separate(fa.nxt, fa.alphabet, p, q, _differ(fa))
                    a, b = _walk(fa, p, w), _walk(fa, q, w)
                    steps[-1]['note'] += f" {cap(fa.who([p, q]))} end in different groups: after {show(w)}, {fa.who([p])} reaches {fa.who([a])} and {fa.who([q])} reaches {fa.who([b])}, and only {fa.who([a if a in fa.final else b])} is accepting."
                else:
                    steps[-1]['note'] += f" {cap(fa.who([p, q]))} end in the same group, so no string tells them apart."
                ok = d == test.get('want', True)
                steps[-1]['note'] += f" Statement {label} is {'true' if ok else 'false'}."
            check(qid, f'statement {label}', ok, cl['expect'])
            scheds.append(schedule(label, text, draw, steps, LEGEND_REFINE))
            continue
        if 'complement_regular' in test:
            steps = [step(f"Swap accepting and non-accepting states of this complete DFA: {_list([s for s in fa.states if s not in fa.final])} become accepting.", 'Complement',
                          n={s: 'now' for s in fa.states if s not in fa.final})]
            if not fa.complete:
                fail(qid, 'complementing by swapping needs a complete DFA')
            comp = fa.dfa().complement()
            for x in words(fa.alphabet, 8):
                if comp.accepts(x) == fa.accepts(x):
                    fail(qid, 'the swapped machine is not the complement')
            steps.append(step(f"The new DFA accepts exactly the strings the old one rejects, so the complement is regular, and every regular language is context-free. Statement {label} is true.", 'Verdict'))
            check(qid, f'statement {label}', True, cl['expect'])
            scheds.append(schedule(label, text, draw, steps))
            continue
        fail(qid, f'unknown claim test {test}')
    return done('fa-claims', scheds, tabs_label=spec.get('tabs', 'statements'))


def mealy_trace(fa, w, steps, expected=None):
    outs, path = fa.outputs(w)
    rows = []
    head = ['Step', 'State', 'In', 'Out', 'Next']
    steps.append(step(f"Start in {fa.start}. Input: {w}.", 'Start', n={fa.start: 'now'}, tape=tape(w, -1, [])))
    for i, c in enumerate(w):
        s, t, o = path[i], path[i + 1], outs[i]
        rows.append([str(i + 1), s, c, o, t])
        note = f"In {s}, input {c} outputs {o} and moves to {t}."
        if expected is not None and expected[i] != o:
            note += f" The required output here is {expected[i]}."
        steps.append(step(note, f'Input {i + 1} of {len(w)}', n={t: 'now'}, e={str(fa.eidx[(s, t)]): 'now'}, tape=tape(w, i, outs[:i + 1]),
                          table=dict(head=head, rows=[list(r) for r in rows], now=[len(rows) - 1])))
    return outs


def mealy_animation(qid, spec):
    """Output traces of Mealy machines: option machines given by formulas checked against a stated
    input/output example."""
    scheds = []
    if 'options' in spec:
        w, want = spec['input'], spec['output']
        for opt in spec['options']:
            edges = []
            for s in (0, 1):
                for b in (0, 1):
                    t, y = int(_ev(qid, opt['t'], s=s, b=b)), int(_ev(qid, opt['y'], s=s, b=b))
                    edges.append([str(s), f'{b}/{y}', str(t)])
            fa = FA(qid, dict(states=['0', '1'], start='0', alphabet='01', edges=edges, pos={'0': [0, 0], '1': [1, 0]}), f"option {opt['label']}")
            steps = []
            outs = mealy_trace(fa, w, steps, list(want))
            got = ''.join(outs)
            ok = got == want
            bad = next((i for i in range(len(w)) if got[i] != want[i]), None)
            steps[-1]['note'] += ' ' + (f"The output {got} is exactly the required {want}." if ok else
                                        f"The output {got} differs from the required {want} first at position {bad + 1}, so this option is wrong.")
            if bad is not None and len(steps) > bad + 2:
                steps[bad + 1]['note'] += ' This is the first mismatch.'
            check(qid, f"option {opt['label']} reproducing the example", ok, opt['expect'])
            scheds.append(schedule(opt['label'], f"Option {opt['label']}: t = {opt['show_t']}, y = {opt['show_y']}", fa.draw(), steps,
                                   [['n-now', 'current state'], ['e-now', 'move just taken']]))
        return done('fa-mealy', scheds, tabs_label='options')
    fail(qid, 'Mealy animation needs the stated input/output example and option formulas')


KINDS = {'fa-run': run_animation, 'fa-count': count_animation, 'fa-subset': subset_animation, 'fa-refine': refine_animation,
         'fa-language': language_animation, 'fa-claims': claims_animation, 'fa-mealy': mealy_animation}
PLAYER = 'automata'
TABS = 'tabs'
