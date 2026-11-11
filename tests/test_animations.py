"""The animation loader: every recorded animation is checked, and a wrong one stops the build."""
import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import animations


class LoaderTest(unittest.TestCase):
    def test_every_recorded_animation_matches_its_answer(self):
        qs = {q['question_id'] for q in json.loads((ROOT / 'data/questions.json').read_text())}
        recorded = set()
        for path in (ROOT / 'data/animations').glob('*.json'):
            recorded |= set(json.loads(path.read_text())['questions'])
        out = animations.load(ROOT, qs)
        self.assertEqual(set(out), recorded)
        for qid, data in out.items():
            with self.subTest(qid=qid):
                self.assertTrue((ROOT / 'site-static/steps' / (data['player'] + '.js')).is_file())

    def write(self, tmp, files):
        (Path(tmp) / 'data/animations').mkdir(parents=True)
        for name, questions in files.items():
            (Path(tmp) / 'data/animations' / name).write_text(json.dumps({'questions': questions}))

    def test_a_wrong_expectation_stops_the_build(self):
        bad = {'Q': {'kind': 'cpu-schedule', 'processes': [['A', 0, 2]], 'metric': 'waiting', 'schedules': [{'policy': 'srtf', 'expect': 1}]}}
        with tempfile.TemporaryDirectory() as tmp:
            self.write(tmp, {'cpu.json': bad})
            with self.assertRaises(SystemExit):
                animations.load(Path(tmp), {'Q'})

    def test_a_question_in_two_files_stops_the_build(self):
        ok = {'Q': {'kind': 'cpu-schedule', 'processes': [['A', 0, 2]], 'metric': 'waiting', 'schedules': [{'policy': 'srtf', 'expect': 0}]}}
        with tempfile.TemporaryDirectory() as tmp:
            self.write(tmp, {'a.json': ok, 'b.json': ok})
            with self.assertRaises(SystemExit):
                animations.load(Path(tmp), {'Q'})

    def test_cache_reuses_only_identical_spec_and_code(self):
        good = {'Q': {'kind': 'cpu-schedule', 'processes': [['A', 0, 2]], 'metric': 'waiting', 'schedules': [{'policy': 'srtf', 'expect': 0}]}}
        with tempfile.TemporaryDirectory() as tmp:
            self.write(tmp, {'cpu.json': good})
            first = animations.load(Path(tmp), {'Q'})
            files = list((Path(tmp) / '.anim-cache').glob('*.json'))
            self.assertEqual(len(files), 1)
            self.assertEqual(animations.load(Path(tmp), {'Q'}), first)  # served from the cache
            files[0].write_text('{damaged')
            self.assertEqual(animations.load(Path(tmp), {'Q'}), first)  # a damaged file is recomputed
            # A changed expectation is a different key, so it is simulated (and fails) afresh.
            bad = json.loads(json.dumps(good)); bad['Q']['schedules'][0]['expect'] = 1
            (Path(tmp) / 'data/animations/cpu.json').write_text(json.dumps({'questions': bad}))
            with self.assertRaises(SystemExit):
                animations.load(Path(tmp), {'Q'})

    def test_cache_key_covers_the_simulator_source(self):
        src = b''.join(f.read_bytes() for f in sorted((ROOT / 'scripts/animations').glob('*.py')))
        import hashlib
        self.assertEqual(animations._CODE, hashlib.sha256(src).hexdigest())

