"""Build-time step data for the 'Step through it' players.

Each family is a module in this package that defines KINDS (animation kind ->
function(qid, spec) returning the player data) and PLAYER (the file
site-static/steps/<PLAYER>.js that draws it). Modules are discovered
automatically. Each family's entries live in data/animations/<family>.json.

Every animation is simulated here, and the build stops if a result differs from
the recorded expectation, so a player can never show a different answer from
the key.
"""
import importlib
import json
import pkgutil

KINDS, PLAYERS = {}, {}
for _info in pkgutil.iter_modules(__path__):
    if _info.name == 'common':
        continue
    _mod = importlib.import_module(f'{__name__}.{_info.name}')
    for _kind, _fn in getattr(_mod, 'KINDS', {}).items():
        if _kind in KINDS:
            raise SystemExit(f'Animation kind {_kind} is defined twice')
        KINDS[_kind], PLAYERS[_kind] = _fn, _mod.PLAYER


def load(root, question_ids):
    folder = root / 'data/animations'
    out, seen = {}, {}
    for path in sorted(folder.glob('*.json')) if folder.is_dir() else []:
        for qid, spec in json.loads(path.read_text())['questions'].items():
            if qid not in question_ids:
                raise SystemExit(f'{path.name} names an unknown question: {qid}')
            if qid in seen:
                raise SystemExit(f'{qid} has animations in both {seen[qid]} and {path.name}')
            if spec.get('kind') not in KINDS:
                raise SystemExit(f'Unknown animation kind for {qid} in {path.name}: {spec.get("kind")}')
            seen[qid] = path.name
            data = KINDS[spec['kind']](qid, spec)
            data['player'] = PLAYERS[spec['kind']]
            out[qid] = data
    return out
