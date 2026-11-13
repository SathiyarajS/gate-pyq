# Instructions for coding agents

Read **HANDOFF.md** first. It is the current task list, with setup, the transcribe and review procedures, and the rules for this repository. The live site is https://sathiyarajs.github.io/gate-pyq/ and it redeploys on every push to `main`.

The most important rules:
- Never mark a transcription `verified` in the session that wrote it. Review happens in a fresh session (HANDOFF.md §3.3).
- Never invent question text, options, figures or official keys.
- Never change existing entries in `data/crops.json` or run `scripts/locate_crops.py`. The only exception: a new-year import adds crops for that year's questions, reviewed in a separate session (`docs/NEW_YEAR_IMPORT.md`).
- Never commit source PDFs: they are local, git-ignored working files (`python scripts/fetch_sources.py` restores them). Commit rendered question images in `site-assets/q/` instead; `validate.py` fails if a reviewed question has none.
- Before every push, run `python scripts/validate.py`, `python -m pytest -q tests` and `node tests/test_transcription_math.js`. Never force-push.
