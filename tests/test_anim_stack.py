import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import stack


class StackTest(unittest.TestCase):
    def test_right_associative_power_and_stated_precedence(self):
        # CS-2004-Q38: ^ > × > + > −, ^ right-associative.
        prec = {'^': [4, 'right'], '×': [3, 'left'], '+': [2, 'left'], '−': [1, 'left']}
        _, steps, out = stack.infix_to_postfix('a+b×c−d^e^f', prec)
        self.assertEqual(' '.join(out), 'a b c × + d e f ^ ^ −')
        self.assertIn('pop ×', steps[6]['note'])          # − arrives: × and + leave the stack
        self.assertEqual(steps[10]['stacks'][0]['items'], ['−', '^', '^'])

    def test_left_associativity_pops_equal_precedence(self):
        _, _, out = stack.infix_to_postfix('a-b-c')
        self.assertEqual(out, ['a', 'b', '-', 'c', '-'])

    def test_function_call_is_output_after_its_argument(self):
        # CS-1998-Q87, worked in the solution.
        _, _, out = stack.infix_to_postfix('3*log(x+1)−a/2', functions=['log'])
        self.assertEqual(' '.join(out), '3 x 1 + log * a 2 / −')

    def test_unbalanced_brackets_stop_the_build(self):
        with self.assertRaises(SystemExit):
            stack.infix_to_postfix('(a+b')

    def test_postfix_evaluation_pops_right_operand_first(self):
        # CS-2015-S3-Q28: 150 − 8, not 8 − 150.
        _, steps, st, _ = stack.postfix_evaluate('10 5 + 60 6 / * 8 −')
        self.assertEqual(st, [142])
        self.assertIn('150 − 8 = 142', steps[-1]['note'])

    def test_stop_after_first_multiplication(self):
        # CS-2007-Q38: stack is [1, 6] right after the first *.
        _, _, st, stopped = stack.postfix_evaluate('8 2 3 ^ / 2 3 * + 5 1 * −', {'after': '*', 'occurrence': 1})
        self.assertEqual((st, stopped), ([1, 6], 8))

    def test_inexact_division_is_refused(self):
        with self.assertRaises(SystemExit):
            stack.postfix_evaluate('7 2 /')

    def test_expression_tree_traversal(self):
        # CS-2016-S2-Q46: root, right, left.
        spec = dict(postfix='3 4 * 5 - 2 ^ 6 7 * 1 + -', traversal=['root', 'right', 'left'],
                    expect=dict(traversal='- + 1 * 7 6 ^ 2 - 5 * 4 3'))
        self.assertTrue(stack.eval_animation('Q', spec)['schedules'][0]['steps'][-1]['final'])
        spec['expect']['traversal'] = '- + 1 * 6 7 ^ 2 - 5 * 3 4'
        with self.assertRaises(SystemExit):
            stack.eval_animation('Q', spec)

    def test_push_pop_trace_and_named_results(self):
        # CS-2021-S1-Q31: s = 62, q = 24.
        _, S, Q, popped, var = stack.run_ops(['push 54', 'push 52', 'pop', 'push 55', 'push 62', 's = pop',
                                              'enqueue 21', 'enqueue 24', 'dequeue', 'enqueue 28', 'enqueue 32', 'q = dequeue'])
        self.assertEqual((popped, var, S, Q), ([52, 62], {'s': 62, 'q': 24}, [54, 55], [28, 32]))
        with self.assertRaises(SystemExit):
            stack.run_ops(['push 1', 'pop', 'pop'])

    def test_stack_permutations(self):
        # CS-1994-Q14: only 3 4 5 2 1 can come out of one stack fed 1..5.
        spec = dict(input=[1, 2, 3, 4, 5], stacks={'Stack': {}},
                    moves=[dict(name='push', **{'from': 'input', 'to': 'Stack'}), dict(name='pop', **{'from': 'Stack', 'to': 'output'})])
        self.assertTrue(stack.stack_moves(spec, [3, 4, 5, 2, 1])[0])
        found, path = stack.stack_moves(spec, [3, 4, 5, 1, 2])
        self.assertFalse(found)
        self.assertEqual(path.count('pop'), 3)               # gets as far as 3, 4, 5

    def test_bounded_second_stack(self):
        # CS-2024-S2-Q48: S2 holds two, so 100 cannot come out first.
        spec = dict(stacks={'S1': {'init': [100, 200, 300, 400], 'cap': 4}, 'S2': {'cap': 2}},
                    moves=[dict(name='T', **{'from': 'S1', 'to': 'S2'}), dict(name='R', **{'from': 'S2', 'to': 'S1'}),
                           dict(name='O', **{'from': 'S1', 'to': 'output'})])
        self.assertFalse(stack.stack_moves(spec, [100, 200, 400, 300])[0])
        self.assertEqual(stack.stack_moves(spec, [400, 200, 100, 300]), (True, ['O', 'T', 'O', 'O', 'R', 'O']))
        spec['stacks']['S2']['cap'] = 3
        self.assertTrue(stack.stack_moves(spec, [100, 200, 400, 300])[0])

    def test_wrong_expectation_stops_the_build(self):
        spec = dict(items=[1, 2, 3], target=[3, 1, 2], options=[[3], [1, 2]], expect=[[3], [1, 2]])
        with self.assertRaises(SystemExit):
            stack.split_animation('Q', spec)
        spec['expect'] = [[3]]
        self.assertEqual(len(stack.split_animation('Q', spec)['schedules']), 2)
