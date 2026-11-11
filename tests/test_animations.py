import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import animations

FOUR = [['A', 0, 10], ['B', 2, 6], ['C', 4, 3], ['D', 6, 7]]


def run(processes, policy, metric='waiting', **kw):
    spec = dict(kind='cpu-schedule', processes=processes, metric=metric, schedules=[dict(policy=policy, expect=kw.pop('expect'), **kw)])
    return animations.cpu_animation('Q', spec)['schedules'][0]


class SchedulingStepsTest(unittest.TestCase):
    def test_srtf_preempts_on_shorter_remaining_time(self):
        s = run(FOUR, 'srtf', expect=6)
        self.assertEqual(s['segs'], [['A', 0, 2], ['B', 2, 4], ['C', 4, 7], ['B', 7, 11], ['D', 11, 18], ['A', 18, 26]])
        self.assertTrue(s['steps'][-1]['final'])

    def test_non_preemptive_sjf_never_interrupts(self):
        s = run(FOUR, 'sjf', expect=7.5)
        self.assertEqual([x[0] for x in s['segs']], ['A', 'C', 'B', 'D'])

    def test_fcfs_runs_in_arrival_order(self):
        s = run(FOUR, 'fcfs', metric='order', expect=['A', 'B', 'C', 'D'])
        self.assertEqual(s['segs'], [['A', 0, 10], ['B', 10, 16], ['C', 16, 19], ['D', 19, 26]])

    def test_round_robin_queues_arrivals_before_the_preempted_process(self):
        # CS-2012-Q41: P2 arrives during P1's first slice, P3 during P2's.
        s = run([['P1', 0, 5], ['P2', 1, 7], ['P3', 3, 4]], 'rr', metric='order', quantum=2, expect=['P1', 'P3', 'P2'])
        self.assertEqual([x[0] for x in s['segs']], ['P1', 'P2', 'P1', 'P3', 'P2', 'P1', 'P3', 'P2'])
        self.assertEqual(s['queue_label'], 'Queue (front first)')

    def test_round_robin_continues_when_nobody_waits(self):
        s = run([['A', 0, 5]], 'rr', metric='turnaround', quantum=2, expect=5)
        self.assertEqual(s['segs'], [['A', 0, 5]])
        self.assertIn('nothing else is waiting', ' '.join(x['note'] for x in s['steps']))

    def test_preemptive_priority(self):
        # CS-2017-S2-Q61: lower number is higher priority.
        procs = [['P1', 0, 11, 2], ['P2', 5, 28, 0], ['P3', 12, 2, 3], ['P4', 2, 10, 1], ['P5', 9, 16, 4]]
        s = run(procs, 'priority-p', expect=29)
        self.assertEqual([x[0] for x in s['segs']], ['P1', 'P4', 'P2', 'P4', 'P1', 'P3', 'P5'])
        self.assertIn('Priority', s['final']['cols'])

    def test_one_process_metric(self):
        # CS-2007-Q55.
        spec = dict(kind='cpu-schedule', processes=[['P1', 0, 20], ['P2', 15, 25], ['P3', 30, 10], ['P4', 45, 15]], metric='waiting', process='P2', schedules=[dict(policy='srtf', expect=15)])
        s = animations.cpu_animation('Q', spec)['schedules'][0]
        self.assertIn("P2's waiting time = completion − arrival − burst = 55 − 15 − 25 = 15", s['steps'][-1]['note'])
        self.assertEqual(s['final']['highlight'], 'P2')

    def test_comparisons(self):
        spec = dict(kind='cpu-schedule', processes=[['P1', 0, 8], ['P2', 0, 7], ['P3', 0, 2], ['P4', 0, 4]], metric='turnaround',
                    schedules=[dict(policy='sjf', expect=10.5), dict(policy='rr', quantum=4, expect=15.75)], compare='difference', expect_compare=5.25)
        out = animations.cpu_animation('Q', spec)
        self.assertIn('Difference = 5.25', out['schedules'][1]['steps'][-1]['note'])
        spec['expect_compare'] = 5
        with self.assertRaises(SystemExit):
            animations.cpu_animation('Q', spec)

    def test_idle_cpu_is_handled(self):
        s = run([['A', 0, 2], ['B', 5, 1]], 'srtf', metric='turnaround', expect=1.5)
        self.assertIn('idle', ' '.join(x['note'] for x in s['steps']))

    def test_more_than_six_processes_need_colour_groups(self):
        procs = [[f'P{i}', i, 1] for i in range(7)]
        spec = dict(kind='cpu-schedule', processes=procs, metric='waiting', schedules=[dict(policy='fcfs', expect=0)])
        with self.assertRaises(SystemExit):
            animations.cpu_animation('Q', spec)
        spec['colors'] = [0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(animations.cpu_animation('Q', spec)['colors'], spec['colors'])

    def test_every_recorded_animation_matches_its_answer(self):
        qs = {q['question_id'] for q in json.loads((ROOT / 'data/questions.json').read_text())}
        recorded = json.loads((ROOT / 'data/animations.json').read_text())['questions']
        self.assertEqual(set(animations.load(ROOT, qs)), set(recorded))

    def test_a_wrong_expectation_stops_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'data').mkdir()
            (Path(tmp) / 'data/animations.json').write_text(json.dumps({'questions': {'Q': {'kind': 'cpu-schedule', 'processes': [['A', 0, 2]], 'metric': 'waiting', 'schedules': [{'policy': 'srtf', 'expect': 1}]}}}))
            with self.assertRaises(SystemExit):
                animations.load(Path(tmp), {'Q'})


