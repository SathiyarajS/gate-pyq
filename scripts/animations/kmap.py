"""Karnaugh maps: fill a 2-4 variable map, find the prime implicants, the essential
ones and a minimal sum of products (or product of sums).

Data: data/animations/kmap.json. Each entry states the function (minterms, maxterms,
a map read row by row, or an expression) and the expected answer. Prime implicants
are found exactly (every cube is tried) and minimal covers by trying every set of
prime implicants, so a check never depends on one arbitrary grouping. The build
stops on any difference.
"""
from itertools import combinations, product

from .common import _list


GRAY = {1: ['0', '1'], 2: ['00', '01', '11', '10']}
MARK = {'prime': lambda v: v + '′', 'not': lambda v: '¬' + v, 'bar': lambda v: ''.join(c + '̄' for c in v)}


# ---------------------------------------------------------------- expressions

def parse(text, names):
    """Parse an expression over `names`: + is OR, juxtaposition (or * and ·) AND,
    a postfix ' or ′ and a prefix ~ or ¬ complement, 0 and 1 constants.
    Returns a tree of ('var', i), ('not', x), ('and', [..]), ('or', [..]), ('const', v)."""
    order = sorted(range(len(names)), key=lambda i: -len(names[i]))
    toks, i = [], 0
    while i < len(text):
        c = text[i]
        if c.isspace() or c in '*·':
            i += 1
        elif c in "+()~¬'′":
            toks.append({'¬': '~', '′': "'"}.get(c, c))
            i += 1
        elif c in '01':
            toks.append(('const', int(c)))
            i += 1
        else:
            for k in order:
                if text.startswith(names[k], i):
                    toks.append(('var', k))
                    i += len(names[k])
                    break
            else:
                raise SystemExit(f'Cannot read {text!r} at {text[i:]!r} (variables {names})')
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take(t=None):
        tok = peek()
        if tok is None or (t is not None and tok != t):
            raise SystemExit(f'Cannot read {text!r}: expected {t or "more"}')
        pos[0] += 1
        return tok

    def sum_():
        terms = [prod_()]
        while peek() == '+':
            take()
            terms.append(prod_())
        return terms[0] if len(terms) == 1 else ('or', terms)

    def prod_():
        fs = [factor()]
        while peek() is not None and peek() not in ('+', ')'):
            fs.append(factor())
        return fs[0] if len(fs) == 1 else ('and', fs)

    def factor():
        if peek() == '~':
            take()
            return ('not', factor())
        tok = take()
        if tok == '(':
            node = sum_()
            take(')')
        elif isinstance(tok, tuple):
            node = tok
        else:
            raise SystemExit(f'Cannot read {text!r}: unexpected {tok!r}')
        while peek() == "'":
            take()
            node = ('not', node)
        return node

    node = sum_()
    if peek() is not None:
        raise SystemExit(f'Cannot read {text!r}: unexpected {peek()!r}')
    return node


def evaluate(node, m, n):
    t = node[0]
    if t == 'var':
        return (m >> (n - 1 - node[1])) & 1
    if t == 'const':
        return node[1]
    if t == 'not':
        return 1 - evaluate(node[1], m, n)
    vals = [evaluate(x, m, n) for x in node[1]]
    return int(all(vals)) if t == 'and' else int(any(vals))


def ones(node, n):
    return frozenset(m for m in range(1 << n) if evaluate(node, m, n))


def _literal(node):
    if node[0] == 'var':
        return node[1], 1
    if node[0] == 'not' and node[1][0] == 'var':
        return node[1][1], 0
    return None


def _clause(node, inner):
    """A product (inner='and') or sum (inner='or') of literals as {var: value}, else None."""
    parts = node[1] if node[0] == inner else [node]
    out = {}
    for p in parts:
        lit = _literal(p)
        if lit is None or out.get(lit[0], lit[1]) != lit[1]:
            return None
        out[lit[0]] = lit[1]
    return out


def two_level(node, form):
    """An SOP (form 'sop') or POS ('pos') as a list of {var: value} clauses, else None.
    In a POS clause the value is the literal's polarity (x -> 1, x' -> 0)."""
    outer, inner = ('or', 'and') if form == 'sop' else ('and', 'or')
    parts = node[1] if node[0] == outer else [node]
    out = [_clause(p, inner) for p in parts]
    return None if any(c is None for c in out) else out


