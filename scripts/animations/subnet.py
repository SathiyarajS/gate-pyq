"""IPv4 addressing: network addresses by ANDing with a mask, host counts, CIDR
block checks, longest-prefix forwarding and IPv4 fragmentation.

Data: data/animations/subnet.json. Every entry is simulated at build time and
checked against the expected answer; the build stops on any difference.

Each step is {note, blocks}; a block is one of
  {t: 'grid', rows: [{label, cells, cls, value}], now, gaps}   address bits in fixed columns
       a cell is text or [text, class]; classes 'net', 'host', 'muted', 'bad', 'dot'
  {t: 'frags', total, rows: [{label, parts: [[start, length, text, cls]]}]}   payload byte ranges
  {t: 'table', head, rows, hl, marks}                           a growing table
  {t: 'line', text, cls}                                        one line of text
Address octets that a mask cuts are drawn bit by bit; whole octets stay in decimal.
"""
from fractions import Fraction


def _check(qid, what, got, want):
    if got != want:
        raise SystemExit(f'Animation for {qid}: {what} is {got!r}, not {want!r}')


def table(head, rows, hl=None, marks=None):
    return dict(t='table', head=list(head), rows=[[str(c) for c in r] for r in rows], hl=hl, marks=marks)


def line(text, cls='steps-ready'):
    return dict(t='line', text=text, cls=cls)


def step(note, *blocks):
    return dict(note=note, blocks=[b for b in blocks if b])


def _finish(kind, short, title, steps, **extra):
    steps[-1]['final'] = True
    return dict(kind=kind, schedules=[dict(short=short, title=title, steps=steps)], count=len(steps), **extra)


# ---------------------------------------------------------------- addresses

def ip(s):
    parts = s.split('.')
    if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        raise SystemExit(f'{s!r} is not an IPv4 address')
    return sum(int(p) << (24 - 8 * k) for k, p in enumerate(parts))


def ip_text(n):
    return '.'.join(str((n >> (24 - 8 * k)) & 255) for k in range(4))


def mask_of(p):
    return (0xFFFFFFFF << (32 - p)) & 0xFFFFFFFF


def prefix_of(mask_text):
    m = ip(mask_text)
    p = bin(m).count('1')
    if m != mask_of(p):
        raise SystemExit(f'Mask {mask_text} is not a contiguous prefix mask')
    return p


def block(text):
    """'10.12.2.0/23' -> (address, prefix)."""
    a, _, p = text.partition('/')
    if not p.isdigit() or not 0 <= int(p) <= 32:
        raise SystemExit(f'{text!r} has no prefix length')
    return ip(a), int(p)


def octet_bits(m):
    return format(m, '08b')


def bit_grid(rows, expand, hide=()):
    """rows: (label, address, prefix or None, value text, row class, {bit index: cell class}).
    Octets in `expand` are drawn as 8 bits, the others in decimal; `hide` octets are left out."""
    out, gaps, cols = [], [], {}
    for label, addr, p, value, cls, marks in rows:
        cells, col = [], 0
        for o in range(4):
            if o in hide:
                continue
            if cells:
                cells.append(['.', 'dot'])
                col += 1
            byte = (addr >> (24 - 8 * o)) & 255
            if o in expand:
                for b in range(8):
                    i = 8 * o + b
                    c = (marks or {}).get(i) or (None if p is None else 'net' if i < p else 'host')
                    cells.append([str((byte >> (7 - b)) & 1), c] if c else str((byte >> (7 - b)) & 1))
                    cols[i] = col
                    col += 1
            else:
                lo, hi = 8 * o, 8 * o + 8
                c = (marks or {}).get(lo) or (None if p is None else 'net' if hi <= p else 'host' if lo >= p else None)
                cells.append([str(byte), c] if c else str(byte))
                cols[lo] = col
                col += 1
        out.append(dict(label=label, cells=cells, cls=cls, value=value))
    return dict(t='grid', rows=out, now=[], gaps=gaps), cols


