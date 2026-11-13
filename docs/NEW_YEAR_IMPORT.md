# Add a new GATE CS year

One Codex (or Claude Code) run takes a new year from the official PDFs to the live site: it finds the papers, cuts the question images, writes the solutions and step-throughs, has them independently reviewed, and merges the result into `main`. Start it with prompt G in `HANDOFF.md`; that is the only thing the user does.

**The repository never stores source PDFs.** They are local, git-ignored working files under `sources/`. What gets committed is the data, the crop boxes, the rendered question images in `site-assets/q/`, and each PDF's URL and sha256 (so `python scripts/fetch_sources.py` can restore and verify it later). `scripts/validate.py` fails if a reviewed question has no committed image.

**The run is unattended. Never stop to ask the user anything.** Make every decision from this document and the repository's rules. Where something can't be resolved (an unreadable figure, a key you disagree with), record it in `DISCREPANCIES.md` or the review audit, leave that one item out or flagged as the steps below say, and carry on with the rest.

## What the run does

Work on the branch `import/gate-cs-<year>`. Nothing reaches the site until step 7 merges that branch into `main`.

### 1. Stage the papers

1. `git pull`. If `origin/import/gate-cs-<year>` already exists, check it out and continue from where it stopped.
2. The year is the one after the latest year in `data/papers.json`. Find its official CS question paper and **final** answer key for every set on the organizing institute's GATE site (usually `gate<year>.<institute>.ac.in`, under downloads or previous papers), unless the prompt gives the links. If the papers or the final keys are not published yet, stop without changing anything and say so in one line. Then:
   ```sh
   git switch -c import/gate-cs-<year>
   python scripts/prepare_year_import.py <year> --sessions '[{"set":1,"paper_url":"https://…","key_url":"https://…"},…]'
   ```
   Use set 1 for a single paper. This saves both PDFs as local working files under `sources/web/<host>/<path>` (git-ignored, never committed) and writes `data/imports/<year>/papers.json` and `questions.json` with the checksums, pages, sessions, question types, marks and key answers. It stops on unexpected numbering, a missing key row or an unsupported key format. If that happens because the institute changed its format, extend the script for the new format, add a test for it using the new PDFs, and re-run. Never type or edit the staged numbers, marks or keys by hand.
3. If this machine can't reach the institute's site, run the **Prepare a new GATE CS year** workflow instead (`gh workflow run import-gate-year.yml -f year=<year> -f sessions='<same JSON>'`). It pushes the same branch using the repository's own token (records only, no PDFs); then `git fetch origin import/gate-cs-<year>`, check it out, and run `python scripts/fetch_sources.py <year>` to download the PDFs it recorded, checked against their sha256.
4. Open each PDF and confirm it is the official paper and the final key for that set, that every question is present, and that numbering, marks, types and key answers match the printed paper. Record anything unresolved in `DISCREPANCIES.md`.

### 2. Register the sources and papers

- Add each paper and key PDF to `audits/crop-source-map.json`, keyed by its path, with its `url` and `sha256` from the staged records, in the same form as the 2026 entries.
- Add each paper to `data/papers.json` in the repository's format, using the 2026 papers as the model and the staged inventory as the data. Never change a recorded sha256 to make a file pass.

### 3. Cut the question images (`data/crops.json`)

New-year crops are the one case where `data/crops.json` may be edited. Only add entries for this year's questions; never change existing entries, and never run `scripts/locate_crops.py`.

For each question add a list of crops `{"file", "page", "bbox", "status": "draft", "method": "text_layer_bounds", "flags": []}`:
- `bbox` is `[x0, y0, x1, y1]` in PDF points. Start from the line with the question's own `Q.<n>` and end before the next question's `Q.<n+1>`, using the PDF's text positions (PyMuPDF). Widen it to include all options, tables, code and figures (`page.get_drawings()`, `page.get_images()`), but no page header, footer or part of a neighbouring question.
- A question that continues onto the next page gets a second crop for that page, in order.

Then check every crop:
```sh
python scripts/render_crops.py --allow-draft --question <id> [--question <id> …] --output /tmp/crops-<year>
python scripts/check_crop_text_coverage.py --paper <paper_id> --source <paper pdf>
```
Look at every rendered image next to its source page and fix any crop that cuts off text, an option or part of a figure, or includes anything else. The coverage script only finds text left outside all crops; it does not approve a crop.

### 4. Write the questions and solutions

