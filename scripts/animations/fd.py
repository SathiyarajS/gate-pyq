"""Functional dependencies: attribute closure, candidate keys, superkeys,
implied FDs, minimal cover, normal forms, lossless join and dependency
preservation.

Data: data/animations/fd.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.

A spec names the attributes (`attrs`: a string of one-letter names or a list of
names) and the FDs (`fds`: strings such as "AB->C" or "rollno,cno->grade").
`parts` become the player's tabs. A part may override `attrs` and `fds`, or
name a sub-relation (`relation`) whose FDs are then projected from the full set.
`do` lists the work in order: "keys", "superkeys", "nf", "cover", "lossless",
"preserve" (both with `components`), {"closure": X, "claim": Y} and
{"implies": "X->Y"}. Every part has an `expect`.
"""
from itertools import combinations

from .common import _list

NF = ['not 1NF', '1NF', '2NF', '3NF', 'BCNF']
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def _names(attrs):
    names = list(attrs) if isinstance(attrs, str) else list(attrs)
    if not names or len(set(names)) != len(names):
        raise SystemExit(f'Bad attribute list: {attrs}')
    return names


def _parse_seq(text, names):
    """Attribute names in the order written."""
    if isinstance(text, (list, tuple)):
        parts = list(text)
    elif all(len(n) == 1 for n in names):
        parts = [c for c in text if c not in ' ,{}']
    else:
        parts = [p.strip() for p in text.strip(' {}').split(',') if p.strip()]
    for p in parts:
        if p not in names:
            raise SystemExit(f'Unknown attribute {p!r} in {text!r}')
    if not parts:
        raise SystemExit(f'Empty attribute set: {text!r}')
    return parts


def _parse_set(text, names):
    return frozenset(_parse_seq(text, names))


def _parse_fd(text, names):
    if '->' not in text:
        raise SystemExit(f'Bad FD: {text!r}')
    left, right = text.split('->')
    return _parse_set(left, names), _parse_set(right, names)


def closure(x, fds):
    """Attribute closure, firing FDs in list order, pass after pass.
    Returns the closure and [(fd index, attributes it added)]."""
    c, fired, changed = set(x), [], True
    while changed:
        changed = False
        for i, (l, r) in enumerate(fds):
            if l <= c and not r <= c:
                fired.append((i, frozenset(r - c)))
                c |= r
                changed = True
    return frozenset(c), fired


class Rel:
    """One relation: its attributes in order and its FDs (all inside it)."""

    def __init__(self, name, names, fds, labels=None):
        self.name, self.names, self.fds = name, names, fds
        self.labels = dict(zip(fds, labels or []))
        self.pos = {n: i for i, n in enumerate(names)}
        self.single = all(len(n) == 1 for n in names)
        self.all = frozenset(names)

    def order(self, s):
        return sorted(s, key=self.pos.__getitem__)

    def t(self, s):
        """AD, or 'name, courseNo' for longer names."""
        return ('' if self.single else ', ').join(self.order(s))

    def br(self, s):
        return '{' + ', '.join(self.order(s)) + '}'

    def k(self, s):
        """A set named in a sentence: AD, rollno, or {name, courseNo}."""
        return self.t(s) if self.single or len(s) == 1 else self.br(s)

    def f(self, fd):
        """An FD as text; a given FD keeps the order it was written in."""
        return self.labels.get(fd) or f'{self.t(fd[0])} → {self.t(fd[1])}'

    def plus(self, s):
        return f'({self.t(s)})⁺'

    def close(self, s):
        return closure(s, self.fds)

    def is_super(self, s):
        return self.close(s)[0] == self.all

    def split(self):
        return [(i, l, a) for i, (l, r) in enumerate(self.fds) for a in self.order(r - l)]

    def fdlist(self):
        return [self.f(fd) for fd in self.fds]


def _are(s, rel):
    s = rel.order(s)
    return f'{s[0]} is' if len(s) == 1 else f'{_list(s)} are'


def _lst(rel, s):
    return _list(rel.order(s))


def _isare(s):
    return 'is' if len(s) == 1 else 'are'


def _strip(rel, have, new=()):
    return dict(label=None, have=rel.order(have), new=rel.order(new))


def _fired_text(rel, fired):
    return '; '.join(f'{rel.f(rel.fds[i])} adds {_lst(rel, add)}' for i, add in fired)


# ---------- the tasks ----------

