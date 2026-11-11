"""Hashing: chaining, linear and quadratic probing, double hashing.

Data: data/animations/hashing.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from fractions import Fraction

from .common import _fmt, _list


HASH_METHODS = {'chaining': 'Separate chaining', 'linear': 'Open addressing, linear probing',
                'quadratic': 'Open addressing, quadratic probing', 'double': 'Open addressing, double hashing'}


def _hash_text(spec):
    a, b, m = spec.get('a', 1), spec.get('b', 0), spec['size']
    inner = ('k' if a == 1 else f'{a}k') + (f' + {b}' if b else '')
    return (f'({inner}) mod {m}' if b or a != 1 else f'k mod {m}'), (lambda k: (a * k + b) % m)


def hash_insert(spec):
    """Insert keys in order. Returns the table after each key and a note on the probes."""
    m, method, keys = spec['size'], spec['method'], spec['keys']
    if method not in HASH_METHODS:
        raise SystemExit('Unknown hashing method: ' + method)
    text, h = _hash_text(spec)
    if method == 'double':
        c, d = spec['h2']['c'], spec['h2']['d']
        h2 = lambda k: c + k % d
    table = [[] for _ in range(m)] if method == 'chaining' else [None] * m
    steps = [dict(key=None, table=_copy(table), slot=None, probed=[], note=f"Empty table with {m} slots (0 to {m - 1}). h(k) = {text}; {HASH_METHODS[method].lower()}." + (f" Probe i uses (h(k) + i·h2(k)) mod {m}, with h2(k) = {c} + (k mod {d})." if method == 'double' else ''))]
    for k in keys:
        home = h(k)
        if method == 'chaining':
            table[home].append(k)
            steps.append(dict(key=k, table=_copy(table), slot=home, probed=[], note=f"h({k}) = {home}. {k} joins the chain at slot {home}" + (f", which now holds {len(table[home])} keys." if len(table[home]) > 1 else '.')))
            continue
        probed, note = [], f"h({k}) = {home}."
        if method == 'double':
            step2 = h2(k)
            note += f" h2({k}) = {c} + ({k} mod {d}) = {step2}."
        for i in range(m):
            slot = (home + (i if method == 'linear' else i * i if method == 'quadratic' else i * step2)) % m
            if table[slot] is None:
                break
            probed.append(slot)
        else:
            raise SystemExit(f'No free slot for {k}')
        if probed:
            hits = _list([f"slot {x} holds {table[x]}" for x in probed])
            note += ' ' + hits[0].upper() + hits[1:] + (', a collision.' if len(probed) == 1 else ': collisions.')
        note += f" Slot {slot} is empty, so {k} goes there."
        table[slot] = k
        steps.append(dict(key=k, table=_copy(table), slot=slot, probed=probed, note=note))
    return steps, table


def _copy(table):
    return [list(x) if isinstance(x, list) else x for x in table]


def hash_animation(qid, spec):
    steps, table = hash_insert(spec)
    expect, m = spec['expect'], spec['size']
    note = 'All done.'
    if 'table' in expect:
        if table != expect['table']:
            raise SystemExit(f'Animation for {qid} ends with {table}, not {expect["table"]}')
        note += ' Final table: ' + ', '.join(f"{i}: {v}" for i, v in enumerate(table) if v not in (None, [])) + '.'
    if 'slot_of' in expect:
        for k, slot in expect['slot_of'].items():
            if table.index(int(k)) != slot:
                raise SystemExit(f'Animation for {qid} puts {k} in slot {table.index(int(k))}, not {slot}')
            note += f' {k} ends up in slot {slot}.'
    if 'empty' in expect:
        empty = [i for i, v in enumerate(table) if v is None]
        if empty != expect['empty']:
            raise SystemExit(f'Animation for {qid} leaves {empty} empty, not {expect["empty"]}')
        note += ' Empty slots: ' + ', '.join(map(str, empty)) + '.'
    if 'chains' in expect:
        lens = [len(x) for x in table]
        got = dict(max=max(lens), min=min(lens), avg=float(Fraction(sum(lens), m)))
        for k, v in expect['chains'].items():
            if abs(got[k] - v) > 1e-9:
                raise SystemExit(f'Animation for {qid}: chain {k} is {got[k]}, not {v}')
        note += f" Chain lengths: {', '.join(map(str, lens))}. Longest {got['max']}, shortest {got['min']}, average {sum(lens)}/{m} = {_fmt(Fraction(sum(lens), m))}."
    steps.append(dict(key=None, table=_copy(table), slot=None, probed=[], final=True, note=note))
    return dict(kind='hash-insert', size=m, chaining=spec['method'] == 'chaining', keys=spec['keys'],
                schedules=[dict(short=HASH_METHODS[spec['method']], title=HASH_METHODS[spec['method']] + ', h(k) = ' + _hash_text(spec)[0], steps=steps)],
                count=len(steps))



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'hash-insert': hash_animation}
PLAYER = 'hashing'
