> **Historical document.** This was the original build specification given to Codex (Nov 2026). It is kept for reference only; the current task list is [HANDOFF.md](../../HANDOFF.md).

# Instructions: GATE PYQ website, PDFs and redrawn questions

You (Codex) built the question bank on branch `work/gate-source-audit`. This file describes the next stage: publish it as a GitHub Pages website with downloadable PDFs, then redraw every question so the site no longer depends on images. Work through the phases in order. Commit after each meaningful step, and push often.

**Repo:** `SathiyarajS/gate-pyq`
**Working branch:** `site`. It is based on `work/gate-source-audit` and already contains `sources/` plus the fetch workflow. Do all work here and open a PR into `main` at the end of Phase 6.
**Site URL (after deploy):** `https://sathiyarajs.github.io/gate-pyq/`. All internal links must work under the `/gate-pyq/` base path; use relative links or a single `BASE_URL` setting.

---

## Status on 10 Nov 2026 (read this before anything else)

Phases 1–4 are done and **live at https://sathiyarajs.github.io/gate-pyq/**. Phase 5 (redraw) has started. Phase 6 is partly done. `release` was merged into **`main`** (PR #1); work on `main` from now on. `site` and `release` are frozen. **`HANDOFF.md` is the current task list.**

### What Claude added on `release`

- **Public release build.** `python scripts/build_site.py --release` builds the public site.
  - No preview banner and no `noindex` tag.
  - PDF download links on every subject page.
  - Every question whose source PDF is in `sources/` shows its original image; the rest fall back to the paraphrase and are listed on the About page.
  - The fail-closed `--preview` path is unchanged, and templates default to preview mode.
- **Year labels.** Labels now read `(GATE 2026 Set 1, Q17)`. Previously they showed the exam-shift number (`(GATE 2026 3, Q17)`).
- **Practice controls.** A–D buttons for MCQ, toggle buttons plus Check for MSQ, and a number box for NAT. The missing "1 mark" option in the marks filter was also added.
- **Image trimming.** `scripts/render_crops.py` trims the empty answer-box area below questions in 2022+ papers (about 200 images). Only blank rows at the bottom are removed; crop metadata is unchanged.
- **PDFs.** `python scripts/build_pdfs.py --release` produces:
  - a cover, a contents page by topic, and bookmarks per topic and question
  - questions that flow continuously instead of one per page
  - 150 DPI greyscale images (about 14 MB per subject PDF instead of 57 MB)
  - a footer showing the subject and page number
- **Missing spaces.** `scripts/fix_glued_numbers.py` restored the space in about 610 places such as "costs7n" → "costs 7n", in both `data/questions.json` and the markdown. It skips identifiers (`log2`, `top1`, `wants1`, `print1`, `binary32`, …) and code, and it is idempotent: if `data/questions.json` conflicts in a merge, take the other side and re-run it.
- **Deployment.** `.github/workflows/pages.yml` runs on PRs to `main` (build and checks) and on push to `main` (build and deploy). Each run:
  1. validates the data
  2. builds the site
  3. builds the Pagefind index
  4. builds the 26 PDFs

  The 2007–2018 papers are committed under `sources/archive/CS/` (byte-identical to the official CS.zip), so no run downloads them.
  6. runs the link check (`scripts/check_links.py`)
  7. deploys
- **Handoff integration.**
  - The CS-2025-S2 checkpoint from Codex's handoff is applied (65 drafts, 8 SVGs, Q12 option D corrected to e−1).
  - The unfinished CS-2024 drafts and review notes are preserved in `handoff/2024-drafts/` (see its README).
- **Tests and checks.** All 31 Python tests, the KaTeX check and `validate.py` pass.

### Still to do, in order

1. **Owner (not you):**
   - make the repo public
   - set Settings → Pages → Source to **GitHub Actions**
   - merge the PR from `release` into `main`; the merge publishes the site
2. **Check the first deploy.** Open the workflow log and confirm that the "Restore 2007-2018 papers" step printed `10 ok, 0 rejected`, and that `du` reports the site under 1 GB.
   - If the Google Drive download fails in CI, commit the 10 PDFs yourself to `sources/archive/CS/`, at the exact paths and sha256 in `audits/crop-source-map.json`.
   - Never run `locate_crops.py` to restore sources.