def closure_steps(rel, x, steps):
    """Step-by-step closure of x: one step per FD that adds something."""
    c, used = set(x), []
    head = rel.plus(x)
    steps.append(dict(head=head, note=f'Start with {head} = {rel.br(x)}' + (': the attributes of the left side themselves.' if len(x) > 1 else '.'),
                      set=dict(_strip(rel, c, x), label=head), fire=[], used=[]))
    full, fired = rel.close(x)
    for i, add in fired:
        l, r = rel.fds[i]
        c |= add
        already = r - add - set(l)
        note = f'{rel.f(rel.fds[i])} applies because {_are(l, rel)} in the closure, so add {_lst(rel, add)}.'
        if already:
            note = note[:-1] + f' ({_lst(rel, already)} {_isare(already)} already there).'
        steps.append(dict(head=head, note=note, set=dict(_strip(rel, c, add), label=head), fire=[i], used=list(used)))
        used.append(i)
    return full, used


def _verdict_step(rel, x, full, used, text, steps, table=None):
    head = rel.plus(x)
    lead = (f'Nothing else applies, so {head} = {rel.br(full)}. ' if used
            else f'No FD has its whole left side inside {rel.br(x)}, so {head} = {rel.br(full)}. ')
    steps.append(dict(head=head, note=lead + text, set=dict(_strip(rel, full), label=head), fire=[], used=list(used), table=table))


def do_closure(rel, item, steps, out):
    x = _parse_set(item['closure'], rel.names)
    full, used = closure_steps(rel, x, steps)
    out.setdefault('closure', {})[x] = full
    if 'claim' in item:
        claim = _parse_set(item['claim'], rel.names)
        ok = claim == full
        out.setdefault('claims', {})[x] = ok
        if ok:
            text = f'This matches the claimed {rel.br(claim)}, so the claim is true.'
        else:
            extra, missing = claim - full, full - claim
            bits = []
            if extra:
                bits.append(f'{_lst(rel, extra)} {_isare(extra)} not in the closure')
            if missing:
                bits.append(f'it leaves out {_lst(rel, missing)}')
            text = f'The claim {rel.br(claim)} is false: ' + ' and '.join(bits) + '.'
    else:
        text = ''
    _verdict_step(rel, x, full, used, text.strip(), steps)


def do_implies(rel, item, steps, out, table):
    l, r = _parse_fd(item['implies'], rel.names)
    full, used = closure_steps(rel, l, steps)
    ok = r <= full
    fd = f'{rel.t(l)} → {rel.t(r)}'
    out.setdefault('implied', {})[(l, r)] = ok
    table['rows'].append([fd, rel.t(full), 'yes' if ok else 'no'])
    if ok:
        text = f'It contains {_lst(rel, r)}, so {fd} follows.'
    else:
        text = f'It does not contain {_lst(rel, r - full)}, so {fd} does not follow.'
    _verdict_step(rel, l, full, used, text, steps, table=_tab(table))


def _tab(table, hi=None):
    rows = [list(r) for r in table['rows']]
    return dict(cols=table['cols'], rows=rows, hi=[len(rows) - 1] if hi is None else hi)


def candidate_keys(rel):
    """Keys by trying sets in order of size. Returns keys and the rows tried."""
    rhs = frozenset().union(*[r - l for l, r in rel.fds]) if rel.fds else frozenset()
    lhs = frozenset().union(*[l for l, r in rel.fds]) if rel.fds else frozenset()
    core = [a for a in rel.names if a not in rhs]
    never = [a for a in rel.names if a in rhs and a not in lhs]
    middle = [a for a in rel.names if a not in core and a not in never]
    keys, tried = [], []
    for k in range(len(middle) + 1):
        for combo in combinations(middle, k):
            s = frozenset(core) | frozenset(combo)
            if not s or any(key <= s for key in keys):
                continue
            full, fired = rel.close(s)
            tried.append((s, full, fired))
            if full == rel.all:
                keys.append(s)
    # Cross-check against every subset.
    brute = []
    for k in range(1, len(rel.names) + 1):
        for s in combinations(rel.names, k):
            s = frozenset(s)
            if rel.is_super(s) and not any(b <= s for b in brute):
                brute.append(s)
    if set(brute) != set(keys):
        raise SystemExit(f'Key search for {rel.name} disagrees with brute force')
    return keys, tried, core, never


