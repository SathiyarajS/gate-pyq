# Handoff to Codex: what's left

Paste this to Codex:

```
In SathiyarajS/gate-pyq, work on branch `main` (use short-lived branches merged by PR
if you prefer). Read CODEX_HANDOFF.md, then the "Status" section at the top of
CODEX_INSTRUCTIONS.md, docs/TRANSCRIPTIONS.md and handoff/2024-drafts/README.md.
Do the tasks in CODEX_HANDOFF.md in order. Commit and push after each paper or task.
```

## Where things stand

- **The site is built and merged into `main`.** `.github/workflows/pages.yml` deploys it to https://sathiyarajs.github.io/gate-pyq/ on every push to `main`, but only once the owner has made the repo public and set Pages → Source to GitHub Actions.
- **Every question is on the site:** 3,406 questions in 13 subject folders, 10 per page, with a collapsible Answer, the year in brackets, discrepancies, two PDFs per subject, and all 9 extras (search, filters, practice, full-paper view, report link, topic chart, permalinks, dark mode, print styles).
- **Question display today:** all 3,406 questions show the original image cropped from the source paper. The 2007–2018 papers are restored from the official CS.zip during each build, hash-checked.
- **Redrawn questions:**
  - 260 drafts exist (2026 S1/S2, 2025 S1/S2), none verified yet.
  - 130 more drafts are in `handoff/2024-drafts/`.
  - The other ~3,016 questions have nothing yet.
  - Drafts stay hidden until verified; meanwhile the crop is shown.
- **Checks:** `scripts/validate.py`, 31 unit tests and `node tests/test_transcription_math.js` pass. The full release build, link check and 26 PDFs were built and checked locally.

## Tasks, in order

### 1. First deployment: already confirmed by Claude
Run `42805316108` on `main` (commit `c959240`) succeeded and deployed to https://sathiyarajs.github.io/gate-pyq/:
- `archive members restored: 10 ok, 0 rejected`
- `3406 questions show the original question image`
- `Rendered 4351 images`, 26 PDFs, `0 broken internal targets`
- `_site` is 746 MB

Only a human spot-check of the live pages remains: one question per subject, a PDF, search, filters, the A–D buttons and a permalink. If the owner reports problems, fix them first.

### 2. Finish the 2024 drafts (`handoff/2024-drafts/`)
Follow `handoff/2024-drafts/CODEX_HANDOFF.md`. In short:
- Apply `review-fixes/` (restore emphasis; Q18/Q19 typographic quotes stay `[sic]` with a discrepancy note; reclassify Q42's discrepancy as `question-error`; add spaces before "will" in S2 Q33 options B/D).
- Regenerate CS-2024-S2 Q22's DFA through the pinned Graphviz DOT route.
- Render every CS-2024-S2 Q36–65 figure as an image and review it, since this was never done.
- Rename the generic generator files uniquely when moving them into `figures/sources/`. Prove that the regenerated SVGs match what was reviewed.
- Commit one paper per commit: `transcribe: CS-2024-S1 (0/65 verified)`.

### 3. Redraw the remaining papers (long-running: about 40 papers)
Work newest first: 2023, 2022, … 1991. For each paper:
1. **Draft.**
   - Typed PDFs (1991–2006, 2013, 2022–2024): extract the text, then correct it line by line against the page.
   - Scanned PDFs (2007–2012, 2014–2021, 2025 S2): OCR with tesseract, then correct every line. Never accept OCR text unchecked.
2. **Figures.** Use SVG with `currentColor`, real `<text>` labels and a `viewBox`. Graphs and automata go through DOT with pinned positions; circuits and timing diagrams are hand-drawn SVG. Copy every label exactly and add nothing.
3. **Compare.** Run `python scripts/compare_transcription.py <paper>` and check every question against its crop.
4. **Check the solution.** Confirm the existing solution still fits the exact wording. If the paraphrase lost a detail that changes the answer, fix the solution and log it in `DISCREPANCIES.md`.
5. **Commit** `transcribe: <paper> (0/<n> verified)` and update `COVERAGE.md` with `scripts/update_redrawn_coverage.py`.

A paper becomes `verified` only after a separate review pass **and** the owner's visual check of that paper's comparison page. Ask the owner, naming the paper and the comparison file. Then set `status: "verified"` with the full `verification` block required by `docs/TRANSCRIPTIONS.md`. Never fill in reviewer or approval fields that didn't actually happen.

Every merge to `main` redeploys the site, and verified questions switch from crop to redrawn automatically.

### 4. Find the missing official keys (optional, long-running)
1,716 entries (1991–2010) have no official key; their answers are independently derived. If an official key for any of those years turns up from IIT or GATE sources, record it exactly as printed, compare it with the derived answers, and log any differences in `DISCREPANCIES.md`.

### 5. Clean-up
- **README.md:** keep the short "Website" section and move the long caveats paragraph to `QUALITY.md`.
- **Scripts:** move the one-off `scripts/check_*.py` into `scripts/checks/` and update any paths in `audits/` that reference them.
- **Known issues:**
  - "Recorded options (source verification pending)" shows raw text for some older questions; render it as a list or drop it once that paper is redrawn.
  - `subjects/*.md` are not regenerated from `data/questions.json`; keep both in sync.
  - After editing question text, re-run `python scripts/fix_glued_numbers.py`. It is idempotent and restores spaces like "costs 7n".

## Rules
- Do not change repository settings (visibility, Pages, permissions); those are the owner's.
- Do not force-push. Re-read the branch before writing, and verify each push landed.
- Keep `data/questions.json` in its compact one-line format: `json.dumps(..., ensure_ascii=False, separators=(",", ":"))`.
- Before every push, run `python scripts/validate.py`, `python -m pytest -q tests` and `node tests/test_transcription_math.js`.