3. **Phase 5 redraw.** This is the main remaining work. Current state:
   - 260 drafts exist (2026 S1/S2, 2025 S1/S2), all `status: draft`
   - 130 more drafts are in `handoff/2024-drafts/`
   - about 3,016 questions have no draft yet

   For each paper, newest first:
   1. Integrate or prepare drafts: extract text for typed PDFs; OCR, then correct line by line, for scanned PDFs.
   2. Make the figures through the pinned DOT or hand-written SVG route.
   3. Generate `scripts/compare_transcription.py <paper>`.
   4. Run a separate review pass.
   5. Ask the owner to visually check that paper's comparison page.
   6. Only then set `status: "verified"` with the full `verification` metadata required by `docs/TRANSCRIPTIONS.md`.
   7. Commit with `transcribe: <paper> (<n>/<total> verified)`.

   For the 2024 papers, first apply `handoff/2024-drafts/review-fixes/`. Then regenerate CS-2024-S2 Q22 through DOT, and inspect every CS-2024-S2 Q36–65 figure as an image. Codex did not finish that check.
4. **Phase 6 leftovers:**
   - shorten README.md (a short "Website" section was added at the top; the long caveats can move to `QUALITY.md`)
   - move the one-off `scripts/check_*.py` into `scripts/checks/`, updating any references in `audits/`
5. **Known small issues:**
   - "Recorded options (source verification pending)" shows raw text for some older questions.
   - `subjects/*.md` are not regenerated from `data/questions.json`; keep both in sync when you edit either.

### Build locally

```sh
pip install -r requirements-site.txt && python -m playwright install chromium && npm ci --ignore-scripts
python scripts/build_site.py --release
npx pagefind --site _site --glob 'search-docs/**/*.html' --output-subdir pagefind
python scripts/build_pdfs.py --release           # about 20 min for all 26 PDFs
python scripts/check_links.py _site
```

---

## 0. Current state (read first)

- **Source of truth:** `data/questions.json` holds 3,406 records, one per original numbered item, across 46 papers listed in `data/papers.json`. Fields used below: `question_id`, `paper_id`, `source_question_number`, `subject`, `question_title`, `question_text` (a paraphrase, not verbatim), `question_type`, `marks`, `official_answer`, `derived_answer`, `solution`, `verification_status`, `discrepancy_ids`, `source_url`, `source_page`, `source_pages`, `source_archive_member`, `key_url`, `key_page`, `exclusion_reason`.
- **Subject counts:** Discrete Math 421, COA 329, OS 302, TOC 279, Algorithms 272, GA 270, DBMS 250, Digital Logic 241, Compiler 241, DS 217, CN 196, C 150, plus 238 records with `subject: "excluded"`. The excluded records are engineering maths, software engineering, web tech and similar topics, each with an `exclusion_reason`.
- **Discrepancies:** `DISCREPANCIES.md` has 471 table rows. Records reference 473 unique IDs, and 4 of those have no row:
  - `CS-2006-Q39-overbar-scope`
  - `CS-1993-Q19-RECOVERED-DIAGRAM-PROVENANCE`
  - `CS-2008-Q60-source-code`
  - `CS-1993-Q19-SUFFICIENT-VERSUS-IFF`

  Add rows for these 4 (or fix the references) before building.
- **`official_answer` formats:**
  - `null` (1,716 records, no official key located)
  - a letter (`B`)
  - a set (`B;C`)
  - a NAT range (`6 to 6`, `2.4 to 2.6`)

  Keep showing these exactly; never invent a key.
- **Question types are inconsistent.** Values include `MCQ`, `MSQ`, `NAT`, `descriptive`, `DESCRIPTIVE`, `fill-in`, `short-answer`, `matching`, `true-false-with-reason` and `conversion`. Normalise them for display (MCQ / MSQ / NAT / Descriptive / Other) without rewriting the stored value.
- **Source PDFs:** `sources/` contains 43 PDFs fetched by `.github/workflows/fetch-sources.yml`, listed in `sources/manifest.json` (URL → local path + sha256). The sha256 check against `source_file_sha256` reported 0 mismatches.
- **Google Drive `CS.zip` is still missing.** This is the official GATE 2026 archive, Drive file id `1popAHO-cX69oQEx_tD0wZXL1tTrBljeO`, covering the 2007–2010, 2012, 2014–2016, 2017 CS2 and 2018 papers and keys.
  - The first fetch failed because gdown 6.x no longer accepts `--fuzzy`.
  - `scripts/fetch_sources.py` is already fixed (commit `21410c8`). It now calls `gdown <id>` and falls back to `https://drive.usercontent.google.com/download?id=...&export=download&confirm=t`.
  - The re-run then failed **before starting any job** (0 jobs, no log), twice. The likely cause is the Actions minutes or billing limit for private repos; it should clear once the repo is public.
  - If you have internet access, run `python scripts/fetch_sources.py` yourself and commit `sources/`. Otherwise, re-trigger the workflow by pushing a change to `scripts/fetch_sources.py`.
  - Confirm that `sources/manifest.json` has `zip_members` populated and `sha_mismatch_count: 0`.
