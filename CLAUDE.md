# Instructions for coding agents

Read **HANDOFF.md** first. It is the current task list, with setup, the transcribe and review procedures, and the rules for this repository. The live site is https://sathiyarajs.github.io/gate-pyq/ and it redeploys on every push to `main`.

The most important rules:
- Never mark a transcription `verified` in the session that wrote it. Review happens in a fresh session (HANDOFF.md §3.3).
- Never invent question text, options, figures or official keys.
- Never edit `data/crops.json` or run `scripts/locate_crops.py`.
- Before every push, run `python scripts/validate.py`, `python -m pytest -q tests` and `node tests/test_transcription_math.js`. Never force-push.
