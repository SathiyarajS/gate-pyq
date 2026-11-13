import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import hashing

class HashingTest(unittest.TestCase):
    def test_linear_probing_wraps_and_records_collisions(self):
        steps, table = hashing.hash_insert(dict(size=5, method='linear', keys=[4, 9, 14]))
        self.assertEqual(table, [9, 14, None, None, 4])
        self.assertEqual(steps[-1]['probed'], [4, 0])

    def test_double_hashing(self):
        # CS-2025-S1-Q65: 24 ends up in slot 10.
        steps, table = hashing.hash_insert(dict(size=11, method='double', h2=dict(c=1, d=7), keys=[63, 50, 25, 79, 67, 24]))
        self.assertEqual(table.index(24), 10)

    def test_chaining_statistics_are_checked(self):
        spec = dict(kind='hash-insert', size=9, method='chaining', keys=[5, 28, 19, 15, 20, 33, 12, 17, 10], expect=dict(chains=dict(max=3, min=0, avg=1)))
        self.assertIn('Longest 3', hashing.hash_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])
        spec['expect']['chains']['max'] = 4
        with self.assertRaises(SystemExit):
            hashing.hash_animation('Q', spec)