- **Text-based vs scanned PDFs.** This decides how Phase 5 works.
  - **Text-based** (text can be extracted): 1991–2006 (GeeksforGeeks reproductions), 2013, 2022, 2023, 2024 S1/S2, 2025 S1, 2026 S1/S2, and most answer keys.
  - **Scanned** (images only): 2011, 2017 S1, 2019, 2020, 2021 (both sessions are in one 91-page file), 2025 S2, the 2021 key, and probably every PDF in `CS.zip`. Check each one once the zip is fetched.
- `source_page` is the 1-based physical page in the source file. 562 records span several pages (`source_pages`). 2014/2015/2016 sessions share a combined PDF, and 2013 uses booklet Code A (`data/booklet-permutations`).

## 1. Settings the owner does by hand (not you)

The owner will:
1. make the repo **public**, and
2. set **Settings → Pages → Source = GitHub Actions**.

Do not try to change repo settings. If the deploy job fails because Pages is not enabled, report it and continue with the other work.

## 2. Scope decisions (already made)

- **12 subject folders, plus a 13th** called `13-other-topics`, titled "Engineering Mathematics & Other Topics". It holds the 238 `excluded` records, so nothing disappears. Show each one's `exclusion_reason` as a small note.
- **Years 1991–2026, CS papers only.** 1990 and the separate IT papers (2004–2008) stay out of scope. Say so on the About page.
- **Within each subject, group questions by topic** (see Phase 3). Inside a topic, sort newest first, then by session, then by question number.

## 3. Topics (new data, needed for grouping, filters and the chart)

Create `data/topics.json` in this shape:

```
{ "<subject-dir>": { "topics": [ {"id": "...", "title": "..."} ], "assign": { "<question_id>": "<topic id>" } } }
```

- Use the official GATE CS syllabus sub-topics for each subject: for example, Algorithms has Asymptotics & Recurrences, Searching & Sorting, Divide & Conquer, Greedy, Dynamic Programming, Graph Algorithms, Hashing and Complexity. Keep each subject to about 6–12 topics and add an "Other" topic as a catch-all.
- Assign every question to exactly one topic by reading its `question_title`, `question_text` and `solution`. Do not use keyword matching alone; review every assignment.
- The build must fail if any question is unassigned.

## 4. Phase 1: Crop the original questions (temporary display)

Goal: until a question is redrawn (Phase 5), the site shows an exact, sharp image of it from the official paper.

1. Write `scripts/locate_crops.py`. It produces `data/crops.json`:

   ```
   { "<question_id>": [ {"file": "sources/...pdf", "page": 18, "bbox": [x0, y0, x1, y1]} ... ] }
   ```

   Units are PDF points. Use one entry per page for questions that span pages.
   - **Text PDFs:** find the question-number markers (`Q.18`, `Q.18.`, `18.`, `Q.1.9`, and so on) with PyMuPDF text search. Each crop runs from one marker to the next, across the full text width. Trim the headers and footers that appear on every page.
   - **Scanned PDFs:** run OCR (`tesseract` with hOCR/TSV output) to find the markers, then do the same.
   - Where detection fails, add the bbox by hand after looking at the rendered page.
   - Validate everything: every record must have at least one crop; no two crops on the same page may overlap; and every crop must contain its question's own number.
