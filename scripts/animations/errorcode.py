"""Error-detecting and error-correcting codes: CRC long division over GF(2),
filling in a Hamming codeword, and the minimum distance of a code.

Data: data/animations/errorcode.json. Every entry is simulated at build time and
checked against the expected answer; the build stops on any difference.

Each step is {note, blocks}; a block is one of
  {t: 'grid', head, rows: [{label, cells, cls, value}], now, gaps}   bits in fixed columns
       a cell is text or [text, class] (class 'muted', 'hit', 'bad', 'new', 'unk')
  {t: 'table', head, rows, hl}                                       a growing table
  {t: 'line', text, cls}                                             one line of text
"""
import re

_SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def _check(qid, what, got, want):
    if got != want:
        raise SystemExit(f'Animation for {qid}: {what} is {got!r}, not {want!r}')


def grid(rows, head=None, now=(), gaps=()):
    out = []
    for r in rows:
        label, cells, cls, value = (list(r) + [None, None])[:4]
        out.append(dict(label=label, cells=[c if isinstance(c, list) else str(c) for c in cells], cls=cls, value=value))
    return dict(t='grid', head=head, rows=out, now=list(now), gaps=list(gaps))


def table(head, rows, hl=None):
    return dict(t='table', head=list(head), rows=[[str(c) for c in r] for r in rows], hl=hl)


def line(text, cls='steps-ready'):
    return dict(t='line', text=text, cls=cls)


def step(note, *blocks):
    return dict(note=note, blocks=[b for b in blocks if b])


def _finish(kind, short, title, steps, **extra):
    steps[-1]['final'] = True
    return dict(kind=kind, schedules=[dict(short=short, title=title, steps=steps)], count=len(steps), **extra)


# ---------------------------------------------------------------- CRC

def poly_bits(g):
    """'x^3+x+1' or '1011' -> '1011'."""
    g = g.replace(' ', '')
    if re.fullmatch('[01]+', g):
        if g[0] != '1' or len(g) < 2:
            raise SystemExit(f'Generator {g} must start with 1 and have degree at least 1')
        return g
    powers = []
    for term in g.split('+'):
        m = re.fullmatch(r'x(?:\^(\d+))?|1', term)
        if not m:
            raise SystemExit(f'Cannot read generator term {term!r}')
        powers.append(0 if term == '1' else int(m.group(1) or 1))
    if len(set(powers)) != len(powers):
        raise SystemExit(f'Generator {g} repeats a term')
    n = max(powers)
    return ''.join('1' if n - i in powers else '0' for i in range(n + 1))


def poly_text(bits):
    n = len(bits) - 1
    terms = [('x' + (str(n - i).translate(_SUP) if n - i > 1 else '')) if n - i else '1' for i, b in enumerate(bits) if b == '1']
    return '+'.join(terms)


def mod2_divide(bits, gen):
    """Long division over GF(2). Returns (remainder, [(column, before, after)])."""
    work, r, xors = list(bits), len(gen) - 1, []
    for i in range(len(bits) - r):
        if work[i] == '1':
            before = ''.join(work)
            for j, g in enumerate(gen):
                work[i + j] = '1' if work[i + j] != g else '0'
            xors.append((i, before, ''.join(work)))
    return ''.join(work[len(bits) - r:]), xors


