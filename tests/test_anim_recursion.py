"""Worked-answer and safety regressions for the recursion family.

Audited against questions.json and DISCREPANCIES.md, not a source-transcription
certification. Q56/Q57 (1997) have unknown marks, not ambiguous execution.
Q36 (2023) is excluded: option A is a figure without text to compare.
Q19 (2024 S1) is excluded: printed quote delimiters change compilation.
"""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import recursion as r

SPECS = json.loads((ROOT / 'data/animations/recursion.json').read_text())['questions']
# Independently recorded keyed option CONTENT or numerical/descriptive answer.
ANSWERS = {
    'CS-1991-Q10': ('calls', 41), 'CS-1995-Q52': ('returns', 3),
    'CS-1997-Q56': ('output', '30'), 'CS-1997-Q57': ('calls', 5),
    'CS-1997-Q58': ('output', '110'), 'CS-1998-Q47': ('returns', 91),
    'CS-2001-Q76': ('output', '3323321'), 'CS-2004-Q31': ('returns', 7),
    'CS-2005-Q31': ('output', '2, 0, 4, 8, 0'), 'CS-2007-Q42': ('returns', 18),
    'CS-2009-Q18': ('output', '8'), 'CS-2010-Q45': ('output', '15'),
    'CS-2011-Q58': ('returns', 12), 'CS-2011-Q59': ('returns', 2),
    'CS-2015-S2-Q24': ('returns', 51), 'CS-2015-S3-Q38': ('calls', 25),
    'CS-2016-S1-Q45': ('output', '3 1 2 2 1 3 4 4 4'),
    'CS-2016-S2-Q47': ('output', '3'), 'CS-2017-S1-Q45': ('output', '53423122233445'),
    'CS-2020-Q56': ('returns', 55), 'CS-2021-S2-Q33': ('returns', 15),
    'CS-2021-S2-Q59': ('output', '60'), 'CS-2024-S2-Q13': ('output', '20101020'),
    'CS-2025-S1-Q61': ('output', '5'), 'CS-2026-S1-Q61': ('smallest', 65536),
}


def program(qid):
    return r.Program(copy.deepcopy(SPECS[qid]['program']), qid)


@pytest.mark.parametrize('qid', ANSWERS)
def test_worked_answers_and_player_contract(qid):
    key, value = ANSWERS[qid]
    assert SPECS[qid]['expect'][key] == value
    before = copy.deepcopy(SPECS[qid])
    data = r.recursion_animation(qid, SPECS[qid])
    assert SPECS[qid] == before  # parsing must never mutate persisted inputs
    assert data['kind'] == 'call-tree'
    assert data['count'] == sum(len(s['steps']) for s in data['schedules'])
    for schedule in data['schedules']:
        assert schedule['steps'][-1]['final']
        assert set(schedule['steps'][-1]['st']) == {'d'}
        assert all(s['note'] for s in schedule['steps'])
        assert all(len(s['st']) == s['n'] for s in schedule['steps'])
        assert all(s['line'] is None or 0 <= s['line'] < len(data['code']) for s in schedule['steps'])
    # A mismatched answer must fail, not silently render a plausible trace.
    bad = copy.deepcopy(SPECS[qid])
    bad['expect'][key] = value + 1 if isinstance(value, int) else value + '9'
    with pytest.raises(SystemExit):
        r.recursion_animation(qid, bad)


def test_inventory_and_tab_label():
    assert set(SPECS) == set(ANSWERS)
    assert r.TABS == 'calls'
    assert 'CS-2023-Q36' not in SPECS
    assert 'CS-2024-S1-Q19' not in SPECS


def test_value_and_reference_descent_and_unwinding():
    for qid, entries, output in [
        ('CS-1997-Q56', ['10', '20', '30', '40', '50'], '30\n'),
        ('CS-1997-Q58', ['z'] * 4, '110\n'),
    ]:
        machine, root = r.trace(program(qid))
        calls = [n for n in r._nodes_of(root) if n.fname == 'recur']
        assert [n.label for n in calls] == [f'recur({v})' for v in entries]
        assert ''.join(machine.out) == output
        assert machine.globals['z'].cells == [int(output)]


def test_shared_static_does_not_reset_on_recursive_entry():
    machine, root = r.trace(program('CS-2020-Q56'))
    assert root.value == 55
    assert machine.statics[('fun1', 'i')].cells == [15]
    assert machine.statics[('fun2', 'i')].cells == [55]


def test_fibonacci_counts_duplicate_calls_not_just_unique_arguments():
    _, root = r.trace(program('CS-1991-Q10'))
    assert (root.value, root.calls) == (21, 41)


def test_nested_log_threshold_and_predecessor():
    p = program('CS-2026-S1-Q61')
    assert r.trace(p, 'foo(65536)')[1].value == 5
    assert r.trace(p, 'foo(65535)')[1].value == 4


def test_stipulated_argument_order_and_unspecified_order_rejection():
    spec = copy.deepcopy(SPECS['CS-2024-S2-Q13'])
    spec['program'].pop('arg_order')
    with pytest.raises(SystemExit, match='order of evaluation'):
        r.recursion_animation('unordered', spec)


@pytest.mark.parametrize('expr, expected', [('7/(-3)', -2), ('(-7)/3', -2), ('(-7)%3', -1), ('7%(-3)', 1)])
def test_c_division_truncates_toward_zero(expr, expected):
    p = r.Program({'functions': [{'name': 'f', 'type': 'int', 'params': [], 'body': [{'return': expr}]}], 'call': 'f()'})
    assert r.trace(p)[1].value == expected


@pytest.mark.parametrize('body, message', [
    ([{'return': '1/0'}], 'division by zero'),
    ([{'return': '2147483647+1'}], 'overflow'),
    ([{'local': 'int', 'vars': [['x', None]]}, {'return': 'x'}], 'before it is set'),
    ([{'local': 'int', 'vars': [['a[]', '{1,2}']]}, {'return': 'a[2]'}], 'outside'),
    ([{'local': 'int', 'vars': [['x', '1']]}, {'return': 'x++ + x'}], 'order of evaluation'),
])
def test_invalid_programs_fail_closed(body, message):
    p = r.Program({'functions': [{'name': 'f', 'type': 'int', 'params': [], 'body': body}], 'call': 'f()'})
    with pytest.raises(SystemExit, match=message):
        r.trace(p)


def test_audited_inputs_and_recorded_keys_have_not_drifted():
    import hashlib
    questions = {q['question_id']: q for q in json.loads((ROOT / 'data/questions.json').read_text())}
    audit = json.loads((ROOT / 'audits/animations/recursion.json').read_text())
    assert {entry['question_id'] for entry in audit['entries']} == set(SPECS)
    for entry in audit['entries']:
        qid = entry['question_id']
        q = questions[qid]
        assert hashlib.sha256(q['question_text'].encode()).hexdigest() == entry['question_text_sha256']
        assert q[entry['answer_source']] == entry['recorded_answer']
        assert q['discrepancy_ids'] == entry['discrepancy_ids']
        assert SPECS[qid]['expect'] == entry['expect']
