import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from discover_groups import discover_candidates, main, normalize_text


def q(qid, text, **kwargs):
    return dict(question_id=qid, question_text=text, subject='algorithms', source_url='https://example.org/paper.pdf#page=1', **kwargs)


def test_math_typography_normalizes_without_destroying_constraints():
    assert normalize_text('$x \\times 2 \\leq 4$') == normalize_text('x×2≤4')
    assert normalize_text('x²') == normalize_text('$x^{2}$') == normalize_text('x^2')
    assert normalize_text('x²') != normalize_text('x2')
    assert normalize_text('x < 4') != normalize_text('x ≤ 4')
    assert normalize_text('A') != normalize_text('a')


def test_exact_candidates_never_become_reviewed_and_input_unchanged():
    questions = [q('a', 'Compute x×2≤4'), q('b', 'Compute $x \\times 2 \\leq 4$')]
    original = copy.deepcopy(questions)
    report = discover_candidates(questions)
    assert questions == original
    c = report['candidates'][0]
    assert c['status'] == 'candidate'
    assert c['source_reviewed'] is c['eligible_for_folding'] is False
    assert c['suggested_relation'] == 'repeat'
    assert c['sources'][0]['source_url'] == questions[0]['source_url']
    assert 'source-verified' in ' '.join(c['guardrails'])


def test_number_variants_are_only_candidates_with_explicit_warning():
    c = discover_candidates([q('a', 'A graph has 3 vertices and 2 edges.'), q('b', 'A graph has 5 vertices and 8 edges.')])['candidates'][0]
    assert 'number-masked-text' in c['evidence']['methods']
    assert 'Numerical-only' in ' '.join(c['guardrails'])
    assert not c['eligible_for_folding']


def test_different_constraints_and_figures_are_flagged_not_folded():
    c = discover_candidates([q('a', 'Find minimum cost path in the directed weighted graph shown in the figure.'), q('b', 'Find maximum cost path in the undirected weighted graph shown in the figure.')], threshold=0.5)['candidates'][0]
    guards = ' '.join(c['guardrails'])
    assert 'Different constraint' in guards
    assert 'Figure-dependent' in guards
    assert c['source_reviewed'] is c['eligible_for_folding'] is False


def test_heuristic_signature_finds_reworded_reasoning_but_does_not_claim_semantics():
    report = discover_candidates([q('a', 'Identify bits for the cache tag and index.'), q('b', 'Split a memory address into cache offset fields.')])
    c = report['candidates'][0]
    assert 'cache-address-decomposition' in c['evidence']['shared_reasoning_signatures']
    assert c['suggested_relation'] == 'pattern'
    assert 'not embedding semantic search' in report['method']
    assert not c['eligible_for_folding']


def test_generic_topic_or_numbers_alone_do_not_produce_candidates():
    assert not discover_candidates([q('a', 'Graph 2 4 8.'), q('b', 'Matrix 2 4 8.')])['candidates']
    assert not discover_candidates([q('a', ''), q('b', '')])['candidates']


def test_deterministic_order_limit_and_subject_boundaries():
    questions = [q('b', 'Find the shortest path using Dijkstra.'), q('a', 'Find the shortest path using Dijkstra.'), q('c', 'Find the shortest path using Dijkstra.')]
    assert discover_candidates(questions) == discover_candidates(list(reversed(questions)))
    report = discover_candidates(questions, limit=1)
    assert report['truncated'] and report['total_candidate_count'] == 3
    assert len(report['candidates']) == 1
    questions[1]['subject'] = 'other'
    assert discover_candidates(questions)['total_candidate_count'] == 1


def test_cli_writes_report_only_and_refuses_data_overwrites(tmp_path):
    path = tmp_path / 'questions.json'
    path.write_text(json.dumps([q('a', 'x=1'), q('b', 'x=1')]))
    original = path.read_bytes()
    output = tmp_path / 'candidates.json'
    main(['--questions', str(path), '--output', str(output)])
    assert json.loads(output.read_text())['report_type'] == 'unreviewed-group-candidates'
    assert path.read_bytes() == original
    for forbidden in (path, ROOT / 'data/repeats.json', ROOT / 'data/groups.json'):
        with pytest.raises(SystemExit):
            main(['--questions', str(path), '--output', str(forbidden)])


def test_invalid_parameters_and_duplicate_ids_are_rejected():
    for kwargs in ({'threshold': -1}, {'threshold': 2}, {'limit': -1}):
        with pytest.raises(ValueError):
            discover_candidates([], **kwargs)
    with pytest.raises(ValueError):
        discover_candidates([q('a', 'text'), q('a', 'text')])
