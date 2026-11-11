import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import fork

FORK = {'op': 'fork'}


class ForkTest(unittest.TestCase):
    def test_straight_line_forks_double(self):
        # CS-2012-Q18: three fork() calls, 1 -> 2 -> 4 -> 8 processes, 7 children.
        out = fork.simulate([FORK, FORK, FORK])
        self.assertEqual(out['totals'], dict(processes=8, children=7, prints=0))
        self.assertEqual([c['label'] for c in out['calls']], ['fork 1', 'fork 2', 'fork 3'])
        # P0 makes P1, P2, P4; P1 makes P3, P5; P2 makes P6; P3 makes P7.
        self.assertEqual([n[0] for n in out['nodes']], [None, 0, 0, 1, 0, 1, 2, 3])

    def test_loop_with_condition(self):
        # CS-2019-Q27: fork only on even i, five rounds, 31 children.
        prog = [{'op': 'for', 'var': 'i', 'from': 0, 'to': 10, 'body': [{'op': 'if', 'cond': 'i % 2 == 0', 'then': [FORK]}]}]
        self.assertEqual(fork.simulate(prog)['totals']['children'], 31)

    def test_symbolic_bound_is_checked_against_the_formula(self):
        spec = dict(kind='fork-tree', program=[{'op': 'for', 'var': 'i', 'from': 0, 'to': 'n', 'body': [FORK]}],
                    cases=[{'n': 2}, {'n': 3}], query='children', expect='2^n−1')
        self.assertEqual(len(fork.fork_animation('Q', spec)['schedules']), 2)
        spec['expect'] = '2^n'
        with self.assertRaises(SystemExit):
            fork.fork_animation('Q', spec)

    def test_wait_and_prints(self):
        # CS-2024-S1-Q57: printf runs 2 + 4 + 8 = 14 times; a childless wait(NULL) returns at once.
        prog = [{'op': 'int', 'var': 'x', 'value': 3},
                {'op': 'while', 'cond': 'x > 0', 'body': [FORK, {'op': 'printf', 'text': 'hello'}, {'op': 'wait'}, {'op': 'dec', 'var': 'x'}]}]
        out = fork.simulate(prog)
        self.assertEqual((out['totals']['prints'], out['totals']['processes']), (14, 8))
        self.assertTrue(any('no children' in s['note'] for s in out['steps']))
        self.assertTrue(any('is woken' in s['note'] for s in out['steps']))

    def test_continue_and_break_make_a_chain(self):
        # CS-2026-S1-Q63: the child continues, the parent breaks: a chain of 4, each prints once.
        prog = [{'op': 'for', 'var': 'i', 'from': 0, 'to': 3, 'body': [
                    {'op': 'if_fork', 'test': '== 0', 'then': [{'op': 'continue'}]}, {'op': 'break'}]},
                {'op': 'printf', 'text': 'Hello!'}, {'op': 'return'}]
        out = fork.simulate(prog)
        self.assertEqual(out['totals']['prints'], 4)
        self.assertEqual([n[0] for n in out['nodes']], [None, 0, 1, 2])
        self.assertIn('printf("Hello!");', out['lines'])

    def test_wrong_expectation_stops_the_build(self):
        with self.assertRaises(SystemExit):
            fork.fork_animation('Q', dict(kind='fork-tree', program=[FORK, FORK], query='children', expect=4))


if __name__ == '__main__':
    unittest.main()
