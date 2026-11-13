import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import dp


class DynamicProgrammingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'data/animations/dp.json'
        cls.questions = json.loads(path.read_text())['questions']

    def tables(self, question_id):
        result = dp.dp_animation(question_id, self.questions[question_id])
        for table in result['schedules']:
            self.assertTrue(table['steps'][-1]['final'])
        return result['schedules']

    def test_matrix_chain_costs_and_explicit_pair(self):
        cases = (
            ('CS-2011-Q48', [0, 3, '19000'], '((M1(M2M3))M4)'),
            ('CS-2016-S2-Q48', [0, 3, '1500'], '(A1((A2A3)A4))'),
            ('CS-2018-Q41', [0, 4, '2173'], 'only in F3F4'),
        )
        for question_id, cell, conclusion in cases:
            with self.subTest(question_id=question_id):
                table, = self.tables(question_id)
                self.assertEqual(table['fill'][-1], cell)
                self.assertIn(conclusion, table['steps'][-1]['note'])

    def test_lcs_counts_distinct_strings(self):
        table, = self.tables('CS-2014-S2-Q47')
        self.assertEqual(table['fill'][-1], [5, 7, '4'])
        final = table['steps'][-1]['note']
        self.assertIn('pqrr, qpqr and qprr', final)
        self.assertIn('4 + 10·3 = 34', final)

    def test_knapsack_compares_optimal_and_greedy(self):
        optimum, greedy = self.tables('CS-2018-Q58')
        self.assertEqual(optimum['fill'][-1], [4, 11, '60'])
        self.assertIn('taking item 1', optimum['steps'][-1]['note'])
        self.assertEqual(greedy['steps'][-1]['took'], [4, 3])
        self.assertIn('60 − 44 = 16', optimum['steps'][-1]['note'])

    def test_knapsack_when_no_item_fits(self):
        optimum, greedy = dp.knapsack('Q', {
            'items': [[3, 6]],
            'capacity': 2,
            'greedy': True,
            'expect': {'optimal': 0, 'greedy': 0, 'difference': 0},
        })
        self.assertEqual(optimum['fill'][-1], [1, 2, '0'])
        self.assertEqual(greedy['steps'][-1]['took'], [])
        for tab in (optimum, greedy):
            self.assertIn('no items', tab['steps'][-1]['note'])

    def test_nondecreasing_subsequence_tracks_predecessor_cells(self):
        table, = self.tables('CS-2024-S2-Q35')
        self.assertEqual([cell[2] for cell in table['fill']], ['1', '2', '2', '1', '3', '2', '4'])
        self.assertEqual(table['steps'][5]['deps'], [[1, 2]])
        self.assertEqual(table['steps'][-1]['path'], [[1, 6], [1, 4], [1, 2], [1, 0]])
        self.assertIn('7 − 4 = 3', table['steps'][-1]['note'])

    def test_wrong_expected_pair_fails(self):
        question_id = 'CS-2018-Q41'
        spec = {**self.questions[question_id], 'expect': {'cost': 2173, 'pairs': ['F1F2']}}
        with self.assertRaisesRegex(SystemExit, 'not the expected'):
            dp.dp_animation(question_id, spec)
