import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import parsing


def sets(lines):
    g = parsing.Grammar(lines)
    first = parsing.first_sets(g, None)
    return g, first, parsing.follow_sets(g, first, None)


def run(spec):
    return parsing.parse_animation('Q', dict(spec))


class ParsingTest(unittest.TestCase):
    def test_first_and_follow_reach_a_fixed_point(self):
        # CS-2012-Q62: A and B are nullable only through S; FOLLOW needs several passes.
        g, first, follow = sets(['S -> a A b B | b A a B | ε', 'A -> S', 'B -> S'])
        self.assertEqual(first['A'], {'a', 'b', 'ε'})
        self.assertEqual(follow['A'], {'a', 'b'})
        self.assertEqual(follow['B'], {'a', 'b', '$'})
        # CS-2017-S1-Q27: R is nullable, S is not, so $ never reaches Q.
        g, first, follow = sets(['P -> x Q R S', 'Q -> y z | z', 'R -> w | ε', 'S -> y'])
        self.assertEqual(follow['Q'], {'w', 'y'})

    def test_ll1_table_and_conflicts(self):
        # CS-2003-Q56: the dangling else puts two productions in M[S′, e].
        out = {}
        parsing.do_ll1(parsing.Grammar(['S -> i E t S S′ | a', 'S′ -> e S | ε', 'E -> b']), [], out)
        self.assertEqual(sorted(out['table'][('S′', 'e')]), [(), ('e', 'S')])
        self.assertEqual(out['table'][('S′', '$')], [()])
        self.assertFalse(out['ll1'])

    def test_lr_state_counts(self):
        # CS-2005-Q60: 6 LR(0)/LALR(1) states and 10 canonical LR(1) states for S -> (S) | a.
        out = {}
        g = parsing.Grammar(['S -> ( S ) | a'], augment=True)
        for m in ('slr', 'lr1', 'lalr'):
            parsing.do_lr(g, m, [], out)
        self.assertEqual(out['states'], {'slr': 6, 'lr1': 10, 'lalr': 6})

    def test_lr0_conflicts_and_lalr(self):
        # CS-2026-S2-Q41: five shift-reduce cells; CS-2025-S2-Q40: LALR(1) but not SLR(1).
        out = {}
        parsing.do_lr(parsing.Grammar(['S -> A C B', 'A -> a A | ε', 'C -> c C | ε', 'B -> b B | b'], augment=True), 'lr0', [], out)
        self.assertEqual((out['states']['lr0'], out['sr_conflicts']['lr0']), (11, 5))
        out = {}
        g = parsing.Grammar(['S -> A a | b A c | d c | b d a', 'A -> d'], augment=True)
        for m in ('slr', 'lalr'):
            parsing.do_lr(g, m, [], out)
        self.assertEqual(out['ok'], {'slr': False, 'lalr': True})

    def test_goto_counts(self):
        # CS-2021-S2-Q61: GOTO(GOTO(I0, <), <) has 8 items.
        spec = dict(kind='parse-lr', augmented=True, grammar=['S′ -> S', 'S -> S # c S | S S | S @ | < S > | a | b | c'],
                    do=[{'goto': ['<', '<']}], expect={'items': 8})
        self.assertTrue(run(spec)['schedules'][0]['steps'][-1]['final'])
        spec['expect'] = {'items': 9}
        with self.assertRaises(SystemExit):
            run(spec)

    def test_shift_reduce_actions(self):
        # CS-1995-Q35 prints 23131; CS-2023-Q60 evaluates 10#011 to 2.375.
        out = {}
        g = parsing.Grammar([{'p': 'S -> x x W', 'print': '1'}, {'p': 'S -> y', 'print': '2'}, {'p': 'W -> S z', 'print': '3'}])
        parsing.do_sr(g, {'sr': 'x x x x y z z'}, [], out)
        self.assertEqual(out['output'], '23131')
        self.assertEqual(out['reductions'], 5)
        spec = dict(kind='parse-sr', grammar=[
            {'p': 'N -> I # F', 'val': '$1 + $3'}, {'p': 'I -> I B', 'val': '2 * $1 + $2'}, {'p': 'I -> B', 'val': '$1'},
            {'p': 'F -> B F', 'val': '($1 + $2) / 2'}, {'p': 'F -> B', 'val': '$1 / 2'}, {'p': 'B -> 0', 'val': '0'}, {'p': 'B -> 1', 'val': '1'}],
            do=[{'sr': '1 0 # 0 1 1'}], expect={'value': '2.375'})
        run(spec)
        spec['expect'] = {'value': '2.5'}
        with self.assertRaises(SystemExit):
            run(spec)

    def test_ambiguous_input_is_refused_for_a_trace(self):
        g = parsing.Grammar(['E -> E + E | id'])
        with self.assertRaises(SystemExit):
            parsing.do_sr(g, {'sr': 'id + id + id'}, [], {})

    def test_predictive_trace_with_embedded_actions(self):
        # CS-2003-Q58: 9+5+2 prints 95+2+.
        out = {}
        g = parsing.Grammar(['S -> T R', "R -> + T {print('+')} R | ε", 'T -> num {print(num.val)}'])
        parsing.do_ll(g, {'ll': 'num:9 + num:5 + num:2'}, [], out)
        self.assertEqual(out['output'], '95+2+')

    def test_parse_tree_counts_and_membership(self):
        # CS-2007-Q79: two trees for aabbab; CS-2017-S1-Q44: babba is not generated even with S -> SS | ε.
        g = parsing.Grammar(['S -> a B | b A', 'B -> b | b S | a B B', 'A -> a | a S | b A A'])
        self.assertEqual(parsing.Trees(g, list('aabbab')).count('S', 0, 6), 2)
        g = parsing.Grammar(['S -> S a S | a S b | b S a | S S | ε'])
        self.assertIsNotNone(parsing.smallest_tree(g, list('abbaa')))
        self.assertIsNone(parsing.smallest_tree(g, list('babba')))
        with self.assertRaises(SystemExit):
            parsing.Trees(g, list('ab')).count('S', 0, 2)

    def test_membership_proof_rows_are_not_compacted_as_trace_rows(self):
        spec = dict(kind='parse-trees', grammar=['S -> a'],
                    do=[{'trees': '', 'generated_only': True}], expect={'generated': {'': False}})
        schedule = run(spec)['schedules'][0]
        self.assertNotIn('cols', schedule)
        self.assertEqual(schedule['steps'][-1]['view'], 'pieces')
        self.assertEqual(schedule['steps'][-1]['rows'], [['S', []]])

    def test_trace_rows_are_compacted_without_losing_the_last_row(self):
        spec = dict(kind='parse-sr', grammar=['S -> a'], do=[{'sr': 'a'}], expect={'reductions': 1})
        schedule = run(spec)['schedules'][0]
        self.assertEqual(schedule['cols'], ['Stack', 'Input', 'Action'])
        self.assertEqual(schedule['rows'][-1]['action'], 'accept')
        self.assertEqual([s['n'] for s in schedule['steps']], [1, 2, 3, 4])
        self.assertTrue(all('rows' not in step for step in schedule['steps']))

    def test_predictive_trace_cannot_use_the_complete_input_as_an_oracle(self):
        # A unique parse tree is not sufficient for one-token predictive parsing.
        g = parsing.Grammar(['S -> a b | a c'])
        with self.assertRaisesRegex(SystemExit, 'LL\\(1\\)'):
            parsing.do_ll(g, {'ll': 'a b'}, [], {})

    def test_missing_and_unknown_expectations_are_rejected(self):
        spec = dict(kind='parse-sets', grammar=['S -> a'], do=['sets'])
        with self.assertRaises(SystemExit):
            run(spec)
        spec['expect'] = {'typo': 1}
        with self.assertRaises(SystemExit):
            run(spec)

    def test_all_retained_specs_serialize_and_expose_player_contract(self):
        import json
        specs = json.loads((ROOT / 'data/animations/parsing.json').read_text())['questions']
        self.assertEqual(len(specs), 34)
        views = set()
        for qid, spec in specs.items():
            with self.subTest(qid=qid):
                result = json.loads(json.dumps(parsing.parse_animation(qid, spec)))
                self.assertEqual(result['count'], sum(len(s['steps']) for s in result['schedules']))
                for schedule in result['schedules']:
                    self.assertTrue(schedule['steps'][-1]['final'])
                    for step in schedule['steps']:
                        views.add(step['view'])
                        self.assertTrue(step['note'])
                        if step['view'] == 'sr':
                            self.assertIn('cols', schedule)
                            self.assertLessEqual(step['n'], len(schedule['rows']))
                        if step['view'] == 'pieces':
                            self.assertIn('rows', step)
                        if step['view'] == 'lr':
                            for ref in step['cards']:
                                self.assertLess(ref['c'], len(schedule['cards']))
        self.assertEqual(views, {'sets', 'll1', 'lr', 'sr', 'derive', 'pieces'})