def crc_animation(qid, spec):
    msg, gen = spec['message'], poly_bits(spec['generator'])
    if not re.fullmatch('[01]+', msg):
        raise SystemExit(f'Animation for {qid}: message {msg!r} is not binary')
    r, n = len(gen) - 1, len(msg)
    dividend = msg + '0' * r
    rem, xors = mod2_divide(dividend, gen)
    width = len(dividend)

    # History rows: ('div', bits) | ('gen', column) | ('res', bits, lead, column). Rows before `current` are greyed.
    def render(hist, current):
        rows = []
        for k, item in enumerate(hist):
            old = k < current
            if item[0] == 'div':
                rows.append(('Dividend', list(item[1]), 'muted' if old else None))
            elif item[0] == 'gen':
                col = item[1]
                rows.append(('⊕ ' + gen, [(gen[j - col] if old else [gen[j - col], 'hit']) if col <= j < col + len(gen) else ''
                                          for j in range(width)], 'muted' if old else None))
            else:
                _, bits, lead, col = item
                cells = [[b, 'new'] if not old and col <= j < col + len(gen) else [b, 'muted'] if j < lead else b
                         for j, b in enumerate(bits)]
                rows.append(('=', cells, 'sum muted' if old else 'sum'))
        return rows

    written = spec['generator'].replace(' ', '')
    shown = None if re.fullmatch('[01]+', written) else poly_text(gen)
    intro = (f'The generator {shown} is the bit string {gen}' if shown else f'The generator is {gen}') + \
        f', of degree {r}. Append {r} zero{"s" if r > 1 else ""} to the message {msg} and divide by {gen}, using XOR instead of subtraction.'
    hist = [('div', dividend)]
    steps = [step(intro, grid(render(hist, 0), gaps=[n]), line(f'Message {msg} followed by {"0" * r}: {dividend}'))]
    lead = 0
    for col, before, after in xors:
        nxt = after.find('1')
        lead_after = nxt if 0 <= nxt < width - r else width - r
        skipped = list(range(lead, col))
        hist += [('gen', col), ('res', after, lead_after, col)]
        note = ''
        if skipped:
            note = (f'Column {skipped[0] + 1} holds 0, so move on. ' if len(skipped) == 1 else
                    f'Columns {skipped[0] + 1} to {skipped[-1] + 1} hold 0, so move on. ')
        note += f'The leftmost 1 is in column {col + 1}: write {gen} under it and XOR. '
        note += f'The value is now {after}.' if lead_after < width - r else \
            f'That leaves {after}: no 1 is left in the first {n} columns, so the division is finished.'
        steps.append(step(note, grid(render(hist, len(hist) - 2), now=range(col, col + len(gen)), gaps=[n])))
        lead = lead_after
    last = render(hist, len(hist))
    last[-1] = ('=', [[b, 'new'] if j >= width - r else [b, 'muted'] for j, b in enumerate(xors[-1][2] if xors else dividend)], 'sum')
    steps.append(step(f'The last {r} bits, {rem}, are the remainder: these are the check bits.',
                      grid(last, now=range(width - r, width), gaps=[n]), line(f'Remainder: {rem}', 'steps-time')))
    sent = msg + rem
    check, _ = mod2_divide(sent, gen)
    if check != '0' * r:
        raise SystemExit(f'Animation for {qid}: {sent} is not divisible by {gen}')
    steps.append(step(f'Replace the {r} appended zeros by {rem}: the frame sent is {sent}. Dividing it by {gen} leaves remainder {check}, as it should.',
                      grid([('Message', list(msg) + [''] * r), ('Check bits', [''] * n + [[b, 'new'] for b in rem]),
                            ('Sent', list(msg) + [[b, 'new'] for b in rem], 'sum')], gaps=[n]),
                      line(f'Transmitted: {sent}', 'steps-time')))
    out = dict(remainder=rem, transmitted=sent)
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('crc', 'CRC', f'CRC with generator {gen}', steps)


# ---------------------------------------------------------------- Hamming codeword with unknown bits

