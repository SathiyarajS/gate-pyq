"""Fail-closed Phase 5 content loading and a deliberately small, escaped renderer.

Review metadata is evidence to audit, not proof that a human review occurred.
See docs/TRANSCRIPTIONS.md. No input HTML is trusted.
"""
import datetime
import html
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from markupsafe import Markup


def inline(text, single_dollar=False):
    math_pattern = r'\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$'
    if single_dollar:
        math_pattern += r'|(?<![\\$])\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$(?!\$)'
    # Code is opaque to math and emphasis. Legacy prose never enables single dollars.
    tokens = re.split('(`[^`\n]+`|' + math_pattern + ')', text, flags=re.S)
    result = []
    for token in tokens:
        if token.startswith('`') and token.endswith('`'):
            result.append('<code>' + html.escape(token[1:-1]) + '</code>')
        elif ((token.startswith('\\(') and token.endswith('\\)')) or (token.startswith('\\[') and token.endswith('\\]')) or (token.startswith('$$') and token.endswith('$$') and len(token)>4) or
              (single_dollar and token.startswith('$') and token.endswith('$') and len(token) > 2)):
            size = 2 if token.startswith(('\\(', '\\[', '$$')) else 1
            display = token.startswith(('\\[', '$$'))
            result.append('<span class="math-source" data-math="' + html.escape(token[size:-size], quote=True) + '" data-display="' + str(display).lower() + '">' + html.escape(token) + '</span>')
        else:
            safe = html.escape(token.replace(r'\|', '|'))
            safe = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', safe)
            safe = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', safe)
            result.append(safe)
    return ''.join(result)


