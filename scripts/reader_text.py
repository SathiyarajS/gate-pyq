"""Display-time cleanup of review wording in solutions, answers and notes.

The data keeps the full review record (which printed copy said what, how a
figure was checked). Readers see one question image: for 1991-2006 that image
is the GFG copy. So, on the page, sentences about the other copy (GateForum)
or about checking work are dropped, and copy labels are removed from the rest.
"""
import re

_CHECKING = re.compile(r'verified visually|visually (checked|verified|inspected|present)|\braster\b|\bOCR\b|extraction/reproduction|'
                       r'figure bits were|(GateForum|GFG) p\d+|\bp\d+\b.*(GateForum|GFG)|newly inspected|Guttitech|community image|'
                       r'source-specific letters|copying a letter between sources|silently (replac|repair|transferr)|without disclosure|'
                       r'not authorize|blindly transferring|retain the separate original ID|unverified|fidelity|third-party|inspected raster|checked visually|'
                       r'was explicitly proposed|independently confirmed|\[sic\]|Keep this discrepancy open|Source page \d+|GateOverflow|'
                       r'official wording remains|official-source|no official key or original exam diagram|enlarged reproductions|inherited B answer|source variant', re.I)
_OTHER_COPY = re.compile(r'GateForum|\bForum\b|\bthe alternate\b|\balternate (reproduction|copy|source|version|wording)\b|'
                         r'\bother reproduction\b|\bsecond reproduction\b', re.I)
_GFG = re.compile(r'\bGFG\b|GeeksforGeeks')
_DROP_HEADINGS = re.compile(r'^\s*(?:\*\*)?(Source discrepancies and qualifications|Visual check)\s*:?(?:\*\*)?\s*$', re.I)
_LABELS = re.compile(r'^(\s*(?:[-*]\s+)?)(?:\*\*)?(Source qualification|Source caveat|Source typography note|Discrepancy retained)\s*:(?:\*\*)?\s*', re.I)
_LEADING = re.compile(r'^(\s*(?:\*\*)?)(Baseline derivation[^:]*|Derivation, answer and qualifications|Derivation and interpretation|Conclusion and qualifications|'
                      r'Worked check / additional reasoning|Method and intermediate reasoning|Teaching detail|Teaching check)\s*:(?:\*\*)?\s*(?=\S)')
_LEADING_NAMES = {'Conclusion and qualifications': 'Conclusion: ', 'Worked check / additional reasoning': 'Check: ', 'Method and intermediate reasoning': 'Method: ',
                  'Teaching detail': '', 'Teaching check': 'Check: '}
_HEADINGS = {
    'Baseline derivation and retained qualifications': 'Solution',
    'Derivation, answer and qualifications': 'Solution',
    'Derivation and interpretation': 'Solution',
    'Conclusion and qualifications': 'Conclusion',
    'Worked check / additional reasoning': 'Check',
    'Method and intermediate reasoning': 'Method',
    'Work through the result and its assumptions': 'Working',
}
_REPHRASE = [
    (re.compile(r'\b(?:In|For|Under|With) (?:the )?(?:enlarged |literal |coherent )?GFG(?: (?:reading|version|text|figure|wording|reproduction|expression|grammar|wiring|guard|instruction stream|floor version))?,?\s+'), ''),
    (re.compile(r'\b(?:the |a )?(?:literal |enlarged )?GFG(?:’s|\'s)?\s+(reading|version|text|figure|wording|reproduction|expression|grammar|wiring|guard|instruction stream|plus signs|phrase|controls)\b'), r'the \1'),
    (re.compile(r'\b(?:the )?(?:supplied )?GeeksforGeeks(?: GFG)?\b'), 'the paper'),
    (re.compile(r'\s*\((?:GFG)\)'), ''),
    (re.compile(r'\b(?:literal )?GFG\s*:\s*'), ''),
    (re.compile(r'\s+(?:for|in) (?:the )?(?:literal )?GFG(?: reproduction)?\b'), ''),
    (re.compile(r'\b([Bb])oth (?:reproductions|sources|source images) (print|show|place|include|retain|give|agree|omit|use|swap|read)\b'), lambda m: ('The' if m.group(1)=='B' else 'the')+' paper '+m.group(2)+'s'),
    (re.compile(r'\b[Bb]oth (?:reproductions|sources|source images)\b'), lambda m: 'The paper' if m.group(0)[0] == 'B' else 'the paper'),
    (re.compile(r'\b(?:either|neither) (?:inspected )?reproduction\b'), 'the paper'),
    (re.compile(r'\b(?:the )?(?:primary |inspected )?reproduction\b'), 'the paper'),
    (re.compile(r'\bas reproduced\b'), 'as printed'),
    (re.compile(r'\breproduced\b'), 'printed'),
    (re.compile(r'\s+in the inspected source\b'), ''),
    (re.compile(r'\(its ([A-E])\)'), r'(\1)'),
]


def _clean_sentence(s):
    """Drop checking notes and anything about the other printed copy; relabel the rest."""
    if _CHECKING.search(s) or _OTHER_COPY.search(s):
        return ''
    for pattern, repl in _REPHRASE:
        s = pattern.sub(repl, s)
    s = re.sub(r'L_GFG\b', 'L', s)
    s = re.sub(r'\bGFG\b', 'the paper', s)
    s = re.sub(r'\b(?:the paper|the supplied the paper)\s+the paper\b', 'the paper', s)
    s = re.sub(r'\b[Tt]he supplied the paper\b', 'the paper', s)
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s[:1].upper() + s[1:] if s[:1].islower() and s[:2] not in ('n ', 'i ', 'x ', 'k ') and not re.match(r'[a-z][\d(=≤≥<>+−-]', s) else s


def reader(value):
    """Return the text a reader should see; unchanged when nothing applies."""
    if not value:
        return value
    text = str(value)
    out = []
    for line in text.split('\n'):
        if _DROP_HEADINGS.match(line):
            continue
        line = _LABELS.sub(r'\1', line)
        line = _LEADING.sub(lambda m: m.group(1) + _LEADING_NAMES.get(m.group(2), 'Solution: '), line)
        heading = re.match(r'^(\s*(?:\*\*)?)(.+?)([.:])((?:\*\*)?\s*)$', line)
        if heading and heading.group(2) in _HEADINGS:
            line = heading.group(1) + _HEADINGS[heading.group(2)] + heading.group(3) + heading.group(4)
            out.append(line); continue
        if not (_CHECKING.search(line) or _OTHER_COPY.search(line) or _GFG.search(line) or re.search(r'reproduc|inspected source', line)):
            out.append(line); continue
        prefix = re.match(r'^(\s*(?:[-*]\s+|\d{1,2}[.)]\s+)?)', line).group(1)
        body = line[len(prefix):]
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z(“"])', body)
        kept = [c for c in (_clean_sentence(x) for x in sentences) if c]
        if kept:
            out.append(prefix + ' '.join(kept))
        elif not prefix.strip():
            out.append('')
    cleaned = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()
    return cleaned


def answer(value):
    """An answer as a reader expects it: '6 to 6' -> '6', 'B;C' -> 'B, C', copy labels removed."""
    if value is None:
        return value
    text = reader(str(value)) or str(value)
    text = re.sub(r'\b(-?\d+(?:\.\d+)?) to \1\b', r'\1', text)
    if re.fullmatch(r'[A-E](;[A-E])+', text):
        text = ', '.join(text.split(';'))
    return text
