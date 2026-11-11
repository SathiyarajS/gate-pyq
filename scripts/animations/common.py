"""Helpers shared by the step-through families."""
from fractions import Fraction


def _fmt(x):
    x = Fraction(x).limit_denominator(1000)
    return str(x.numerator) if x.denominator == 1 else ('%.2f' % float(x)).rstrip('0').rstrip('.')


def _list(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]


def _same(value, expect):
    if isinstance(expect, list):
        return value == expect
    if isinstance(expect, str):
        return str(value) == expect
    return abs(float(value) - float(expect)) < 1e-9


def _log2(n, what):
    if n <= 0 or n & (n - 1):
        raise SystemExit(f'{what} = {n} is not a power of two')
    return n.bit_length() - 1


def _size(n, unit='B'):
    """2^k units in binary prefixes: 32768 B -> '32 KB'."""
    for p, name in ((60, 'E'), (50, 'P'), (40, 'T'), (30, 'G'), (20, 'M'), (10, 'K')):
        if n >= 1 << p and n % (1 << p) == 0:
            return f'{n >> p} {name}{unit}'
    return f'{n}{unit}' if unit.startswith(' ') else f'{n} {unit}'
