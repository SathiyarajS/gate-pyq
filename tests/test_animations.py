import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import animations


class SchedulingStepsTest(unittest.TestCase):
    def test_srtf_preempts_on_shorter_remaining_time(self):
        data, avg = animations.cpu_schedule([['A', 0, 10], ['B', 2, 6], ['C', 4, 3], ['D', 6, 7]], 'srtf', 'waiting')
        self.assertEqual(data['segs'], [['A', 0, 2], ['B', 2, 4], ['C', 4, 7], ['B', 7, 11], ['D', 11, 18], ['A', 18, 26]])
        self.assertEqual(float(avg), 6.0)
        self.assertTrue(data['steps'][-1]['final'])

    def test_non_preemptive_sjf_never_interrupts(self):
        data, avg = animations.cpu_schedule([['A', 0, 10], ['B', 2, 6], ['C', 4, 3], ['D', 6, 7]], 'sjf', 'waiting')
        self.assertEqual([s[0] for s in data['segs']], ['A', 'C', 'B', 'D'])
        self.assertEqual(float(avg), 7.5)

    def test_idle_cpu_is_handled(self):
        data, avg = animations.cpu_schedule([['A', 0, 2], ['B', 5, 1]], 'srtf', 'turnaround')
        self.assertIn('idle', ' '.join(s['note'] for s in data['steps']))
        self.assertEqual(float(avg), 1.5)

    def test_every_recorded_animation_matches_its_answer(self):
        qs = {q['question_id'] for q in json.loads((ROOT / 'data/questions.json').read_text())}
        self.assertEqual(len(animations.load(ROOT, qs)), 8)

    def test_a_wrong_expectation_stops_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'data').mkdir()
            (Path(tmp) / 'data/animations.json').write_text(json.dumps({'questions': {'Q': {'kind': 'cpu-schedule', 'processes': [['A', 0, 2]], 'metric': 'waiting', 'schedules': [{'policy': 'srtf', 'expect': 1}]}}}))
            with self.assertRaises(SystemExit):
                animations.load(Path(tmp), {'Q'})
