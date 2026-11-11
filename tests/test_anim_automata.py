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
    'CS-2014-S1-Q26': '{q₀,q₁,q₂}',
    'CS-2017-S2-Q49': '{q0,q1,q2}',
    'CS-2003-Q50': 'C. 7',
    'CS-2003-Q55': 'L1={0,1}*',
    'CS-2012-Q22': '(B) {ε}',
    'CS-2007-Q75': '(B) 2',
    'CS-2011-Q55': '(A) Start p; final s; p:a→s,b→q; q:a→s,b→r; r:a,b→r; s:a,b→s',
    'CS-2006-Q34': '(D) 9',
    'CS-2007-Q29': '(A) 15',
    'CS-1998-Q40': '2, 5, 8, 3',  # B is the second entry, 5.
    'CS-2007-Q74': '(C) b*a(a+b)*',
    'CS-2009-Q41': 'C ending 00',
    'CS-2014-S1-Q46': 'B: I,III only',
    'CS-2021-S1-Q48': 'D (q1,q0)',
    'CS-2022-Q12': 'D (ba*a+ab*b)*(ab*+ba*)',
    'CS-2023-Q14': 'C 1(0+11)*',
    'CS-2024-S2-Q22': 'A 0*1(0+10*1)*',
    'CS-2024-S2-Q41': 'B 0*+(1+0(00)*)(11)*',
    'CS-2025-S1-Q50': 'C words ending in bab',
    'CS-2004-Q86': '(A) Divisible by 3 and 2 respectively',
    'CS-2012-Q56': '(D) (00,1,01),(00,0,q),(01,1,11),(10,0,00),(11,0,10)',
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
    fa = a.FA('test', SPECS['CS-2014-S1-Q26']['machine'])
    assert fa.run_from({'q0'}, '0011') == {'q0', 'q1', 'q2'}
    fa = a.FA('test', SPECS['CS-2017-S2-Q49']['machine'])
    assert fa.closure({'q2'})[0] == {'q0', 'q2'}
    assert fa.run_from({'q2'}, 'aba') == {'q0', 'q1', 'q2'}


def test_wrong_and_unknown_expected_states_fail():
    for states in [['q3'], ['q0', 'q1', 'q2', 'made-up']]:
        spec = copy.deepcopy(SPECS['CS-2014-S1-Q26'])
        spec['runs'][0]['expect']['states'] = states
        with pytest.raises(SystemExit):
            a.run_animation('test', spec)


def test_count_uses_fixed_positions_and_rejects_wrong_answer():
    spec = copy.deepcopy(SPECS['CS-2003-Q50'])
    spec['expect']['count'] = 8
    with pytest.raises(SystemExit, match='not the expected 8'):
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
    fa = a.FA('test', SPECS['CS-2007-Q75']['machine'])
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
    'CS-2014-S1-Q26': 'ad1500516dcfb9c6',
    'CS-2017-S2-Q49': 'ef9f157848d8e32a',
    'CS-2003-Q50': '238852d49c9591b4',
    'CS-2021-S2-Q27': '39d1c1b3eb72cf33',
    'CS-2003-Q55': '6f369f1919b749b7',
    'CS-2012-Q22': '19faf51786fddc04',
    'CS-2007-Q75': '97575087b566aeb4',
    'CS-2011-Q55': '60a2ae65b6c83e4e',
    'CS-2015-S1-Q49': '9fcc3e022d31f167',
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
    'CS-1991-Q71': '4aa91fd7c2ad1406',
    'CS-1997-Q81': '662e6e9c95004aec',
    'CS-1993-Q68': '8060a6c6abe797c9',
    'CS-2001-Q55': '955f5a3b6f140242',
    'CS-2001-Q56': '32638f77a1cbe9f6',
    'CS-2002-Q98': 'cdc0d4a488112eae',
    'CS-1994-Q34': 'd9a14854aff9e522',
    'CS-2007-Q74': '69c318e513c91d7d',
    'CS-2009-Q41': '61164a4736a70f30',
    'CS-2014-S1-Q46': '9747e4c08affd21a',
    'CS-2021-S1-Q48': '4c56f3c9724cf29c',
    'CS-2022-Q12': '3dc9f8e6fafa0b48',
    'CS-2023-Q14': 'e44639d6bb38108c',
    'CS-2024-S2-Q22': '17f7bfbc1cc73205',
    'CS-2024-S2-Q41': 'c5f413d67893c06a',
    'CS-2025-S1-Q50': '9fe37907f9f28f17',
    'CS-2004-Q86': 'c34bbe2729900551',
    'CS-2012-Q56': '91f1819301696873',
    'CS-2021-S2-Q38': 'de23ae028cfd2618',
}


def test_unstated_mealy_demo_is_rejected():
    with pytest.raises(SystemExit, match='stated input/output'):
        a.mealy_animation('test', {'demo': '0110', 'machine': {}})