def do_keys(rel, steps, out):
    keys, tried, core, never = candidate_keys(rel)
    head = 'Candidate keys'
    if len(core) == 1:
        intro = f'{core[0]} never appears on the right of an FD, so every key must contain it.'
    elif core:
        intro = f'{_list(rel.order(core))} never appear on the right of an FD, so every key must contain them.'
    else:
        intro = 'Every attribute appears on the right of some FD, so no attribute is forced into every key.'
    if never:
        intro += (f' {never[0]} appears only on the right, so no key needs it.' if len(never) == 1
                  else f' {_list(rel.order(never))} appear only on the right, so no key needs them.')
    intro += ' Try sets from smallest up, skipping any set that contains a key already found.'
    steps.append(dict(head=head, note='Find the candidate keys. ' + intro, fire=[], used=[]))
    table = dict(cols=['Set', 'Closure', 'Key?'], rows=[])
    # One step per key found; the sets of one size that are not keys share a step.
    for size in sorted({len(s) for s, _, _ in tried}):
        group = [x for x in tried if len(x[0]) == size]
        for s, full, fired in group:
            if full != rel.all:
                continue
            table['rows'].append([rel.t(s), rel.t(full), 'yes'])
            p = rel.plus(s)
            note = (f'{p}: {_fired_text(rel, fired)}. ' if fired else '') + f'That is every attribute, so {rel.k(s)} is a candidate key.'
            steps.append(dict(head=head, note=note, set=dict(_strip(rel, full, full - s), label=p),
                              fire=[], used=[i for i, _ in fired], table=_tab(table)))
        misses = [x for x in group if x[1] != rel.all]
        if not misses:
            continue
        start = len(table['rows'])
        for s, full, fired in misses:
            table['rows'].append([rel.t(s), rel.t(full), 'no'])
        if len(misses) == 1:
            s, full, fired = misses[0]
            p = rel.plus(s)
            note = (f'{p}: {_fired_text(rel, fired)}. ' if fired else f'{p} = {rel.br(s)}: no FD applies. ')
            note += f'{_lst(rel, rel.all - full)} {"is" if len(rel.all - full) == 1 else "are"} still missing, so {rel.k(s)} is not a key.'
            extra = dict(set=dict(_strip(rel, full, full - s), label=p), used=[i for i, _ in fired])
        else:
            flat = [rel.plus(s) for s, full, _ in misses if full == s]
            grow = [f'{rel.plus(s)} = {rel.br(full)}' for s, full, _ in misses if full != s]
            bits = []
            if flat:
                bits.append(f'{_list(flat)} {"gets" if len(flat) == 1 else "get"} nothing new')
            if grow:
                bits.append(_list(grow))
            note = 'Not keys: ' + '; '.join(bits) + '. None of these reaches every attribute.'
            extra = {}
        steps.append(dict(dict(head=head, note=note, fire=[], used=[], table=_tab(table, hi=list(range(start, len(table['rows']))))), **extra))
    names = [rel.k(k) for k in keys]
    last = steps[-1]
    last['note'] += (f' The only candidate key is {names[0]}.' if len(keys) == 1
                     else f' Nothing else is left to try: the candidate keys are {_list(names)}, {len(keys)} in all.')
    out['keys'] = keys
    return keys


def do_superkeys(rel, keys, steps, out):
    supers = [frozenset(s) for k in range(1, len(rel.names) + 1) for s in combinations(rel.names, k) if rel.is_super(frozenset(s))]
    supers = [s for s in supers if any(key <= s for key in keys)]
    n = len(supers)
    if len(keys) == 1:
        rest = rel.all - keys[0]
        note = (f'Every superkey contains a candidate key. The only key is {rel.k(keys[0])}, so a superkey is {rel.k(keys[0])} '
                f'plus any choice of the other {len(rest)} attributes ({_lst(rel, rest)}): 2{str(len(rest)).translate(SUP)} = {n}.')
    else:
        note = f'A superkey is any set that contains at least one of the keys {_list([rel.k(k) for k in keys])}. There are {n} such sets.'
    items = [rel.t(s) for s in sorted(supers, key=lambda s: (len(s), [rel.pos[a] for a in rel.order(s)]))]
    steps.append(dict(dict(head='Superkeys', note=note, fire=[], used=[]), **(dict(chips=dict(label=f'Superkeys ({n}):', items=items)) if n <= 64 else {})))
    out['superkeys'] = n


def nf_level(rel, keys, nonatomic):
    """Highest normal form by testing every attribute set (used as a cross-check)."""
    if nonatomic:
        return 0
    prime = frozenset().union(*keys)
    nonprime = rel.all - prime
    level = 4
    for k in range(1, len(rel.names)):
        for s in combinations(rel.names, k):
            s = frozenset(s)
            full = rel.close(s)[0]
            y = full - s
            if not y or full == rel.all:
                continue
            level = min(level, 3)
            if y & nonprime:
                level = min(level, 2)
                if any(s < key for key in keys):
                    level = min(level, 1)
    return level


