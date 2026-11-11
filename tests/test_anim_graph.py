import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import graph

# CS-2004-Q44's graph, used by several tests.
ARCS = [['P', 'Q', 1], ['P', 'S', 6], ['P', 'T', 7], ['Q', 'R', 1], ['Q', 'S', 4], ['R', 'S', 2], ['R', 'U', 1], ['S', 'T', 3], ['S', 'U', 2], ['T', 'U', 2]]


def g(**spec):
    return graph.Graph('Q', spec)


class ShortestPathTest(unittest.TestCase):
    def test_dijkstra_order_and_distances(self):
        r = graph.dijkstra(g(directed=True, edges=ARCS), 'P')
        self.assertEqual(r['order'], ['P', 'Q', 'R', 'U', 'S', 'T'])
        self.assertEqual({v: int(d) for v, d in r['dist'].items()}, dict(P=0, Q=1, R=2, U=3, S=4, T=7))
        self.assertTrue(r['steps'][0]['note'].startswith('Start at P'))

    def test_a_tie_stops_the_build_unless_the_question_leaves_it_open(self):
        spec = dict(kind='graph-paths', algo='dijkstra', directed=True, source='a', edges=[['a', 'b', 1], ['a', 'c', 1], ['b', 'd', 1], ['c', 'd', 1]], expect={'dist': {'d': 2}})
        with self.assertRaises(SystemExit):
            graph.paths_animation('Q', spec)
        self.assertEqual(graph.paths_animation('Q', dict(spec, ties='any'))['kind'], 'graph-paths')

    def test_lowering_a_settled_vertex_stops_the_build(self):
        spec = dict(kind='graph-paths', algo='dijkstra', directed=True, source='a', edges=[['a', 'b', 1], ['a', 'c', 2], ['c', 'b', -5]], expect={'dist': {'b': 1}})
        with self.assertRaises(SystemExit):
            graph.paths_animation('Q', spec)

    def test_wrong_expectation_stops_the_build(self):
        spec = dict(kind='graph-paths', algo='dijkstra', directed=True, source='P', edges=ARCS, expect={'order': ['P', 'Q', 'R', 'S', 'T', 'U']})
        with self.assertRaises(SystemExit):
            graph.paths_animation('Q', spec)

    def test_edge_bounded_rounds(self):
        # CS-2010-Q61: 1 to 2 with at most three edges costs 8 (1-0-4-2); unbounded it is 7.
        w = [[0, 1, 8, 1, 4], [1, 0, 12, 4, 9], [8, 12, 0, 7, 3], [1, 4, 7, 0, 2], [4, 9, 3, 2, 0]]
        spec = dict(kind='graph-paths', algo='bounded', nodes=[0, 1, 2, 3, 4], matrix=w, source=1, target=2, rounds=3, expect={'dist': 8, 'path': [1, 0, 4, 2]})
        last = graph.paths_animation('Q', spec)['schedules'][0]['steps'][-1]['note']
        self.assertIn('1–0–4–2', last)
        self.assertIn('only 7 away', last)

    def test_dag_scores(self):
        spec = dict(kind='graph-paths', algo='dag', directed=True, source='s', start_score=1, combine='product', best='max',
                    edges=[['s', 'a', 2], ['s', 'b', 3], ['a', 't', 5], ['b', 't', 3]], expect={'scores': {'t': 10}, 'total': 16})
        self.assertIn('= 16', graph.paths_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])