2. Write `scripts/render_crops.py`. It renders each crop at 3× (216 DPI) into `site-assets/q/<question_id>-<n>.webp` (quality about 80), with lossless PNG as a fallback if WebP is unavailable. Do this in CI rather than committing thousands of images; keep the folder out of git.
3. Visually spot-check at least 3 questions per paper by opening the images, and fix the boxes. Keep the checker notes in `audits/crops.md`.
4. **Display rules for crop images:**
   - `width: 100%; max-width: 820px; height: auto`
   - `loading="lazy"` and explicit `width`/`height` attributes so the layout doesn't jump
   - Tapping an image opens it full size so it can be zoomed
   - The paraphrase sits underneath in a collapsed "Text version" block, which doubles as alt text and as searchable text
   - In dark mode, put the image on a white card. Never invert it.

## 5. Phase 2: Site generator

Write `scripts/build_site.py` (Python + Jinja2) that turns `data/*.json` plus `DISCREPANCIES.md` into a static site in `_site/`. Use no front-end framework; keep the JavaScript small, vanilla and progressively enhanced, so pages work without it.

### URL structure

```
/                                   Home: subject cards (question count, topic count, PDF links), global search, About
/<subject-dir>/                      Subject page 1 (Q1–10); topic list; topic-frequency chart; PDF downloads
/<subject-dir>/page/<n>/             10 questions per page, continuous numbering across the subject
/<subject-dir>/topic/<topic-id>/     Same layout, filtered to one topic (also 10 per page)
/papers/                             List of all 46 papers
/papers/<paper_id>/                  Full paper in original order (mock-test view, optional 3-hour timer)
/q/<question_id>/                    Permalink; redirects to the page and anchor where the question lives
/discrepancies/                      Every discrepancy, grouped by subject, linked to its question
/about/                              Sources, scope, verification levels, how to report errors
/pdf/<subject-dir>.pdf               With answers (see Phase 3)
/pdf/<subject-dir>-questions.pdf     Questions only
```

Pagination: 10 questions per page in topic order (Section 2). Show page numbers at the top and bottom, plus Prev and Next links.

### One question block (the core requirement)

```
Q14.  (GATE 2025 CS1 · Q18) · 1 mark · MCQ        ⚠ discrepancy   🔗 link   ⚑ report
[question: redrawn version if verified, else crop image(s)]
▸ Text version (paraphrase)                      (collapsed)
[practice controls]                              (see feature 4)
▸ Answer                                         (collapsed <details><summary>Answer</summary>)
    Official key: B
       - or "Official key: none located; answer below is independently derived"
       - for NAT, show the range exactly; for MSQ, show all options
    Our answer: B          (show only if it differs from the key or no key exists)
    Detailed solution: <solution, formatted, maths via KaTeX>
    ⚠ Discrepancy: <type, summary, official key vs our answer, status>   (one block per discrepancy ID)
    Source: official paper p.18 · answer key p.1   (links)
```

- The **year in brackets** is required on every question, on the site and in the PDFs, as `(GATE <year> <session>, Q<source number>)`. Examples: `(GATE 2025 CS1, Q18)`, `(GATE 1998, Q1.9)`. Use the printed number when `printed_question_number` exists.
- The Answer section uses a native `<details>` element and stays collapsed by default.
- The ⚠ badge shows whenever `discrepancy_ids` is not empty. It must not reveal the answer.
- The block's anchor id is `question_id`.

### The 9 extra features