def do_nf(rel, keys, nonatomic, steps, out):
    head = 'Normal form'
    table = dict(cols=['Form', 'Holds?', 'Because'], rows=[])

    def add(form, ok, why, note, **kw):
        table['rows'].append([form, 'yes' if ok else 'no', why])
        steps.append(dict(dict(head=head, note=note, fire=[], used=[], table=_tab(table)), **kw))

    if nonatomic:
        add('1NF', False, f'{nonatomic} is set-valued', f'{nonatomic} holds a set of values rather than one atomic value, so {rel.name} is not even in 1NF.')
        level = 0
    else:
        prime = frozenset().union(*keys)
        nonprime = rel.all - prime
        level = 1
        add('1NF', True, 'atomic values', f'Every value is atomic, so {rel.name} is in 1NF. Prime attributes (those in some key): {_lst(rel, prime)}.'
            + (f' Non-prime: {_lst(rel, nonprime)}.' if nonprime else ' Every attribute is prime.'))
        split = rel.split()
        # 2NF
        bad = None
        if nonprime:
            for i, l, a in split:
                key = next((k for k in keys if l < k), None)
                if a in nonprime and key:
                    bad = (i, l, a, key, None)
                    break
            if not bad:
                for key in keys:
                    for k in range(1, len(key)):
                        for s in combinations(rel.order(key), k):
                            s = frozenset(s)
                            full = rel.close(s)[0]
                            hit = rel.order((full - s) & nonprime)
                            if hit and not bad:
                                bad = (None, s, hit[0], key, full)
        if bad:
            i, l, a, key, full = bad
            if i is not None:
                add('2NF', False, f'{rel.f(rel.fds[i])} is partial',
                    f'{rel.f(rel.fds[i])}: {rel.k(l)} is only part of the key {rel.k(key)}, and {a} is not prime. '
                    f'This partial dependency breaks 2NF, so the highest normal form is 1NF.', bad=[i])
            else:
                add('2NF', False, f'{rel.t(l)} → {a} is partial',
                    f'{rel.plus(l)} = {rel.br(full)} contains the non-prime {a}, but {rel.k(l)} is only part of the key {rel.k(key)}. '
                    f'This partial dependency breaks 2NF, so the highest normal form is 1NF.', set=dict(_strip(rel, full), label=rel.plus(l)))
        else:
            level = 2
            if not nonprime:
                table['rows'].append(['2NF', 'yes', 'all attributes prime'])
                add('3NF', True, 'all attributes prime', f'Every attribute is prime, so no FD can break 2NF or 3NF: {rel.name} is in 3NF.')
            elif all(len(k) == 1 for k in keys):
                add('2NF', True, 'single-attribute keys', f'Every candidate key is a single attribute, so nothing can depend on part of a key: {rel.name} is in 2NF.')
            else:
                parts = []
                for key in keys:
                    for k in range(1, len(key)):
                        parts += [frozenset(s) for s in combinations(rel.order(key), k) if frozenset(s) not in parts]
                shown = ', '.join(f'{rel.plus(s)} = {rel.br(rel.close(s)[0])}' for s in parts)
                add('2NF', True, 'no partial dependency',
                    (f'Parts of keys reach no non-prime attribute: {shown}. ' if len(parts) <= 6 else '')
                    + f'No non-prime attribute depends on only part of a key, so {rel.name} is in 2NF.')
            # 3NF
            bad = next(((i, l, a) for i, l, a in split if a in nonprime and not rel.is_super(l)), None)
            if not nonprime:
                level = 3
            elif bad:
                i, l, a = bad
                full = rel.close(l)[0]
                add('3NF', False, f'{rel.f(rel.fds[i])}',
                    f'{rel.f(rel.fds[i])}: {rel.plus(l)} = {rel.br(full)} is not every attribute, so {rel.k(l)} is not a superkey, '
                    f'and {a} is not prime. This breaks 3NF, so the highest normal form is 2NF.',
                    bad=[i], set=dict(_strip(rel, full), label=rel.plus(l)))
            else:
                level = 3
                loose = [i for i, l, a in split if not rel.is_super(l)]
                loose = [rel.f(rel.fds[i]) for i in dict.fromkeys(loose)]
                add('3NF', True, 'superkey or prime',
                    (f'{_list(loose)} {"has" if len(loose) == 1 else "have"} no superkey on the left, but only prime attributes on the right, which 3NF allows. ' if loose else '')
                    + f'Every FD has a superkey on the left or only prime attributes on the right, so {rel.name} is in 3NF.')
            if level == 3:
                bad = next(((i, l) for i, l, a in split if not rel.is_super(l)), None)
                if bad:
                    i, l = bad
                    full = rel.close(l)[0]
                    add('BCNF', False, f'{rel.f(rel.fds[i])}',
                        f'{rel.f(rel.fds[i])}: {rel.plus(l)} = {rel.br(full)} is not every attribute, so {rel.k(l)} is not a superkey. '
                        f'This breaks BCNF, so the highest normal form is 3NF.', bad=[i], set=dict(_strip(rel, full), label=rel.plus(l)))
                else:
                    level = 4
                    add('BCNF', True, 'every left side a superkey', f'The left side of every FD is a superkey, so {rel.name} is in BCNF, the highest normal form here.')
        if level != nf_level(rel, keys, nonatomic):
            raise SystemExit(f'Normal-form test for {rel.name} disagrees with the exhaustive check')
    out['nf'] = NF[level]
    return level


