# Handoff: remaining work (for Codex or Claude Code on your own computer)

The site is live at **https://sathiyarajs.github.io/gate-pyq/** and redeploys automatically on every push to `main` (about 20 min). What's left is mostly **redrawing questions** as real text and vector figures, which is long-running work. The owner does **no manual review**; the agent reviews its own work in a *separate* session using screenshots (see "How a paper gets verified").

**Progress at a glance:** [docs/CHECKLIST.md](docs/CHECKLIST.md) lists every task and, per paper, how many questions are drafted, verified and live.

---

To add a new exam year, run prompt G below; nothing else is needed. The steps it follows are in [docs/NEW_YEAR_IMPORT.md](docs/NEW_YEAR_IMPORT.md).

## 1. One-time setup on your computer

You need git, Python 3.12, Node.js 20+, Graphviz (`dot`) and Tesseract OCR.

| | macOS (Homebrew) | Ubuntu / WSL |
|---|---|---|
| Tools | `brew install python@3.12 node graphviz tesseract` | `sudo apt install python3.12-venv nodejs npm graphviz tesseract-ocr` |

Then run:

```sh
git clone https://github.com/SathiyarajS/gate-pyq.git
cd gate-pyq
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements-site.txt pytesseract
python -m playwright install chromium
npm ci --ignore-scripts
python scripts/validate.py && python -m pytest -q tests && node tests/test_transcription_math.js
```

On Windows, run all of this inside WSL.

You don't need to read the rest of this file yourself. The agent reads it automatically: `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code) point here.

---

## 2. Prompts to paste

Start every prompt from the `gate-pyq` folder with the virtual environment active.

**A. Finish the 2024 drafts (do this first, once)**
```
Read HANDOFF.md and do task 3.1 (finish the CS-2024-S1 and CS-2024-S2 drafts).
Do not mark anything verified. Commit and push to main when done.
```

**B. Transcribe the next paper (repeat; one paper per session)**
```
Read HANDOFF.md. Do task 3.2 for the next paper in the "Order" list that has no
data/transcriptions/<paper>.json yet. Transcribe all its questions as drafts,
generate its comparison screenshots, self-check them, commit and push to main.
Do not mark anything verified.
```

**C. Review a drafted paper (repeat; must be a NEW session, never the one that transcribed it)**
```
Read HANDOFF.md. Do task 3.3 (independent review) for the newest paper whose
data/transcriptions/<paper>.json still has draft entries and that you did not
transcribe in this session. Commit and push to main.
```

**E. Finish a step-through family (repeat; one branch per session)**
```
Read HANDOFF.md §3.6 and §3.7. Pick the first family in the §3.7 table whose status
is not "merged". Check out its wip/anim-<name> branch, finish it (simulator, data,
player, tests) following §3.6, run every check in §3.7, commit and push to that
same wip branch. Do not merge to main.
```

**F. Review and merge a finished step-through family (must be a NEW session)**
```
Read HANDOFF.md §3.7. Review the finished wip/anim-<name> branch you did not write,
using the review checklist there. If it passes, merge it into main with --no-ff,
run all checks, push main, delete the wip branch, and update the §3.7 table.
If it fails, push fixes to the wip branch or drop the failing questions.
```

**G. Add the next exam year (one run, nothing else to do)**

Once GATE has published the new papers and final keys, run this in the `gate-pyq` folder and leave it:
```sh
git pull
codex exec --full-auto -c sandbox_workspace_write.network_access=true "Read docs/NEW_YEAR_IMPORT.md and add the next GATE CS year to the site, start to finish, without asking me anything."
```
or, with Claude Code:
```sh
git pull
claude -p "Read docs/NEW_YEAR_IMPORT.md and add the next GATE CS year to the site, start to finish, without asking me anything." --dangerously-skip-permissions
```
It works out the year, finds the official PDFs, does every step including the separate review, merges into `main` (which deploys the site) and ends with a short summary. The run needs network access to download the papers and push. With Claude Code: `claude -p "<same prompt>" --dangerously-skip-permissions`.

**D. Optional unattended loop.** This runs the agent with full permissions inside this folder, so only use it in this repo.

```sh
# Codex CLI
while true; do codex exec --full-auto "$(cat .agent-prompt-B)"; codex exec --full-auto "$(cat .agent-prompt-C)"; done
# Claude Code
while true; do claude -p "$(cat .agent-prompt-B)" --dangerously-skip-permissions; claude -p "$(cat .agent-prompt-C)" --dangerously-skip-permissions; done
```

