import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import trees

class HeapAndBstTest(unittest.TestCase):
    def test_heap_insert_delete_and_build(self):
        _, a = trees.heap_ops(dict(start=[10, 8, 5, 3, 2], ops=[['insert', [1, 7]]]))
        self.assertEqual(a, [10, 8, 7, 3, 2, 1, 5])  # CS-2014-S2-Q22
        _, a = trees.heap_ops(dict(start=[25, 14, 16, 13, 10, 8, 12], ops=[['delete', 2]]))
        self.assertEqual(a, [14, 13, 12, 8, 10])  # CS-2009-Q60
        _, a = trees.heap_ops(dict(ops=[['build', [82, 101, 90, 11, 111, 75, 33, 131, 44, 93]]]))
        self.assertEqual(a[:3], [131, 111, 90])  # CS-2024-S1-Q41

    def test_ternary_heap(self):
        _, a = trees.heap_ops(dict(arity=3, start=[9, 5, 6, 8, 3, 1], ops=[['insert', [7, 2, 10, 4]]]))
        self.assertEqual(a, [10, 7, 9, 8, 3, 1, 5, 2, 6, 4])  # CS-2006-Q77

    def test_bst_queries(self):
        spec = dict(kind='bst', keys=[15, 10, 12, 11, 20, 18, 16, 19], from_preorder=True, query='postorder', expect=[11, 12, 10, 16, 19, 18, 20, 15])
        out = trees.bst_animation('Q', spec)
        self.assertEqual(out['schedules'][0]['steps'][-1]['out'], spec['expect'])
        self.assertEqual(trees.bst_animation('Q', dict(kind='bst', keys=[10, 1, 3, 5, 15, 12, 16], query='height', expect=3))['kind'], 'bst')
        with self.assertRaises(SystemExit):
            trees.bst_animation('Q', dict(kind='bst', keys=[10, -4, 15, 30, 20, 5, 60, 19], query='depth', node=19, expect=3))