def do_cover(rel, steps, out):
    head = 'Minimal cover'
    g = []
    for l, r in rel.fds:
        for a in rel.order(r - l):
            if (l, a) not in [(x['l'], x['a']) for x in g]:
                g.append(dict(l=l, a=a, gone=False))

    def live(skip=None):
        return [(x['l'], frozenset([x['a']])) for j, x in enumerate(g) if not x['gone'] and j != skip]

    def show(**kw):
        return dict(dict(head=head, fdlist=[f'{rel.t(x["l"])} → {x["a"]}' for x in g], gone=[j for j, x in enumerate(g) if x['gone']], fire=[], used=[]), **kw)

    multi = [fd for fd in rel.fds if len(fd[1] - fd[0]) > 1]
    if multi:
        parts = '; '.join(f'{rel.f(fd)} becomes ' + _list([f'{rel.t(fd[0])} → {a}' for a in rel.order(fd[1] - fd[0])]) for fd in multi)
        steps.append(show(note=f'Find a minimal cover. First give every FD a single attribute on the right: {parts}.'))
    else:
        steps.append(show(note='Find a minimal cover. Every FD already has a single attribute on the right.'))
    for j, x in enumerate(g):
        if len(x['l']) < 2 or x['gone']:
            continue
        before, dropped, tried = x['l'], [], []
        for b in rel.order(before):
            if len(x['l']) < 2:
                break
            rest = x['l'] - {b}
            full = closure(rest, live())[0]
            tried.append((rest, full))
            if x['a'] in full:
                x['l'] = rest
                dropped.append((b, rest, full))
        old = f'{rel.t(before)} → {x["a"]}'
        if dropped:
            b, rest, full = dropped[0]
            note = (f'In {old}, {_list([d[0] for d in dropped])} {"is" if len(dropped) == 1 else "are"} extra: '
                    f'{rel.plus(rest)} = {rel.br(full)} already contains {x["a"]}. It becomes {rel.t(x["l"])} → {x["a"]}.')
            dup = next((k for k, y in enumerate(g) if k != j and not y['gone'] and y['l'] == x['l'] and y['a'] == x['a']), None)
            if dup is not None:
                x['gone'] = True
                note += ' That FD is already in the list, so drop the copy.'
            steps.append(show(note=note, fire=[j], set=dict(_strip(rel, full), label=rel.plus(rest))))
        else:
            checks = ', '.join(f'{rel.plus(r)} = {rel.br(f)}' for r, f in tried)
            steps.append(show(note=f'In {old}, no attribute on the left can be dropped: {checks}, and none contains {x["a"]}.', fire=[j]))
    for j, x in enumerate(g):
        if x['gone']:
            continue
        full = closure(x['l'], live(skip=j))[0]
        fd = f'{rel.t(x["l"])} → {x["a"]}'
        if x['a'] in full:
            x['gone'] = True
            steps.append(show(note=f'{fd} is redundant: without it, {rel.plus(x["l"])} = {rel.br(full)} still contains {x["a"]}. Remove it.',
                              fire=[j], set=dict(_strip(rel, full), label=rel.plus(x['l']))))
        else:
            steps.append(show(note=f'{fd} is needed: without it, {rel.plus(x["l"])} = {rel.br(full)} does not contain {x["a"]}.',
                              fire=[j], set=dict(_strip(rel, full), label=rel.plus(x['l']))))
    cover = [(x['l'], x['a']) for x in g if not x['gone']]
    # The result must be equivalent to the original set.
    for l, r in rel.fds:
        if not r <= closure(l, [(a, frozenset([b])) for a, b in cover])[0]:
            raise SystemExit(f'Minimal cover for {rel.name} lost {rel.f((l, r))}')
    steps[-1]['note'] += ' Minimal cover: ' + ', '.join(f'{rel.t(l)} → {a}' for l, a in cover) + '.'
    out['cover'] = set(cover)


def _components(rel, part):
    comps = part.get('components')
    if not comps or len(comps) < 2:
        raise SystemExit(f'{rel.name}: a decomposition needs at least two components')
    out = [(name, _parse_set(attrs, rel.names)) for name, attrs in comps.items()]
    if frozenset().union(*[c for _, c in out]) != rel.all:
        raise SystemExit(f'{rel.name}: the components do not cover every attribute')
    return out