Save prompts B and C to `.agent-prompt-B` and `.agent-prompt-C` first; these files are gitignored. Stop the loop with Ctrl-C. Each call is a fresh session, so the review is always done by a different session than the transcription.

---

## 3. Tasks

### 3.1 Finish the 2024 drafts (`handoff/2024-drafts/`)
Follow `handoff/2024-drafts/CODEX_HANDOFF.md` and apply `handoff/2024-drafts/review-fixes/`. In short:
- Restore emphasis in S1 Q22, Q30 and Q34. Keep `[sic]` on the typographic quotes in S1 Q18/Q19 and add a narrow discrepancy note without changing the answer.
- Reclassify S1 Q42's BASE-CASE discrepancy as `question-error` instead of duplicating it.
- Add spaces before "will" in S2 Q33 options B and D, and restore the listed emphasis and paragraphs. The Q33 typography note must not imply the function definition fails to compile.
- Regenerate the S2 Q22 DFA through Graphviz DOT with pinned positions.
- Check S2 Q8's second pie-chart title in the screenshots.
- Inspect every S2 Q36–65 figure as an image; this was never done. Add a qualification to S2 Q36 for its printed typographic quotes and en-dash.
- Move generator scripts into `figures/sources/` with unique names (`CS-2024-S1-first.py`, …) and confirm the regenerated SVGs match the reviewed ones.
- Write `data/transcriptions/CS-2024-S1.json` and `CS-2024-S2.json` (all `status: "draft"`) and `audits/transcription-<paper>-draft-review.json`, following the CS-2025-S1 example.
- Commit one paper per commit: `transcribe: CS-2024-S1 (0/65 verified)`.

### 3.2 Transcribe a paper (session type B)

**Order** (newest first; ✓ = drafts already exist):
CS-2026-S2 ✓, CS-2026-S1 ✓, CS-2025-S2 ✓, CS-2025-S1 ✓, CS-2024-S2, CS-2024-S1, CS-2023, CS-2022, CS-2021-S2, CS-2021-S1, CS-2020, CS-2019, CS-2018, CS-2017-S2, CS-2017-S1, CS-2016-S2, CS-2016-S1, CS-2015-S3, CS-2015-S2, CS-2015-S1, CS-2014-S3, CS-2014-S2, CS-2014-S1, CS-2013, CS-2012, CS-2011, CS-2010, CS-2009, CS-2008, CS-2007, CS-2006 … CS-1991.

For each paper:
1. **Find each question's source.** Questions are listed in `data/questions.json` (filter by `paper_id`), and each one's page and bounding box in the original PDF are in `data/crops.json`. Render the crops with `python scripts/render_crops.py --question <id> …`; the images go to `site-assets/q/`.
2. **Write the exact text.** Copy the wording, numbers, variable names and option order exactly.
   - **Typed PDFs** (1991–2006, 2013, 2022–2026 S1): extract the text with PyMuPDF from the crop's bounding box, then correct it line by line against the crop image.
   - **Scanned PDFs** (2007–2012, 2014–2021, 2025 S2): OCR the crop image with Tesseract, then correct every line against the image. Never keep OCR text unchecked.
   - Maths goes in `$…$` or `$$…$$` (KaTeX). Code goes in fenced blocks with exact indentation. Tables are Markdown tables.
   - Keep obvious source typos and mark them `[sic]`, with a `question-error` row in `DISCREPANCIES.md`.
   - Shared "common data" stems are stored once (see `shared_context` and `docs/TRANSCRIPTIONS.md`).
3. **Redraw the figures as SVG** in `figures/<question_id>-<n>.svg`, with the generator or `.dot` source in `figures/sources/`.
   - Use `currentColor` for strokes and text so dark mode works, real `<text>` labels (at least 12 px), and a `viewBox` with no fixed width.
   - Graphs, trees and automata: Graphviz DOT, with pinned positions when the layout matters.
   - Circuits, timing diagrams and memory layouts: hand-written SVG.
   - Copy every label, weight, arrow, start/accept marker and gate exactly, and add nothing.