# ---------------------------------------------------------------- cubes

def cube_of(clause, n, form):
    """(value, free) for a clause; a POS clause covers the cells where it is 0."""
    val = free = 0
    for i in range(n):
        bit = 1 << (n - 1 - i)
        if i not in clause:
            free |= bit
        elif (clause[i] if form == 'sop' else 1 - clause[i]):
            val |= bit
    return val, free


def cells(cube, n):
    val, free = cube
    return [m for m in range(1 << n) if m & ~free == val]


def fixed(cube, n):
    """{var index: value} for the variables a cube holds fixed."""
    val, free = cube
    return {i: (val >> (n - 1 - i)) & 1 for i in range(n) if not free >> (n - 1 - i) & 1}


def literals(cube, n):
    return len(fixed(cube, n))


def prime_implicants(target, dc, n):
    """Every maximal cube inside target | dc that covers at least one target cell."""
    allowed = set(target) | set(dc)
    cubes = [(v, f) for f in range(1 << n) for v in range(1 << n) if v & f == 0 and all(m in allowed for m in cells((v, f), n))]
    ok = set(cubes)
    primes = [c for c in cubes if not any(((c[0] & ~(1 << b)), c[1] | (1 << b)) in ok for b in range(n) if not c[1] >> b & 1)]
    primes = [c for c in primes if set(cells(c, n)) & set(target)]
    return sorted(primes, key=lambda c: (-len(cells(c, n)), cells(c, n)))


def minimal_covers(primes, target, n):
    """All covers of target by primes with the fewest terms, then the fewest literals.
    Also returns the fewest literals of any cover (to catch a terms/literals conflict)."""
    target = set(target)
    if not target:
        return [()], 0
    best, covers, fewest_lits = None, [], None
    for k in range(1, len(primes) + 1):
        for combo in combinations(range(len(primes)), k):
            if target <= {m for j in combo for m in cells(primes[j], n)}:
                cost = (k, sum(literals(primes[j], n) for j in combo))
                fewest_lits = cost[1] if fewest_lits is None else min(fewest_lits, cost[1])
                if best is None or cost < best:
                    best, covers = cost, [combo]
                elif cost == best:
                    covers.append(combo)
    return covers, fewest_lits


# ---------------------------------------------------------------- the map