def chase(rel, comps):
    """The tableau test. Returns (lossless, [(tableau, changed cells, fd index, rows)])."""
    tab = [['a' if a in c else f'b{i + 1}' for a in rel.names] for i, (_, c) in enumerate(comps)]
    trace, changed = [], True
    split = rel.split()
    while changed and not any(all(v == 'a' for v in row) for row in tab):
        changed = False
        for i, l, a in split:
            cols = [rel.pos[x] for x in rel.order(l)]
            groups = {}
            for r, row in enumerate(tab):
                groups.setdefault(tuple(row[c] for c in cols), []).append(r)
            c = rel.pos[a]
            for rows in groups.values():
                vals = {tab[r][c] for r in rows}
                if len(rows) < 2 or len(vals) < 2:
                    continue
                target = 'a' if 'a' in vals else min(vals, key=lambda v: int(v[1:]))
                cells = []
                for r, row in enumerate(tab):
                    if row[c] in vals and row[c] != target:
                        row[c] = target
                        cells.append([r, c])
                trace.append(([list(row) for row in tab], cells, i, rows, a, target))
                changed = True
                if any(all(v == 'a' for v in row) for row in tab):
                    break
            if any(all(v == 'a' for v in row) for row in tab):
                break
    return any(all(v == 'a' for v in row) for row in tab), trace, tab


def do_lossless(rel, part, steps, out):
    comps = _components(rel, part)
    head = 'Lossless join'
    lossless, trace, final = chase(rel, comps)
    if len(comps) == 2:
        (n1, c1), (n2, c2) = comps
        common = c1 & c2
        if not common:
            ok = False
            note = (f'{n1} and {n2} have no attribute in common, so joining them pairs every row of one with every row of the other. '
                    f'That adds rows that were never there: the decomposition is lossy.')
            steps.append(dict(head=head, note=note, fire=[], used=[]))
        else:
            full, fired = rel.close(common)
            p = rel.plus(common)
            ok = c1 <= full or c2 <= full
            which = n1 if c1 <= full else n2
            steps.append(dict(head=head, note=f'Two relations join without extra rows exactly when their common attributes determine all of one of them. '
                                              f'Here {n1} ∩ {n2} = {rel.br(common)}, so work out {p}.',
                              fire=[], used=[], set=dict(_strip(rel, common), label=p)))
            note = (f'{p}: {_fired_text(rel, fired)}, giving {rel.br(full)}. ' if fired else f'{p} = {rel.br(full)}: no FD applies. ')
            if ok:
                note += f'That contains all of {which}, so the common attributes are a key of {which} and the join is lossless.'
            else:
                note += f'That contains neither all of {n1} nor all of {n2}, so the join can create extra rows: the decomposition is lossy.'
            steps.append(dict(head=head, note=note, fire=[], used=[i for i, _ in fired], set=dict(_strip(rel, full, full - common), label=p)))
        if ok != lossless:
            raise SystemExit(f'{rel.name}: binary lossless test disagrees with the chase')
    else:
        names = [n for n, _ in comps]
        start = [['a' if a in c else f'b{i + 1}' for a in rel.names] for i, (_, c) in enumerate(comps)]
        tb = lambda t, cells=(): dict(cols=rel.names, rows=[n for n in names], cells=t, new=[list(x) for x in cells])
        steps.append(dict(head=head, note=f'Test with a table: one row per relation. A row has a in the columns its relation contains and its own b elsewhere. '
                                           f'Each FD makes rows that agree on its left side agree on its right side too. A row of all a\'s means lossless.',
                          fire=[], used=[], tableau=tb(start)))
        for t, cells, i, rows, a, target in trace:
            rn = _list([names[r] for r in rows])
            note = (f'{rel.f(rel.fds[i])}: rows {rn} agree on {rel.t(rel.fds[i][0])}, so their {a} entries must be equal: '
                    + ('they all become a.' if target == 'a' else f'they all become {target}, the same unknown value.'))
            others = [names[r] for r, _ in cells if r not in rows]
            if others:
                note += f' Row {_list(others)} had the same value in column {a}, so it changes too.'
            done = [names[r] for r, row in enumerate(t) if all(v == 'a' for v in row)]
            if done:
                note += f' Row {done[0]} is now all a\'s, so the decomposition is lossless.'
            steps.append(dict(head=head, note=note, fire=[i], used=[], tableau=tb(t, cells)))
        if not lossless:
            steps.append(dict(head=head, note='No FD changes the table any more, and no row is all a\'s, so the decomposition is lossy.',
                              fire=[], used=[], tableau=tb(final)))
        ok = lossless
    out['lossless'] = ok