4. **Write `data/transcriptions/<paper>.json`** in the format in `docs/TRANSCRIPTIONS.md`, with every entry `status: "draft"`. Record what you checked in `notes`.
5. **Screenshot and self-check.** Run `python scripts/screenshot_comparisons.py <paper>`. Open every `audits/compare-shots/<paper>/*-desktop.jpg` and `*-mobile-dark.jpg` and fix anything that doesn't match the original on the left. Regenerate and repeat until it all matches.
6. **Check the solution** against the exact wording. If the old paraphrase lost a detail that changes the answer, fix the solution in `data/questions.json` and the matching `subjects/*.md`, and log it in `DISCREPANCIES.md`. Never change an official key.
7. **Run the checks:** `python scripts/fix_glued_numbers.py`, `python scripts/validate.py`, `python -m pytest -q tests`, `node tests/test_transcription_math.js`, `python scripts/update_redrawn_coverage.py`, and `python scripts/update_checklist.py` (refreshes the progress table in `docs/CHECKLIST.md`).
8. **Commit and push** to `main` as `transcribe: <paper> (0/<n> verified)`. Push `audits/transcription-<paper>-draft-review.json` too, but not the screenshots (they're gitignored).

### 3.3 Independent review (session type C, always a fresh session)

Nothing reaches the site until this step passes.

1. Run `git pull`, then `python scripts/screenshot_comparisons.py <paper>`.
2. For **every** question, open both screenshots and compare the redraw on the right with the original on the left, item by item: every word, number, symbol, sub- and superscript, option letter and order, code character, table cell, figure label, edge, arrow and marker. Also check the full source page around the crop for anything the crop missed.
3. Check that the existing solution and answer still match the exact wording.
4. **If anything is wrong:** fix it, re-screenshot and re-check. Leave that question as `draft` if it can't be made exact, for example because the source is illegible; log a `figure-missing` or `question-error` row.
5. **If everything is exactly right,** set the entry's status to verified and add:
   ```json
   "status": "verified",
   "verified_on": "<today, YYYY-MM-DD>",
   "verification": {
     "method": "independent-visual-comparison",
     "transcriber": "<name of the session/tool that wrote the draft, from git log>",
     "reviewer": "<this session, e.g. claude-code-review-2026-11-12 or codex-review-2026-11-12>",
     "solution_checked": true,
     "rendered_comparison_checked": true
   }
   ```
   Put in `notes` what you compared, and the commit whose screenshots you reviewed. Fill in these fields only for checks you actually did. `reviewer` must differ from `transcriber`, and the build rejects entries where they match.
6. Run the checks from 3.2 step 7. Commit and push as `review: <paper> (<verified>/<n> verified)`. Verified text is stored and checked by every build, but the site keeps showing the original image until `show_redrawn_text` in `data/site-settings.json` is switched to `true` (owner's decision; leave it `false`).

### 3.4 Clean-up (any time; small)
- **Scripts:** move the one-off `scripts/check_*.py` into `scripts/checks/`, fixing any paths in `audits/` that reference them.
- **Older questions:** "Recorded options (source verification pending)" shows raw text for some of them. Render it as a list, or drop it once that paper is verified.

### 3.6 Step-through animations (one family at a time)
"Step through it" sits inside "Answer & solution", closed by default, and never appears in PDFs. Each **family** (CPU scheduling, hashing, …) owns its own files, so families can be added in parallel without touching each other:

| File | What goes in it |
|---|---|
| `scripts/animations/<family>.py` | The simulator. Define `KINDS = {'<kind>': fn}`, `PLAYER = '<family>'` and, if a question can have several tabs, `TABS = '<word>'` (e.g. `'schedules'`, shown as “3 schedules”); `fn(qid, spec)` returns `{kind, schedules: [{short, title, steps: [...]}], count, ...}`. Each step needs a `note`; the last one has `final: True`. Shared helpers are in `scripts/animations/common.py` (read-only for families). Discovered automatically. |
| `data/animations/<family>.json` | `{"description": ..., "questions": {"CS-…": spec}}`. |
| `site-static/steps/<family>.js` | `window.gateStepsRegister(({el, h, css}) => ({'<kind>': (schedule, data, step, index, width) => [nodes]}))`. Loaded only when a reader opens one. Use `css(...)` for styles, `steps-table`, `steps-table-wrap`, `steps-time`, `steps-ready`, and colours `var(--s0)`–`var(--s5)`, `var(--accent)`, `var(--muted)`, `var(--line)`, `var(--panel)`. |
| `tests/test_anim_<family>.py` | Unit tests for the simulator, from worked solutions. |

Rules:
- **The simulator computes; the spec only states the question's inputs and the expected answer.** Every spec has an expectation (`expect`, and where the solution states them, intermediate facts such as fault positions or the visiting order) taken from the official key, or from our recorded answer where no key exists. On any difference the simulator raises `SystemExit`, which fails the build. Never weaken a check to make an entry pass; leave that question out instead.
- Include a question only if its text states every input. Leave it out if the input is only in a figure, the source copies disagree, the key depends on a non-standard reading, or the question is conceptual.
- Notes are plain sentences a student can follow ("Slot 6 holds 50, a collision."). No review or source wording.
- Do not edit `scripts/animations/__init__.py`, `common.py`, `site-static/steps.js`, other families' files, or `templates/`. If the core needs a change, say so instead.
- Check: `python scripts/build_site.py --release`, then `python scripts/checks/check_study_views_browser.py` (opens one question of every kind), and look at the player at 390 px wide.
- Simulations are cached in `.anim-cache/` (gitignored; CI keeps it between runs), keyed on each spec and the source of every module in `scripts/animations/`. Changing either recomputes the result. Set `GATE_ANIM_CACHE=0` to bypass the cache when timing or debugging a simulator.
- Practicalities learned so far: in a git worktree with no `node_modules`, symlink the main checkout's for `node tests/test_transcription_math.js` and remove the link before committing; serve `_site` on a free port (another session may hold 8000/8765); the global `th:first-child{min-width:180px}` and `td,th` border rules apply inside players, so cancel them in your family CSS; off-screen articles use `content-visibility`, so read text with `textContent` in scripts.

### 3.7 Step-through families still in progress (handed over 11 Nov 2026)
381 questions have step-throughs in 24 families. The six branches from the 11 November handoff have been independently reviewed and merged, and all `wip/*` branches were deleted on 13 Nov 2026 (start a new `wip/anim-<name>` branch from `main` for a new family). A second check on 11 November covered all 157 entries in parsing, subnet, window, errorcode, automata, pipeline, schedule, sorting, dp, banker and ctrace: expectations against the keys and keyed option text, the open discrepancies, and one player per family at 390 px. Nothing needed changing.

| Branch | Families | State when stopped | Left to do |
|---|---|---|---|
| ~~`wip/anim-recursion`~~ | recursion | **merged** (25 questions; independently reviewed 11 Nov) | none |
| `wip/anim-automata` | automata | **merged** (18 independently reviewed questions) | none |
| `wip/anim-networks` | subnet, window, errorcode | **merged** (40 independently reviewed questions) | none |
| `wip/anim-misc` | pipeline, schedule, sorting, dp, banker | **merged** (40 independently reviewed questions across five branches) | none |
| `wip/anim-parsing` | parsing | **merged** (31 independently reviewed questions) | none |
| `wip/anim-ctrace` | ctrace (C program traces) | **merged** (13 independently reviewed questions) | none |

"Pass the build check" means each recorded answer matches what the simulator computes. It does **not** mean the entries have been reviewed. Candidate question lists are in `handoff/anim-candidates/<branch>.json`. These are keyword matches, many of them false positives.

**Finishing a family** (prompt E), on its `wip/anim-<name>` branch:
1. `git fetch origin && git checkout wip/anim-<name> && git merge origin/main` (the new files never clash with main).
2. Complete the simulator, `data/animations/<family>.json`, `site-static/steps/<family>.js` and `tests/test_anim_<family>.py` (§3.6). Leave out anything §3.6 says to leave out; when in doubt, leave it out.
3. Run `python scripts/build_site.py --release`, `python scripts/checks/check_study_views_browser.py`, `python scripts/validate.py`, `python -m pytest -q tests` and `node tests/test_transcription_math.js`. Look at two or three of the family's players at 390×900 in Chromium (Playwright) and fix any layout problems.
4. Commit and push to the same branch. Record what you included and left out (with one-line reasons) in the commit message.

**Review checklist** (prompt F, in a session that did not write the family):
- For every entry, the expectation equals `official_answer`, or `derived_answer` when there is no official key. NAT keys may be ranges.
- For MCQ and MSQ, the expected content is exactly the text of the keyed option or options in `question_text`, not just the letter.
- The spec transcribes the question's inputs faithfully, with nothing added. Check the IDs against `DISCREPANCIES.md`; drop an entry when an open discrepancy affects the result.
- Notes are plain sentences a student can follow, with no review or source wording.
- Look at the player at 390 px wide: no sideways page scroll, labels readable, no JS errors.
- Each family module sets `TABS` if its questions can have several tabs.
- Merge with `git merge --no-ff`, run every check, push `main`, then `git push origin --delete wip/anim-<name>` and mark the row "merged" above.

### 3.5 Missing official keys (optional)
1,716 entries (1991–2010) have no official key. If an official IIT/GATE key for one of those years turns up, record it exactly as printed and log any disagreement with our answers in `DISCREPANCIES.md`.

---

## 4. Preview locally (optional)

```sh
python scripts/build_site.py --release && npx pagefind --site _site --glob 'search-docs/**/*.html' --output-subdir pagefind
python -m http.server -d _site 8000      # open http://localhost:8000
python scripts/build_pdfs.py --release   # 26 PDFs into _site/pdf (a few minutes)
```

## 5. Rules
- Work on `main` (or short branches merged by PR). Never force-push. `git pull` before you start and verify each push landed.
- Do not change repository settings (visibility, Pages, permissions).
- Keep `data/questions.json` in its compact one-line format: `json.dumps(..., ensure_ascii=False, separators=(",", ":"))`.
- Never change existing entries in `data/crops.json` and never run `scripts/locate_crops.py`; crop boundaries are already reviewed. The one exception is adding crops for a new year's questions during a new-year import (`docs/NEW_YEAR_IMPORT.md`), which a separate session must review. Never change a recorded sha256 to make a different file pass.
- Never invent question text, options, figures or official keys.
- Leave `show_redrawn_text` in `data/site-settings.json` as `false`. Redrawn text is collected for later; only the owner switches it on.
- `star_worker_url` in `data/site-settings.json` turns on the "★ Star on GitHub" links (footer and Feedback page). It is the address of a deployment of [SathiyarajS/star-button-worker](https://github.com/SathiyarajS/star-button-worker) with `SITE = "https://sathiyarajs.github.io/gate-pyq/"` and `REPO = "SathiyarajS/gate-pyq"`; leave it empty until that is deployed. If something can't be read, keep it `draft` and log it.
- Before every push, run `python scripts/validate.py`, `python -m pytest -q tests` and `node tests/test_transcription_math.js`.

## 6. Current state (11 Nov 2026)
- **13 Nov 2026 clean-up:** source PDFs are no longer stored in the repo. The rendered question images (`site-assets/q/`, 4,351 files) and each PDF's URL and sha256 are, and `python scripts/fetch_sources.py` restores the PDFs locally when needed. Internal notes moved to `docs/`. License: MIT (code) and CC BY-NC-SA 4.0 (our content). The question papers belong to their setters. History was squashed to a single commit; re-clone any older checkout.
- **Questions:** 3,406 from 46 CS papers (1991–2026), in 13 subject folders. Every question shows its original image; the answers, solutions and 470+ discrepancy notes are live. Two PDFs per subject.
- **Redraws:**
  - Drafts exist for CS-2026-S1/S2 and CS-2025-S1/S2 (260 questions), none verified.
  - CS-2024 drafts are in `handoff/2024-drafts/`.
  - About 3,016 questions have nothing yet.
- **Study aids:** `/weightage/` (marks by subject and topic, 2003 on), syllabus flags from `data/syllabus.json` (topic-level, against the official GATE 2027 CS syllabus; update that file when a new syllabus is published), and `/offline/` (service worker `templates/site/sw.js`, per-subject and per-paper offline packs). The logic is in `scripts/site_features.py`. Repeated questions are in `data/repeats.json` (only `reviewed` pairs fold; same setup and requested answer, values may change) and method-level groups in `data/problem-patterns.json`. Every accepted group needs per-member source evidence. Subject and topic pages are single newest-first lists (50 per page by default, or all). Grouped questions link to `/<subject>/similar/<group-id>/`; the “One per method” filter keeps the newest of each group. See `docs/QUESTION_GROUPS.md`.
- **Step-throughs:** 381 questions in 24 families (§3.6, §3.7). They are closed by default under "Answer & solution" and never appear in PDFs.
- **Checks:** `scripts/validate.py`, the unit tests (176) and the KaTeX check pass on `main`.
- **Background:** `docs/history/CODEX_INSTRUCTIONS.md` has the original spec and history. `docs/TRANSCRIPTIONS.md` defines the transcription format and verification rules.
- **If a browser won't run locally:** pushing transcription changes to `main` also triggers `.github/workflows/review-shots.yml`, which publishes the same screenshots to the `review-shots` branch (`git fetch origin review-shots`).
