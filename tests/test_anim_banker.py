"""Worked source cases and invalid-vector checks for the Banker player."""

import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations.banker import banker_animation

SPECS = json.loads((ROOT / 'data/animations/banker.json').read_text())['questions']


def schedules(qid):
    return banker_animation(qid, SPECS[qid])['schedules']


@pytest.mark.parametrize(('qid', 'initial_work', 'order', 'final_work', 'answer'), [
    ('CS-1996-Q85', [2, 2, 0], ['P1', 'P2', 'P0'], [4, 5, 5], 'the state is safe'),
    ('CS-2007-Q57', [0, 1, 2], ['P1', 'P0', 'P2'], [5, 5, 5], 'P2 is the only one'),
    ('CS-2017-S2-Q43', [2], ['P3', 'P1', 'P2'], [9], 'A safe state is not deadlocked'),
    ('CS-2018-Q49', [3, 3, 0], ['P0', 'P2', 'P1', 'P3'], [8, 4, 6], 'the state is safe'),
])
def test_worked_completion_order(qid, initial_work, order, final_work, answer):
    steps = schedules(qid)[0]['steps']
    assert steps[0]['work'] == initial_work
    assert [step['now'] for step in steps if 'now' in step] == order
    assert steps[-1]['work'] == final_work
    assert answer in steps[-1]['note']
    assert steps[-1]['final']


def test_unsafe_request_is_rolled_back():
    start, trial, *_, finish = schedules('CS-1996-Q86')[0]['steps']
    assert start['work'] == [2, 2, 0]
    assert trial['work'] == [2, 1, 0]
    assert finish['work'] == start['work']
    assert finish['rows'] == start['rows']
    assert finish['rolled_back']
    assert 'The request is deferred' in finish['note']


def test_two_requests_are_independent_and_only_req2_is_granted():
    first, second = schedules('CS-2014-S1-Q41')
    assert first['steps'][0] == second['steps'][0]
    assert first['steps'][1]['work'] == [3, 2, 0]
    assert second['steps'][1]['work'] == [1, 2, 2]
    assert 'The request is deferred' in first['steps'][-1]['note']
    assert 'The request is granted' in second['steps'][-1]['note']


def test_aborting_p2_or_p1_and_p4_breaks_both_deadlock_cycles():
    as_given, abort_a, abort_b, abort_c, abort_d = schedules('CS-2025-S2-Q48')
    for schedule in (as_given, abort_a, abort_b):
        assert 'the state is deadlocked' in schedule['steps'][-1]['note']
    for schedule, aborted in ((abort_c, {'P2'}), (abort_d, {'P1', 'P4'})):
        finish = schedule['steps'][-1]
        assert 'the state is deadlock-free' in finish['note']
        assert {row[0] for row in finish['rows'] if row[-1] == 'aborted'} == aborted
        assert finish['work'] == [1, 1, 1, 1]


@pytest.mark.parametrize('vector', [[0, 1], [0, 1, 0, 0], [0, -1, 0]])
def test_bad_request_vector_cannot_change_inventory(vector):
    spec = copy.deepcopy(SPECS['CS-1996-Q86'])
    spec['checks'][0]['request']['vector'] = vector
    with pytest.raises(SystemExit, match='Request must list one nonnegative integer'):
        banker_animation('test', spec)


def test_duplicate_abort_cannot_release_resources_twice():
    spec = copy.deepcopy(SPECS['CS-2025-S2-Q48'])
    spec['checks'][-1]['abort'] = ['P2', 'P2']
    with pytest.raises(SystemExit, match='each aborted process must be listed once'):
        banker_animation('test', spec)