def hamming_animation(qid, spec):
    layout, values = spec['layout'], dict(spec['values'])
    n = len(layout)
    pos = {name: n - i for i, name in enumerate(layout)}  # positions numbered from the right, starting at 1
    checks = sorted((name for name in layout if name.startswith('c')), key=lambda c: pos[c])
    for c in checks:
        p = pos[c]
        if int(c[1:]) != p or p & (p - 1):
            raise SystemExit(f'Animation for {qid}: check bit {c} is at position {p}, not a matching power of two')
    for name in layout:
        if name.startswith('d') and not pos[name] & (pos[name] - 1):
            raise SystemExit(f'Animation for {qid}: data bit {name} sits at power-of-two position {pos[name]}')
    if set(values) != set(layout):
        raise SystemExit(f'Animation for {qid}: values do not match the layout')
    unknown = [k for k, v in values.items() if isinstance(v, str)]
    unk_names = sorted({values[k] for k in unknown})
    group = {c: [name for name in layout if pos[name] & pos[c]] for c in checks}
    head = [str(pos[name]) for name in layout]

    def val(name, solved):
        v = values[name]
        if isinstance(v, str):
            return [str(solved[v]), 'new'] if v in solved else [v, 'unk']
        return str(v)

    def view(solved, now=None, extra=()):
        rows = [('Bit', layout, 'muted'), ('Value', [val(x, solved) for x in layout])]
        for c in checks:
            cells = [(val(x, solved) if x in group[c] else '') for x in layout]
            rows.append((c + ' group', cells, 'hl' if c == now else None))
        return grid(rows, head=head, now=[layout.index(x) for x in group[now]] if now else ())

    groups_text = '; '.join(f'{c}: positions {", ".join(str(pos[x]) for x in sorted(group[c], key=lambda x: pos[x]))}' for c in checks)
    steps = [step(f'Number the positions from the right, 1 to {n}. Each check bit sits at a power of two and covers every position whose binary number has that bit set ({groups_text}).', view({}))]
    # The parity convention comes from the groups with no unknown bit.
    known = [c for c in checks if not any(isinstance(values[x], str) for x in group[c])]
    if not known:
        raise SystemExit(f'Animation for {qid}: no check group is fully known, so the parity convention is not determined')
    parities = {c: sum(values[x] for x in group[c]) % 2 for c in known}
    if len(set(parities.values())) != 1:
        raise SystemExit(f'Animation for {qid}: the fully known groups disagree on the parity convention')
    parity = parities[known[0]]
    word = 'even' if parity == 0 else 'odd'
    counts = [sum(values[x] for x in group[c]) for c in known]
    if len(known) == 1:
        seen = f'The {known[0]} group has no unknown bit and holds {counts[0]} ones, an {word} number.'
    else:
        seen = f'The {" and ".join(known)} groups have no unknown bit and hold {" and ".join(map(str, counts))} ones, all {word}.'
    steps.append(step(f'{seen} So the code uses {word} parity: every group must hold an {word} number of ones.',
                      view({}, known[0]), line(f'Parity: {word}')))
    solved, rows, pending = {}, [], [c for c in checks if c not in known]
    while pending:
        progress = False
        for c in list(pending):
            missing = sorted({values[x] for x in group[c] if isinstance(values[x], str) and values[x] not in solved})
            if len(missing) > 1:
                continue
            pending.remove(c)
            ones = sum(values[x] if not isinstance(values[x], str) else solved.get(values[x], 0) for x in group[c] if not (isinstance(values[x], str) and values[x] in missing))
            if missing:
                u = missing[0]
                cnt = sum(1 for x in group[c] if values[x] == u)
                if cnt != 1:
                    raise SystemExit(f'Animation for {qid}: {u} appears {cnt} times in the {c} group')
                solved[u] = (parity - ones) % 2
                note = f'The {c} group has one unknown, {u}, and {ones} other ones. For an {word} total, {u} = {solved[u]}.'
                rows.append([c, u, solved[u]])
            else:
                if ones % 2 != parity:
                    raise SystemExit(f'Animation for {qid}: the {c} group fails {word} parity')
                note = f'Check: the {c} group now holds {ones} ones, {word} as required.'
            steps.append(step(note, view(solved, c), table(['Group', 'Unknown', 'Value'], rows, len(rows) - 1) if rows else None))
            progress = True
        if not progress:
            raise SystemExit(f'Animation for {qid}: the unknowns cannot be found one group at a time')
    for c in checks:
        if sum(values[x] if not isinstance(values[x], str) else solved[values[x]] for x in group[c]) % 2 != parity:
            raise SystemExit(f'Animation for {qid}: the {c} group fails {word} parity')
    answer = ', '.join(f'{u} = {solved[u]}' for u in unk_names)
    steps.append(step(f'Every group now holds an {word} number of ones, so {answer}.', view(solved),
                      table(['Group', 'Unknown', 'Value'], rows), line(answer, 'steps-time')))
    for k, v in spec['expect'].items():
        _check(qid, k, solved.get(k), v)
    return _finish('hamming-fill', 'Hamming', f'{n}-bit Hamming codeword, {word} parity', steps)


# ---------------------------------------------------------------- minimum distance of a code

def distance_animation(qid, spec):
    words = spec['codewords']
    if len({len(w) for w in words}) != 1 or not all(re.fullmatch('[01]+', w) for w in words):
        raise SystemExit(f'Animation for {qid}: codewords must be binary strings of one length')
    rows, best = [], None
    steps = [step(f'The Hamming distance of two words is the number of positions where they differ: XOR them and count the 1s. Check all {len(words) * (len(words) - 1) // 2} pairs.',
                  grid([(f'Word {k + 1}', list(w)) for k, w in enumerate(words)]))]
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]
            x = ''.join('1' if p != q else '0' for p, q in zip(a, b))
            d = x.count('1')
            best = d if best is None else min(best, d)
            rows.append([f'{a}, {b}', x, d])
            steps.append(step(f'{a} and {b} differ in {d} position{"s" if d != 1 else ""}. Smallest so far: {best}.',
                              grid([('', list(a)), ('', list(b)), ('XOR', [[c, 'hit'] if c == '1' else [c, 'muted'] for c in x], 'sum', f'{d}')]),
                              table(['Pair', 'XOR', 'Distance'], rows, len(rows) - 1)))
    q = (best - 1) // 2
    steps.append(step(f'The minimum distance is {best}. A code always corrects q errors when 2q < {best}, so it corrects up to {q} error{"s" if q != 1 else ""} (and detects up to {best - 1}).',
                      table(['Pair', 'XOR', 'Distance'], rows), line(f'Minimum distance {best}; corrects {q}', 'steps-time')))
    out = dict(min_distance=best, correct=q, detect=best - 1)
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('code-distance', 'Distance', f'{len(words)} codewords of {len(words[0])} bits', steps)


KINDS = {'crc': crc_animation, 'hamming-fill': hamming_animation, 'code-distance': distance_animation}
PLAYER = 'errorcode'
TABS = 'parts'
