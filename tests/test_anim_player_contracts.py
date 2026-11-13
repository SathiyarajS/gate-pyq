"""Run the family player DOM-contract scripts that read the simulator's data on stdin."""
import json, shutil, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import animations


def family_data(name):
    out = {}
    for qid, spec in json.loads((ROOT / f'data/animations/{name}.json').read_text())['questions'].items():
        data = animations.KINDS[spec['kind']](qid, spec)
        data['player'] = animations.PLAYERS[spec['kind']]
        out[qid] = data
    return out


@unittest.skipUnless(shutil.which('node'), 'node is not installed')
class PlayerContractTest(unittest.TestCase):
    def test_parsing_player_draws_every_step(self):
        run = subprocess.run(['node', str(ROOT / 'tests/test_anim_parsing_player.js')], input=json.dumps(family_data('parsing')),
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr[-2000:])
        self.assertIn('passed', run.stdout)


if __name__ == '__main__':
    unittest.main()
