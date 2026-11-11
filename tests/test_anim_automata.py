"""Automata worked results and fail-closed expectations, audited against question_text.

Exclusions and their reasons live in the family's JSON. Source fingerprints below
pin the text/key actually checked, so later transcription changes require review.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import automata as a

DATA = json.loads((ROOT / 'data/animations/automata.json').read_text())
SPECS = DATA['questions']
QUESTIONS = {q['question_id']: q for q in json.loads((ROOT / 'data/questions.json').read_text())}


def source_fingerprint(q):
    return hashlib.sha256(json.dumps([q['question_text'], q.get('official_answer'), q.get('derived_answer')], ensure_ascii=False).encode()).hexdigest()[:16]


# MCQ/MSQ content, not merely key letters, used in the spec audit.
KEYED_CONTENT = {
    'CS-2017-S2-Q49': '{q0,q1,q2}',
    'CS-2006-Q34': '(D) 9',
    'CS-2007-Q29': '(A) 15',
    'CS-1998-Q40': '2, 5, 8, 3',  # B is the second entry, 5.
    'CS-2021-S2-Q38': 'B t=b,y=sb',
}


@pytest.mark.parametrize('qid', SPECS)
def test_audited_input_and_key_stay_unchanged(qid):
    assert source_fingerprint(QUESTIONS[qid]) == SOURCE_FINGERPRINTS[qid]
    if qid in KEYED_CONTENT:
        assert KEYED_CONTENT[qid] in QUESTIONS[qid]['question_text']
    if QUESTIONS[qid]['question_type'] == 'NAT':
        import re
        bounds = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', QUESTIONS[qid]['official_answer'])]
        assert min(bounds) <= SPECS[qid]['expect']['count'] <= max(bounds)


@pytest.mark.parametrize('qid,spec', SPECS.items())
def test_every_question_computes_and_every_tab_finishes(qid, spec):
    result = a.KINDS[spec['kind']](qid, spec)
    assert result['kind'] == spec['kind']
    assert result['count'] == sum(len(s['steps']) for s in result['schedules'])
    for schedule in result['schedules']:
        assert schedule['steps'][-1]['final'] is True
        assert all(step['note'].strip() for step in schedule['steps'])
    if len(result['schedules']) > 1:
        assert a.TABS


def test_nfa_and_epsilon_closure_worked_states():
    fa = a.FA('test', SPECS['CS-2017-S2-Q49']['machine'])
    assert fa.closure({'q2'})[0] == {'q0', 'q2'}
    assert fa.run_from({'q2'}, 'aba') == {'q0', 'q1', 'q2'}


def test_wrong_and_unknown_expected_states_fail():
    for states in [['q3'], ['q0', 'q1', 'q2', 'made-up']]:
        spec = copy.deepcopy(SPECS['CS-2017-S2-Q49'])
        spec['runs'][0]['expect']['states'] = states
        with pytest.raises(SystemExit):
            a.run_animation('test', spec)


def test_count_uses_fixed_positions_and_rejects_wrong_answer():
    # A complete accepting loop accepts all four strings with the middle bit fixed.
    spec = {
        'machine': {
            'states': ['s'], 'start': 's', 'final': ['s'], 'alphabet': '01',
            'edges': [['s', '0,1', 's']],
        },
        'length': 3,
        'fixed': {'2': '1'},
        'expect': {'count': 8},
    }
    with pytest.raises(SystemExit, match='number of accepted strings is 4, not the expected 8'):
        a.count_animation('test', spec)


def test_exact_equivalence_and_shortest_counterexample():
    left = a.Lang('test', {'regex': '(0+1)*00'}, ['0', '1'])
    right = a.Lang('test', {'regex': '(0+1)*0'}, ['0', '1'])
    assert left.dfa.witness(right.dfa, lambda x, y: x != y) == '0'
    assert left.dfa.witness(left.dfa, lambda x, y: x != y) is None


def test_bounded_enumeration_is_not_a_proof():
    fa = a.FA('test', {'states': ['s'], 'start': 's', 'final': ['s'], 'alphabet': '0', 'edges': [['s', '0', 's']]})
    lang = a.Lang('test', {'member': 'len(w) < 100', 'text': 'short strings'}, ['0'])
    with pytest.raises(SystemExit, match='cannot prove'):
        a.compare('test', fa, fa.accepts, lang, 'eq')


def test_minimization_drops_unreachable_and_merges_equivalent():
    fa = a.FA('test', {
        'states': ['q0', 'q1', 'q2', 'q3'], 'start': 'q0',
        'final': ['q1', 'q2'], 'alphabet': 'ab',
        'edges': [
            ['q0', 'a', 'q1'], ['q0', 'b', 'q0'],
            ['q1', 'a', 'q2'], ['q1', 'b', 'q1'],
            ['q2', 'a', 'q1'], ['q2', 'b', 'q2'],
            ['q3', 'a', 'q1'], ['q3', 'b', 'q2'],
        ],
    })
    steps = []
    groups = a.refine_steps(fa, steps)
    assert {frozenset(x) for x in groups} == {frozenset(['q0']), frozenset(['q1', 'q2'])}
    assert 'q3' in steps[0]['note'] and 'cannot be reached' in steps[0]['note']


def test_mealy_outputs_match_given_string():
    result = a.mealy_animation('test', SPECS['CS-2021-S2-Q38'])
    assert [s['short'] for s in result['schedules']] == ['A', 'B', 'C', 'D']
    correct = result['schedules'][1]['steps'][-1]
    assert ''.join(correct['tape']['out']) == '00000001000001100'


def test_expected_dfa_is_not_used_to_construct_answer():
    spec = copy.deepcopy(SPECS['CS-2001-Q56'])
    spec['expect']['dfa']['final'] = ['EE']
    with pytest.raises(SystemExit, match='differs from the recorded DFA'):
        a.language_animation('test', spec)


SOURCE_FINGERPRINTS = {
    'CS-2017-S2-Q49': 'ef9f157848d8e32a',
    'CS-2025-S1-Q59': 'fd74c941d4a908c4',
    'CS-2015-S2-Q45': '4ead45e841facbe9',
    'CS-2016-S2-Q26': '09c892022323f588',
    'CS-2017-S1-Q32': '0e5ec2731acd42da',
    'CS-2017-S2-Q35': 'd2883cde9545424e',
    'CS-2020-Q61': '0cdb4d66e49fc5f8',
    'CS-2023-Q63': '4480e849ca7d0c80',
    'CS-2025-S2-Q60': 'd54f5736edbb2dd9',
    'CS-2006-Q34': 'bbf0a4a8062a7d5f',
    'CS-2007-Q29': 'fce15a0831fa41cd',
    'CS-1998-Q40': 'bdcdb34823ff172f',
    'CS-1997-Q81': '662e6e9c95004aec',
    'CS-1993-Q68': '8060a6c6abe797c9',
    'CS-2001-Q55': '955f5a3b6f140242',
    'CS-2001-Q56': '32638f77a1cbe9f6',
    'CS-2002-Q98': 'cdc0d4a488112eae',
    'CS-2021-S2-Q38': 'de23ae028cfd2618',
}


def test_unstated_mealy_demo_is_rejected():
    with pytest.raises(SystemExit, match='stated input/output'):
        a.mealy_animation('test', {'demo': '0110', 'machine': {}})
