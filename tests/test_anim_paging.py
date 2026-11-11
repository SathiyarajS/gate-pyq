import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import paging

class PageReplacementTest(unittest.TestCase):
    REFS = [1, 2, 3, 2, 4, 1, 3, 2, 4, 1]  # CS-2012-Q52

    def test_policies_match_the_worked_solution(self):
        for policy, faults in (('fifo', [1, 2, 3, 5, 6, 8]), ('lru', [1, 2, 3, 5, 6, 7, 8, 9, 10]), ('optimal', [1, 2, 3, 5, 8])):
            with self.subTest(policy=policy):
                self.assertEqual(paging.page_replace(self.REFS, 3, policy)[1], faults)

    def test_lru_updates_recency_on_a_hit_but_fifo_does_not(self):
        fifo, _ = paging.page_replace(self.REFS, 3, 'fifo')
        lru, _ = paging.page_replace(self.REFS, 3, 'lru')
        self.assertEqual(fifo['steps'][4]['order'], 'Load order (oldest first): 1, 2, 3')
        self.assertEqual(lru['steps'][4]['order'], 'Recency (least recent first): 1, 3, 2')

    def test_windowed_optimal_looks_only_at_the_window(self):
        data, faults = paging.page_replace([1, 3, 2, 4, 2, 3, 1, 2, 4, 3, 1, 4], 3, 'optimal-window', 4)
        self.assertEqual(faults, [1, 2, 3, 4, 7, 10])
        self.assertIn('page 2 is not used in it', data['steps'][10]['note'])

    def test_rank_and_wrong_positions(self):
        spec = dict(kind='page-replace', frames=3, refs=self.REFS, policies=[dict(policy='fifo', expect=6), dict(policy='optimal', expect=5)],
                    compare='rank', expect_compare=['optimal', 'fifo'])
        self.assertIn('Optimal 5 < FIFO 6', paging.page_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])
        spec['policies'][0]['positions'] = [1, 2, 3]
        with self.assertRaises(SystemExit):
            paging.page_animation('Q', spec)
