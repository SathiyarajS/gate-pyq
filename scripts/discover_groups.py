#!/usr/bin/env python3
"""Produce an offline, unreviewed grouping-candidate report, never folding data.

Usage: python scripts/discover_groups.py --output /tmp/group-candidates.json
Text/math normalization and curated lexical reasoning signatures are heuristics,
not embeddings, mathematical equivalence proofs, or source review. Every result
requires comparison of both original questions, constraints, options, figures,
and solution reasoning before a separate reviewed grouping decision.
"""
import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
STOP = set('a an the of in on to for and or is are be with from by find compute determine given which what how this that its as at it'.split())
# Each signature requires all of its concept clauses. Intentionally narrow;
# broad subject labels alone must never imply a shared solution pattern.
SIGNATURES = {
    'counting-inclusion-exclusion': (r'inclusion.?exclusion', r'count|number|union|sets?'),
    'conditional-probability-bayes': (r'bayes|conditional probability|condition on', r'probability|p\('),
    'cache-address-decomposition': (r'cache', r'tag|index|offset', r'bits?|address'),
    'pipeline-hazard-timing': (r'pipeline', r'hazard|stall|forwarding', r'cycles?|time'),
    'recurrence-master-theorem': (r'recurrence|t\(n\)', r'master theorem|recursion tree'),
    'shortest-path-relaxation': (r'shortest path', r'dijkstra|bellman.ford|relax'),
    'functional-dependency-closure': (r'functional dependenc', r'closure|candidate keys?'),
    'automaton-distinguishable-states': (r'automat|dfa|states?', r'distinguish|myhill|nerode'),
    'network-window-delay-product': (r'window|sequence', r'bandwidth.delay|round.trip|propagation'),
    'semaphore-interleaving': (r'semaphore', r'interleav|deadlock|wait|signal'),
    'determinant-scaling': (r'determinant|det\(', r'scal|multilinear'),
}
CONSTRAINT = re.compile(r'\b(?:not|except|only|exactly|at least|at most|minimum|maximum|directed|undirected|connected|disconnected|acyclic|cyclic|positive|negative|distinct|simple|weighted|unweighted|replacement|independent|dependent|strictly|nonnegative)\b|<=|>=|!=|<|>')
FIGURE = re.compile(r'\b(?:figure|diagram|shown|graph below|table below|circuit|drawing)\b')
NUMBER = re.compile(r'(?<![\w.])\d+(?:\.\d+)?(?![\w.])')