def do_preserve(rel, part, steps, out):
    comps = _components(rel, part)
    head = 'Dependency preservation'
    table = dict(cols=['FD', 'Preserved?'], rows=[])
    lost = []
    for i, (l, r) in enumerate(rel.fds):
        fd = rel.f((l, r))
        home = next((n for n, c in comps if l | r <= c), None)
        if home:
            ok = True
            note = f'{fd} lies inside {home}, so {home} can check it on its own.'
            z = frozenset(l | r)
        else:
            z, trace, changed = set(l), [], True
            while changed and not r <= z:
                changed = False
                for n, c in comps:
                    got = (closure(z & c, rel.fds)[0] & c) - z
                    if got:
                        z |= got
                        trace.append((n, got))
                        changed = True
            ok = r <= z
            note = f'{fd} does not fit inside one relation. Start from {rel.br(l)} and close it inside each relation in turn: '
            note += ('; '.join(f'{n} adds {_lst(rel, g)}' for n, g in trace) if trace else 'no relation adds anything') + '. '
            note += (f'That reaches {_lst(rel, r)}, so {fd} is preserved.' if ok
                     else f'{_lst(rel, r - z)} {_isare(r - z)} never reached, so {fd} is not preserved.')
        if not ok:
            lost.append((l, r))
        table['rows'].append([fd, 'yes' if ok else 'no'])
        steps.append(dict(dict(head=head, note=note, fire=[i], used=[], table=_tab(table)),
                          **({} if home else dict(set=dict(_strip(rel, z, z - l), label=f'Reached from {rel.k(l)}')))))
    steps[-1]['note'] += (' Every FD is preserved.' if not lost else ' Not preserved: ' + ', '.join(rel.f(fd) for fd in lost) + '.')
    out['preserved'] = not lost
    out['lost'] = set(lost)


def project(full, names, name):
    """FDs of the sub-relation `names`, as a small cover of the projection."""
    sub = frozenset(names)
    given = []
    for i, l, a in full.split():
        if l <= sub and a in sub and (l, a) not in given:
            given.append((l, a))
    derived = []
    for k in range(1, len(names)):
        for s in combinations(names, k):
            s = frozenset(s)
            for a in names:
                if a not in s and a in full.close(s)[0] and (s, a) not in given and (s, a) not in derived:
                    derived.append((s, a))
    g = given + derived
    # Left-reduce, drop duplicates, then drop redundant FDs from the end.
    reduced = []
    for l, a in g:
        for b in sorted(l, key=full.pos.__getitem__):
            if len(l) > 1 and a in full.close(l - {b})[0]:
                l = l - {b}
        if (l, a) not in reduced:
            reduced.append((l, a))
    for j in range(len(reduced) - 1, -1, -1):
        l, a = reduced[j]
        rest = [(x, frozenset([y])) for k, (x, y) in enumerate(reduced) if k != j]
        if a in closure(l, rest)[0]:
            reduced.pop(j)
    merged = []
    for l, a in reduced:
        hit = next((m for m in merged if m[0] == l), None)
        if hit:
            hit[1].add(a)
        else:
            merged.append([l, {a}])
    order = {n: i for i, n in enumerate(names)}
    merged.sort(key=lambda m: (min(order[x] for x in m[0]), len(m[0])))
    rel = Rel(name, list(names), [(l, frozenset(r)) for l, r in merged])
    for k in range(1, len(names) + 1):
        for s in combinations(names, k):
            s = frozenset(s)
            if rel.close(s)[0] != full.close(s)[0] & sub:
                raise SystemExit(f'Projection onto {name} is wrong for {s}')
    return rel


def _check(qid, name, expect, out, rel):
    if not expect:
        raise SystemExit(f'Animation for {qid} ({name}) has no expectation')
    for k, want in expect.items():
        if k in ('1nf', '2nf', '3nf', 'bcnf'):
            if 'nf' not in out:
                raise SystemExit(f'Animation for {qid} ({name}): {k} expected but no normal form computed')
            got = NF.index(out['nf']) >= NF.index(k.upper() if k != 'bcnf' else 'BCNF')
        elif k == 'keys':
            got, want = set(out.get('keys', [])), {_parse_set(x, rel.names) for x in want}
        elif k == 'key_count':
            got = len(out.get('keys', []))
        elif k in ('closure', 'claims'):
            got = out.get(k, {})
            want = {_parse_set(x, rel.names): (_parse_set(v, rel.names) if k == 'closure' else v) for x, v in want.items()}
            got = {x: got.get(x) for x in want}
        elif k == 'implied':
            got = out.get('implied', {})
            want = {_parse_fd(x, rel.names): v for x, v in want.items()}
            got = {x: got.get(x) for x in want}
        elif k == 'cover':
            got = out.get('cover')
            want = {(l, a) for x in want for l, r in [_parse_fd(x, rel.names)] for a in r}
        elif k == 'lost':
            got, want = out.get('lost'), {_parse_fd(x, rel.names) for x in want}
        elif k in ('nf', 'superkeys', 'lossless', 'preserved'):
            got = out.get(k)
        else:
            raise SystemExit(f'Animation for {qid}: unknown expectation {k}')
        if got != want:
            raise SystemExit(f'Animation for {qid} ({name}): {k} is {got}, not {want}')