class KMap:
    def __init__(self, qid, spec):
        self.qid = qid
        self.names = spec['vars']
        self.n = n = len(self.names)
        if not 2 <= n <= 4:
            raise SystemExit(f'{qid}: a K-map needs 2 to 4 variables')
        self.form = spec.get('form', 'sop')
        if self.form not in ('sop', 'pos'):
            raise SystemExit(f'{qid}: unknown form {self.form}')
        self.style = spec.get('notation', 'prime')
        if self.style not in MARK:
            raise SystemExit(f'{qid}: unknown notation {self.style}')
        self.F = spec.get('name', 'F')
        given = [k for k in ('minterms', 'maxterms', 'map', 'expr') if k in spec]
        if len(given) != 1:
            raise SystemExit(f'{qid}: give exactly one of minterms, maxterms, map or expr')
        self.source = given[0]
        idx = {v: i for i, v in enumerate(self.names)}
        if self.source == 'map':
            rows, cols = spec['map']['rows'], spec['map']['cols']
        else:
            rows, cols = self.names[:n // 2], self.names[n // 2:]
        if sorted(rows + cols) != sorted(self.names) or not rows or not cols:
            raise SystemExit(f'{qid}: map rows {rows} and columns {cols} must split the variables {self.names}')
        self.rows, self.cols = [idx[v] for v in rows], [idx[v] for v in cols]
        self.rcodes, self.ccodes = GRAY[len(rows)], GRAY[len(cols)]
        self.grid = [[self._cell(r, c) for c in self.ccodes] for r in self.rcodes]
        N = 1 << n
        dc = set(spec.get('dontcares', []))
        self.expr = None
        if self.source == 'minterms':
            on = set(spec['minterms'])
        elif self.source == 'maxterms':
            on = set(range(N)) - set(spec['maxterms']) - dc
        elif self.source == 'expr':
            self.expr = parse(spec['expr'], self.names)
            on = set(ones(self.expr, n))
            if dc:
                raise SystemExit(f'{qid}: an expression cannot also have don\'t-cares')
        else:
            cellv = spec['map']['cells']
            if len(cellv) != len(self.rcodes) or any(len(r) != len(self.ccodes) for r in cellv):
                raise SystemExit(f'{qid}: the map must be {len(self.rcodes)} rows of {len(self.ccodes)}')
            on = set()
            for r, row in enumerate(cellv):
                for c, v in enumerate(row):
                    m = self.grid[r][c]
                    if v == 1:
                        on.add(m)
                    elif v == 'X':
                        dc.add(m)
                    elif v != 0:
                        raise SystemExit(f'{qid}: map cells are 0, 1 or "X", not {v!r}')
        if not all(0 <= m < N for m in on | dc) or on & dc:
            raise SystemExit(f'{qid}: minterms and don\'t-cares must be distinct indices below {N}')
        self.on, self.dc = frozenset(on), frozenset(dc)
        self.off = frozenset(set(range(N)) - on - dc)
        self.spec = spec

    def _cell(self, rcode, ccode):
        bits = [0] * self.n
        for i, b in zip(self.rows, rcode):
            bits[i] = int(b)
        for i, b in zip(self.cols, ccode):
            bits[i] = int(b)
        return int(''.join(map(str, bits)), 2)

    # text
    def lit(self, i, v):
        return self.names[i] if v else MARK[self.style](self.names[i])

    def term(self, cube, form=None):
        form = form or self.form
        fx = fixed(cube, self.n)
        if form == 'sop':
            return ''.join(self.lit(i, v) for i, v in fx.items()) or '1'
        lits = [self.lit(i, 1 - v) for i, v in fx.items()]
        return '0' if not lits else lits[0] if len(lits) == 1 else '(' + ' + '.join(lits) + ')'

    def join(self, cubes, form=None):
        form = form or self.form
        if not cubes:
            return '0' if form == 'sop' else '1'
        return (' + ' if form == 'sop' else '').join(self.term(c, form) for c in cubes)

    def where(self, cube):
        return _list([f'{self.names[i]} = {v}' for i, v in fixed(cube, self.n).items()]) if fixed(cube, self.n) else 'everywhere'

    def show(self, node, top=True):
        t = node[0]
        if t == 'var':
            return self.names[node[1]]
        if t == 'const':
            return str(node[1])
        if t == 'not':
            if node[1][0] == 'var':
                return self.lit(node[1][1], 0)
            inner = self.show(node[1])
            return '(' + inner + ')′' if self.style == 'prime' else '¬(' + inner + ')'
        if t == 'and':
            return ''.join('(' + self.show(x, False) + ')' if x[0] == 'or' else self.show(x, False) for x in node[1])
        return ' + '.join(self.show(x, False) for x in node[1])

    def cube_for(self, ms):
        """The cube whose cells are exactly ms, if there is one."""
        ms = sorted(ms)
        for f in range(1 << self.n):
            for v in range(1 << self.n):
                if v & f == 0 and cells((v, f), self.n) == ms:
                    return v, f
        return None

    def on_text(self, ms):
        ms = sorted(ms)
        return ('cell ' if len(ms) == 1 else 'cells ') + _list([str(m) for m in ms])

    def vars_text(self, idxs):
        return ''.join(self.names[i] for i in idxs)


def _value(km, m):
    return 1 if m in km.on else 'X' if m in km.dc else 0


def _fill_steps(km):
    """Steps that fill the map: one per row for a minterm list or a map, one per term
    (or factor) for an expression."""
    N, steps = 1 << km.n, []
    cellv = [None] * N
    if km.source != 'expr':
        what = {'minterms': 'minterms', 'maxterms': 'maxterms', 'map': 'cells'}[km.source]
        for r, code in enumerate(km.rcodes):
            new = km.grid[r]
            for m in new:
                cellv[m] = _value(km, m)
            parts = []
            for v, word in ((1, '1'), (0, '0'), ('X', 'X (don\'t-care)')):
                ms = sorted(m for m in new if _value(km, m) == v)
                if ms:
                    parts.append(f"{word} in {km.on_text(ms)}")
            note = f"Row {km.vars_text(km.rows)} = {code}: " + '; '.join(parts) + '.'
            if r == 0:
                lead = {'minterms': f'Each listed minterm is a 1, ', 'maxterms': f'Each listed maxterm is a 0, ', 'map': 'Copy the map one row at a time. '}[km.source]
                if km.source == 'minterms':
                    lead += 'each don\'t-care an X and every other cell a 0. ' if km.dc else 'every other cell a 0. '
                elif km.source == 'maxterms':
                    lead += 'each don\'t-care an X and every other cell a 1. ' if km.dc else 'every other cell a 1. '
                note = lead + note
            steps.append(dict(phase='Fill the map', cells=list(cellv), groups=[], hi=list(new), note=note))
        return steps
    node, neg = km.expr, False
    while node[0] == 'not' and node[1][0] != 'var':
        node, neg = node[1], not neg
    parts = node[1] if node[0] in ('or', 'and') else [node]
    top = node[0] if node[0] in ('or', 'and') else 'or'
    # In a sum each term sets its 1s; in a product each factor sets its 0s.
    hit = 1 if top == 'or' else 0
    val = hit if not neg else 1 - hit
    F = km.F
    for p in parts:
        ms = sorted(m for m in range(N) if evaluate(p, m, km.n) == hit)
        new = [m for m in ms if cellv[m] is None]
        old = [m for m in ms if cellv[m] is not None]
        for m in new:
            cellv[m] = val
        cube = km.cube_for(ms) if ms else None
        txt = km.show(p)
        where = f" where {km.where(cube)}" if cube else ''
        if not ms:
            note = f"{txt} is never {hit}, so it adds nothing."
        else:
            if neg:
                note = f"{txt} is {hit}{where} ({km.on_text(ms)}), which makes the {'bracket 1' if top == 'or' else 'product 0'}, so {F} = {val} there."
            elif top == 'or':
                note = f"{txt} is 1{where}, so {F} = 1 in {km.on_text(ms)}."
            else:
                note = f"{txt} is 0{where}, so {F} = 0 in {km.on_text(ms)}."
            if old and new:
                note += f" ({km.on_text(old).capitalize()} {'is' if len(old) == 1 else 'are'} already set.)"
            elif old:
                note += ' Those cells are already set.'
        steps.append(dict(phase='Fill the map', cells=list(cellv), groups=[], hi=new, note=note))
    rest = [m for m in range(N) if cellv[m] is None]
    for m in rest:
        cellv[m] = 1 - val
    if rest:
        steps.append(dict(phase='Fill the map', cells=list(cellv), groups=[], hi=rest,
                          note=f"The one cell left, {rest[0]}, is {1 - val}." if len(rest) == 1 else
                          f"Every other cell ({_list([str(m) for m in rest])}) is {1 - val}."))
    for m in range(N):
        if cellv[m] != _value(km, m):
            raise SystemExit(f'{km.qid}: map filling went wrong at cell {m}')
    return steps


def kmap_solve(qid, spec):
    """Build the steps and the facts that the expectations are checked against."""
    km = KMap(qid, spec)
    n, F, sop = km.n, km.F, km.form == 'sop'
    target = km.on if sop else km.off
    full = [_value(km, m) for m in range(1 << n)]
    rv, cv = km.vars_text(km.rows), km.vars_text(km.cols)
    wrap = []
    if len(km.rows) == 2:
        wrap.append('top and bottom')
    if len(km.cols) == 2:
        wrap.append('left and right')
    if len(km.rows) == len(km.cols):
        first = f"Rows are {rv} and columns are {cv}, both in Gray-code order ({', '.join(km.ccodes)})"
    else:
        first = f"Rows are {rv} ({', '.join(km.rcodes)}) and columns are {cv} in Gray-code order ({', '.join(km.ccodes)})"
    first += ', so cells side by side differ in exactly one variable.'
    if wrap:
        first += f" The map wraps around: its {' and its '.join(wrap)} edges are neighbours too."
    first += ' The small number in each cell is its minterm index.'
    steps = [dict(phase='Start', cells=[None] * (1 << n), groups=[], hi=[], note=first)]
    steps += _fill_steps(km)

    primes = prime_implicants(target, km.dc, n)
    pis = [dict(text=km.term(c), cells=cells(c, n), lits=literals(c, n)) for c in primes]
    word = '1s' if sop else '0s'
    shown = []
    for k, c in enumerate(primes):
        ms = cells(c, n)
        size = 'a single cell' if len(ms) == 1 else f'a group of {len(ms)} cells'
        used = sorted(set(ms) & km.dc)
        note = (f"Prime implicant {k + 1}: {pis[k]['text']} covers {_list([str(m) for m in ms])}, {size} in which {km.where(c)}. " if sop else
                f"Group of 0s {k + 1}: {_list([str(m) for m in ms])}, {size} in which {km.where(c)}, gives the sum term {pis[k]['text']}. ")
        if used:
            note += f"It uses the don't-care{'s' if len(used) > 1 else ''} {_list([str(m) for m in used])}. "
        note += f"It cannot grow without taking in a {'0' if sop else '1'}."
        if k == 0 and sop:
            note = f"Now group the {word}: each group is a block of 1, 2, 4 or 8 cells (wrapping round the edges) holding only 1s and Xs. " + note
        elif k == 0:
            note = f"For a product of sums, group the 0s instead: each block of 0s and Xs gives one sum term. " + note
        if k == len(primes) - 1:
            note += f" That makes {len(primes)} prime implicant{'s' if len(primes) != 1 else ''} in all." if sop else f" That makes {len(primes)} groups of 0s in all."
        shown.append([k, 'pi'])
        steps.append(dict(phase='Prime implicants' if sop else 'Groups of 0s', cells=full, groups=[[j, 'new' if j == k else 'pi'] for j, _ in shown], hi=[], note=note))

    # Essential prime implicants: the only group covering some required cell.
    covers_of = {m: [k for k, c in enumerate(primes) if m in cells(c, n)] for m in target}
    essential, why = [], {}
    for m in sorted(target):
        if len(covers_of[m]) == 1:
            k = covers_of[m][0]
            if k not in essential:
                essential.append(k)
            why.setdefault(k, []).append(m)
    essential.sort()
    if essential:
        bits = [f"{km.on_text(why[k])} {'is' if len(why[k]) == 1 else 'are'} covered only by {pis[k]['text']}" for k in essential]
        bits[0] = bits[0][0].upper() + bits[0][1:]
        note = _list(bits) + f", so {'that group is' if len(essential) == 1 else 'these ' + str(len(essential)) + ' groups are'} essential."
    else:
        note = f"Every {'1' if sop else '0'} lies in at least two groups, so no group is essential."
    steps.append(dict(phase='Essential prime implicants' if sop else 'Essential groups', cells=full,
                      groups=[[k, 'ess' if k in essential else 'pi'] for k in range(len(primes))],
                      hi=sorted(m for k in essential for m in why[k]), note=note))

    covers, fewest_lits = minimal_covers(primes, target, n)
    cost = (len(covers[0]), sum(pis[j]['lits'] for j in covers[0]))
    return km, dict(steps=steps, primes=primes, pis=pis, essential=essential, covers=covers, cost=cost, fewest_lits=fewest_lits, full=full)


# ---------------------------------------------------------------- checks

def _equiv(km, node):
    e = ones(node, km.n)
    missing = sorted(km.on - e)
    extra = sorted(km.off & e)
    return e, missing, extra


def _cost_of(km, node):
    """(terms, literals) of a two-level expression in the map's form, or None."""
    cl = two_level(node, km.form)
    if cl is None:
        return None
    return len(cl), sum(len(c) for c in cl), [cube_of(c, km.n, km.form) for c in cl]


def _claim(km, sol, claim):
    """Evaluate one statement. Returns (holds, step) where step shows it on the map."""
    t, v, F, n = claim['type'], claim.get('value'), km.F, km.n
    hi, bad = [], []
    if t in ('equivalent', 'minimal'):
        node = parse(v, km.names)
        txt = km.show(node)
        e, missing, extra = _equiv(km, node)
        hi = sorted(e)
        bad = missing + extra
        ok = not bad
        if bad:
            m = bad[0]
            note = f"{txt}: cell {m} is {'a 1' if m in km.on else 'a 0'} on the map but {txt} is {0 if m in km.on else 1} there, so it is not equivalent."
            if t == 'minimal':
                note += ' It cannot be a minimal form of the map.'
        else:
            note = f"{txt} is 1 on {km.on_text(e) if e else 'no cell'}: every 1 of the map and no 0{' (don’t-cares may go either way)' if km.dc else ''}, so it is equivalent."
        if t == 'minimal' and ok:
            c = _cost_of(km, node)
            want = sol['cost']
            if c is None or c[:2] != want:
                ok = False
                note += f" But it {'is not a two-level form' if c is None else f'has {c[0]} terms and {c[1]} literals'}, and the minimum is {want[0]} terms and {want[1]} literals."
            else:
                note += f" It has {want[0]} terms and {want[1]} literals, the minimum, so it is a minimal form."
        label = f"{F} = {txt}" if t == 'equivalent' else f"{txt} is minimal"
    elif t in ('minterms', 'maxterms'):
        if km.dc:
            raise SystemExit(f'{km.qid}: a minterm list claim needs a fully specified function')
        want = km.on if t == 'minterms' else km.off
        ok = set(v) == set(want)
        sym = 'Σm' if t == 'minterms' else 'ΠM'
        label = f"{F} = {sym}({', '.join(map(str, v))})"
        hi = sorted(want)
        what = '1s' if t == 'minterms' else '0s'
        note = f"{label}: the {what} of the map are at {_list([str(m) for m in sorted(want)])}, so this is {'true' if ok else 'false'}."
    elif t == 'independent_of':
        i = km.names.index(v)
        bit = 1 << (n - 1 - i)
        diff = [m for m in range(1 << n) if not m & bit and _value(km, m) != _value(km, m | bit) and 'X' not in (_value(km, m), _value(km, m | bit))]
        ok = not diff
        label = f"{F} is independent of {v}"
        if ok:
            note = f"Flipping {v} never changes {F} (each cell matches its partner across the {v} boundary), so {F} is independent of {v}."
        else:
            a = diff[0]
            hi, bad = [a, a | bit], [a, a | bit]
            note = f"Cells {a} and {a | bit} differ only in {v}, but {F} is {_value(km, a)} and {_value(km, a | bit)} there, so {F} depends on {v}."
    elif t in ('implicant', 'prime', 'minterm'):
        node = parse(v, km.names)
        cl = two_level(node, 'sop')
        if cl is None or len(cl) != 1:
            raise SystemExit(f'{km.qid}: {v} is not a single product term')
        cube = cube_of(cl[0], n, 'sop')
        ms = cells(cube, n)
        txt = km.show(node)
        hi = ms
        implicant = all(m in km.on or m in km.dc for m in ms)
        zeros = [m for m in ms if m in km.off]
        if t == 'minterm':
            ok = len(cl[0]) == n and implicant
            label = f"{txt} is a minterm"
            missing = [km.names[i] for i in range(n) if i not in cl[0]]
            note = (f"{txt} names all {n} variables and its cell {ms[0]} is a 1, so it is a minterm." if ok else
                    f"{txt} is not a minterm: a minterm names all {n} variables, and {txt} leaves out {_list(missing)}." if missing else
                    f"{txt} names every variable, but its cell {ms[0]} is not a 1.")
        elif t == 'implicant':
            ok = implicant
            label = f"{txt} is an implicant"
            note = (f"{txt} covers {km.on_text(ms)}, all 1s, so whenever {txt} = 1, {F} = 1: it is an implicant." if ok else
                    f"{txt} covers cell {zeros[0]}, a 0, so it is not an implicant.")
            bad = zeros
        else:
            big = [p for p in sol['primes'] if set(ms) <= set(cells(p, n))]
            ok = implicant and cube in sol['primes']
            label = f"{txt} is a prime implicant"
            if not implicant:
                note = f"{txt} covers cell {zeros[0]}, a 0, so it is not even an implicant, let alone prime."
                bad = zeros
            elif ok:
                note = f"{txt} covers {km.on_text(ms)} and cannot grow without taking in a 0, so it is a prime implicant."
            else:
                p = big[0]
                note = f"{txt} is an implicant but not prime: its cells lie inside the larger group {km.term(p, 'sop')} ({_list([str(m) for m in cells(p, n)])})."
    else:
        raise SystemExit(f'{km.qid}: unknown claim type {t}')
    want = claim['holds']
    if ok != want:
        raise SystemExit(f'Animation for {km.qid}: "{label}" {"holds" if ok else "fails"}, but the answer needs it to {"hold" if want else "fail"}')
    # A short key under the map says what the shading and dashed boxes mean.
    if t in ('equivalent', 'minimal'):
        key = f'Shaded: where {txt} is 1.' + (' Dashed box: where it disagrees with the map.' if bad else '')
    elif t in ('minterms', 'maxterms'):
        key = f"Shaded: the {'1s' if t == 'minterms' else '0s'} of the map."
    elif t == 'independent_of':
        key = f'Shaded: two cells that differ only in {v}.' if bad else ''
    else:
        key = 'Shaded: the cells the term covers.' + (' Dashed box: a 0 inside it.' if bad else '')
    return ok, label, dict(phase='Check: ' + label, cells=sol['full'], groups=[], hi=hi, bad=bad, key=key, note=note)


def kmap_animation(qid, spec):
    km, sol = kmap_solve(qid, spec)
    n, F, sop, pis = km.n, km.F, km.form == 'sop', sol['pis']
    expect = spec['expect']
    steps, covers, (T, L) = sol['steps'], sol['covers'], sol['cost']
    form = 'sum of products' if sop else 'product of sums'

    # Choose which minimal cover to draw: the expected one if it is listed.
    pick = covers[0]
    wanted = [expect['minimal']] if 'minimal' in expect else [c['value'] for c in expect.get('claims', []) if c['type'] == 'minimal' and c['holds']]
    for w in wanted:
        c = _cost_of(km, parse(w, km.names))
        match = [cov for cov in covers if c and {sol['primes'][j] for j in cov} == set(c[2])]
        if match:
            # Keep the answer's own term order, so the map shows the option as printed.
            pick = tuple(sol['primes'].index(t) for t in c[2])
            break
    ess = sol['essential']
    left = sorted(set(km.on if sop else km.off) - {m for k in ess for m in pis[k]['cells']})
    extra = [j for j in pick if j not in ess]
    expr = km.join([sol['primes'][j] for j in pick])
    if not left:
        note = f"The essential groups already cover every {'1' if sop else '0'}, so {F} = {expr}."
    else:
        note = (f"{km.on_text(left).capitalize()} {'is' if len(left) == 1 else 'are'} not yet covered. "
                f"The fewest extra groups that cover {'it' if len(left) == 1 else 'them'}: {_list([pis[j]['text'] for j in extra])}. So {F} = {expr}.")
    others = [c for c in covers if set(c) != set(pick)]
    if others:
        alt = [km.join([sol['primes'][j] for j in c]) for c in others]
        note += f" {'Another choice' if len(alt) == 1 else 'Other choices'} with the same cost: {'; '.join(alt)}."
    steps.append(dict(phase='Minimal ' + form, cells=sol['full'], groups=[[k, 'pick' if k in pick else 'off'] for k in range(len(pis))],
                      hi=left, expr=f"{F} = {expr}", note=note))

    final = [f"Minimal {form}: {F} = {expr}, with {T} {'' if sop else 'sum '}term{'s' if T != 1 else ''} and {L} literal{'s' if L != 1 else ''}."]
    if sol['fewest_lits'] < L and ('minimal' in expect or 'literals' in expect or any(c['type'] == 'minimal' for c in expect.get('claims', []))):
        raise SystemExit(f'{qid}: the fewest terms ({T}) and the fewest literals ({sol["fewest_lits"]}) need different covers, so "minimal" is ambiguous')

    if 'minimal' in expect:
        node = parse(expect['minimal'], km.names)
        e, missing, extra_ = _equiv(km, node)
        c = _cost_of(km, node)
        if missing or extra_:
            raise SystemExit(f'Animation for {qid}: {expect["minimal"]} is not equivalent to the map (cells {missing + extra_})')
        if c is None or c[:2] != (T, L):
            raise SystemExit(f'Animation for {qid}: {expect["minimal"]} costs {c and c[:2]}, but the minimum is {(T, L)}')
        for r in expect.get('rejects', []):
            rn = parse(r, km.names)
            rc = _cost_of(km, rn)
            if not (set(_equiv(km, rn)[1]) | set(_equiv(km, rn)[2])) and rc is not None and rc[:2] == (T, L):
                raise SystemExit(f'Animation for {qid}: the other option {r} is also minimal')
        if len(covers) > 1:
            final.append(f"(It is one of {len(covers)} minimal choices.)")
    if 'literals' in expect and expect['literals'] != L:
        raise SystemExit(f'Animation for {qid}: the minimum is {L} literals, not {expect["literals"]}')
    if 'prime_implicants' in expect:
        if expect['prime_implicants'] != len(pis):
            raise SystemExit(f'Animation for {qid}: {len(pis)} prime implicants, not {expect["prime_implicants"]}')
        final.append(f"Prime implicants: {len(pis)} ({_list([p['text'] for p in pis])}).")
    if 'essential' in expect:
        want = expect['essential']
        got = [pis[k]['text'] for k in ess]
        if isinstance(want, int):
            if want != len(ess):
                raise SystemExit(f'Animation for {qid}: {len(ess)} essential prime implicants, not {want}')
        else:
            wc = set()
            for w in want:
                cl = two_level(parse(w, km.names), km.form)
                if cl is None or len(cl) != 1:
                    raise SystemExit(f'{qid}: essential term {w} is not a single term')
                wc.add(cube_of(cl[0], n, km.form))
            if wc != {sol['primes'][k] for k in ess}:
                raise SystemExit(f'Animation for {qid}: essential prime implicants are {got}, not {want}')
        final.append(f"Essential prime implicants: {len(ess)}" + (f" ({_list(got)})." if got else '.'))
    if 'minterms' in expect:
        if km.dc or sorted(expect['minterms']) != sorted(km.on):
            raise SystemExit(f'Animation for {qid}: the 1s are {sorted(km.on)}, not {expect["minterms"]}')
        final.insert(0, f"{F} = Σm({', '.join(map(str, sorted(km.on)))}).")
    if 'on_count' in expect:
        if expect['on_count'] != len(km.on):
            raise SystemExit(f'Animation for {qid}: {F} has {len(km.on)} minterms, not {expect["on_count"]}')
        final.insert(0, f"{F} is 1 on {len(km.on)} cell{'s' if len(km.on) != 1 else ''} ({_list([str(m) for m in sorted(km.on)])}), so {len(km.on)} minterm{'s' if len(km.on) != 1 else ''}.")
    if 'independent_count' in expect:
        if km.dc:
            raise SystemExit(f'{qid}: independence needs a fully specified function')
        free = [i for i in range(n) if all(_value(km, m) == _value(km, m ^ (1 << (n - 1 - i))) for m in range(1 << n))]
        if len(free) != expect['independent_count']:
            raise SystemExit(f'Animation for {qid}: {F} is independent of {len(free)} variables, not {expect["independent_count"]}')
        dep = [km.names[i] for i in range(n) if i not in free]
        final.append(f"{F} uses only {_list(dep)}, so it is independent of {len(free)} variable{'s' if len(free) != 1 else ''}: {_list([km.names[i] for i in free])}.")
    held, failed = [], []
    for claim in expect.get('claims', []):
        ok, label, step = _claim(km, sol, claim)
        steps.append(step)
        (held if ok else failed).append(label)
    if held or failed:
        final.append(('Holds: ' + '; '.join(held) + '.' if held else 'None of the statements holds.') + (' Fails: ' + '; '.join(failed) + '.' if failed else ''))
    steps.append(dict(phase='Finished', cells=sol['full'], groups=[[k, 'pick'] for k in pick], hi=[], expr=f"{F} = {expr}", final=True, note=' '.join(final)))
    for s in steps:
        s.setdefault('bad', [])
    data = dict(kind='kmap', vars=km.names, rows=km.rows, cols=km.cols, rcodes=km.rcodes, ccodes=km.ccodes, grid=km.grid,
                form=km.form, pis=[dict(text=p['text'], cells=p['cells']) for p in pis])
    data['schedules'] = [dict(short='K-map', title=_title(km), steps=steps)]
    data['count'] = len(steps)
    return data


def _title(km):
    F, args = km.F, ', '.join(km.names)
    if km.source == 'minterms':
        t = f"{F}({args}) = Σm({', '.join(map(str, sorted(km.on)))})"
    elif km.source == 'maxterms':
        t = f"{F}({args}) = ΠM({', '.join(map(str, sorted(km.off)))})"
    elif km.source == 'expr':
        t = f"{F} = {km.show(km.expr)}"
    else:
        t = f"{F}({args}) as given on the map"
    if km.dc and km.source != 'map':
        t += f" + d({', '.join(map(str, sorted(km.dc)))})"
    return t + ('; minimal product of sums' if km.form == 'pos' else '')


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'kmap': kmap_animation}
PLAYER = 'kmap'
