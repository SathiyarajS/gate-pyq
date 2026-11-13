# Contributing

Thanks for helping make this a reliable place to study GATE CS.

## Report a mistake

The quickest way is the **Report issue** link under any question on the website. It opens a GitHub issue with the question's ID filled in. General comments go on the site's **Feedback** page (GitHub Discussions).

Please say what is wrong (the answer, the solution, the question image, a step-through) and, if you can, why. If the official key is involved, link the official key PDF.

## Fix it yourself

1. Fork the repository and make your change.
   - Question data, answers and solutions are in `data/questions.json`, and the same text is in `subjects/<subject>/<year>.md`. Change both.
   - Discrepancies go in `DISCREPANCIES.md`.
2. Run the checks:
   ```sh
   pip install -r requirements-site.txt pytest && npm ci --ignore-scripts
   python scripts/validate.py && python -m pytest -q tests && node tests/test_transcription_math.js
   ```
3. Open a pull request. The site build runs on it automatically.

## Rules for every change

- **Never change an official answer key** to match a solution. If the key looks wrong, keep it as published and record the disagreement in `DISCREPANCIES.md`.
- **Never invent** question text, options, figures or keys.
- **Don't commit source PDFs.** Only each paper's link and sha256 are stored; `python scripts/fetch_sources.py` restores the PDFs locally. Question images go in `site-assets/q/` via `scripts/render_crops.py`.
- Keep `data/questions.json` in its compact single-line format: `json.dumps(..., ensure_ascii=False, separators=(",", ":"))`.
- Never edit existing entries in `data/crops.json`, and never run `scripts/locate_crops.py`.

## Coding agents (Codex, Claude Code)

Start from [AGENTS.md](AGENTS.md) and [HANDOFF.md](HANDOFF.md). They hold the remaining work, ready-to-paste prompts and the review rules. Adding a new exam year is a single run; see [docs/NEW_YEAR_IMPORT.md](docs/NEW_YEAR_IMPORT.md).
