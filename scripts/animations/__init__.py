"""Build-time step data for the 'Step through it' players.

Each family is a module in this package that defines KINDS (animation kind ->
function(qid, spec) returning the player data) and PLAYER (the file
site-static/steps/<PLAYER>.js that draws it), and optionally TABS (the word for
several tabs, e.g. 'schedules'; default 'versions'). Modules are discovered
automatically. Each family's entries live in data/animations/<family>.json.

Every animation is simulated here, and the build stops if a result differs from
the recorded expectation, so a player can never show a different answer from
the key.

Results are cached in .anim-cache/, keyed on the question's spec and the source
of every module in this package. Changing the data or any simulator code
recomputes the result, and only results that passed their checks are stored.
Set GATE_ANIM_CACHE=0 to bypass the cache.
"""
import hashlib
import importlib
import json
import os
import pkgutil
from pathlib import Path

KINDS, PLAYERS, TABS = {}, {}, {}
for _info in pkgutil.iter_modules(__path__):
    if _info.name == 'common':
        continue
    _mod = importlib.import_module(f'{__name__}.{_info.name}')
    for _kind, _fn in getattr(_mod, 'KINDS', {}).items():
        if _kind in KINDS:
            raise SystemExit(f'Animation kind {_kind} is defined twice')
        KINDS[_kind], PLAYERS[_kind] = _fn, _mod.PLAYER
        TABS[_kind] = getattr(_mod, 'TABS', 'versions')


_CODE = hashlib.sha256(b''.join(f.read_bytes() for f in sorted(Path(__file__).parent.glob('*.py')))).hexdigest()


def _simulate(root, qid, spec):
    """Simulate one entry, or reuse a cached result for the same spec and simulator code.

    The result goes through JSON either way, so a cached and a fresh build are identical.
    """
    use_cache = os.environ.get('GATE_ANIM_CACHE', '1') != '0'
    key = hashlib.sha256((_CODE + qid + json.dumps(spec, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
    path = root / '.anim-cache' / f'{key}.json'
    if use_cache and path.is_file():
        try:
            return json.loads(path.read_text())
        except ValueError:
            pass  # a damaged cache file is simply recomputed
    text = json.dumps(KINDS[spec['kind']](qid, spec), ensure_ascii=False)
    if use_cache:
        try:
            path.parent.mkdir(exist_ok=True)
            tmp = path.with_suffix(f'.{os.getpid()}.tmp')  # the tests and the build may run at once
            tmp.write_text(text)
            tmp.replace(path)
        except OSError:
            pass  # caching is only an optimisation
    return json.loads(text)


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
            data = _simulate(root, qid, spec)
            data['player'] = PLAYERS[spec['kind']]
            data.setdefault('tabs_label', TABS[spec['kind']])
            out[qid] = data
    return out