def fd_animation(qid, spec):
    universe = _names(spec['attrs']) if 'attrs' in spec else None
    schedules, results = [], {}
    for part in spec.get('parts', [spec]):
        name = part.get('name', 'R')
        names = _names(part['attrs']) if 'attrs' in part else universe
        fds = part.get('fds', spec.get('fds'))
        if names is None or fds is None:
            raise SystemExit(f'Animation for {qid} ({name}) has no attributes or FDs')
        sep = '' if all(len(n) == 1 for n in names) else ', '
        labels = [' → '.join(sep.join(_parse_seq(side, names)) for side in x.split('->')) for x in fds]
        base = Rel(name, names, [_parse_fd(x, names) for x in fds], labels)
        steps, out = [], {}
        if 'relation' in part:
            sub = _parse_seq(part['relation'], names)
            rel = project(base, sub, name)
            steps.append(dict(head=f'FDs in {name}', note=f'Only FDs among {_lst(rel, rel.all)} matter in {name}. Working them out from the closures of its attribute sets, '
                                                          f'these hold: ' + ', '.join(rel.fdlist()) + '.', fire=[], used=[]))
        else:
            rel = base
        keys, table = None, dict(cols=['FD', 'Closure of left side', 'Follows?'], rows=[])
        for item in part['do']:
            if isinstance(item, dict) and 'closure' in item:
                do_closure(rel, item, steps, out)
            elif isinstance(item, dict) and 'implies' in item:
                do_implies(rel, item, steps, out, table)
            elif item == 'keys':
                keys = do_keys(rel, steps, out)
            elif item == 'superkeys':
                do_superkeys(rel, keys or candidate_keys(rel)[0], steps, out)
            elif item == 'nf':
                if keys is None and not part.get('nonatomic'):
                    raise SystemExit(f'Animation for {qid} ({name}): find the keys before the normal form')
                do_nf(rel, keys or [], part.get('nonatomic'), steps, out)
            elif item == 'cover':
                do_cover(rel, steps, out)
            elif item == 'lossless':
                do_lossless(rel, part, steps, out)
            elif item == 'preserve':
                do_preserve(rel, part, steps, out)
            else:
                raise SystemExit(f'Animation for {qid}: unknown task {item}')
        if len(table['rows']) > 1:
            yes = [r[0] for r in table['rows'] if r[2] == 'yes']
            no = [r[0] for r in table['rows'] if r[2] == 'no']
            if not yes:
                steps[-1]['note'] += f' Neither {no[0]} nor {no[1]} follows.' if len(no) == 2 else ' None of them follows.'
            elif not no:
                steps[-1]['note'] += ' All of them follow.'
            else:
                steps[-1]['note'] += f' {_list(yes)} {"follows" if len(yes) == 1 else "follow"}; {_list(no)} {"does" if len(no) == 1 else "do"} not.'
        _check(qid, name, part.get('expect'), out, rel)
        results[name] = out
        if len(steps) < 2:
            raise SystemExit(f'Animation for {qid} ({name}) has fewer than two steps')
        schedules.append(dict(short=part.get('short', name), title=part.get('title', f'{name}({", ".join(rel.names)})'),
                              attrs=rel.names, fds=rel.fdlist(), steps=steps))
    if 'gain' in spec:
        g = spec['gain']
        old = NF.index(results[g['old']]['nf'])
        new = min(NF.index(results[n]['nf']) for n in g['new'])
        if new <= old:
            raise SystemExit(f'Animation for {qid}: the decomposition gains no normal form')
        gained = NF[old + 1]
        if gained != spec.get('expect', {}).get('gained'):
            raise SystemExit(f'Animation for {qid}: first normal form gained is {gained}, not {spec.get("expect", {}).get("gained")}')
        schedules[-1]['steps'][-1]['note'] += (f' {g["old"]} was in {NF[old]} only, and every new relation is in at least {NF[new]}, '
                                               f'so the weakest normal form gained is {gained}.')
    for s in schedules:
        s['steps'][-1]['final'] = True
    return dict(kind='fd', schedules=schedules, count=sum(len(s['steps']) for s in schedules))


# Animation kinds this family provides, and the player file that draws them.
KINDS = {'fd': fd_animation}
PLAYER = 'fd'
TABS = 'parts'