def cut_octets(*prefixes):
    """Octets a prefix boundary falls inside."""
    return {p // 8 for p in prefixes if p is not None and p % 8 and p < 32}


def _grid(rows, expand, hide=(), now_bits=()):
    g, cols = bit_grid(rows, expand, hide)
    g['now'] = sorted({cols[i] for i in now_bits if i in cols})
    return g


def _plural(n, word):
    return f'{n} {word}' + ('' if n == 1 else 's')


# ---------------------------------------------------------------- same subnet?

def same_subnet_animation(qid, spec):
    hosts = spec['hosts']
    steps, out = [], {}
    rule = 'Two addresses are in the same network when ANDing each with the mask gives the same network address: a 1 in the mask keeps the bit, a 0 clears it.'
    if 'mask' in spec:                      # one mask, several hosts: which share a subnet?
        mask = spec['mask']
        p = prefix_of(mask)
        m = mask_of(p)
        ex = cut_octets(p)
        steps.append(step(f'The mask {mask} has {p} leading 1 bits, so it is /{p}. {rule}',
                          _grid([('Mask', m, p, f'/{p}', None, None)], ex)))
        rows, nets = [], {}
        for name, addr in hosts:
            a = ip(addr)
            net = a & m
            nets.setdefault(net, []).append(name)
            rows.append([name, addr, ip_text(net)])
            steps.append(step(f'{name}: {addr} AND {mask} = {ip_text(net)}.',
                              _grid([(name, a, p, addr, None, None), ('Mask', m, p, mask, 'muted', None),
                                     ('AND', net, p, ip_text(net), 'sum', None)], ex, now_bits=range(p)),
                              table(['Host', 'Address', 'Network'], rows, len(rows) - 1)))
        groups = list(nets.values())
        text = '; '.join((_list(g) + (' share ' if len(g) > 1 else ' is alone in ') + ip_text(n)) for n, g in nets.items())
        steps.append(step(f'Compare the network addresses: {text}.', table(['Host', 'Address', 'Network'], rows),
                          line('Same subnet: ' + ('; '.join(_list(g) for g in groups if len(g) > 1) or 'none'), 'steps-time')))
        out['groups'] = groups
        short, title = 'Subnets', f'Mask {mask} (/{p})'
    elif 'masks' in spec:                   # two hosts, several masks: which masks separate them?
        (na, aa), (nb, ab) = hosts
        a, b = ip(aa), ip(ab)
        steps.append(step(f'{rule} Try each mask on {na} = {aa} and {nb} = {ab}.'))
        rows, sep = [], []
        for mask in spec['masks']:
            p = prefix_of(mask)
            m = mask_of(p)
            ex = cut_octets(p) | ({3} if p >= 24 else set())
            x, y = a & m, b & m
            same = x == y
            if not same:
                sep.append(mask)
            rows.append([f'/{p}', ip_text(x), ip_text(y), 'same' if same else 'different'])
            steps.append(step(f'With {mask} (/{p}): {na} gives {ip_text(x)} and {nb} gives {ip_text(y)}, ' +
                              ('the same network.' if same else 'different networks.'),
                              _grid([(na, a, p, aa, None, None), (nb, b, p, ab, None, None), ('Mask', m, p, mask, 'muted', None),
                                     (f'{na} AND', x, p, ip_text(x), 'sum', None), (f'{nb} AND', y, p, ip_text(y), 'sum' if same else 'sum bad', None)],
                                    ex, now_bits=range(p)),
                              table(['Mask', na, nb, 'Result'], rows, len(rows) - 1)))
        steps.append(step(('Only ' if len(sep) == 1 else '') + _list(sep) + (' puts' if len(sep) == 1 else ' put') +
                          f' {na} and {nb} in different networks, so ' + ('it' if len(sep) == 1 else 'they') + ' must not be used.',
                          table(['Mask', na, nb, 'Result'], rows), line('Separating mask: ' + _list(sep), 'steps-time')))
        out['separating'] = sep
        short, title = 'Masks', f'{na} and {nb} under each mask'
    else:                                   # each host applies its own mask
        steps.append(step(f'{rule} Each host applies its own mask to both addresses.'))
        views, rows = {}, []
        for name, addr, mask in hosts:
            p = prefix_of(mask)
            m = mask_of(p)
            a = ip(addr)
            for other, oaddr, _ in hosts:
                if other == name:
                    continue
                o = ip(oaddr)
                same = (a & m) == (o & m)
                verdict = 'local' if same else 'remote'
                views.setdefault(name, {})[other] = verdict
                rows.append([name, f'/{p}', ip_text(a & m), ip_text(o & m), verdict])
                steps.append(step(f'{name} uses {mask} (/{p}): its own network is {ip_text(a & m)} and {other} masks to {ip_text(o & m)}, ' +
                                  ('the same, so ' + name + f' treats {other} as local.' if same else 'different, so ' + name + f' treats {other} as remote.'),
                                  _grid([(name, a, p, addr, None, None), (other, o, p, oaddr, None, None), ('Mask', m, p, mask, 'muted', None),
                                         (f'{name} AND', a & m, p, ip_text(a & m), 'sum', None),
                                         (f'{other} AND', o & m, p, ip_text(o & m), 'sum' if same else 'sum bad', None)],
                                        cut_octets(p), now_bits=range(p)),
                                  table(['Host', 'Mask', 'Own network', 'Other', 'Verdict'], rows, len(rows) - 1)))
        text = '; '.join(f'{v} sees {o} as {w}' for v, d in views.items() for o, w in d.items())
        steps.append(step(f'The masks differ, so the views need not agree: {text}.', table(['Host', 'Mask', 'Own network', 'Other', 'Verdict'], rows),
                          line(text[0].upper() + text[1:], 'steps-time')))
        out['views'] = views
        short, title = 'Views', 'Each host applies its own mask'
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('same-subnet', short, title, steps)


def _list(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


# ---------------------------------------------------------------- sizes

CLASS_PREFIX = {'A': 8, 'B': 16, 'C': 24}


def subnet_size_animation(qid, spec):
    steps, out = [], {}
    if 'subnets' in spec:                   # mask for a number of subnets of a classful network
        base = CLASS_PREFIX[spec['class']]
        k = (spec['subnets'] - 1).bit_length()  # the smallest k with 2^k >= subnets
        p = base + k
        m = mask_of(p)
        ex = cut_octets(base, p)
        steps.append(step(f'A class {spec["class"]} network has a {base}-bit network part, so {32 - base} bits are left for subnets and hosts.',
                          _grid([('Class ' + spec['class'], mask_of(base), base, f'/{base}', None, None)], ex)))
        steps.append(step(f'{spec["subnets"]} subnets need {k} subnet bits, because 2^{k} = {1 << k}' +
                          (f' and 2^{k - 1} = {1 << (k - 1)} is too few.' if k else '.'),
                          _grid([('Class ' + spec['class'], mask_of(base), base, f'/{base}', 'muted', None),
                                 ('Mask', m, p, f'/{p}', None, {i: 'new' for i in range(base, p)})], ex, now_bits=range(base, p)),
                          line(f'Subnet bits: {k}')))
        mt = ip_text(m)
        steps.append(step(f'The prefix grows to {base} + {k} = {p} bits. Written in decimal, the mask is {mt}, leaving {32 - p} host bits per subnet.',
                          _grid([('Mask', m, p, mt, 'sum', None)], ex), line(f'Mask: {mt}', 'steps-time')))
        out['mask'] = mt
        short, title = 'Mask', f'{spec["subnets"]} subnets of a class {spec["class"]} network'
    else:
        if 'mask' in spec:
            p = prefix_of(spec['mask'])
            mt = spec['mask']
        else:
            p = spec['prefix']
            mt = ip_text(mask_of(p))
        m = mask_of(p)
        ex = cut_octets(p)
        ones = [bin((m >> (24 - 8 * o)) & 255).count('1') for o in range(4)]
        if 'address' not in spec:
            steps.append(step(f'Write the mask {mt} in binary. Its 1 bits, ' + ' + '.join(str(x) for x in ones if x) + f' = {p}, are the network part.',
                              _grid([('Mask', m, p, f'/{p}', None, None)], ex | {o for o in range(4) if 0 < ones[o] < 8})))
        h = 32 - p
        total = 1 << h
        hosts = total - 2 if h >= 2 else 0
        if 'address' in spec:
            a = ip(spec['address'])
            net, bc = a & m, a | (~m & 0xFFFFFFFF)
            steps.append(step(f'/{p} means the mask {mt}: {p} network bits and {h} host bits.',
                              _grid([('Address', a, p, spec['address'], None, None), ('Mask', m, p, mt, 'muted', None)], ex)))
            steps.append(step(f'Set every host bit to 0 to get the network address {ip_text(net)}.',
                              _grid([('Address', a, p, spec['address'], 'muted', None),
                                     ('Network', net, p, ip_text(net), 'sum', {i: 'new' for i in range(p, 32)})], ex, now_bits=range(p, 32))))
            steps.append(step(f'Set every host bit to 1 to get the broadcast address {ip_text(bc)}.',
                              _grid([('Address', a, p, spec['address'], 'muted', None), ('Network', net, p, ip_text(net), 'muted', None),
                                     ('Broadcast', bc, p, ip_text(bc), 'sum', {i: 'new' for i in range(p, 32)})], ex, now_bits=range(p, 32))))
            first, last = net + 1, bc - 1
            steps.append(step(f'Hosts use the addresses in between: {ip_text(first)} to {ip_text(last)}. The last usable host is {ip_text(last)}, whose fourth octet is {last & 255}.',
                              table(['Address', 'Use'], [[ip_text(net), 'network'], [ip_text(first), 'first host'], [ip_text(last), 'last host'], [ip_text(bc), 'broadcast']], 2),
                              line(f'Last host: {ip_text(last)}', 'steps-time')))
            out.update(network=ip_text(net), broadcast=ip_text(bc), last_host=ip_text(last), last_host_octet4=last & 255)
            short, title = 'Block', f'{spec["address"]}/{p}'
        else:
            steps.append(step(f'That leaves 32 − {p} = {h} host bits, so the subnet has 2^{h} = {total} addresses.',
                              _grid([('Mask', m, p, f'/{p}', None, None)], ex), line(f'Addresses: {total}')))
            steps.append(step(f'The all-0 host part names the subnet and the all-1 host part is its broadcast address, so {total} − 2 = {hosts} addresses are left for hosts.',
                              table(['Host bits', 'Addresses', 'Reserved', 'Usable hosts'], [[h, total, 2, hosts]]), line(f'Hosts: {hosts}', 'steps-time')))
            short, title = 'Hosts', f'Mask {mt} (/{p})'
        out.update(prefix=p, addresses=total, hosts=hosts)
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('subnet-size', short, title, steps)


# ---------------------------------------------------------------- CIDR blocks

def _range(a, p):
    m = mask_of(p)
    return a & m, (a & m) | (~m & 0xFFFFFFFF)


def cidr_check_animation(qid, spec):
    parent = block(spec['parent']) if 'parent' in spec else None
    need = spec['need']
    steps, rows = [], []
    if parent:
        pa, pp = parent
        if pa & mask_of(pp) != pa:
            raise SystemExit(f'Animation for {qid}: parent {spec["parent"]} is not aligned')
        plo, phi = _range(pa, pp)
        psize = 1 << (32 - pp)
    intro = []
    if parent:
        intro.append(f'The parent block {spec["parent"]} runs from {ip_text(plo)} to {ip_text(phi)}, {psize} addresses.')
    if 'hosts' in need:
        intro.append(f'A block for {need["hosts"]} hosts needs at least {need["hosts"]} + 2 addresses (network and broadcast).')
    if 'addresses' in need:
        intro.append(f'A block for {need["addresses"]} addresses needs at least that many.')
    if 'range' in need:
        lo, hi = map(ip, need['range'])
        intro.append(f'The block must cover exactly {need["range"][0]} to {need["range"][1]}: {hi - lo + 1} addresses.')
    if 'shares' in need:
        sizes = [Fraction(s) * psize for s in need['shares']]
        intro.append('The shares need ' + _list([f'{s} = {int(z)} addresses' for s, z in zip(need['shares'], sizes)]) + '.')
    intro.append('A block a.b.c.d/p is valid only if its host bits are all 0 (it starts on a multiple of its size).')
    steps.append(step(' '.join(intro)))

    def check(text, want_size=None):
        a, p = block(text)
        m = mask_of(p)
        lo, hi = _range(a, p)
        size = 1 << (32 - p)
        aligned = (a & m) == a
        inside = parent is None or (plo <= lo and hi <= phi)
        if 'hosts' in need:
            big, why = size - 2 >= need['hosts'], f'{size - 2} hosts'
        elif 'addresses' in need:
            big, why = size >= need['addresses'], f'{size} addresses'
        elif 'range' in need:
            big, why = (lo, hi) == tuple(map(ip, need['range'])), f'{size} addresses'
        else:
            big, why = size == want_size, f'{size} addresses'
        ok = aligned and inside and big
        bad = {i: 'bad' for i in range(p, 32) if (a >> (31 - i)) & 1}
        g = _grid([(text, a, p, ip_text(a), None, bad), ('Mask', m, p, ip_text(m), 'muted', None), ('AND', a & m, p, ip_text(a & m), 'sum', None)],
                  cut_octets(p), now_bits=range(p, 32))
        parts = []
        parts.append(f'its host bits are all 0, so it is aligned' if aligned else f'its host bits are not all 0 (it masks to {ip_text(a & m)}), so it is not a valid block start')
        if aligned:
            parts.append(f'it covers {ip_text(lo)} to {ip_text(hi)}')
            if parent:
                parts.append('inside the parent block' if inside else 'outside the parent block')
            if 'range' in need:
                parts.append('exactly the required range' if big else 'not the required range')
            elif want_size is not None:
                parts.append(f'{size} addresses, ' + ('the right size' if big else f'not {int(want_size)}'))
            else:
                parts.append(f'{why}, ' + ('enough' if big else 'too few'))
        return ok, (lo, hi), g, parts, size, aligned, inside

    def row(text, r, size, aligned, inside, ok):
        return [text, f'{ip_text(r[0])} – {ip_text(r[1])}' if aligned else '—', size, 'yes' if aligned else 'no',
                ('yes' if inside else 'no') if parent and aligned else '—', 'valid' if ok else 'invalid']

    head = ['Block', 'Range', 'Size', 'Aligned', 'Inside'] if parent else ['Block', 'Range', 'Size', 'Aligned']
    valid = []
    for cand in spec['candidates']:
        if isinstance(cand, list):         # an allocation of several blocks, one per share
            oks, ranges = [], []
            for text, z in zip(cand, sizes):
                ok, r, g, parts, size, aligned, inside = check(text, z)
                oks.append(ok)
                ranges.append(r)
                rows.append(row(text, r, size, aligned, inside, ok)[:len(head)] + ['ok' if ok else 'invalid'])
                steps.append(step(f'{text}: ' + '; '.join(parts) + '.', g, table(head + ['Result'], rows, len(rows) - 1)))
            disjoint = all(ranges[i][1] < ranges[j][0] or ranges[j][1] < ranges[i][0] for i in range(len(ranges)) for j in range(i + 1, len(ranges)))
            ok = all(oks) and disjoint
            if ok:
                valid.append(cand)
            steps.append(step(f'Together: ' + (' and '.join(cand)) + (' do not overlap' if disjoint else ' overlap') +
                              (', and both are valid, so this allocation works.' if ok else ', so this allocation fails.' if all(oks) else '; at least one block is invalid, so this allocation fails.'),
                              table(head + ['Result'], rows, len(rows) - 1)))
        else:
            ok, r, g, parts, size, aligned, inside = check(cand)
            if ok:
                valid.append(cand)
            rows.append(row(cand, r, size, aligned, inside, ok)[:len(head)] + ['valid' if ok else 'invalid'])
            steps.append(step(f'{cand}: ' + '; '.join(parts) + '. ' + ('Valid.' if ok else 'Not valid.'), g, table(head + ['Result'], rows, len(rows) - 1)))
    names = [' and '.join(v) if isinstance(v, list) else v for v in valid]
    steps.append(step('Valid: ' + (_list(names) if names else 'none') + '.', table(head + ['Result'], rows),
                      line('Valid: ' + ('; '.join(names) if names else 'none'), 'steps-time')))
    _check(qid, 'valid', valid, spec['expect']['valid'])
    return _finish('cidr-check', 'Blocks', 'Check each block: aligned, the right size' + (', inside the parent' if parent else ''), steps)


# ---------------------------------------------------------------- longest-prefix match

def lpm_animation(qid, spec):
    routes = []
    for dest, hop in spec['routes']:
        if isinstance(dest, list):
            a, p = ip(dest[0]), prefix_of(dest[1])
            text = f'{dest[0]}/{p}'
        else:
            (a, p), text = block(dest), dest
        if a & mask_of(p) != a:
            raise SystemExit(f'Animation for {qid}: route {text} has host bits set')
        routes.append((text, a, p, str(hop)))
    default = spec.get('default')
    steps = [step('A destination matches a route when its first p bits equal the route prefix. Among the matches the router takes the longest prefix' +
                  (f'; with no match it uses the default route ({default}).' if default else '.'),
                  table(['Prefix', 'Next hop'], [[t, h] for t, _, _, h in routes] + ([['default', default]] if default else [])))]
    rows, hops = [], []
    prefixes = [p for _, _, p, _ in routes]
    for dtext in spec['destinations']:
        d = ip(dtext)
        # Leading octets fixed by every prefix and equal everywhere are shown once; octets no prefix reaches are left out.
        hide = set()
        for o in range(4):
            if all(p >= 8 * (o + 1) for p in prefixes) and len({(x >> (24 - 8 * o)) & 255 for x in [d] + [a for _, a, _, _ in routes]}) == 1:
                hide.add(o)
            else:
                break
        hide |= {o for o in range(4) if all(p <= 8 * o for p in prefixes)}
        expand = cut_octets(*prefixes) - hide
        grows, matches = [('Destination', d, None, '', None, None)], []
        for text, a, p, hop in routes:
            ok = (d & mask_of(p)) == a
            marks = {}
            for i in range(32):
                if i >= p:
                    marks[i] = 'muted'
                else:
                    marks[i] = 'ok' if ((d >> (31 - i)) & 1) == ((a >> (31 - i)) & 1) else 'bad'
            for o in range(4):     # a decimal octet inside the prefix that differs is marked as a whole
                if o not in expand and 8 * o < p and ((d >> (24 - 8 * o)) & 255) != ((a >> (24 - 8 * o)) & 255):
                    marks[8 * o] = 'bad'
            grows.append((f'/{p} → {hop}', a, p, '✓' if ok else '✗', None if ok else 'muted-row', marks))
            if ok:
                matches.append((p, text, hop))
        common = '.'.join(str((d >> (24 - 8 * o)) & 255) for o in sorted(hide) if o < min(o2 for o2 in range(4) if o2 not in hide)) if hide else ''
        if matches:
            p, text, hop = max(matches)
            if [m[0] for m in matches].count(p) > 1:
                raise SystemExit(f'Animation for {qid}: two routes of length /{p} match {dtext}')
            note = f'{dtext} matches ' + _list([m[1] for m in matches]) + f'. The longest is /{p}, so it goes to {hop}.'
        else:
            if not default:
                raise SystemExit(f'Animation for {qid}: {dtext} matches no route and there is no default')
            hop, p = default, None
            note = f'{dtext} matches no prefix, so it takes the default route to {hop}.'
        hops.append(hop)
        rows.append([dtext, ', '.join(f'/{m[0]}' for m in matches) or 'none', hop])
        blocks = [line(f'All rows start {common}; the remaining octets are shown.') if common else None,
                  _grid(grows, expand, hide),
                  table(['Destination', 'Matching prefixes', 'Next hop'], rows, len(rows) - 1)]
        steps.append(step(note, *blocks))
    out = dict(hops=hops)
    final = table(['Destination', 'Matching prefixes', 'Next hop'], rows)
    if 'count' in spec:
        target, each = spec['count']['hop'], spec['count']['packets_each']
        n = hops.count(target)
        out['count'] = n * each
        steps.append(step(f'{_plural(n, "destination")} use{"s" if n == 1 else ""} {target}, each with {each} packets: {n} × {each} = {n * each} packets.',
                          final, line(f'Packets via {target}: {n * each}', 'steps-time')))
    else:
        steps.append(step('Next hops: ' + ', '.join(f'{d} → {h}' for d, h in zip(spec['destinations'], hops)) + '.', final,
                          line('Next hop' + ('s' if len(hops) > 1 else '') + ': ' + ', '.join(hops), 'steps-time')))
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('lpm', 'Forwarding', 'Longest-prefix match', steps)


# ---------------------------------------------------------------- fragmentation

def fragment(frags, mtu, header):
    """Split each (offset, length, more) whose header + length exceeds the MTU.
    Non-final pieces carry a multiple of 8 bytes. Returns the new list and the split made of each input."""
    room = (mtu - header) // 8 * 8
    if room <= 0:
        raise SystemExit(f'MTU {mtu} leaves no room after a {header}-byte header')
    out, splits = [], []
    for off, length, more in frags:
        if header + length <= mtu:
            out.append((off, length, more))
            splits.append(None)
            continue
        pieces, at = [], off
        while at < off + length:
            rest = off + length - at
            take = rest if header + rest <= mtu else room  # only the final piece may be a non-multiple of 8
            last = at + take == off + length
            pieces.append((at, take, more if last else True))
            at += take
        out += pieces
        splits.append(pieces)
    return out, splits, room


def _sizes(ns):
    """[80, 80, 80, 20] -> '3 × 80 + 20'."""
    out, k = [], 0
    while k < len(ns):
        j = k
        while j < len(ns) and ns[j] == ns[k]:
            j += 1
        out.append(f'{j - k} × {ns[k]}' if j - k > 2 else ' + '.join([str(ns[k])] * (j - k)))
        k = j
    return ' + '.join(out)


def _frag_rows(frags, header):
    return [[k + 1, f'{off}–{off + n - 1}', n, header + n, off // 8, 1 if more else 0] for k, (off, n, more) in enumerate(frags)]


FRAG_HEAD = ['#', 'Payload bytes', 'Payload', 'Total length', 'Offset (÷8)', 'MF']


def _frags_block(stages, total):
    rows = []
    for label, frags, cls in stages:
        rows.append(dict(label=label, parts=[[off, n, str(n), cls] for off, n, _ in frags]))
    return dict(t='frags', total=total, rows=rows)


def fragment_run(spec, header):
    if 'payload' in spec:
        payload = spec['payload']
    else:
        payload = spec['total'] - header
    frags = [(0, payload, False)]
    history = []
    for mtu in spec['mtus']:
        frags, splits, room = fragment(frags, mtu, header)
        history.append((mtu, frags, splits, room))
    return payload, frags, history


def fragment_animation(qid, spec):
    header = spec.get('header', 20)
    payload, frags, history = fragment_run(spec, header)
    parts = spec.get('parts')
    if parts and sum(n for _, n in parts) != payload:
        raise SystemExit(f'Animation for {qid}: the payload parts do not add up to {payload}')
    if 'payload' in spec:
        how = (f'the {payload}-byte {parts[0][0]}' if len(parts) == 1 else ' + '.join(f'{n} bytes of {what}' for what, n in parts) + f' = {payload} bytes') \
            if parts else f'{payload} bytes'
        first = f'The IP payload is {how}. Each fragment gets its own {header}-byte IP header.'
    else:
        first = f'The datagram is {spec["total"]} bytes including its {header}-byte header, so the payload is {spec["total"]} − {header} = {payload} bytes' + \
            (f' ({_list([f"{n} bytes of {what}" for what, n in parts])})' if parts else '') + '. Each fragment gets its own header.'
    steps = [step(first + ' Offsets count 8-byte units, so every fragment except the last must carry a multiple of 8 bytes.',
                  _frags_block([('Payload', [(0, payload, False)], 0)], payload))]
    stages = [('Payload', [(0, payload, False)], 0)]
    prev = [(0, payload, False)]
    for k, (mtu, frags_now, splits, room) in enumerate(history):
        label = spec['links'][k] if 'links' in spec else f'MTU {mtu}'
        raw = mtu - header
        cap = (f'{label}: the MTU' if 'links' in spec else 'The MTU') + f' {mtu} leaves {mtu} − {header} = {raw} bytes for data' + \
            (f', rounded down to a multiple of 8: {room}.' if raw != room else f', a multiple of 8.')
        if all(s is None for s in splits):
            stages.append((label, frags_now, k + 1))
            steps.append(step(f'{cap} ' + ('Everything already fits, so nothing changes.' if len(prev) > 1 else f'The {header + prev[0][1]}-byte datagram fits, so nothing changes.'),
                              _frags_block(stages, payload), table(FRAG_HEAD, _frag_rows(frags_now, header))))
            prev = frags_now
            continue
        steps.append(step(cap + (' Routers do not reassemble: each arriving fragment is split on its own.' if len(prev) > 1 else ''),
                          _frags_block(stages, payload)))
        done = []
        for (off, n, more), piece in zip(prev, splits):
            if piece is None:
                done.append((off, n, more))
                note = f'The {n}-byte piece at byte {off} fits, so it passes unchanged.'
            else:
                done += piece
                sizes = _sizes([x[1] for x in piece])
                note = (f'The {n}-byte piece at byte {off} is too big: split it into {sizes}.' if k or len(prev) > 1
                        else f'Split the {n} bytes into {sizes}: ' + _plural(len(piece), 'fragment') + '.')
            steps.append(step(note, _frags_block(stages + [(label, done, k + 1)], payload),
                              table(FRAG_HEAD, _frag_rows(done, header), len(done) - 1)))
        stages.append((label, frags_now, k + 1))
        prev = frags_now
    out = dict(count=len(frags), delivered_bytes=sum(header + n for _, n, _ in frags),
               last_offset=frags[-1][0] // 8, last_total=header + frags[-1][1])
    for i, (off, n, more) in enumerate(frags):
        out.update({f'fragment_{i + 1}_mf': 1 if more else 0, f'fragment_{i + 1}_total': header + n, f'fragment_{i + 1}_offset': off // 8})
    if any(off % 8 for off, _, _ in frags):
        raise SystemExit(f'Animation for {qid}: a fragment starts off an 8-byte boundary')
    if sum(n for _, n, _ in frags) != payload:
        raise SystemExit(f'Animation for {qid}: the fragments lose bytes')
    ask = spec.get('ask', ['count'])
    bits = []
    if 'count' in ask:
        bits.append(f'{len(frags)} fragments arrive')
    if 'delivered_bytes' in ask:
        bits.append('their total length is ' + ' + '.join(str(header + n) for _, n, _ in frags) + f' = {out["delivered_bytes"]} bytes')
    if 'last' in ask:
        bits.append(f'the last one starts at byte {frags[-1][0]}, offset {frags[-1][0]} ÷ 8 = {out["last_offset"]}, and is {header} + {frags[-1][1]} = {out["last_total"]} bytes long')
    for a in ask:
        if a.startswith('fragment_'):
            i = int(a.split('_')[1])
            off, n, more = frags[i - 1]
            bits.append(f'fragment {i} has MF = {1 if more else 0}, total length {header} + {n} = {header + n} and offset {off} ÷ 8 = {off // 8}')
    rows = _frag_rows(frags, header)
    hl = int(ask[0].split('_')[1]) - 1 if ask[0].startswith('fragment_') else len(frags) - 1 if 'last' in ask else None
    note = '; '.join(bits) + '.'
    if spec.get('header_unstated'):
        # The question gives no header size: the count must not depend on it.
        for h in range(20, 61, 4):
            if len(fragment_run(spec, h)[1]) != len(frags):
                raise SystemExit(f'Animation for {qid}: the fragment count changes with a {h}-byte header')
        note += f' The question does not give the header size; any legal IPv4 header (20 to 60 bytes) gives the same count.'
    steps.append(step(note[0].upper() + note[1:], _frags_block(stages, payload), table(FRAG_HEAD, rows, hl),
                      line('Answer: ' + '; '.join(bits), 'steps-time')))
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('fragment', 'Fragments', 'IPv4 fragmentation, MTU ' + ' then '.join(str(m) for m in spec['mtus']), steps)


def fragment_header_animation(qid, spec):
    mf, hlen, total, off = spec['mf'], spec['hlen'], spec['total'], spec['offset']
    hb = hlen * 4
    n = total - hb
    first = off * 8
    last = first + n - 1
    pos = 'last' if mf == 0 and off > 0 else 'first' if mf == 1 and off == 0 else 'middle' if mf == 1 else 'only'
    rows = []
    steps = [step(f'Read the fields: MF = {mf}, HLEN = {hlen}, total length = {total}, fragment offset = {off}.',
                  table(['Field', 'Value', 'Meaning'], [['MF', mf, ''], ['HLEN', hlen, ''], ['Total length', total, ''], ['Offset', off, '']]))]
    rows.append(['MF and offset', f'{mf}, {off}', {'last': 'MF = 0 and offset > 0: the last fragment', 'first': 'MF = 1 and offset 0: the first fragment',
                                                   'middle': 'MF = 1 and offset > 0: a middle fragment', 'only': 'MF = 0 and offset 0: not fragmented'}[pos]])
    steps.append(step(f'MF = {mf} and offset {off}: this is the {pos} fragment.' if pos != 'only' else 'MF = 0 and offset 0: the datagram is not fragmented.',
                      table(['Quantity', 'Value', 'Why'], rows, 0)))
    rows.append(['Header', f'{hb} bytes', f'HLEN counts 4-byte words: {hlen} × 4'])
    rows.append(['Payload', f'{n} bytes', f'{total} − {hb}'])
    steps.append(step(f'HLEN counts 4-byte words, so the header is {hlen} × 4 = {hb} bytes and the payload is {total} − {hb} = {n} bytes.',
                      table(['Quantity', 'Value', 'Why'], rows, 2)))
    rows.append(['First byte', first, f'offset × 8 = {off} × 8'])
    rows.append(['Last byte', last, f'{first} + {n} − 1'])
    steps.append(step(f'The offset counts 8-byte units: the first payload byte is number {off} × 8 = {first}, and the last is {first} + {n} − 1 = {last}.',
                      _frags_block([('This fragment', [(first, n, False)], 1)], max(last + 1, first + n)),
                      table(['Quantity', 'Value', 'Why'], rows, 4), line(f'{pos.capitalize()} fragment, bytes {first} to {last}', 'steps-time')))
    out = dict(position=pos, first=first, last=last)
    for k, v in spec['expect'].items():
        _check(qid, k, out.get(k), v)
    return _finish('fragment-header', 'Header', 'Reading an IPv4 fragment header', steps)


KINDS = {'same-subnet': same_subnet_animation, 'subnet-size': subnet_size_animation, 'cidr-check': cidr_check_animation,
         'lpm': lpm_animation, 'fragment': fragment_animation, 'fragment-header': fragment_header_animation}
PLAYER = 'subnet'
TABS = 'parts'