Move the staged rows into `data/questions.json` (compact one-line format, see HANDOFF §5) using the 2026 records as the model:
- Classify each question by subject and topic (`data/topics.json`). Questions outside the 12 subjects use subject `excluded` with an `exclusion_reason`.
- Write a self-contained paraphrase in `question_text` with every given and option needed to answer it. Never invent text, options, figures or keys.
- Solve it from the paper before looking at the key, then compare. Keep the official key unchanged. If the official key and your answer differ, record both and add a row to `DISCREPANCIES.md`.
- Add the same questions and solutions to `subjects/<subject>/<year>.md`, following the 2026 files.

The site shows each question as its original image, so a new year needs no redrawn text (`data/transcriptions/`). Don't add any during the import, and leave `show_redrawn_text` in `data/site-settings.json` switched off.

### 5. Add step-throughs

Follow HANDOFF §3.6. For each question whose inputs are all stated in the question and whose answer an existing kind can compute, add an entry to `data/animations/<kind>.json`. Add a new kind only for a type of question that recurs and that no kind covers, with its simulator, player and tests. The build re-runs every step-through and fails if one disagrees with the key. Check a few players at 390×900 in Chromium.

### 6. Independent review (a separate session)

The session that wrote the crops, solutions and step-throughs must not approve them. Start a fresh reviewer from the shell, so this stays one run for the user but the review has none of the writer's context:

```sh
codex exec --full-auto "$(cat <<'EOF'
Read AGENTS.md, HANDOFF.md and docs/NEW_YEAR_IMPORT.md. You are the independent reviewer for the GATE CS <year> import on the current branch; you did not write it. Do step 6 ("Reviewer's checklist") of docs/NEW_YEAR_IMPORT.md for every <year> question, then commit on this branch. Do not merge.
EOF
)"
```
(With Claude Code, use `claude -p "…" --dangerously-skip-permissions` in the same way.) Wait for it to finish, then continue with step 7 using its commits.

**Reviewer's checklist**
1. **Crops.** Render every crop for the year and compare each image with its full source page: the whole question, all options, every table cell and figure, and nothing from neighbouring questions or the page furniture. Fix bounds where needed. For each correct crop set `"status": "verified"`, `"review_status": "independent_source_bounds_review_passed"` and `"review_audit": "audits/crops-<paper_id>.json"`, and write that audit file in the format of `audits/crops-CS-2026-S1.json`. If a crop cannot be made exact, remove that question's crop entry (the question then shows its text and source link) and say so in the audit's `limitations`. The site shows only verified crops, so no draft may remain: each one ends up verified or removed. Then render the verified crops into the committed image folder and commit it:
   ```sh
   python scripts/render_crops.py --paper <paper_id> [--paper <paper_id> …]   # e.g. --paper CS-2027-S1 --paper CS-2027-S2
   git add site-assets/q data/crops.json audits/
   ```
   This writes `site-assets/q/<id>-<n>.webp` and updates `site-assets/q/manifest.json` (with each crop's fingerprint).
2. **Solutions.** Re-solve each question from the source page, check the paraphrase keeps every given and option, and compare with the official key. Fix errors. Fill in the review fields the 2026 records carry (`verification_status`, `independent_review`, …) only for checks actually done.
3. **Step-throughs.** Check that each animation's inputs match the question exactly and that its result is the keyed answer.

### 7. Finish and merge

```sh
git rm -r data/imports/<year>
git status --short sources/   # must show nothing: PDFs are never committed
python scripts/update_checklist.py
python scripts/validate.py && python -m pytest -q tests && node tests/test_transcription_math.js
python scripts/build_site.py --release
```
Confirm in the built site that the new year appears on the home page, the papers list, its paper pages, the subject year filters and the topic heatmap, with its question images (`validate.py` has already checked that every reviewed question's image is committed). Then merge and push (never force-push):

```sh
git push origin import/gate-cs-<year>
git switch main && git pull && git merge --no-ff import/gate-cs-<year> && git push origin main
```

The push to `main` deploys the site. Finish with a short summary: questions per set, any excluded or discrepant questions, crops removed in review, and how many questions got step-throughs.

## The import script and workflow

`scripts/prepare_year_import.py` supports the modern digital papers: continuous numbering with General Aptitude first, and a key whose table has selectable text. It accepts only HTTPS links on `.ac.in` hosts, refuses papers already in the repository, and requires the year to be the one after the latest in `data/papers.json`.

The **Prepare a new GATE CS year** workflow (`.github/workflows/import-gate-year.yml`) runs the same script on GitHub and pushes the branch `import/gate-cs-<year>`. It uses only the built-in repository token: it opens no pull request, so no secret or extra repository setting is needed.