def normalize_text(text):
    """Normalize typography, retaining case, numbers, operators and math structure.

    This is not an algebra simplifier. In particular x^2 and x2 stay distinct.
    """
    text = str(text or '')
    text = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', lambda m: '^{' + ''.join(str('⁰¹²³⁴⁵⁶⁷⁸⁹'.index(c)) for c in m[0]) + '}', text)
    text = unicodedata.normalize('NFC', text)
    for old, new in {'−': '-', '×': '*', '·': '*', '≤': '<=', '≥': '>=', '≠': '!=', '“': '"', '”': '"', '’': "'", '\\times': '*', '\\cdot': '*', '\\leq': '<=', '\\geq': '>=', '\\neq': '!='}.items():
        text = text.replace(old, new)
    text = re.sub(r'\\(?:left|right)(?![a-zA-Z])', '', text)
    text = text.replace('\\(', '').replace('\\)', '').replace('\\[', '').replace('\\]', '').replace('$', '')
    text = re.sub(r'\^([0-9]+)(?![0-9{])', r'^{\1}', text)
    text = re.sub(r'\s*([=<>!*+^{}()/,-])\s*', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def tokens(text):
    return set(re.findall(r'[a-z][a-z0-9_]+', text.lower())) - STOP


def reasoning_signatures(question):
    text = normalize_text(question.get('question_text', '') + '\n' + question.get('solution', '')).lower()
    return {name for name, clauses in SIGNATURES.items() if all(re.search(c, text) for c in clauses)}


def source_pointer(q):
    return {k: q.get(k) for k in ('question_id', 'paper_id', 'source_question_number', 'source_page', 'source_url', 'source_page_url', 'source_file_sha256', 'question_text_status')}


def discover_candidates(questions, threshold=0.64, limit=None):
    """Return ranked pair suggestions. Input records and review state are untouched."""
    if not 0 <= threshold <= 1:
        raise ValueError('threshold must be between 0 and 1')
    if limit is not None and limit < 0:
        raise ValueError('limit must be nonnegative')
    ids = [q['question_id'] for q in questions]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate question_id')
    buckets = defaultdict(list)
    for q in questions:
        normalized = normalize_text(q.get('question_text', ''))
        if not normalized:
            continue
        buckets[q.get('subject') or q.get('subject_dir') or '__unknown__'].append((q, normalized, tokens(normalized), reasoning_signatures(q)))
    candidates = []
    for subject in sorted(buckets):
        for left, right in itertools.combinations(sorted(buckets[subject], key=lambda x: x[0]['question_id']), 2):
            a, ta, wa, sa = left
            b, tb, wb, sb = right
            shared = sorted(sa & sb)
            overlap = len(wa & wb) / len(wa | wb) if wa | wb else 0
            exact = ta == tb
            numeric = ta != tb and NUMBER.sub('#', ta) == NUMBER.sub('#', tb)
            methods = []
            if exact:
                methods.append('normalized-text-math')
            if numeric:
                methods.append('number-masked-text')
            if overlap >= threshold and len(wa & wb) >= 4:
                methods.append('lexical-overlap')
            if shared:
                methods.append('lexical-reasoning-signature')
            if not methods:
                continue
            guards = ['Source review required: compare complete wording, options, figures, constraints and solution reasoning.']
            if numeric:
                guards.append('Numerical-only similarity is not proof of the same reasoning or equivalence; values can change cases and validity.')
            if set(CONSTRAINT.findall(ta.lower())) != set(CONSTRAINT.findall(tb.lower())):
                guards.append('Different constraint or operator markers: do not merge without resolving the distinction.')
            if FIGURE.search((ta + ' ' + tb).lower()) or any(q.get('figures') or q.get('figure') for q in (a, b)):
                guards.append('Figure-dependent content: inspect both original figures; text similarity cannot establish equivalence.')
            if not all(q.get('source_transcription_verified') is True for q in (a, b)):
                guards.append('At least one text is not a source-verified transcription; paraphrases may omit essential distinctions.')
            if not all(q.get('source_url') or q.get('source_page_url') for q in (a, b)):
                guards.append('Missing source link: locate the original before review.')
            if a.get('question_type') != b.get('question_type'):
                guards.append('Different response types: review options and task requirements separately.')
            candidates.append({
                'candidate_id': a['question_id'] + '__' + b['question_id'],
                'question_ids': [a['question_id'], b['question_id']],
                'status': 'candidate', 'source_reviewed': False, 'eligible_for_folding': False,
                'suggested_relation': 'repeat' if exact else 'pattern',
                'score': round(1.0 if exact else 0.95 if numeric else max(overlap, 0.65 if shared else 0), 4),
                'evidence': {'methods': methods, 'lexical_jaccard': round(overlap, 4), 'shared_reasoning_signatures': shared,
                             'normalized_text': [ta, tb], 'shared_lexical_terms': sorted(wa & wb)},
                'sources': [source_pointer(a), source_pointer(b)], 'guardrails': guards,
            })
    candidates.sort(key=lambda c: (-c['score'], c['question_ids']))
    total = len(candidates)
    return {'schema_version': 1, 'report_type': 'unreviewed-group-candidates',
            'method': 'Deterministic text/math normalization and lexical reasoning heuristics; not embedding semantic search.',
            'policy': 'Discovery only. Never consumed by folding. A separate source-reviewed grouping decision is required. Preserve every original question.',
            'input_question_count': len(questions), 'total_candidate_count': total,
            'truncated': limit is not None and total > limit,
            'candidates': candidates if limit is None else candidates[:limit]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--questions', type=Path, default=ROOT / 'data/questions.json')
    parser.add_argument('--output', type=Path, help='Report path outside data/ (default: stdout).')
    parser.add_argument('--threshold', type=float, default=0.64)
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args(argv)
    if args.output and (args.output.resolve() == args.questions.resolve() or (ROOT / 'data').resolve() in args.output.resolve().parents):
        parser.error('Candidate reports must not overwrite input or repository data files.')
    try:
        result = discover_candidates(json.loads(args.questions.read_text()), args.threshold, args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