class PageReplacementTest(unittest.TestCase):
    REFS = [1, 2, 3, 2, 4, 1, 3, 2, 4, 1]  # CS-2012-Q52

    def test_policies_match_the_worked_solution(self):
        for policy, faults in (('fifo', [1, 2, 3, 5, 6, 8]), ('lru', [1, 2, 3, 5, 6, 7, 8, 9, 10]), ('optimal', [1, 2, 3, 5, 8])):
            with self.subTest(policy=policy):
                self.assertEqual(animations.page_replace(self.REFS, 3, policy)[1], faults)

    def test_lru_updates_recency_on_a_hit_but_fifo_does_not(self):
        fifo, _ = animations.page_replace(self.REFS, 3, 'fifo')
        lru, _ = animations.page_replace(self.REFS, 3, 'lru')
        self.assertEqual(fifo['steps'][4]['order'], 'Load order (oldest first): 1, 2, 3')
        self.assertEqual(lru['steps'][4]['order'], 'Recency (least recent first): 1, 3, 2')

    def test_windowed_optimal_looks_only_at_the_window(self):
        data, faults = animations.page_replace([1, 3, 2, 4, 2, 3, 1, 2, 4, 3, 1, 4], 3, 'optimal-window', 4)
        self.assertEqual(faults, [1, 2, 3, 4, 7, 10])
        self.assertIn('page 2 is not used in it', data['steps'][10]['note'])

    def test_rank_and_wrong_positions(self):
        spec = dict(kind='page-replace', frames=3, refs=self.REFS, policies=[dict(policy='fifo', expect=6), dict(policy='optimal', expect=5)],
                    compare='rank', expect_compare=['optimal', 'fifo'])
        self.assertIn('Optimal 5 < FIFO 6', animations.page_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])
        spec['policies'][0]['positions'] = [1, 2, 3]
        with self.assertRaises(SystemExit):
            animations.page_animation('Q', spec)