1. **Topic grouping** within each subject (Section 3), with a topic sidebar or list on the subject pages.
2. **Search** across all questions with [Pagefind](https://pagefind.app). Run it as a post-build step: `npx pagefind@1 --site _site`. Index the paraphrase, the redrawn text once it exists, and the title, year and topic; do not index solutions. Add filter facets for subject, year and type.
3. **Filters** on subject pages: year range, marks (1/2), type (MCQ/MSQ/NAT/Descriptive), and "has discrepancy". Filtering loads `/<subject-dir>/index.json` and renders the matching questions client-side, 10 per page. With JavaScript disabled, the normal pages still work.
4. **Practice mode.** Above the Answer section:
   - MCQ: buttons A–D
   - MSQ: checkboxes A–D plus a Check button
   - NAT: a number input checked against the accepted range
   - Descriptive: a "Reveal" button only

   After answering, mark the attempt correct or wrong against the official key (or against our answer when no key exists, saying so) and expand the Answer section. Store attempted and bookmarked state per question in `localStorage`, wrapping every access in try/catch so pages work when storage is blocked. Show "x / y attempted" per subject, and add a "Bookmarked" filter.
5. **Full-paper view** (`/papers/<paper_id>/`): every question in its original order with original marks, plus an optional on-page timer.
6. **Two PDFs per subject:** with answers, and questions only (Phase 3).
7. **Report an issue:** each ⚑ link opens `https://github.com/SathiyarajS/gate-pyq/issues/new` with the title prefilled as `[<question_id>] ` and a body containing the permalink. Add a `.github/ISSUE_TEMPLATE/question-issue.md` template.
8. **Topic-frequency chart** on each subject page: a topics × years grid (a heat table), rendered at build time as inline SVG or HTML with no chart library. It must be readable in light and dark mode, and each cell should show its count on hover or as a title.
9. **Permalinks, dark mode, print styles:**
   - `/q/<id>/` redirects, and each question has a "copy link" button.
   - Dark mode follows `prefers-color-scheme`, with a manual toggle remembered in `localStorage`. Define colours as CSS variables.
   - Print CSS expands all answers, hides the navigation, and avoids splitting a question across pages.

### Formatting and quality

- **Solutions:** render markdown-like text (numbered steps, code, tables). Typeset maths with self-hosted KaTeX (pin a version, no CDN dependency at runtime).
- **Layout:** mobile-first. No horizontal scroll at 360 px width; large code blocks scroll inside their own box.
- **Accessibility:** use semantic headings, alt text for images, and visible focus states.
- **Build-time checks.** The build must fail if:
  - any question is missing from both the subject pages and the paper views
  - the count per subject differs from `data/questions.json`
  - a `discrepancy_id` has no row
  - a crop image is missing
  - any internal link is broken (run a link checker on `_site/`)

## 6. Phase 3: PDFs

Write `scripts/build_pdfs.py`. For each subject, build a print-only HTML page from the same templates and print it with Playwright Chromium.

- **`<subject>.pdf` (with answers):**
  - cover page with the subject, a "generated on" date, and the source and verification note
  - clickable contents by topic
  - then each question: number, year in brackets, marks and type, the question (redrawn or crop), the official key or "none located", our answer if it differs, the detailed solution, and any discrepancy notes
- **`<subject>-questions.pdf`:** the same, without answers, plus an answer index at the end (question number → official key / our answer) for self-checking.
- Use A4 with page numbers in the footer, and use `page.pdf(outline=True, tagged=True)` so the PDF has bookmarks. If the Playwright version lacks `outline`, add bookmarks afterwards with `pypdf`.
- Keep each PDF under about 40 MB by downscaling crops to about 150 DPI in the PDF build.
- Discrepancies appear in the with-answers PDF exactly as on the site.

## 7. Phase 4: Deployment

Add `.github/workflows/pages.yml`:

- **Triggers:** push to `main`, plus `workflow_dispatch`. Also run the build without deploying on pull requests and on pushes to `site`, so the build is checked before merge.
- **Steps:**
  1. checkout
  2. Python 3.12; `pip install pymupdf jinja2 playwright pypdf pillow`; `playwright install --with-deps chromium`
  3. Node 20
  4. `python scripts/validate.py`
  5. `python scripts/render_crops.py`
  6. `python scripts/build_site.py`
  7. `python scripts/build_pdfs.py`
  8. `npx pagefind@1 --site _site`
  9. link check
  10. `actions/upload-pages-artifact@v3` (path `_site`)
  11. `actions/deploy-pages@v4`
- **Permissions:** `pages: write`, `id-token: write`, `contents: read`; environment `github-pages`.
- Never commit `_site/`, rendered images or PDFs; add them to `.gitignore`.
- Upload `_site` as a normal workflow artifact on non-main runs too, so the owner can preview it.

## 8. Phase 5: Redraw every question (replaces crops)

Goal: each question is shown as real text and vector drawings, so it is sharp at any zoom, reflows on phones, is searchable and works in dark mode. Crops stay available behind a "View original" toggle.

### Storage

- Store one file per paper: `data/transcriptions/<paper_id>.json`, mapping `question_id` to:
  ```
  { "stem": "<markdown + $LaTeX$>",
    "options": {"A": "...", ...},
    "figures": ["figures/<question_id>-1.svg"],
    "status": "draft|verified",
    "checked_pages": [18],
    "notes": "" }
  ```
- Figure sources live next to their SVGs (`figures/*.dot`, `figures/*.tex` or hand-written SVG). Always commit both the source and the rendered SVG.
- Shared context (the "common data" stems used by linked questions; see `shared_context`) is stored once and referenced.

### Transcription rules

- **Verbatim.** Use the exact wording, punctuation, variable names, numbers and option order of the source. Do not fix the source's grammar.
  - Obvious typos stay in, marked `[sic]`, with a discrepancy row of type `question-error`.
  - For text-based PDFs, start from the extracted text, then correct it line by line against the rendered page.
  - For scanned PDFs, start from OCR (tesseract), then correct it line by line. OCR output is never accepted unchecked.
- **Maths:** use LaTeX inline (`$...$`) or display (`$$...$$`).
- **Code:** use fenced blocks with a language. Preserve indentation and line breaks exactly.
- **Tables:** use markdown tables, or HTML tables for merged cells.
- **Figures:** redraw as SVG.
  - Use `currentColor` for strokes and text, so drawings work in dark mode.
  - Text inside an SVG must be real `<text>`, with a minimum font size of 12 px at 100% width.
  - Use `viewBox` with no fixed width, so drawings scale.
  - Graphs, trees and automata: use Graphviz DOT, with node positions pinned (`pos`, `neato -n`) when the original layout matters, for example crossing edges or a stated geometry.
  - Circuits: use hand-written SVG or CircuiTikZ compiled to SVG.
  - Timing diagrams, Gantt charts and memory layouts: use hand-written SVG.
  - Copy every label, weight, arrow direction, initial or accepting marker, and gate type exactly. Add nothing that isn't in the original.
- If any part is unreadable, keep the crop for that question, set `status: "draft"`, and add a `figure-missing` discrepancy row.

### Verification (required before `status: "verified"`)

1. `scripts/compare_transcription.py <paper_id>` renders each redrawn question next to its crop in `audits/compare/<paper_id>.html`.
2. Make a second, separate pass over every question. Check each number, symbol, option, label and edge against the crop. Record `verified_on` and what was checked in `notes`.
3. Confirm that the question's existing solution still matches the verbatim wording. If the paraphrase lost a detail that changes the answer, fix the solution and log the change in `DISCREPANCIES.md`.

### Display rule

The site shows the redrawn version when `status == "verified"`, otherwise the crop. Both the site and the PDFs pick this up automatically on the next build.

### Order and cadence

- Go newest paper first: 2026 S2 → 1991. Do text-based papers before scanned ones within the same era if that is faster.
- Use one paper per commit, with the message `transcribe: <paper_id> (<n>/<total> verified)`.
- Keep `COVERAGE.md` updated with a "Redrawn" column, and show a "x% redrawn" figure on the About page.

## 9. Phase 6: Merge and clean up

1. Open a PR from `site` into `main`.
   - **Title:** "GitHub Pages site, PDFs and question crops"
   - **Description:** what was built, the preview artifact link, and the known limitations
2. After the merge, confirm that the Pages deploy succeeded and that the site loads at `https://sathiyarajs.github.io/gate-pyq/`.
3. **README:** rewrite it to be short. Cover what the site is, the link, how to report errors, and how to build locally. Move the long caveat paragraphs to `/about/` and `QUALITY.md`.
4. **`scripts/`:** move the 30+ one-off `check_*.py` scripts to `scripts/checks/` and add a one-line README there.
5. Continue Phase 5 on `main` (or on short-lived branches merged per batch of papers).

## 10. Acceptance checklist (run before saying a phase is done)

- [ ] `python scripts/validate.py` passes.
- [ ] The site's per-subject counts sum to 3,406, and each matches `data/questions.json`; every `question_id` appears exactly once across the subject pages and exactly once in its paper view.
- [ ] Every question shows its year in brackets, its marks and type, and a working collapsed Answer section with the official key (or the "none located" note) and the detailed solution.
- [ ] All 481 questions that have discrepancies show the ⚠ badge and their discrepancy text, on the site and in the with-answers PDF.
- [ ] Each of the 13 subjects has 2 PDFs that open and have bookmarks, with question counts matching the site.
- [ ] Every crop image exists. Spot-check notes cover at least 3 questions per paper.
- [ ] No broken internal links; search returns results; filters, practice mode, bookmarks, dark mode and the permalink redirects all work.
- [ ] Screenshots at 360 px and 1280 px wide, in light and dark mode, of: the home page, a subject page, an expanded answer and a paper view. Save them in `audits/screenshots/` and check them.
- [ ] Before marking a Phase 5 paper verified, its comparison page has been reviewed for every question.