class MstTest(unittest.TestCase):
    EDGES = [['n1', 'n2', 2], ['n1', 'n3', 8], ['n1', 'n6', 3], ['n2', 'n4', 4], ['n2', 'n5', 12], ['n3', 'n4', 7], ['n4', 'n5', 9], ['n4', 'n6', 4]]  # CS-2001-Q81

    def test_kruskal_weight_and_ties(self):
        r = graph.kruskal(g(edges=self.EDGES))
        self.assertEqual(r['weight'], 25)
        self.assertEqual([m for _, m in r['ways']], [1, 1, 2, 1, 1, 1])

    def test_count_matches_every_spanning_tree(self):
        # CS-2024-S2-Q59: 9 minimum spanning trees.
        e = [['a', 'b', 1], ['a', 'f', 1], ['c', 'd', 1], ['d', 'e', 1], ['a', 'g', 2], ['b', 'g', 2], ['f', 'g', 2], ['c', 'g', 2], ['d', 'g', 2], ['e', 'g', 2], ['b', 'c', 3], ['f', 'e', 3]]
        graph.mst_animation('Q', dict(kind='graph-mst', query='count', edges=e, expect={'count': 9, 'weight': 8}))
        with self.assertRaises(SystemExit):
            graph.mst_animation('Q', dict(kind='graph-mst', query='count', edges=e, expect={'count': 6}))

    def test_tree_path_needs_a_unique_tree(self):
        with self.assertRaises(SystemExit):
            graph.mst_animation('Q', dict(kind='graph-mst', query='path', edges=self.EDGES, **{'from': 'n2', 'to': 'n6'}, expect={'path_weight': 5}))

    def test_kruskal_order_check(self):
        # CS-2009-Q38: taking b-c (4) before a-c (3) is impossible.
        e = [['a', 'b', 5], ['a', 'c', 3], ['b', 'c', 4], ['b', 'e', 2], ['b', 'd', 6], ['c', 'd', 5], ['d', 'e', 6], ['d', 'f', 6], ['c', 'f', 6], ['e', 'f', 3], ['e', 'g', 5], ['f', 'g', 4]]
        spec = dict(kind='graph-mst', query='check', edges=e, orders=[
            dict(label='A', seq=[['b', 'e'], ['e', 'f'], ['a', 'c'], ['b', 'c'], ['f', 'g'], ['c', 'd']], expect=True),
            dict(label='D', seq=[['b', 'e'], ['e', 'f'], ['b', 'c'], ['a', 'c'], ['f', 'g'], ['c', 'd']], expect=False)])
        self.assertEqual(len(graph.mst_animation('Q', spec)['schedules']), 2)
        spec['orders'][1]['expect'] = True
        with self.assertRaises(SystemExit):
            graph.mst_animation('Q', spec)


class SearchAndTopoTest(unittest.TestCase):
    def test_bfs_and_dfs_orders(self):
        # CS-2008-Q19 and CS-2003-Q21.
        b = g(edges=[['M', 'N'], ['N', 'O'], ['O', 'P'], ['P', 'Q'], ['Q', 'M'], ['Q', 'N'], ['M', 'R']])
        self.assertTrue(graph.bfs_check(b, list('QMNPRO'), 'C')[0])
        self.assertFalse(graph.bfs_check(b, list('QMNPOR'), 'D')[0])
        d = g(nodes=list('abefgh'), edges=[['a', 'e'], ['a', 'b'], ['a', 'f'], ['e', 'b'], ['e', 'g'], ['b', 'f'], ['b', 'h'], ['f', 'h'], ['f', 'g'], ['g', 'h']])
        self.assertTrue(graph.dfs_check(d, list('abfhge'), 'III')[0])
        self.assertFalse(graph.dfs_check(d, list('abfehg'), 'II')[0])

    def test_dfs_backtracks(self):
        d = g(edges=[['a', 'b'], ['a', 'c']])
        ok, steps = graph.dfs_check(d, list('abc'), 'X')
        self.assertTrue(ok)
        self.assertIn('backs up to a', steps[2]['note'])

    def test_topological_orders(self):
        top = g(directed=True, edges=[['a', 'b'], ['b', 'c'], ['c', 'f'], ['a', 'd'], ['d', 'e'], ['e', 'f']])
        self.assertEqual(len(graph.all_topo(top)), 6)  # CS-2016-S1-Q21
        with self.assertRaises(SystemExit):
            graph.all_topo(g(directed=True, edges=[['a', 'b'], ['b', 'a']]))

    def test_double_bfs_checks_every_start(self):
        path = dict(kind='graph-search', algo='double-bfs', edges=[['a', 'b'], ['b', 'c'], ['c', 'd']], show_from='b', expect=3)
        self.assertEqual(graph.search_animation('Q', path)['kind'], 'graph-search')
        # On a 5-cycle with a tail the two-BFS answer depends on the start, so the build stops.
        bad = dict(path, edges=[['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'e'], ['e', 'a'], ['a', 'x']], expect=3)
        with self.assertRaises(SystemExit):
            graph.search_animation('Q', bad)


class GraphInputTest(unittest.TestCase):
    def test_bad_input_stops_the_build(self):
        for spec in (dict(edges=[['a', 'b'], ['b', 'a']]), dict(edges=[['a', 'a']]), dict(nodes=['a'], edges=[['a', 'b']]),
                     dict(nodes=[0, 1], matrix=[[0, 1], [2, 0]]), dict(nodes=['a', 'b'], edges=[['a', 'b']], pos={'a': [0, 0]})):
            with self.subTest(spec=spec), self.assertRaises(SystemExit):
                graph.Graph('Q', spec)


if __name__ == '__main__':
    unittest.main()
