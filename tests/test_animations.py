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