def rich(value, single_dollar=False):
    def cells(line):
        line = line.strip()
        if line.startswith('|'): line = line[1:]
        if line.endswith('|') and not line.endswith(r'\|'): line = line[:-1]
        # Pipes inside math/code are content, not cell separators. Preserve tokens
        # verbatim; escaped prose pipes are unescaped only by inline().
        protected = r'(`[^`\n]*`|\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$|(?<![\\$])\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$(?!\$))'
        output = ['']
        for index, part in enumerate(re.split(protected, line)):
            if index % 2:
                output[-1] += part
            else:
                pieces = re.split(r'(?<!\\)\|', part)
                output[-1] += pieces[0]
                output.extend(pieces[1:])
        return output
    result = []
    chunks = re.split(r'(```[^\n]*\n.*?```|^[ \t]*\\\[.*?\\\][ \t]*(?=\n|$)|^[ \t]*\$\$.*?\$\$[ \t]*(?=\n|$))', str(value or ''), flags=re.S | re.M)
    for chunk in chunks:
        if chunk.startswith('```'):
            result.append('<pre><code>' + html.escape(chunk.split('\n', 1)[-1].removesuffix('```')) + '</code></pre>')
            continue
        if chunk.strip().startswith(('$$', r'\[')) and chunk.strip().endswith(('$$', r'\]')):
            result.append(inline(chunk.strip(), single_dollar)); continue
        lines = chunk.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if i + 1 < len(lines) and '|' in line and all(re.fullmatch(r'\s*:?-{3,}:?\s*', c) for c in cells(lines[i + 1])):
                heads = cells(line)
                rows = []
                i += 2
                while i < len(lines) and '|' in lines[i] and lines[i].strip():
                    rows.append(cells(lines[i])); i += 1
                result.append('<div class="table-scroll"><table><thead><tr>' + ''.join('<th scope="col">' + inline(c.strip(), single_dollar) + '</th>' for c in heads) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + inline(c.strip(), single_dollar) + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>')
                continue
            match = re.match(r'^\s*(?:(\d+)[.)]|([-*]))\s+(.*)', line)
            if match:
                tag = 'ol' if match[1] else 'ul'
                items = []
                start = ' start="' + str(int(match[1])) + '"' if match[1] else ''
                while i < len(lines):
                    m = re.match(r'^\s*(?:(\d+)[.)]|([-*]))\s+(.*)', lines[i])
                    if not m or bool(m[1]) != bool(match[1]): break
                    items.append('<li' + (' value="' + str(int(m[1])) + '"' if m[1] else '') + '>' + inline(m[3], single_dollar) + '</li>'); i += 1
                result.append('<' + tag + start + '>' + ''.join(items) + '</' + tag + '>')
                continue
            result.append('<p>' + inline(line, single_dollar) + '</p>'); i += 1
    return Markup(''.join(result))


SVG_TAGS = {'svg', 'g', 'path', 'line', 'polyline', 'polygon', 'rect', 'circle', 'ellipse', 'text', 'tspan', 'title', 'desc', 'defs', 'marker'}
SVG_ATTRS = {'viewBox', 'xmlns', 'role', 'aria-label', 'id', 'd', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'dx', 'dy', 'cx', 'cy', 'r', 'rx', 'ry', 'points', 'width', 'height', 'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'stroke-dasharray', 'fill-rule', 'text-anchor', 'dominant-baseline', 'font-size', 'font-family', 'font-weight', 'transform', 'opacity', 'fill-opacity', 'stroke-opacity', 'marker-start', 'marker-mid', 'marker-end', 'markerWidth', 'markerHeight', 'refX', 'refY', 'orient', 'markerUnits', 'preserveAspectRatio'}


def safe_svg(root, name):
    """Return only an allowlisted inline SVG, or raise. Never load external resources."""
    if not isinstance(name, str) or not re.fullmatch(r'figures/[A-Za-z0-9_-]+\.svg', name):
        raise ValueError('Figure must be a local figures/<name>.svg path')
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_relative_to((root / 'figures').resolve()) or (root / name).is_symlink():
        raise ValueError('Figure escapes figures directory')
    raw = path.read_text()
    if len(raw) > 1_000_000 or '<!' in raw or '<?' in raw:
        raise ValueError('SVG declarations/entities are unsupported')
    tree = ET.fromstring(raw)
    if tree.tag not in ('svg', '{http://www.w3.org/2000/svg}svg'):
        raise ValueError('Not an SVG document')
    vb = [float(x) for x in re.split(r'[\s,]+', tree.get('viewBox', '').strip())]
    if len(vb) != 4 or not all(math.isfinite(x) for x in vb) or vb[2] <= 0 or vb[3] <= 0 or 'width' in tree.attrib or 'height' in tree.attrib:
        raise ValueError('SVG needs a finite viewBox and no fixed dimensions')
    ids = set()
    refs = []
    for node in tree.iter():
        tag = node.tag.removeprefix('{http://www.w3.org/2000/svg}')
        if tag not in SVG_TAGS: raise ValueError('Unsupported SVG element: ' + tag)
        node.tag = tag
        for attr, value in node.attrib.items():
            if attr not in SVG_ATTRS: raise ValueError('Unsupported SVG attribute: ' + attr)
            if attr in ('fill', 'stroke') and value not in ('currentColor', 'none'):
                raise ValueError('SVG colors must be currentColor or none')
            if attr == 'id':
                if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', value) or value in ids: raise ValueError('Invalid SVG id')
                ids.add(value)
            if attr.startswith('marker-'):
                m = re.fullmatch(r'url\(#([A-Za-z][A-Za-z0-9_-]*)\)', value)
                if not m: raise ValueError('Only local marker references are supported')
                refs.append(m[1])
            elif re.search(r'url\s*\(|https?:|data:|javascript:|//', value, re.I):
                raise ValueError('External SVG resource forbidden')
        if 'font-size' in node.attrib:
            if not re.fullmatch(r'\d+(?:\.\d+)?(?:px)?', node.attrib['font-size']) or float(node.attrib['font-size'].removesuffix('px')) < 12:
                raise ValueError('SVG text must be at least 12px')
    if any(ref not in ids for ref in refs): raise ValueError('Missing SVG marker')
    # Scope IDs to the content hash to prevent collisions between different figures.
    import hashlib
    prefix = 'f' + hashlib.sha256(raw.encode()).hexdigest()[:16] + '-'
    for node in tree.iter():
        if 'id' in node.attrib: node.set('id', prefix + node.get('id'))
        for attr in ('marker-start', 'marker-mid', 'marker-end'):
            if attr in node.attrib: node.set(attr, node.get(attr).replace('url(#', 'url(#' + prefix))
    tree.set('xmlns', 'http://www.w3.org/2000/svg')
    tree.set('fill', tree.get('fill', 'currentColor'))
    tree.set('font-size', tree.get('font-size', '16'))
    tree.set('role', 'img')
    if not tree.get('aria-label') and not any(n.tag == 'title' and (n.text or '').strip() for n in tree):
        raise ValueError('SVG needs title or aria-label')
    return Markup(ET.tostring(tree, encoding='unicode'))


def checked(entry, pages):
    """Require explicit independent-review evidence. This does not perform review."""
    try:
        date = datetime.date.fromisoformat(entry.get('verified_on', ''))
        review = entry.get('verification', {})
        return (entry.get('status') == 'verified' and date <= datetime.date.today()
                and isinstance(entry.get('notes'), str) and bool(entry['notes'].strip())
                and isinstance(entry.get('checked_pages'), list)
                and all(type(p) is int and p > 0 for p in entry['checked_pages'])
                and set(pages) <= set(entry['checked_pages'])
                and review.get('method') == 'independent-visual-comparison'
                and review.get('solution_checked') is True
                and review.get('rendered_comparison_checked') is True
                and isinstance(review.get('reviewer'), str) and bool(review['reviewer'].strip())
                and isinstance(review.get('transcriber'), str) and bool(review['transcriber'].strip())
                and review['reviewer'].strip() != review['transcriber'].strip())
    except (ValueError, TypeError, AttributeError):
        return False


def render_entry(root, entry, contexts):
    if not isinstance(entry, dict) or not isinstance(entry.get('stem'), str) or not entry['stem'].strip(): raise ValueError('Missing stem')
    options = entry.get('options', {})
    figures = entry.get('figures', [])
    refs = entry.get('shared_context_refs', [])
    if not isinstance(options, dict) or any(k not in ('A', 'B', 'C', 'D', 'E', 'F') or not isinstance(v, str) for k, v in options.items()): raise ValueError('Invalid options')
    if not isinstance(figures, list) or not isinstance(refs, list) or any(not isinstance(r, str) for r in refs): raise ValueError('Invalid figures or contexts')
    parts = []
    for ref in refs:
        if ref not in contexts: raise ValueError('Missing shared context: ' + ref)
        context = contexts[ref]
        if context.get('shared_context_refs'): raise ValueError('Nested contexts unsupported')
        parts.append('<section class="shared-transcription"><h3>Shared context</h3>' + str(render_entry(root, context, {})) + '</section>')
    parts.append(str(rich(entry['stem'], single_dollar=True)))
    for figure in figures:
        parts.append('<figure class="transcription-figure">' + str(safe_svg(root, figure)) + '</figure>')
    if options:
        parts.append('<dl class="transcription-options">' + ''.join('<dt>(' + k + ')</dt><dd>' + str(rich(v, single_dollar=True)) + '</dd>' for k, v in options.items()) + '</dl>')
    return Markup(''.join(parts))


def load_paper(root, paper_id):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', paper_id): raise ValueError('Unsafe paper identifier')
    path = root / 'data/transcriptions' / (paper_id + '.json')
    if not path.resolve().is_relative_to(root.resolve()): raise ValueError('Transcription path escapes repository')
    data = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(data, dict) or not isinstance(data.get('_contexts', {}), dict): raise ValueError('Invalid paper transcription mapping')
    return data


def resolve(root, question, paper):
    entry = paper.get(question['question_id'])
    if not isinstance(entry, dict): return None
    # Do not suppress legacy source context unless reviewed context replacements
    # are explicitly linked. A verified stem alone does not prove completeness.
    if (question.get('shared_context') or question.get('shared_context_reference')) and not entry.get('shared_context_refs'):
        return None
    pages = question.get('source_pages') or [question.get('source_page')]
    if not checked(entry, pages): return None
    contexts = paper.get('_contexts', {})
    try:
        for ref in entry.get('shared_context_refs', []):
            context = contexts.get(ref)
            if not isinstance(context, dict) or not checked(context, context.get('checked_pages', [])) or not context.get('checked_pages'): return None
        rendered = render_entry(root, entry, contexts)
    except (ValueError, TypeError, KeyError, OSError, ET.ParseError):
        return None
    return {'html': rendered, 'entry': entry, 'search': '\n'.join([entry['stem'], *entry.get('options', {}).values(), *[contexts[r]['stem'] for r in entry.get('shared_context_refs', [])]])}
