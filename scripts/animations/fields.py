"""Address fields: cache tag/index/offset, TLB tags, paging and translation.

Data: data/animations/fields.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from .common import _log2, _size


def address_fields(spec):
    """Derive address fields (tag/index/offset, page number/offset) and related sizes.

    Every value is computed from the stated parameters; sizes are in addressable
    units unless the spec says otherwise.
    """
    mode, unit = spec['mode'], spec.get('unit', 'byte')
    U = 'B' if unit == 'byte' else ' words'
    rows, steps, fields, out = [], [], [], {}

    def step(name, value, how, note, field=None):
        if field:
            fields.insert(0, field)
        rows.append([name, value, how])
        steps.append(dict(fields=[list(f) for f in fields], rows=[list(r) for r in rows], note=note))

    steps.append(dict(fields=[], rows=[], note=spec.get('intro', 'Work out each field from the right: the offset first, then the index, and the tag is what is left.' if mode in ('cache', 'tlb') else 'Split the address into page number and offset, then size the tables.')))
    if 'address_bits' in spec:
        A = spec['address_bits']
        step('Address bits', A, 'given', f'Addresses are {A} bits.')
    elif 'memory' in spec:
        A = _log2(spec['memory'], 'memory size')
        step('Address bits', A, f'log₂({_size(spec["memory"], U)})', f'{_size(spec["memory"], U)} of {unit}-addressable memory needs {A}-bit addresses, since 2^{A} = {spec["memory"]}.')
    else:
        A = None
    out['address'] = A
    if mode == 'cache':
        cache, ways = spec['cache'], spec.get('ways', 1)
        block = spec.get('block')
        if block:
            off = _log2(block, 'block size')
            step('Offset bits', off, f'log₂({block})', f"A block holds {spec.get('block_text', _size(block, U))}" + (f' = {block} {unit}s' if spec.get('block_text') else '') + f", so the offset needs {off} bits.", ['Offset', off])
            out['offset'] = off
            lines = cache // block
            step('Lines', lines, f'{_size(cache, U)} ÷ {_size(block, U)}', f'The cache holds {_size(cache, U)} in blocks of {_size(block, U)}: {lines} lines.')
            out['lines'] = lines
            if ways == 'full':
                sets, idx = 1, 0
                step('Index bits', 0, 'fully associative', 'Fully associative: any block can go in any line, so there is no index field.')
            else:
                sets = lines // ways
                idx = _log2(sets, 'number of sets')
                how = f'{lines} ÷ {ways}' if ways > 1 else 'one line per set'
                step('Sets' if ways > 1 else 'Index bits', sets if ways > 1 else idx, how if ways > 1 else f'log₂({lines})',
                     (f'{ways}-way: {lines} lines in sets of {ways} gives {sets} sets.' if ways > 1 else f'Direct-mapped: each of the {lines} lines is its own set, so the index needs {idx} bits.'),
                     None if ways > 1 else ['Index', idx])
                if ways > 1:
                    step('Index bits', idx, f'log₂({sets})', f'Choosing one of {sets} sets needs {idx} bits.', ['Index', idx])
            out['sets'], out['index'] = sets, idx
            low = off + idx
        else:
            low = _log2(cache // ways, 'cache size ÷ ways')
            step('Index + offset bits', low, f'log₂({_size(cache, U)} ÷ {ways})', f'Each way holds {_size(cache // ways, U)}, and the index and offset together address one byte of a way: {low} bits, whatever the block size.', ['Index + offset', low])
        if A is not None:
            tag = A - low
            parts = ' − '.join(str(x) for x in [A] + [f[1] for f in fields])
            step('Tag bits', tag, parts, f'The tag is what is left: {parts} = {tag} bits.', ['Tag', tag])
            out['tag'] = tag
            if 'extra_bits' in spec:
                per = tag + spec['extra_bits']
                total = per * out['lines']
                step('Bits per line', per, f'{tag} + {spec["extra_bits"]}', f'Each line stores the {tag}-bit tag plus {spec["extra_bits"]} bits ({spec.get("extra_text", "status bits")}): {per} bits.')
                step('Directory bits', total, f'{per} × {out["lines"]}', f'Over {out["lines"]} lines: {per} × {out["lines"]} = {total} bits = {_size(total, " bits")}.')
                out['directory_bits'] = total
            if spec.get('tag_store'):
                total = tag * out['lines']
                step('Tag storage', total, f'{tag} × {out["lines"]}', f'All tags together: {tag} × {out["lines"]} = {total} bits = {_size(total // 8)}.' if total % 8 == 0 else f'All tags together: {tag} × {out["lines"]} = {total} bits.')
                out['tag_store_bits'] = total
            if 'split' in spec:
                addr = int(spec['split'], 16)
                bits = format(addr, f'0{A}b')
                vals, pos = {}, 0
                for name, w in fields:
                    chunk = bits[pos:pos + w]
                    vals[name] = int(chunk, 2) if chunk else 0
                    pos += w
                text = ', '.join(f'{n} {vals[n]:X}H' for n, _ in fields)
                step('Split of ' + spec['split'].upper() + 'H', text, 'cut the binary into fields', f'{spec["split"].upper()}H in binary is {bits}. Cutting it into fields: {text}.')
                out['split'] = {n: format(v, 'X') for n, v in vals.items()}
    elif mode == 'tlb':
        page, entries, ways = spec['page'], spec['entries'], spec.get('ways', 'full')
        off = _log2(page, 'page size')
        step('Page offset bits', off, f'log₂({_size(page)})', f'Pages are {_size(page)}, so the offset is {off} bits.', ['Offset', off])
        vpn = A - off
        step('Page number bits', vpn, f'{A} − {off}', f'The virtual page number is {A} − {off} = {vpn} bits.')
        sets = 1 if ways == 'full' else entries // ways
        idx = _log2(sets, 'TLB sets')
        if ways != 'full':
            step('TLB sets', sets, f'{entries} ÷ {ways}', f'{entries} entries, {ways}-way: {sets} sets, chosen by the low {idx} bits of the page number.', ['Index', idx])
        tag = vpn - idx
        step('Tag bits', tag, f'{vpn} − {idx}', f'The TLB tag is the rest of the page number: {vpn} − {idx} = {tag} bits.', ['Tag', tag])
        out.update(offset=off, vpn=vpn, sets=sets, index=idx, tag=tag)
    elif mode == 'page':
        page = spec['page']
        off = _log2(page, 'page size')
        step('Offset bits', off, f'log₂({_size(page)})', f'Pages are {_size(page)}, so the offset is {off} bits.', ['Offset', off])
        vpn = A - off
        step('Page number bits', vpn, f'{A} − {off}', f'The page number is the rest: {A} − {off} = {vpn} bits.', ['Page number', vpn])
        out.update(offset=off, vpn=vpn, entries=1 << vpn)
        step('Page-table entries', f'2^{vpn}', 'one per page', f'A one-level table has one entry per virtual page: 2^{vpn} entries.')
        if 'pte' in spec:
            pte = spec['pte']
            size = (1 << vpn) * pte
            step('Table size', _size(size), f'2^{vpn} × {pte} B', f'Each entry is {pte} bytes, so the table takes 2^{vpn} × {pte} = {_size(size)}.')
            out['table_bytes'] = size
            per = page // pte
            if spec.get('levels'):
                k = _log2(per, 'entries per page')
                levels = -(-vpn // k)
                step('Entries per page', per, f'{_size(page)} ÷ {pte} B', f'One page holds {per} entries, so each level resolves {k} bits.')
                step('Levels', levels, f'⌈{vpn} ÷ {k}⌉', f'{vpn} page-number bits at {k} per level need ⌈{vpn}/{k}⌉ = {levels} levels.')
                out['levels'] = levels
            if spec.get('per_page'):
                step('Entries per page', per, f'{_size(page)} ÷ {pte} B', f'One page holds {_size(page)} ÷ {pte} = {per} entries.')
                out['entries_per_page'] = per
            if 'physical_bits' in spec:
                frame = spec['physical_bits'] - off
                spare = pte * 8 - frame
                step('Frame number bits', frame, f'{spec["physical_bits"]} − {off}', f'Physical addresses are {spec["physical_bits"]} bits, so a frame number is {frame} bits.')
                step('Spare bits per entry', spare, f'{pte * 8} − {frame}', f'A {pte * 8}-bit entry has {spare} bits left for protection and other flags.')
                out['spare_bits'] = spare
    elif mode == 'translate':
        page, va, frames = spec['page'], spec['virtual'], spec['frames']
        pg, off = divmod(va, page)
        step('Page', pg, f'⌊{va} ÷ {page}⌋', f'{va} ÷ {page} = page {pg}, remainder {off}.')
        step('Offset', off, f'{va} mod {page}', f'The offset within the page is {off}.')
        fr = frames[pg]
        step('Frame', fr, f'page {pg} → frame {fr}', f'Page {pg} is in frame {fr}.')
        pa = fr * page + off
        step('Physical address', pa, f'{fr} × {page} + {off}', f'Physical address = {fr} × {page} + {off} = {pa}.')
        out['physical'] = pa
    elif mode == 'tlb-size':
        page, reach = spec['page'], spec['reach']
        entries = reach // page
        off = _log2(page, 'page size')
        step('Entries', entries, f'{_size(reach)} ÷ {_size(page)}', f'The TLB covers {_size(reach)} with {_size(page)} pages: {entries} entries.')
        vpn = _log2(spec['virtual'], 'virtual space') - off
        pfn = _log2(spec['physical'], 'physical space') - off
        step('Page number bits', vpn, f'log₂({_size(spec["virtual"])}) − {off}', f'{_size(spec["virtual"])} of virtual space in {_size(page)} pages: {vpn}-bit page numbers.')
        step('Frame number bits', pfn, f'log₂({_size(spec["physical"])}) − {off}', f'{_size(spec["physical"])} of physical memory: {pfn}-bit frame numbers.')
        extra = spec.get('extra_bits', 0)
        bits = vpn + pfn + extra
        step('Bits per entry', bits, f'{vpn} + {pfn} + {extra}', f'Each entry holds the page number, frame number and {extra} other bits ({spec.get("extra_text", "")}): {bits} bits = {bits // 8} bytes.' if bits % 8 == 0 else f'Each entry holds {bits} bits.')
        total = entries * bits // 8
        step('TLB size', total, f'{entries} × {bits // 8} B', f'{entries} entries × {bits // 8} bytes = {total} bytes.')
        out['tlb_bytes'] = total
    else:
        raise SystemExit('Unknown address mode: ' + mode)
    return steps, out, A


def fields_animation(qid, spec):
    steps, out, A = address_fields(spec)
    for k, v in spec['expect'].items():
        if out.get(k) != v:
            raise SystemExit(f'Animation for {qid}: {k} is {out.get(k)}, not {v}')
    steps[-1] = dict(steps[-1], final=True)
    titles = {'cache': 'Cache address fields', 'tlb': 'TLB tag', 'page': 'Paging', 'translate': 'Address translation', 'tlb-size': 'TLB size'}
    return dict(kind='address-fields', bits=A, schedules=[dict(short='Fields', title=titles[spec['mode']], steps=steps)], count=len(steps))



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'address-fields': fields_animation}
PLAYER = 'fields'