class DiskSchedulingTest(unittest.TestCase):
    QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]  # the standard textbook queue, head at 53

    def path(self, policy, direction='up'):
        d = animations.disk_schedule(53, self.QUEUE, policy, direction, 0, 199)
        return d['total'], [m[1] for m in d['moves']]

    def test_policies(self):
        self.assertEqual(self.path('fcfs')[0], 640)
        self.assertEqual(self.path('sstf'), (236, [65, 67, 37, 14, 98, 122, 124, 183]))
        self.assertEqual(self.path('scan', 'down'), (236, [37, 14, 0, 65, 67, 98, 122, 124, 183]))
        self.assertEqual(self.path('look', 'down')[0], 208)
        self.assertEqual(self.path('cscan'), (382, [65, 67, 98, 122, 124, 183, 199, 0, 14, 37]))
        self.assertEqual(self.path('clook'), (322, [65, 67, 98, 122, 124, 183, 14, 37]))

    def test_sstf_tie_stops_the_build(self):
        with self.assertRaises(SystemExit):
            animations.disk_schedule(50, [40, 60], 'sstf')

    def test_reversal_cost(self):
        # CS-2018-Q63: 200 cylinders at 20 per 100, three reversals at 15.
        spec = dict(kind='disk-schedule', start=80, requests=[72, 134, 20, 86, 116, 16], lo=0, hi=199, metric='cost',
                    cost=dict(per=20, cylinders=100, reversal=15), policies=[dict(policy='sstf', expect=85)])
        self.assertIn('changes direction 3 times', animations.disk_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])


class HashingTest(unittest.TestCase):
    def test_linear_probing_wraps_and_records_collisions(self):
        steps, table = animations.hash_insert(dict(size=5, method='linear', keys=[4, 9, 14]))
        self.assertEqual(table, [9, 14, None, None, 4])
        self.assertEqual(steps[-1]['probed'], [4, 0])

    def test_double_hashing(self):
        # CS-2025-S1-Q65: 24 ends up in slot 10.
        steps, table = animations.hash_insert(dict(size=11, method='double', h2=dict(c=1, d=7), keys=[63, 50, 25, 79, 67, 24]))
        self.assertEqual(table.index(24), 10)

    def test_chaining_statistics_are_checked(self):
        spec = dict(kind='hash-insert', size=9, method='chaining', keys=[5, 28, 19, 15, 20, 33, 12, 17, 10], expect=dict(chains=dict(max=3, min=0, avg=1)))
        self.assertIn('Longest 3', animations.hash_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])
        spec['expect']['chains']['max'] = 4
        with self.assertRaises(SystemExit):
            animations.hash_animation('Q', spec)


class HeapAndBstTest(unittest.TestCase):
    def test_heap_insert_delete_and_build(self):
        _, a = animations.heap_ops(dict(start=[10, 8, 5, 3, 2], ops=[['insert', [1, 7]]]))
        self.assertEqual(a, [10, 8, 7, 3, 2, 1, 5])  # CS-2014-S2-Q22
        _, a = animations.heap_ops(dict(start=[25, 14, 16, 13, 10, 8, 12], ops=[['delete', 2]]))
        self.assertEqual(a, [14, 13, 12, 8, 10])  # CS-2009-Q60
        _, a = animations.heap_ops(dict(ops=[['build', [82, 101, 90, 11, 111, 75, 33, 131, 44, 93]]]))
        self.assertEqual(a[:3], [131, 111, 90])  # CS-2024-S1-Q41

    def test_ternary_heap(self):
        _, a = animations.heap_ops(dict(arity=3, start=[9, 5, 6, 8, 3, 1], ops=[['insert', [7, 2, 10, 4]]]))
        self.assertEqual(a, [10, 7, 9, 8, 3, 1, 5, 2, 6, 4])  # CS-2006-Q77

    def test_bst_queries(self):
        spec = dict(kind='bst', keys=[15, 10, 12, 11, 20, 18, 16, 19], from_preorder=True, query='postorder', expect=[11, 12, 10, 16, 19, 18, 20, 15])
        out = animations.bst_animation('Q', spec)
        self.assertEqual(out['schedules'][0]['steps'][-1]['out'], spec['expect'])
        self.assertEqual(animations.bst_animation('Q', dict(kind='bst', keys=[10, 1, 3, 5, 15, 12, 16], query='height', expect=3))['kind'], 'bst')
        with self.assertRaises(SystemExit):
            animations.bst_animation('Q', dict(kind='bst', keys=[10, -4, 15, 30, 20, 5, 60, 19], query='depth', node=19, expect=3))
