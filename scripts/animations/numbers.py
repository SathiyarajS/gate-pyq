"""Number systems: radix conversion, unknown bases, signed representations,
column arithmetic with carries and overflow, IEEE-754 binary32 and Booth recoding.

Data: data/animations/numbers.json. Every entry is simulated at build time with exact
integer and fraction arithmetic and checked against the expected answer; the build
stops on any difference.

Each step is {note, blocks}; a block is one of
  {t: 'table', head, rows, hl, mono, marks}   a growing table (hl = current row)
  {t: 'grid', rows: [{label, cells, cls}], now, gaps}   digits aligned in columns
  {t: 'groups', label, items: [{top, bits, c, now}]}    bit groups under their digit
  {t: 'line', text, cls}                      one line of text
Table cells may write a numeral's base as 224_5 or 13_r; the player draws it as a subscript.
"""
import itertools
import re
from fractions import Fraction
from math import isqrt

DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NAMES = {2: 'binary', 8: 'octal', 10: 'decimal', 16: 'hexadecimal'}
LIMIT = 200  # bases 2..LIMIT are tried when searching for an unknown base
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
_SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
ORDINAL = ['Rightmost', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth']


# ---------------------------------------------------------------- small helpers

def sub(b):
    return str(b).translate(_SUB)


def sup(k):
    return str(k).translate(_SUP)


def num(s, b):
    """A numeral for a note: 224₅."""
    return f'{s}{sub(b)}'


def dec(x):
    """Exact decimal text of a fraction ('6.625', '-60.25'), or p/q if it does not terminate."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    d, k2, k5 = x.denominator, 0, 0
    while d % 2 == 0:
        d, k2 = d // 2, k2 + 1
    while d % 5 == 0:
        d, k5 = d // 5, k5 + 1
    if d != 1:
        return f'{x.numerator}/{x.denominator}'
    k = max(k2, k5)
    whole, frac = divmod(int(abs(x) * 10 ** k), 10 ** k)
    return ('-' if x < 0 else '') + f'{whole}.{str(frac).rjust(k, "0")}'.rstrip('0')


def show(x):
    """A value for display: exact decimal with a real minus sign; very long ones approximated."""
    if isinstance(x, Irr):
        return f'√{show(x.square)}'
    s = dec(x)
    if len(s) > 16:
        m = f'{float(x):.8g}'
        if 'e' in m:
            mant, ex = m.split('e')
            s = f'≈ {mant} × 10{sup(int(ex))}'
        else:
            s = '≈ ' + m
    return s.replace('-', '−')


def eq(x):
    """'= 6.25', or '≈ 1.43 × 10⁻⁶' when the exact decimal is too long to show."""
    s = show(x)
    return s if s.startswith('≈') else '= ' + s


def digit(ch, base):
    v = DIGITS.find(ch.upper())
    if v < 0 or v >= base:
        raise SystemExit(f'{ch} is not a digit in base {base}')
    return v


def value_of(s, base):
    whole, _, frac = s.partition('.')
    v = Fraction(0)
    for ch in whole:
        v = v * base + digit(ch, base)
    for k, ch in enumerate(frac, 1):
        v += Fraction(digit(ch, base), base ** k)
    return v


def to_base(n, base, width=0):
    if n < 0:
        raise SystemExit(f'to_base needs a non-negative number, not {n}')
    s = ''
    while n:
        n, r = divmod(n, base)
        s = DIGITS[r] + s
    return (s or '0').rjust(width, '0')


def binary_text(x):
    """Binary numeral of a non-negative fraction with a power-of-two denominator."""
    whole, frac, f = int(x), x - int(x), ''
    while frac:
        frac *= 2
        f += str(int(frac))
        frac -= int(frac)
        if len(f) > 160:
            raise SystemExit(f'{x} has no finite binary expansion')
    return to_base(whole, 2) + ('.' + f if f else '')


def expansion(s, base):
    """(digit, power, digit value, contribution) for each digit, most significant first."""
    whole, _, frac = s.partition('.')
    return [(ch, len(whole) - 1 - i, digit(ch, base), digit(ch, base) * Fraction(base) ** (len(whole) - 1 - i))
            for i, ch in enumerate(whole + frac)]


def expand_text(s, base):
    terms = []
    for ch, k, d, _ in expansion(s, base):
        terms.append(str(d) if k == 0 else f'{d}×{base}' if k == 1 else f'{d}×{base}{sup(k)}')
    return ' + '.join(terms)


def _log2(n):
    if n < 2 or n & (n - 1):
        raise SystemExit(f'{n} is not a power of two')
    return n.bit_length() - 1


def table(head, rows, hl=None, mono=(), marks=None, wrap=()):
    return dict(t='table', head=list(head), rows=[[str(c) for c in r] for r in rows], hl=hl, mono=list(mono),
                marks=list(marks) if marks else None, wrap=list(wrap))


def line(text, cls='steps-ready'):
    return dict(t='line', text=text, cls=cls)


def grid(rows, now=(), gaps=()):
    return dict(t='grid', rows=[dict(label=l, cells=[str(c) for c in cells], cls=cls) for l, cells, cls in rows],
                now=list(now), gaps=list(gaps))


def groups(label, items):
    return dict(t='groups', label=label, items=[dict(top=str(t), bits=b, c=c, now=bool(n)) for t, b, c, n in items])


def step(note, *blocks):
    return dict(note=note, blocks=[b for b in blocks if b])


def _finish(kind, schedules, **extra):
    for s in schedules:
        s['steps'][-1]['final'] = True
    return dict(kind=kind, schedules=schedules, count=sum(len(s['steps']) for s in schedules), **extra)


def _check(qid, what, got, want):
    if got != want:
        raise SystemExit(f'Animation for {qid}: {what} is {got!r}, not {want!r}')


def _same_digits(a, b):
    return (a.upper().lstrip('0') or '0') == (b.upper().lstrip('0') or '0')


# ---------------------------------------------------------------- radix conversion

def expand_steps(s, base):
    """Positional expansion to decimal, one digit per step."""
    rows, total, steps = [], Fraction(0), []
    head = ['Digit', 'Place value', 'Digit × place']
    for ch, k, d, c in expansion(s, base):
        total += c
        pv = Fraction(base) ** k
        rows.append([ch, f'{base}{sup(k)} = {show(pv)}', f'{d} × {show(pv)} = {show(c)}'])
        name = f'{ch} ({d})' if d >= 10 else ch
        steps.append(step(f'The digit {name} is in the {base}{sup(k)} place: {d} × {show(pv)} = {show(c)}. Running total: {show(total)}.',
                          table(head, rows, len(rows) - 1, [0]), line(f'Running total: {show(total)}')))
    return steps, total, rows


def divide_steps(n, base):
    """Repeated division by the new base; the remainders are the digits, last one first."""
    rows, digits, steps = [], '', []
    while True:
        q, r = divmod(n, base)
        digits = DIGITS[r] + digits
        rows.append([n, q, str(r) if r < 10 else f'{r} = {DIGITS[r]}'])
        note = f'{n} ÷ {base} = {q} remainder {r}' + (f', the digit {DIGITS[r]}' if r >= 10 else '')
        note += '. The quotient is 0, so stop.' if q == 0 else f'. Carry on with {q}.'
        steps.append(step(note, table(['Number', f'Quotient (÷ {base})', 'Remainder'], rows, len(rows) - 1, [2]),
                          line(f'Digits so far, read upwards: {digits}')))
        n = q
        if n == 0:
            return steps, digits, rows


def regroup_steps(s, fb, tb):
    """Power-of-two bases: each digit becomes a fixed number of bits, then the bits are regrouped."""
    kf, kt = _log2(fb), _log2(tb)
    src = [[ch, '', 3, False] for ch in s]
    steps = [step(f'Each {NAMES[fb]} digit is exactly {kf} bits and each {NAMES[tb]} digit is exactly {kt} bits, so write the number in binary and regroup the bits.',
                  groups(NAMES[fb].capitalize(), src))]
    bits = ''
    for i, ch in enumerate(s):
        b = format(digit(ch, fb), f'0{kf}b')
        bits += b
        src[i][1] = b
        steps.append(step(f'{NAMES[fb].capitalize()} {ch} is {b}.', groups(NAMES[fb].capitalize(), [x[:3] + [k == i] for k, x in enumerate(src)])))
    pad = (-len(bits)) % kt
    padded = '0' * pad + bits
    chunks = [padded[i:i + kt] for i in range(0, len(padded), kt)]
    out = [['', c, 0, False] for c in chunks]
    left = groups(NAMES[fb].capitalize(), [x[:3] + [False] for x in src])
    steps.append(step(f'That is {len(bits)} bits: {bits}. ' + (f'Add {pad} zero{"s" if pad > 1 else ""} on the left to make whole groups of {kt}.' if pad else f'They split exactly into groups of {kt}.'),
                      left, groups('Regrouped', out)))
    for j in reversed(range(len(chunks))):
        v = int(chunks[j], 2)
        out[j][0] = DIGITS[v]
        steps.append(step(f'The group {chunks[j]} is {v}' + (f', the digit {DIGITS[v]}.' if v >= 10 else '.'),
                          left, groups(NAMES[tb].capitalize(), [x[:3] + [k == j] for k, x in enumerate(out)])))
    result = ''.join(x[0] for x in out)
    short = result.lstrip('0') or '0'
    steps.append(step(f'So {num(s, fb)} = {num(short, tb)}.' + (' The leading 0 adds nothing.' if short != result else ''),
                      left, groups(NAMES[tb].capitalize(), [x[:3] + [False] for x in out]), line(f'Result: {short}', 'steps-time')))
    return steps, short


def convert_animation(qid, spec):
    s, fb, tb = spec['numeral'].upper(), spec['from'], spec['to']
    value = value_of(s, fb)
    if spec.get('method') == 'regroup':
        steps, result = regroup_steps(s, fb, tb)
        if value_of(result, tb) != value:
            raise SystemExit(f'Animation for {qid}: regrouping changed the value')
    else:
        steps = [step(f'Write {num(s, fb)} as a sum of digit × place value' + (', then divide by ' + str(tb) + ' repeatedly to get the new digits.' if tb != 10 else '.'))]
        more, value2, rows = expand_steps(s, fb)
        steps += more
        result = dec(value2)
        if tb != 10:
            if value2.denominator != 1:
                raise SystemExit(f'Animation for {qid}: only whole numbers are converted by division')
            steps.append(step(f'So {num(s, fb)} = {value2} in decimal. Now divide by {tb} again and again; each remainder is the next digit from the right.',
                              table(['Digit', 'Place value', 'Digit × place'], rows + [['', 'Total', show(value2)]], len(rows), [0])))
            more, result, _ = divide_steps(int(value2), tb)
            steps += more
            steps.append(step(f'Reading the remainders from the last one up gives {result}, so {num(s, fb)} = {num(result, tb)}.',
                              *more[-1]['blocks'][:1], line(f'Result: {result}', 'steps-time')))
        else:
            steps.append(step(f'Adding the contributions: {num(s, fb)} = {show(value2)}.',
                              table(['Digit', 'Place value', 'Digit × place'], rows + [['', 'Total', show(value2)]], len(rows), [0]),
                              line(f'Result: {show(value2)}', 'steps-time')))
    out = dict(result=result)
    if 'pattern' in spec:
        pat = spec['pattern']
        if len(pat) != len(result):
            raise SystemExit(f'Animation for {qid}: {result} does not fit the pattern {pat}')
        letters = {}
        for p, r in zip(pat, result):
            if p.islower():
                if letters.setdefault(p, int(r)) != int(r):
                    raise SystemExit(f'Animation for {qid}: {p} takes two values')
            elif p != r:
                raise SystemExit(f'Animation for {qid}: {result} does not fit the pattern {pat}')
        out.update(letters=letters, sum=sum(letters.values()))
        names = ' and '.join(f'{k} = {v}' for k, v in letters.items())
        steps.append(step(f'Matching {result} with {pat} digit by digit gives {names}, so ' + ' + '.join(letters) + f' = {out["sum"]}.',
                          table(['Pattern'] + list(pat), [['Value'] + list(result)], mono=range(len(pat) + 1)),
                          line(f'Answer: {out["sum"]}', 'steps-time')))
    for k, v in spec['expect'].items():
        got = out.get(k)
        if k == 'result' and isinstance(v, str) and '.' not in v:
            if not _same_digits(str(got), v):
                _check(qid, k, got, v)
        else:
            _check(qid, k, got, v)
    title = f'{NAMES.get(fb, f"base {fb}")} to {NAMES.get(tb, f"base {tb}")}'
    title = title[0].upper() + title[1:]
    return _finish('radix-convert', [dict(short='Convert', title=title, steps=steps)])


def compare_animation(qid, spec):
    """Which of several numerals equal a target numeral: expand each to decimal."""
    ts, tb = spec['target']
    tv = value_of(ts, tb)
    rows, marks, equal = [[f'{ts}_{tb}', expand_text(ts, tb), show(tv), 'target']], ['is-running'], []
    head = ['Numeral', 'Expansion', 'Decimal', '']
    steps = [step(f'Expand every numeral as digit × place value and compare the decimal values with {num(ts, tb)}.'),
             step(f'{num(ts, tb)} = {expand_text(ts, tb)} = {show(tv)}.', table(head, rows, 0, [0], marks))]
    for s, b in spec['options']:
        v = value_of(s, b)
        same = v == tv
        if same:
            equal.append([s, b])
        rows.append([f'{s}_{b}', expand_text(s, b), show(v), 'equal' if same else 'differs'])
        marks = [m if m != 'is-running' else None for m in marks] + ['is-running']
        steps.append(step(f'{num(s, b)} = {expand_text(s, b)} = {show(v)}, ' + ('the same value.' if same else f'not {show(tv)}.'),
                          table(head, rows, len(rows) - 1, [0], marks)))
        marks[-1] = 'is-good' if same else 'is-probed'
    steps.append(step('Equal to ' + num(ts, tb) + ': ' + ', '.join(num(s, b) for s, b in equal) + '.', table(head, rows, None, [0], marks)))
    _check(qid, 'equal numerals', equal, spec['expect']['equal'])
    return _finish('radix-compare', [dict(short='Compare', title=f'Numerals equal to {num(ts, tb)}', steps=steps)])


# ---------------------------------------------------------------- expressions with numerals

class Irr:
    """The square root of a rational that is not a perfect square: never equal to a rational."""
    def __init__(self, square):
        self.square = square


_TOK = re.compile(r'\s*(?:(?P<numeral>[0-9A-Za-z.]+)_(?P<base>[0-9]+|[a-z])|(?P<number>\d+(?:\.\d+)?)'
                  r'|(?P<name>sqrt|[A-Za-z][A-Za-z0-9]*)|(?P<op>[-+−×*/÷^()=<>√]))')
_OPS = {'−': '-', '×': '*', '÷': '/', '√': 'sqrt'}


def tokens(text):
    out, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m or m.end() == pos:
            raise SystemExit(f'Cannot read the expression {text!r} at {text[pos:]!r}')
        pos = m.end()
        if m['numeral'] is not None:
            out.append(('numeral', m['numeral'], int(m['base']) if m['base'].isdigit() else m['base']))
        elif m['number'] is not None:
            out.append(('num', Fraction(m['number'])))
        elif m['name'] is not None:
            out.append(('op', 'sqrt') if m['name'] == 'sqrt' else ('var', m['name']))
        else:
            out.append(('op', _OPS.get(m['op'], m['op'])))
    return out


def parse_expr(text):
    toks, i = tokens(text), [0]

    def peek():
        return toks[i[0]] if i[0] < len(toks) else ('end', None)

    def take(op=None):
        t = peek()
        if op and t != ('op', op):
            raise SystemExit(f'Expected {op} in {text!r}')
        i[0] += 1
        return t

    def primary():
        t = take()
        if t[0] in ('num', 'var', 'numeral'):
            return t
        if t == ('op', '('):
            e = additive()
            take(')')
            return e
        if t == ('op', 'sqrt'):
            return ('sqrt', primary())
        raise SystemExit(f'Unexpected {t} in {text!r}')

    def power():
        b = primary()
        if peek() == ('op', '^'):
            take()
            return ('bin', '^', b, unary())
        return b

    def unary():
        if peek() == ('op', '-'):
            take()
            return ('neg', unary())
        return power()

    def term():
        e = unary()
        while True:
            t = peek()
            if t in (('op', '*'), ('op', '/')):
                take()
                e = ('bin', t[1], e, unary())
            elif t[0] in ('var', 'numeral', 'num') or t in (('op', '('), ('op', 'sqrt')):
                e = ('bin', '*', e, unary())  # implicit multiplication: 4(X+Y), 3C
            else:
                return e

    def additive():
        e = term()
        while peek() in (('op', '+'), ('op', '-')):
            e = ('bin', take()[1], e, term())
        return e

    e = additive()
    if peek() in (('op', '='), ('op', '<'), ('op', '>')):
        e = ('cmp', take()[1], e, additive())
    if peek()[0] != 'end':
        raise SystemExit(f'Unexpected {peek()} in {text!r}')
    return e


def evaluate(node, env, bad=None):
    """Exact value of an expression. Digits that are too big for their base go to `bad`."""
    t = node[0]
    if t == 'num':
        return node[1]
    if t == 'var':
        return env[node[1]]
    if t == 'numeral':
        _, digits, base = node
        b = base if isinstance(base, int) else env[base]
        whole, _, frac = digits.partition('.')
        v = Fraction(0)
        for k, ch in enumerate(whole + frac):
            d = env[ch] if ch.islower() else DIGITS.index(ch.upper())
            if d >= b and bad is not None:
                bad.append((ch, d, b))
            v += d * Fraction(b) ** (len(whole) - 1 - k)
        return v
    if t == 'neg':
        return -_rational(evaluate(node[1], env, bad))
    if t == 'sqrt':
        v = _rational(evaluate(node[1], env, bad))
        if v < 0:
            raise SystemExit('Square root of a negative number')
        a, b = isqrt(v.numerator), isqrt(v.denominator)
        return Fraction(a, b) if a * a == v.numerator and b * b == v.denominator else Irr(v)
    if t == 'bin':
        a, b = evaluate(node[2], env, bad), evaluate(node[3], env, bad)
        a, b = _rational(a), _rational(b)
        op = node[1]
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            if b == 0:
                raise SystemExit('Division by zero')
            return a / b
        if b.denominator != 1:
            raise SystemExit('Only whole powers are supported')
        return a ** int(b)
    if t == 'cmp':
        a, b = evaluate(node[2], env, bad), evaluate(node[3], env, bad)
        if isinstance(a, Irr) or isinstance(b, Irr):
            if node[1] != '=':
                raise SystemExit('Ordering comparisons with square roots are not supported')
            return False
        return a == b if node[1] == '=' else a < b if node[1] == '<' else a > b
    raise SystemExit(f'Unknown expression node {t}')


def _rational(v):
    if isinstance(v, Irr):
        raise SystemExit('Arithmetic on an irrational square root is not supported')
    return v


_PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
_SHOW = {'+': ' + ', '-': ' − ', '*': ' × ', '/': ' ÷ ', '^': '^'}


def fmt(node, env=None, cells=False):
    """An expression as text; with env, names and numerals are replaced by their values."""
    t = node[0]
    if t == 'num':
        return show(node[1])
    if t == 'var':
        if env is None:
            return node[1]
        v = show(env[node[1]])
        return f'({v})' if v.startswith('−') else v
    if t == 'numeral':
        if env is not None:
            return show(evaluate(node, env))
        return f'{node[1]}_{node[2]}' if cells else num(node[1], node[2]) if isinstance(node[2], int) else f'({node[1]}) in base {node[2]}'
    if t == 'neg':
        return '−' + fmt(node[1], env, cells)
    if t == 'sqrt':
        inner = fmt(node[1], env, cells)
        return '√' + inner if node[1][0] != 'bin' and not inner.startswith('−') else '√(' + inner + ')'
    if t == 'cmp':
        return fmt(node[2], env, cells) + f' {node[1]} ' + fmt(node[3], env, cells)
    op, a, b = node[1], node[2], node[3]
    sa, sb = fmt(a, env, cells), fmt(b, env, cells)
    if a[0] == 'bin' and _PREC[a[1]] < _PREC[op]:
        sa = f'({sa})'
    if b[0] == 'bin' and (_PREC[b[1]] < _PREC[op] or (_PREC[b[1]] == _PREC[op] and op in '-/')):
        sb = f'({sb})'
    if op == '^':
        return sa + (sup(sb) if sb.isdigit() else '^' + sb)
    return sa + _SHOW[op] + sb


def _numerals(node, out):
    if node[0] == 'numeral':
        out.append(node)
    for x in node[1:]:
        if isinstance(x, tuple):
            _numerals(x, out)
    return out


# ---------------------------------------------------------------- unknown bases and digits

_LETTER_SUB = dict(zip('aehijklmnoprstuvx', 'ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ'))


def side(e, env):
    """One side of an equation with values put in: '54 ÷ 8 = 6.75', or just '38'."""
    v = evaluate(e, env)
    text, value = fmt(e, env), show(v)
    if isinstance(v, Irr):
        return value
    return value if text == value else f'{text} = {value}'


def _retitle(e, numeral):
    t = e[0]
    if t == 'numeral':
        return numeral(e)
    if t in ('num', 'var'):
        return fmt(e)
    if t == 'neg':
        return '−' + _retitle(e[1], numeral)
    if t == 'sqrt':
        return '√(' + _retitle(e[1], numeral) + ')'
    if t == 'cmp':
        return _retitle(e[2], numeral) + f' {e[1]} ' + _retitle(e[3], numeral)
    op, a, b = e[1], _retitle(e[2], numeral), _retitle(e[3], numeral)
    if e[2][0] == 'bin' and _PREC[e[2][1]] < _PREC[op]:
        a = f'({a})'
    if e[3][0] == 'bin' and (_PREC[e[3][1]] < _PREC[op] or (_PREC[e[3][1]] == _PREC[op] and op in '-/')):
        b = f'({b})'
    return a + (sup(b) if op == '^' and b.isdigit() else _SHOW[op] + b)


def _title(eqs):
    """Equations as plain text for the player's title line, which takes no markup."""
    nums = [n for e in eqs for n in _numerals(e, [])]
    letters = {n[2] for n in nums if isinstance(n[2], str)}
    if len(letters) == 1 and all(isinstance(n[2], str) for n in nums) and next(iter(letters)) not in _LETTER_SUB:
        return ' and '.join(_retitle(e, lambda n: n[1]) for e in eqs) + f', all in base {next(iter(letters))}'

    def one(n):
        if isinstance(n[2], int):
            return num(n[1], n[2])
        return n[1] + _LETTER_SUB[n[2]] if n[2] in _LETTER_SUB else f'({n[1]}) in base {n[2]}'
    return ' and '.join(_retitle(e, one) for e in eqs)


def equation_animation(qid, spec):
    """Numerals with an unknown base or unknown digits: try each choice, or list every solution."""
    eqs = [(text, parse_expr(text)) for text in spec['equations']]
    for text, e in eqs:
        if e[0] != 'cmp' or e[1] != '=':
            raise SystemExit(f'Animation for {qid}: {text!r} is not an equation')
    nums = [n for _, e in eqs for n in _numerals(e, [])]
    unknowns, base_letters, digit_bases = [], set(), {}
    for _, digits, base in nums:
        for ch in digits:
            if ch.islower():
                digit_bases.setdefault(ch, set()).add(base)
                unknowns.append(ch)
        if isinstance(base, str):
            base_letters.add(base)
            unknowns.append(base)
    unknowns = list(dict.fromkeys(unknowns))
    if base_letters & set(digit_bases):
        raise SystemExit(f'Animation for {qid}: a letter cannot be both a base and a digit')

    def domain(u):
        if u in base_letters:
            return range(2, LIMIT + 1)
        known = [b for b in digit_bases[u] if isinstance(b, int)]
        return range(0, min(known)) if known else range(0, LIMIT)

    def same(x, y):
        return not isinstance(x, Irr) and not isinstance(y, Irr) and x == y

    def trial(env):
        bad = []
        sides = [(evaluate(e[2], env, bad), evaluate(e[3], env, bad)) for _, e in eqs]
        return all(same(x, y) for x, y in sides), sides, bad

    shown = list(dict.fromkeys(n for n in nums if isinstance(n[2], str) or any(c.islower() for c in n[1])))
    fixed = list(dict.fromkeys(n for n in nums if n not in shown and n[2] != 10))
    bare = all(e[2][0] == 'numeral' and e[3][0] == 'numeral' for _, e in eqs)
    labels = spec.get('labels') or ([] if bare else ['Check'] if len(eqs) == 1 else [f'Equation {k + 1}' for k in range(len(eqs))])
    head = unknowns + [f'{n[1]}_{n[2]}' for n in shown] + labels + ['']

    def row(env, holds, sides, bad):
        cells = [env[u] for u in unknowns] + [show(evaluate(n, env)) for n in shown]
        if not bare:
            cells += [f'{show(x)} {"=" if same(x, y) else "≠"} {show(y)}' for x, y in sides]
        if bad:
            ch, d, b = bad[0]
            cells.append(f'{ch} = {d} is too big for base {b}' if ch.islower() else f'{ch} is not a digit in base {b}')
        else:
            cells.append('works' if holds else 'no')
        return cells

    def why(env, holds, sides, bad):
        parts = [f'{n[1]} in base {env[n[2]] if isinstance(n[2], str) else n[2]} is {show(evaluate(n, env))}' for n in shown]
        note = ', '.join(f'{u} = {env[u]}' for u in unknowns) + ': ' + ', '.join(parts) + '.'
        if not bare:
            for k, ((_, e), (x, y)) in enumerate(zip(eqs, sides)):
                prefix = f' {spec["labels"][k]}:' if spec.get('labels') else ''
                if isinstance(x, Irr):
                    note += f'{prefix} {show(x)} is not a whole number, so it cannot equal {side(e[3], env)}.'
                else:
                    note += f'{prefix} {side(e[2], env)}, ' + ('which matches' if same(x, y) else 'not') + f' {side(e[3], env)}.'
        if bad:
            ch, d, b = bad[0]
            what = f'{ch} = {d} is not a digit in base {b}' if ch.islower() else f'the digit {ch} cannot appear in base {b}'
            note += f' The values match, but {what}.' if holds else f' Also, {what}.'
        else:
            note += ' This works.' if holds else ' This does not work.'
        return note

    intro = 'A base must be larger than every digit written in it. '
    for _, digits, base in fixed:
        intro += f'{num(digits, base)} = {expand_text(digits, base)} = {show(value_of(digits, base))}. '
    single_base = len(unknowns) == 1 and unknowns[0] in base_letters
    found = None
    if 'options' in spec:
        intro += 'Try each offered choice.'
        tries = [dict(o) for o in spec['options']]
    elif single_base:
        u = unknowns[0]
        low = max([2] + [DIGITS.index(c.upper()) + 1 for n in nums if n[2] == u for c in n[1] if c != '.'])
        found = [{u: b} for b in range(2, LIMIT + 1) if trial({u: b})[0] and not trial({u: b})[2]]
        if not found:
            raise SystemExit(f'Animation for {qid}: no base works')
        intro += f'The largest digit in base {u} is {low - 1}, so try {u} = {low}, {low + 1}, … in turn.'
        tries = [{u: b} for b in range(low, found[-1][u] + 2)]
    else:
        intro += 'List every choice of ' + ' and '.join(unknowns) + ' that makes the values equal, then keep those whose digits are valid.'
        tries = [dict(zip(unknowns, vals)) for vals in itertools.product(*[domain(u) for u in unknowns])]
        tries = [env for env in tries if trial(env)[0]]
    if len(tries) > 12:
        raise SystemExit(f'Animation for {qid}: too many rows to show')
    rows, marks, solutions = [], [], []
    steps = [step(intro.strip(), table(head, [], None, range(len(head))))]
    for env in tries:
        holds, sides, bad = trial(env)
        ok = holds and not bad
        if ok:
            solutions.append(env)
        rows.append(row(env, holds, sides, bad))
        marks = [m if m != 'is-running' else None for m in marks] + ['is-running']
        steps.append(step(why(env, holds, sides, bad), table(head, rows, len(rows) - 1, (), marks)))
        marks[-1] = 'is-good' if ok else 'is-probed'
    if found is not None and found != solutions:
        raise SystemExit(f'Animation for {qid}: the bases shown miss a solution')
    if not solutions:
        final = 'No choice works.'
    elif len(unknowns) == 1:
        u = unknowns[0]
        final = f'Only {u} = {solutions[0][u]} works.' if len(solutions) == 1 else f'{len(solutions)} values work: ' + ', '.join(str(x[u]) for x in solutions) + '.'
    else:
        pairs = ', '.join('(' + ', '.join(str(x[u]) for u in unknowns) + ')' for x in solutions)
        final = (f'{len(solutions)} choices of (' if len(solutions) > 1 else 'One choice of (') + ', '.join(unknowns) + f') work{"" if len(solutions) > 1 else "s"}: {pairs}.'
    steps.append(step(final, table(head, rows, None, (), marks), line(f'Solutions: {len(solutions)}', 'steps-time')))
    schedules = [dict(short='Find the base' if base_letters else 'Find the digits', title=spec.get('title') or _title([e for _, e in eqs]), steps=steps)]
    out = dict(solutions=solutions, count=len(solutions))
    if 'then' in spec:
        if len(solutions) != 1:
            raise SystemExit(f'Animation for {qid}: "then" needs exactly one solution')
        env = solutions[0]
        e = parse_expr(spec['then'])
        if e[0] != 'bin' or e[1] not in '+-' or e[2][0] != 'numeral' or e[3][0] != 'numeral' or e[2][2] != e[3][2]:
            raise SystemExit(f'Animation for {qid}: "then" must add or subtract two numerals in the same base')
        b = env[e[2][2]] if isinstance(e[2][2], str) else e[2][2]
        more, result = column_steps(e[2][1], e[3][1], b, e[1])
        if value_of(result, b) != evaluate(e, env):
            raise SystemExit(f'Animation for {qid}: column arithmetic disagrees with the value')
        out['then'] = result
        schedules.append(dict(short=f'Work in base {b}', title=f'{e[2][1]} {"+" if e[1] == "+" else "−"} {e[3][1]} in base {b}', steps=more))
    for k, v in spec['expect'].items():
        _check(qid, k, out[k], v)
    return _finish('radix-equation', schedules, tabs_label='parts')


# ---------------------------------------------------------------- column arithmetic in any base

def _col(i):
    return f'{ORDINAL[i]} column' if i < len(ORDINAL) else f'Column {i + 1} from the right'


def column_steps(a, b, base, op, intro=None):
    """Add or subtract two numerals column by column, with carries or borrows."""
    a, b = a.upper(), b.upper()
    n = max(len(a), len(b))
    A = [digit(c, base) for c in a.rjust(n, '0')]
    B = [digit(c, base) for c in b.rjust(n, '0')]
    w = n + 1
    carry, res = [''] * w, [''] * w
    top, bottom = [''] + list(a.rjust(n, ' ')), [''] + list(b.rjust(n, ' '))
    word = 'carry' if op == '+' else 'borrow'
    sign = '+' if op == '+' else '−'

    def view(now):
        return grid([(word, carry, 'carry'), ('', top, ''), (sign, bottom, ''), ('=', res, 'sum')], now)
    steps = [step(intro or (f'Line the numbers up on the right and {"add" if op == "+" else "subtract"} one column at a time in base {base}, ' +
                            ('carrying 1 whenever a column reaches ' if op == '+' else 'borrowing one ') + f'{base}.'), view([]))]
    c = 0
    for i in range(n):
        col = w - 1 - i
        x, y = A[n - 1 - i], B[n - 1 - i]
        if op == '+':
            t = x + y + c
            d, c2 = t % base, t // base
            note = f'{_col(i)}: {x} + {y}' + (f' + carry {c}' if c else '') + f' = {t}'
            note += f', which is {c2} × {base} + {d}: write {DIGITS[d]} and carry {c2}.' if c2 else f': write {DIGITS[d]}.'
        else:
            t = x - c
            if t < y:
                d, c2 = t + base - y, 1
                note = f'{_col(i)}: ' + (f'{x} − 1 (lent to the column on the right) = {t}, which' if c else f'{x}') + f' is smaller than {y}, so borrow {base} from the next column: {t} + {base} − {y} = {d}.'
            else:
                d, c2 = t - y, 0
                note = f'{_col(i)}: {x} − 1 (lent to the column on the right) = {t}, and {t} − {y} = {d}.' if c else f'{_col(i)}: {x} − {y} = {d}.'
        res[col] = DIGITS[d]
        c = c2
        if c:
            carry[col - 1] = '1'
        steps.append(step(note, view([col])))
    if c and op == '+':
        res[0] = '1'
        steps.append(step(f'The last carry 1 becomes the leading digit.', view([0])))
    elif c:
        raise SystemExit('The subtraction would be negative')
    result = ''.join(res).lstrip('0') or '0'
    steps.append(step(f'The result is {num(result, base)}.', view([]), line(f'Result: {result}', 'steps-time')))
    return steps, result


def arith_animation(qid, spec):
    steps, result = column_steps(spec['a'], spec['b'], spec['base'], spec['op'].replace('−', '-'), spec.get('intro'))
    want = value_of(spec['a'], spec['base']) + (1 if spec['op'] == '+' else -1) * value_of(spec['b'], spec['base'])
    if value_of(result, spec['base']) != want:
        raise SystemExit(f'Animation for {qid}: column arithmetic disagrees with the value')
    _check(qid, 'result', result, spec['expect']['result'])
    return _finish('base-arith', [dict(short='Columns', title=f'{spec["a"]} {spec["op"].replace("-", "−")} {spec["b"]} in base {spec["base"]}', steps=steps)])


# ---------------------------------------------------------------- signed representations

def twos(bits):
    return int(bits, 2) - (1 << len(bits) if bits[0] == '1' else 0)


def sign_magnitude(bits):
    m = int(bits[1:], 2)
    return -m if bits[0] == '1' else m


def invert(bits):
    return ''.join('1' if b == '0' else '0' for b in bits)


def add_bits(a, b, cin=0):
    """Ripple addition. Returns the sum bits and carries[i] = carry into column i (0 = leftmost), plus carry out."""
    n = len(a)
    carry, out, c = [0] * (n + 1), [''] * n, cin
    carry[n] = cin
    for i in reversed(range(n)):
        t = int(a[i]) + int(b[i]) + c
        out[i], c = str(t % 2), t // 2
        carry[i] = c
    return ''.join(out), carry  # carry[i] for i < n is the carry OUT of column i; carry[n] is carry-in


def _powers(m):
    return ' + '.join(str(1 << k) for k in reversed(range(m.bit_length())) if m >> k & 1) or '0'


def _hex(bits):
    return ''.join(DIGITS[int(bits[i:i + 4], 2)] for i in range(0, len(bits), 4))


def _nibbles(bits):
    return ' '.join(bits[i:i + 4] for i in range(0, len(bits), 4)) if len(bits) % 4 == 0 else bits


def _gaps(n):
    return [k for k in range(1, n) if (n - k) % 4 == 0] if n > 8 and n % 4 == 0 else []


def encode_animation(qid, spec):
    """Write a decimal integer in n-bit two's complement: magnitude, invert, add one."""
    v, n = spec['value'], spec['bits']
    lo, hi = -(1 << n - 1), (1 << n - 1) - 1
    if not lo <= v <= hi:
        raise SystemExit(f'Animation for {qid}: {v} does not fit in {n} bits')
    m = abs(v)
    mag = format(m, f'0{n}b')
    gaps = _gaps(n)
    steps = [step(f'{n}-bit two\'s complement holds {show(lo)} to {hi}, so {show(v)} fits.' +
                  (' Write the magnitude in binary, invert every bit, then add 1.' if v < 0 else ' A positive number is stored as ordinary binary with leading zeros.')),
             step(f'{m} = {_powers(m)}, so in {n} bits it is {_nibbles(mag)}.', grid([(f'{m}', list(mag), '')], gaps=gaps))]
    result = mag
    if v < 0:
        inv = invert(mag)
        steps.append(step(f'Invert every bit: {_nibbles(inv)}.', grid([(f'{m}', list(mag), 'muted'), ('invert', list(inv), '')], gaps=gaps)))
        result, carry = add_bits(inv, '0' * (n - 1) + '1')
        crow = [str(c) if c else '' for c in carry[1:]]
        steps.append(step(f'Add 1: {_nibbles(result)}.', grid([('carry', crow, 'carry'), ('invert', list(inv), ''), ('+1', [''] * (n - 1) + ['1'], ''), ('=', list(result), 'sum')], gaps=gaps)))
    if twos(result) != v:
        raise SystemExit(f'Animation for {qid}: encoding check failed')
    out = dict(bits=result)
    final = f'So {show(v)} is {_nibbles(result)} in {n}-bit two\'s complement.'
    blocks = [grid([('=', list(result), 'sum')], gaps=gaps)]
    if n % 4 == 0:
        out['hex'] = _hex(result)
        final = final[:-1] + f', or {out["hex"]} in hexadecimal.'
        blocks.append(groups('Hex', [(DIGITS[int(result[i:i + 4], 2)], result[i:i + 4], 3, False) for i in range(0, n, 4)]))
    steps.append(step(final, *blocks, line(f'Result: {out.get("hex") if spec.get("show") == "hex" else _nibbles(result)}', 'steps-time')))
    for k, w in spec['expect'].items():
        _check(qid, k, out[k], w)
    return _finish('signed-encode', [dict(short='Encode', title=f'{show(v)} in {n}-bit two\'s complement', steps=steps)])


def _decode_work(p):
    """Steps that read one two's-complement pattern."""
    n, v = len(p), twos(p)
    gaps = _gaps(n)
    if p[0] == '0':
        return v, [step(f'{p} starts with 0, so it is positive: {_powers(v)} = {v}.', grid([('bits', list(p), '')], gaps=gaps))]
    inv = invert(p)
    mag, _ = add_bits(inv, '0' * (n - 1) + '1')
    if int(mag, 2) % (1 << n) != -v % (1 << n):
        raise SystemExit(f'Decoding check failed for {p}')
    return v, [step(f'{p} starts with 1, so it is negative. Invert the bits: {inv}.', grid([('bits', list(p), 'muted'), ('invert', list(inv), '')], gaps=gaps)),
               step(f'Add 1: {mag} = {int(mag, 2)}, so {p} is {show(v)}.', grid([('bits', list(p), 'muted'), ('invert', list(inv), 'muted'), ('+1', list(mag), 'sum')], gaps=gaps))]


def decode_animation(qid, spec):
    """Read two's-complement patterns; optionally test each against a target value or a divisor."""
    pats, test = spec['patterns'], spec.get('test', {})
    head = ['Pattern', 'Value'] + (['Check'] if test else [])
    rows, marks, values, match = [], [], [], []
    intro = 'A leading 0 means the number is positive. A leading 1 means negative: invert the bits and add 1 to get its size.'
    if 'equals' in test:
        intro += f' Look for the pattern whose value is {show(test["equals"])}.'
    steps = [step(intro)]
    divisor = None
    if 'divisible_by' in test:
        divisor, work = _decode_work(test['divisible_by'])
        work[-1]['note'] += ' This is the divisor.'
        for w in work:
            w['blocks'].append(line(f'Divisor: {test["divisible_by"]}'))
        steps += work
    for p in pats:
        v, work = _decode_work(p)
        values.append(v)
        ok, check = False, ''
        if 'equals' in test:
            ok = v == test['equals']
            check = 'match' if ok else 'no'
            work[-1]['note'] += ' That is the one.' if ok else ''
        elif divisor is not None:
            ok = v % divisor == 0
            dv = f'({show(divisor)})' if divisor < 0 else show(divisor)
            check = f'÷ {dv} = {show(Fraction(v, divisor))}'
            work[-1]['note'] += f' {show(v)} ÷ {dv} = {show(Fraction(v, divisor))}' + (', a whole number.' if ok else ', not a whole number.')
        if ok:
            match.append(p)
        rows.append([p, show(v)] + ([check] if test else []))
        marks = [m if m != 'is-running' else None for m in marks] + ['is-running']
        for w in work:
            w['blocks'].append(table(head, rows, len(rows) - 1, [0], marks))
        steps += work
        marks[-1] = ('is-good' if ok else 'is-probed') if test else None
    if test:
        final = (f'Only {match[0]} works.' if len(match) == 1 else 'These work: ' + ', '.join(match) + '.') if match else 'None works.'
        result = ', '.join(match)
    else:
        final = ('So the value is ' + show(values[0]) + '.') if len(values) == 1 else 'Values: ' + ', '.join(show(v) for v in values) + '.'
        result = ', '.join(show(v) for v in values)
    steps.append(step(final, table(head, rows, None, [0], marks), line(f'Result: {result}', 'steps-time')))
    out = dict(values=values, match=match)
    for k, w in spec['expect'].items():
        _check(qid, k, out[k], w)
    return _finish('signed-decode', [dict(short='Decode', title="Two's complement", steps=steps)])


_OP = re.compile(r'(?P<k>\d+)\*?(?P<x>[A-Za-z]\w*|[01]+)|(?P<neg>-?)(?P<a>[A-Za-z]\w*|[01]+)(?P<op>[+-])(?P<b>[A-Za-z]\w*|[01]+)')


def signed_ops_animation(qid, spec):
    n, rep, names = spec['bits'], spec.get('repr', 'twos'), spec.get('operands', {})

    def bits_of(tok):
        b = names.get(tok, tok)
        if len(b) != n or set(b) - set('01'):
            raise SystemExit(f'Animation for {qid}: {tok} is not a {n}-bit pattern')
        return b

    if rep == 'sign-magnitude':
        return _sm_ops(qid, spec, n, bits_of)
    if rep != 'twos':
        raise SystemExit(f'Animation for {qid}: unknown representation {rep}')
    lo, hi = -(1 << n - 1), (1 << n - 1) - 1
    schedules, overflow, results = [], [], {}
    for label in spec['ops']:
        m = _OP.fullmatch(label.replace('−', '-').replace(' ', ''))
        if not m or m['neg']:
            raise SystemExit(f'Animation for {qid}: cannot read the operation {label}')
        gaps = _gaps(n)
        if m['k']:
            k, x = int(m['k']), m['x']
            if k == 2:
                a_tok, b_tok, op = x, x, '+'
            else:
                steps, res, over = _shift_steps(bits_of(x), x, k, n, lo, hi)
                schedules.append(dict(short=label, title=f'{label} in {n}-bit two\'s complement', steps=steps))
                results[label] = _hex(res) if n % 4 == 0 else res
                if over:
                    overflow.append(label)
                continue
        else:
            a_tok, b_tok, op = m['a'], m['b'], m['op']
        A, B = bits_of(a_tok), bits_of(b_tok)
        va, vb = twos(A), twos(B)
        true = va + vb if op == '+' else va - vb
        B2, cin = (B, 0) if op == '+' else (invert(B), 1)
        S, carry = add_bits(A, B2, cin)
        say = lambda tok, bits: f'{tok} = {bits}' if tok in names else bits
        intro = (f'{say(a_tok, A)} is {show(va)}' + ('' if a_tok == b_tok else f' and {say(b_tok, B)} is {show(vb)}') +
                 f'. {n} bits hold {show(lo)} to {hi}.')
        if m['k']:
            intro += f' 2{x} is {x} + {x}.'
        if op == '-':
            intro += f' To subtract, add {b_tok} with every bit inverted ({B2}) and a carry of 1 into the rightmost column.'
        crow, srow = [''] * (n + 1), [''] * (n + 1)
        if cin:
            crow[n] = '1'
        rows = lambda: grid([('carry', crow, 'carry'), (a_tok, [''] + list(A), ''), ('+', [''] + list(B2), ''), ('=', srow, 'sum')], now_cols, [g + 1 for g in gaps])
        now_cols = []
        steps = [step(intro, rows())]
        c = cin
        for j in range(n):
            col = n - 1 - j
            t = int(A[col]) + int(B2[col]) + c
            srow[col + 1] = str(t % 2)
            note = f'{_col(j)}: {A[col]} + {B2[col]}' + (f' + carry {c}' if c else '') + f' = {t}: write {t % 2}' + (', carry 1.' if t >= 2 else '.')
            c = t // 2
            if c:
                crow[col] = '1'
            now_cols = [col + 1]
            steps.append(step(note, rows()))
        c_in_sign, c_out = carry[1], carry[0]
        over = c_in_sign != c_out
        if over != (not lo <= true <= hi):
            raise SystemExit(f'Animation for {qid}: carry rule and range disagree for {label}')
        if not over and twos(S) != true:
            raise SystemExit(f'Animation for {qid}: sum check failed for {label}')
        now_cols = [0, 1]
        verdict = (f'The carry into the sign bit is {c_in_sign} and the carry out is {c_out}. ' +
                   (f'They differ, so this overflows: the true value {show(true)} is outside {show(lo)} to {hi}, and {S} would read as {show(twos(S))}.' if over else
                    f'They agree, so there is no overflow: {S} is {show(true)}.'))
        steps.append(step(verdict, rows(), line(('Overflow' if over else 'No overflow') + f': {label} = {show(true)}', 'steps-time')))
        if over:
            overflow.append(label)
        results[label] = S
        schedules.append(dict(short=label, title=f'{label} in {n}-bit two\'s complement', steps=steps))
    out = dict(overflow=overflow, results=results)
    for k, w in spec['expect'].items():
        _check(qid, k, out[k] if k != 'results' else {x: out[k][x] for x in w}, w)
    return _finish('signed-ops', schedules)


def _shift_steps(P, x, k, n, lo, hi):
    s = _log2(k)
    v = twos(P)
    true = k * v
    gaps = _gaps(n)
    rows = [(x, list(P), '')]
    steps = [step(f'{x} = {_hex(P) if n % 4 == 0 else P} is {_nibbles(P)} = {show(v)}. Multiplying by {k} shifts left {s} places, one place per doubling.',
                  grid(rows, gaps=gaps))]
    cur = P
    for j in range(1, s + 1):
        cur = cur[1:] + '0'
        rows = [(r[0], r[1], 'muted') for r in rows] + [(f'×{1 << j}', list(cur), '')]
        steps.append(step(f'Shift left {"once" if j == 1 else "once more"} (×{1 << j}): the leftmost bit drops off and a 0 comes in on the right. {_nibbles(cur)} is {show(twos(cur))}.', grid(rows, gaps=gaps)))
    over = not lo <= true <= hi
    if not over and twos(cur) != true:
        raise SystemExit('shift check failed')
    hexed = _hex(cur) if n % 4 == 0 else cur
    steps.append(step(f'{k} × ' + (f'({show(v)})' if v < 0 else show(v)) + f' = {show(true)}, ' + (f'outside {show(lo)} to {hi}: overflow.' if over else f'inside {show(lo)} to {hi}, so no overflow. The result is {hexed}' + (' in hexadecimal.' if n % 4 == 0 else '.')),
                      grid(rows[-1:], gaps=gaps), groups('Hex', [(DIGITS[int(cur[i:i + 4], 2)], cur[i:i + 4], 3, False) for i in range(0, n, 4)]) if n % 4 == 0 else None,
                      line(f'Result: {hexed}', 'steps-time')))
    return steps, cur, over


def _sm_ops(qid, spec, n, bits_of):
    names = spec['operands']
    hi = (1 << n - 1) - 1
    vals = {k: sign_magnitude(bits_of(k)) for k in names}
    steps = [step(f'Sign-magnitude: 1 sign bit and {n - 1} magnitude bits, so the values run from −{hi} to +{hi}. Decode the operands, work out each result and check the range.')]
    for k, b in names.items():
        mag = int(b[1:], 2)
        steps.append(step(f'{k} = {b}: sign {b[0]} ({"negative" if b[0] == "1" else "positive"}), magnitude {b[1:]} = {_powers(mag)} = {mag}, so {k} = {show(vals[k])}.',
                          groups(k, [('sign', b[0], 1, False), ('magnitude', b[1:], 0, False)])))
    head, rows, marks, bad = ['Operation', 'Value', 'Fits?'], [], [], []
    for label in spec['ops']:
        m = _OP.fullmatch(label.replace('−', '-').replace(' ', ''))
        if not m or m['k']:
            raise SystemExit(f'Animation for {qid}: cannot read the operation {label}')
        a, b = vals[m['a']], vals[m['b']]
        a2 = -a if m['neg'] else a
        v = a2 + b if m['op'] == '+' else a2 - b
        fits = -hi <= v <= hi
        if not fits:
            bad.append(label)
        sa = (f'−({show(a)})' if a < 0 else f'−{a}') if m['neg'] else show(a)
        sb = f'({show(b)})' if b < 0 else show(b)
        rows.append([label, show(v), 'yes' if fits else 'no'])
        marks = [x if x != 'is-running' else None for x in marks] + ['is-running']
        steps.append(step(f'{label} = {sa} {"+" if m["op"] == "+" else "−"} {sb} = {show(v)}, ' + ('which fits.' if fits else f'outside −{hi} to +{hi}: it cannot be represented.'),
                          table(head, rows, len(rows) - 1, [], marks)))
        marks[-1] = 'is-probed' if fits else 'is-good'
    steps.append(step('Not representable: ' + (', '.join(bad) if bad else 'none') + '.', table(head, rows, None, [], marks), line('Overflow: ' + (', '.join(bad) or 'none'), 'steps-time')))
    for k, w in spec['expect'].items():
        _check(qid, k, {'overflow': bad}[k], w)
    return _finish('signed-ops', [dict(short='Sign-magnitude', title=f'{n}-bit sign-magnitude', steps=steps)])


# ---------------------------------------------------------------- IEEE-754 binary32

def f32_decode(bits):
    s, e, f = bits[0], int(bits[1:9], 2), int(bits[9:], 2)
    sign = -1 if s == '1' else 1
    if e == 255:
        return ('infinity' if f == 0 else 'NaN'), None
    if e == 0:
        return ('zero', Fraction(0)) if f == 0 else ('subnormal', sign * Fraction(f, 1 << 23) * Fraction(1, 1 << 126))
    return 'normal', sign * (1 + Fraction(f, 1 << 23)) * Fraction(2) ** (e - 127)


def f32_encode(v):
    """Exact binary32 bits of v, or SystemExit if v needs rounding or is out of the normal range."""
    if v == 0:
        return '0' * 32, 0, Fraction(0)
    m, e = abs(Fraction(v)), 0
    while m >= 2:
        m, e = m / 2, e + 1
    while m < 1:
        m, e = m * 2, e - 1
    if not -126 <= e <= 127:
        raise SystemExit(f'{v} is outside the normal binary32 range')
    f = (m - 1) * (1 << 23)
    if f.denominator != 1:
        raise SystemExit(f'{v} is not exactly representable in binary32')
    return ('1' if v < 0 else '0') + format(e + 127, '08b') + format(int(f), '023b'), e, m


def _fields(bits, now=None):
    return groups('Fields', [('sign', bits[0], 1, now == 0), ('exponent', bits[1:9], 0, now == 1), ('fraction', bits[9:], 2, now == 2)])


def _hexgroups(bits):
    return groups('Hex', [(DIGITS[int(bits[i:i + 4], 2)], bits[i:i + 4], 3, False) for i in range(0, 32, 4)])


def _frac_short(f):
    t = f.rstrip('0')
    return (t + ' then zeros') if t else 'all zeros'


def _frac_terms(f):
    ones = [k + 1 for k, b in enumerate(f) if b == '1']
    if not ones:
        return '0'
    if len(ones) > 6:
        return show(Fraction(int(f, 2), 1 << 23))
    return ' + '.join(f'1/{1 << k}' for k in ones) + (f' = {show(sum(Fraction(1, 1 << k) for k in ones))}' if len(ones) > 1 else '')


def _summary(bits):
    cls, v = f32_decode(bits)
    e = int(bits[1:9], 2)
    sig = 1 + Fraction(int(bits[9:], 2), 1 << 23)
    if cls != 'normal':
        return cls, v, f'{cls}'
    return cls, v, f'{"−" if bits[0] == "1" else ""}{show(sig)} × 2{sup(e - 127)}'


def decode_f32_steps(bits, source):
    """Detailed decode of one binary32 pattern."""
    head, rows = ['Field', 'Meaning'], []
    steps = []
    if source.get('hex'):
        steps.append(step(f'Write {source["hex"]} in binary, 4 bits for each hex digit.', _hexgroups(bits)))
    steps.append(step('Split the 32 bits: 1 sign bit, 8 exponent bits, 23 fraction bits.', _fields(bits)))
    cls, v = f32_decode(bits)
    s, e, f = bits[0], bits[1:9], bits[9:]
    rows.append(['Sign', 'negative' if s == '1' else 'positive'])
    steps.append(step(f'The sign bit is {s}, so the number is {"negative" if s == "1" else "positive"}.', _fields(bits, 0), table(head, rows, 0)))
    E = int(e, 2)
    if cls == 'normal':
        rows.append(['Exponent', f'{E} − 127 = {E - 127}'])
        note = f'The exponent bits {e} are {E}. Subtract the bias 127: the power of two is {show(E - 127)}.'
    else:
        rows.append(['Exponent', 'all ' + ('zeros' if E == 0 else 'ones') + ': special'])
        note = f'The exponent bits are all {"zeros" if E == 0 else "ones"}, which is reserved for special values.'
    steps.append(step(note, _fields(bits, 1), table(head, rows, 1)))
    F = int(f, 2)
    if cls == 'normal':
        sig = 1 + Fraction(F, 1 << 23)
        rows.append(['Fraction', f'1 + {show(Fraction(F, 1 << 23))} = {show(sig)}'])
        note = (f'The fraction bits .{f.rstrip("0") or "0"} are {_frac_terms(f)}. ' if F else 'The fraction bits are all zero. ') + \
               f'Put back the hidden leading 1: the significand is {binary_text(sig)}₂ = {show(sig)}.'
        steps.append(step(note, _fields(bits, 2), table(head, rows, 2)))
        steps.append(step(f'Value = {"−" if s == "1" else ""}{show(sig)} × 2{sup(E - 127)} {eq(v)}.', _fields(bits), table(head, rows, None),
                          line(f'Value: {show(v)}', 'steps-time')))
    else:
        rows.append(['Fraction', 'zero' if F == 0 else 'not zero'])
        what = {'zero': f'the special value {"−" if s == "1" else "+"}0, not a normalized number', 'subnormal': 'a subnormal number',
                'infinity': f'{"−" if s == "1" else "+"}infinity', 'NaN': 'NaN (not a number)'}[cls]
        steps.append(step(f'The fraction is {"zero" if F == 0 else "not zero"}, so this is {what}.', _fields(bits, 2), table(head, rows, 2)))
        steps.append(step(f'So the pattern is {what}.', _fields(bits), table(head, rows, None), line(f'Value: {what}', 'steps-time')))
    return steps, cls, v


def _sig(m):
    t = binary_text(m)
    return t if '.' in t else t + '.0'


def encode_f32_steps(v, label=None):
    bits, e, m = f32_encode(v)
    head, rows = ['Field', 'Bits', 'Why'], []
    a = abs(Fraction(v))
    label = label or show(v)
    norm = f'{_sig(m)}₂ × 2{sup(e)}'
    rows.append(['Sign', bits[0], 'negative' if v < 0 else 'positive'])
    steps = [step(f'{label} is {"negative" if v < 0 else "positive"}, so the sign bit is {bits[0]}.', table(head, rows, 0, [1]))]
    if len(dec(a)) > 12:
        steps.append(step(f'In binary the value is already of the form 1.x × 2^e: {norm}.', table(head, rows, None, [1]), line(f'Value = {norm}')))
        tag = f'Value = {norm}'
    else:
        whole, frac = int(a), a - int(a)
        parts = []
        if whole:
            parts.append(f'{whole} = {to_base(whole, 2)}₂')
        if frac:
            parts.append(f'{show(frac)} = {binary_text(frac)[1:] if whole else binary_text(frac)}₂')
        bt = binary_text(a)
        steps.append(step(' and '.join(parts) + (f', so {show(a)} = {bt}₂.' if whole and frac else '.'), table(head, rows, None, [1]), line(f'{show(a)} = {bt}₂')))
        steps.append(step((f'Move the binary point {abs(e)} place{"s" if abs(e) > 1 else ""} {"left" if e > 0 else "right"} so a single 1 is in front: {norm}.' if e else f'It is already of the form 1.x: {norm}.'),
                          table(head, rows, None, [1]), line(f'{show(a)} = {norm}')))
        tag = f'{show(a)} = {norm}'
    rows.append(['Exponent', bits[1:9], f'{show(e)} + 127 = {e + 127}'])
    steps.append(step(f'Biased exponent: {show(e)} + 127 = {e + 127} = {bits[1:9]}₂.', table(head, rows, 1, [1]), line(tag)))
    rows.append(['Fraction', _frac_short(bits[9:]), 'bits after the leading 1'])
    steps.append(step(f'The leading 1 is not stored. The fraction field holds the bits after the point: {_frac_short(bits[9:])}.', table(head, rows, 2, [1]), line(tag)))
    hx = _hex(bits)
    steps.append(step(f'Sign {bits[0]}, exponent {show(e)} (stored as {bits[1:9]}), fraction {_frac_short(bits[9:])}. Read the 32 bits in groups of four: {hx}.',
                      _fields(bits), _hexgroups(bits), line(f'Result: {hx}', 'steps-time')))
    return steps, bits, e


def ieee_animation(qid, spec):
    out, schedules = {}, []
    if 'encode' in spec:
        v = Fraction(spec['encode'])
        steps, bits, e = encode_f32_steps(v)
        out.update(hex=_hex(bits), exponent=e, fraction=bits[9:])
        schedules.append(dict(short='Encode', title=f'{show(v)} in IEEE-754 single precision', steps=steps))
    elif 'decode' in spec or 'bits' in spec or 'fields' in spec:
        if 'decode' in spec:
            bits, source = format(int(spec['decode'], 16), '032b'), dict(hex=spec['decode'])
        elif 'bits' in spec:
            bits, source = spec['bits'], {}
        else:
            fl = spec['fields']
            bits, source = fl['s'] + fl['e'] + fl['f'], {}
        if len(bits) != 32:
            raise SystemExit(f'Animation for {qid}: a binary32 pattern has 32 bits')
        steps, cls, v = decode_f32_steps(bits, source)
        out.update({'class': cls, 'value': dec(v) if v is not None else None})
        if 'options' in spec:
            opts = {k: Fraction(x) for k, x in spec['options'].items()}
            best = min(opts, key=lambda k: abs(opts[k] - v))
            if sum(1 for k in opts if abs(opts[k] - v) == abs(opts[best] - v)) > 1:
                raise SystemExit(f'Animation for {qid}: two options are equally close')
            rows = [[k, show(opts[k]), show(abs(opts[k] - v))] for k in opts]
            marks = ['is-good' if k == best else 'is-probed' for k in opts]
            steps[-1].pop('final', None)
            steps.append(step(f'Compare {show(v)} with the offered values: {best} is the closest.', table(['Option', 'Value', 'Distance'], rows, None, [], marks),
                              line(f'Closest: {best}', 'steps-time')))
            out['closest'] = best
        schedules.append(dict(short='Decode', title='IEEE-754 single precision', steps=steps))
    elif 'registers' in spec:
        regs = {k: format(int(h, 16), '032b') for k, h in spec['registers'].items()}
        env, rows, steps = {}, [], []
        head = ['Name', 'Hex', 'Value']
        steps.append(step('Decode each register: value = (−1)^sign × 1.fraction × 2^(exponent − 127).'))
        for k, bits in regs.items():
            cls, v, form = _summary(bits)
            if cls != 'normal':
                raise SystemExit(f'Animation for {qid}: {k} is not a normal number')
            env[k] = v
            E = int(bits[1:9], 2)
            rows.append([k, spec['registers'][k], form if eq(v).startswith('≈') else f'{form} {eq(v)}'])
            steps.append(step(f'{k} = {spec["registers"][k]}: sign {bits[0]}, exponent {bits[1:9]} = {E}, so 2{sup(E - 127)}; fraction .{bits[9:].rstrip("0") or "0"} gives significand {binary_text(1 + Fraction(int(bits[9:], 2), 1 << 23))}₂. {k} = {form}{" " + eq(v) if not eq(v).startswith("≈") else ""}.',
                              _fields(bits), table(head, rows, len(rows) - 1, [1])))
        decoded = table(head, rows, None, [1])
        if 'compute' in spec:
            e = parse_expr(spec['compute'])
            v = evaluate(e, env)
            note = f'{spec["compute"].replace("/", " ÷ ")} = {fmt(e, env)} {eq(v)}.'
            if e[0] == 'bin' and e[1] == '+' and e[2][0] == e[3][0] == 'var':
                note = _align_note(e[2][1], e[3][1], regs, env) or note
            steps.append(step(note, decoded, line(f'{spec["compute"]} {eq(v)}')))
            more, bits, _ = encode_f32_steps(v, spec['compute'].replace('/', ' ÷ ').replace('+', ' + '))
            steps += more
            out['hex'] = _hex(bits)
        if 'statements' in spec:
            srows, marks, truth = [], [], {}
            for text in spec['statements']:
                e = parse_expr(text)
                if e[0] != 'cmp':
                    raise SystemExit(f'Animation for {qid}: {text} is not a statement')
                ok = evaluate(e, env)
                truth[text] = ok
                L, R = evaluate(e[2], env), evaluate(e[3], env)
                note = f'{text}: the left side is {side(e[2], env)} and the right side is {side(e[3], env)}, so it is {"true" if ok else "false"}.'
                rel = e[1] if ok else {'=': '≠', '>': '≤', '<': '≥'}[e[1]]
                srows.append([text, f'{show(L)} {rel} {show(R)}', 'true' if ok else 'false'])
                marks = [m if m != 'is-running' else None for m in marks] + ['is-running']
                steps.append(step(note, decoded, table(['Statement', 'Values', ''], srows, len(srows) - 1, [], marks)))
                # Highlight what the question asks for: the true statements, or the false ones.
                marks[-1] = 'is-good' if ok != ('false' in spec['expect']) else 'is-probed'
            out['true'] = [t for t in spec['statements'] if truth[t]]
            out['false'] = [t for t in spec['statements'] if not truth[t]]
            steps.append(step('True: ' + (', '.join(out['true']) or 'none') + '. False: ' + (', '.join(out['false']) or 'none') + '.', decoded,
                              table(['Statement', 'Values', ''], srows, None, [], marks)))
        schedules.append(dict(short='Registers', title='IEEE-754 single precision', steps=steps))
    elif 'choices' in spec:
        rows, marks, steps, vals = [], [], [], {}
        head = ['Choice', 'Value']
        steps.append(step('Decode each choice. An exponent of all ones is reserved for infinity and NaN, which are not ordinary numbers.'))
        for label, fl in spec['choices'].items():
            bits = fl['s'] + fl['e'] + fl['f']
            cls, v, form = _summary(bits)
            E = int(fl['e'], 2)
            if cls == 'normal':
                vals[label] = v
                note = f'{label}: exponent {E} − 127 = {E - 127} and significand {show(1 + Fraction(int(fl["f"], 2), 1 << 23))}, so the value is {show(v)}.'
                rows.append([label, f'{form} {eq(v)}'])
            else:
                note = f'{label}: the exponent is {E}' + (' (all ones) and the fraction is not zero, so this is NaN, not a number.' if cls == 'NaN' else f', so this is {cls}.')
                rows.append([label, cls])
                if cls != 'NaN':
                    vals[label] = v
            marks = [m if m != 'is-running' else None for m in marks] + ['is-running']
            steps.append(step(note, _fields(bits), table(head, rows, len(rows) - 1, [], marks, wrap=[0, 1])))
            marks[-1] = None
        best = max(vals, key=lambda k: vals[k])
        marks = ['is-good' if r[0] == best else 'is-probed' for r in rows]
        steps.append(step(f'The largest number is {best}.', table(head, rows, None, [], marks, wrap=[0, 1]), line(f'Largest: {best}', 'steps-time')))
        out['largest'] = best
        schedules.append(dict(short='Compare', title='IEEE-754 single precision', steps=steps))
    else:
        raise SystemExit(f'Animation for {qid}: nothing to do')
    for k, w in spec['expect'].items():
        _check(qid, k, out.get(k), w)
    return _finish('ieee754', schedules)


def _align_note(a, b, regs, env):
    """X + Y for two normal numbers of the same sign: line up the exponents and add significands."""
    ea, eb = int(regs[a][1:9], 2) - 127, int(regs[b][1:9], 2) - 127
    if regs[a][0] != regs[b][0]:
        return None
    if ea < eb:
        a, b, ea, eb = b, a, eb, ea
    sa, sb = abs(env[a]) / Fraction(2) ** ea, abs(env[b]) / Fraction(2) ** ea
    total = sa + sb
    note = f'Line up the exponents: {b} = {binary_text(abs(env[b]) / Fraction(2) ** eb)}₂ × 2{sup(eb)} = {binary_text(sb)}₂ × 2{sup(ea)}. ' if ea != eb else ''
    note += f'Add the significands: {binary_text(sa)}₂ + {binary_text(sb)}₂ = {binary_text(total)}₂, so {a} + {b} = {binary_text(total)}₂ × 2{sup(ea)}.'
    return note


# ---------------------------------------------------------------- Booth recoding

def booth_animation(qid, spec):
    q, mcand = spec['multiplier'].replace(' ', ''), spec['multiplicand'].replace(' ', '')
    n = len(q)
    bits = list(q) + ['0']
    action = [''] * n
    adds = subs = 0
    gaps = [k for k in range(1, n) if (n - k) % 4 == 0] + [n]

    def view(now):
        return grid([('Q', bits, ''), ('+/−', action + [''], 'sum')], now, gaps)
    if set(q + mcand) - set('01'):
        raise SystemExit(f'Animation for {qid}: Booth operands must be bit strings')
    steps = [step('Radix-2 Booth reads the multiplier Q from the right, one bit with the bit to its right (a 0 is appended after the last bit). '
                  'The pair 10 subtracts the multiplicand M (−), 01 adds it (+), and 00 or 11 does nothing (·). Only Q decides the count; M is ' + _nibbles(mcand) + '.', view([n]))]
    for i in range(n):
        col = n - 1 - i
        pair = bits[col] + bits[col + 1]
        if pair == '10':
            subs += 1
            action[col], what = '−', 'subtract M'
        elif pair == '01':
            adds += 1
            action[col], what = '+', 'add M'
        else:
            action[col], what = '·', 'no arithmetic'
        steps.append(step(f'i = {i}: q{sub(i)} q{sub(i - 1) if i else "₋₁"} = {pair}, so {what}. So far {adds} addition{"s" * (adds != 1)} and {subs} subtraction{"s" * (subs != 1)}.',
                          view([col, col + 1])))
    total = adds + subs
    steps.append(step(f'In all: {adds} additions + {subs} subtractions = {total} operations on the multiplicand.', view([]), line(f'Total: {total}', 'steps-time')))
    _check(qid, 'count', total, spec['expect']['count'])
    return _finish('booth', [dict(short='Booth', title='Radix-2 Booth recoding of Q', steps=steps)])


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'radix-convert': convert_animation, 'radix-compare': compare_animation, 'radix-equation': equation_animation,
         'base-arith': arith_animation, 'signed-encode': encode_animation, 'signed-decode': decode_animation,
         'signed-ops': signed_ops_animation, 'ieee754': ieee_animation, 'booth': booth_animation}
PLAYER = 'numbers'
TABS = 'options'  # signed-ops shows one tab per offered operation
