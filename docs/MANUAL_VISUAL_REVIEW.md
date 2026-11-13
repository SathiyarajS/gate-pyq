# Private manual visual review

Use a local checkout and your own browser. Nothing here publishes a site, changes repository visibility, enables Pages, or certifies a transcription. Keep downloaded originals and generated previews private. Commands below use macOS/Linux shell syntax and run from the repository root.

## 1. Get the latest review files

For a new checkout (requires your existing access to the repository):

```sh
git clone --branch site --single-branch https://github.com/SathiyarajS/gate-pyq.git
cd gate-pyq
```

For an existing clean checkout, inspect `git status` first, preserve your own edits, then:

```sh
git switch site
git pull --ff-only
```

Record `git rev-parse HEAD` with your feedback. Ensure `data/transcriptions/CS-2026-S2.json` and `scripts/compare_transcription.py` exist. If the latest review changes have not reached `site`, wait for the confirmed push rather than reviewing an older snapshot.

Use Python 3.12 and Node.js 20 or newer:

```sh
python3.12 -m venv .local-source-cache/review-venv
. .local-source-cache/review-venv/bin/activate
python -m pip install -r requirements-site.txt
npm ci --ignore-scripts
python scripts/validate.py
```

The Python dependencies include Jinja2/MarkupSafe, PyMuPDF and Pillow; the npm lockfile supplies local KaTeX and Pagefind. Dependency installation needs internet access. Subsequent math rendering uses local assets.

## 2. Start with just 2026 S2 (recommended)

All 65 entries are source-reviewed **draft transcriptions**, not verified redraws. The comparison page renders drafts deliberately; the ordinary site and its PDF build do not promote them. Crop-boundary review of all 3,406 records is a separate completed check, not proof that transcription, browser layout or PDFs passed.

A fresh clone may not include the original PDFs, even when manifest metadata is present. For this paper you need only one original:

- Source: https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf
- Expected SHA-256: `5016950bc4e5c96676fb526e3247bab243a3dde422b6cb40a8531cc9b45f36ff`
- Save it locally as `sources/web/gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf` (create the parent directories if needed).

Download through your browser from the source link if the file is absent. Do not substitute a similarly named paper or update expected hashes to make a different download pass. Public availability is not a redistribution licence.

Check the file, render exactly the 65 reviewed original crops, and create the comparison:

```sh
python - <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
p = Path('sources/web/gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf')
expected = '5016950bc4e5c96676fb526e3247bab243a3dde422b6cb40a8531cc9b45f36ff'
if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
    raise SystemExit('Missing or changed original PDF: stop and report this.')
questions = [q['question_id'] for q in json.loads(Path('data/questions.json').read_text())
             if q['paper_id'] == 'CS-2026-S2']
if len(questions) != 65:
    raise SystemExit('Expected 65 questions; confirm checkout version.')
subprocess.run([sys.executable, 'scripts/render_crops.py',
                *[a for q in questions for a in ('--question', q)]], check=True)
subprocess.run([sys.executable, 'scripts/compare_transcription.py', 'CS-2026-S2'], check=True)
PY
```

This does not require `--allow-draft`: the original crop bounds are reviewed, although the transcriptions remain drafts. The renderer independently rechecks source hashes. If it says `missing or changed source`, stop and check the file rather than regenerating crop metadata.

In a separate terminal at the repository root, start a loopback-only server:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory .
```

Open **http://127.0.0.1:8000/audits/compare/CS-2026-S2.html** on the same computer. This address works only while your local server is running. Do not bind to `0.0.0.0`, use a tunnel, or upload this directory. Serving the repository root also makes its other files available to local processes, so stop the server with Ctrl+C when finished.

Review Q1 through Q65, not just spot samples. At 1280 px the crop and transcription are side by side; at 360 px they stack. Click a crop to inspect it full size. Also open the original PDF and check the indicated physical pages to detect omitted context outside a crop. If the page says no rendered crop is available, no transcription exists, or KaTeX is unavailable, that part of review is blocked, not passed.

## 3. Site layout and answers

Use a fresh `_site` output. If it already exists, rename it to a backup outside the repository instead of mixing builds. With the virtual environment active:

```sh
python scripts/build_site.py --preview --output _site
npm run index:search
python scripts/build_pdfs.py --preview --site _site --html-only
```

Open **http://127.0.0.1:8000/_site/** and **http://127.0.0.1:8000/_site/papers/CS-2026-S2/** using the same local server. This minimal site build uses labelled paraphrases where no accepted transcription exists. It does **not** provide the 65 draft redraws as normal site questions; review those on the comparison page.

To add original crops to the full site, all required source PDFs must be available, not just CS2.pdf. Once restored and hash-checked as below, use a fresh output:

```sh
python scripts/build_site.py --preview --with-reviewed-crops --output _site-crop-preview
./node_modules/.bin/pagefind --site _site-crop-preview --glob 'search-docs/**/*.html' --output-subdir pagefind
python scripts/build_pdfs.py --preview --site _site-crop-preview --html-only
```

Then open **http://127.0.0.1:8000/_site-crop-preview/**. `--with-reviewed-crops` regenerates the whole crop collection; it is not a one-paper option. Do not select this route with only one restored source.

### Restore other sources only if needed

`audits/crop-source-map.json` lists logical source filenames, download URLs, expected hashes and archive-member names. Restore PDFs at those logical paths, or create an ignored `.local-source-cache/source-paths.json` mapping each logical filename to an absolute path on **your** computer. Example shape:

```json
{"sources/example.pdf": "/absolute/path/on/your/computer/example.pdf"}
```

Use actual filenames from the map, not the example. For archive-backed papers, extract the exact listed member from the stated archive. An archive itself is not the required member PDF. Paths from another computer will not work.

This read-only check reports all missing or mismatched inputs without changing audit data:

```sh
python - <<'PY'
import hashlib, json
from pathlib import Path
sources = json.loads(Path('audits/crop-source-map.json').read_text())['sources']
cache = Path('.local-source-cache/source-paths.json')
paths = json.loads(cache.read_text()) if cache.is_file() else {}
bad = []
for logical, info in sources.items():
    p = Path(logical)
    if not p.is_file():
        p = Path(paths.get(logical) or '/missing-source')
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != info['sha256']:
        bad.append(logical)
for name in bad:
    print('MISSING OR CHANGED:', name)
print(f'{len(sources) - len(bad)}/{len(sources)} sources match expected hashes')
raise SystemExit(bool(bad))
PY
```

Do not run `locate_crops.py` to restore sources: it regenerates crop/audit metadata and would replace reviewed bounds. `fetch_sources.py` is a bulk downloader that rewrites the source manifest, not a read-only restore/check helper. Neither is needed for the one-paper review above.

## 4. Review checklist

Use browser responsive tools at **360 px** and **1280 px**, each in **light** and **dark** mode. The site has a theme toggle. The comparison page has no theme button: use browser/OS colour-scheme emulation (and clear this origin's saved theme if it overrides the emulation).

- **Every draft question:** exact wording, punctuation, variables, constants, signs, subscripts, superscripts, fractions, quantifiers and all option text/order. Check shared context and multi-part continuation against the full source pages.
- **Math:** typeset output appears, not raw `$...$` or missing glyphs; no clipped expressions. Check both themes and widths.
- **Figures:** every label, edge, arrow direction, weight, initial/accepting marker and geometric relation agrees with the original. SVG text is readable at normal width and zoom; no dark-mode invisible strokes. Do not accept a visually plausible redraw without source comparison.
- **Layout:** no whole-page horizontal overflow at 360 px; long code/math/table content is usable inside its own box; no cut-off options or overlapping text. Original crops stay white and are never colour-inverted.
- **Site pages:** home, subject page, expanded answer and full paper view in all four width/theme combinations. Check keyboard focus, pagination, filters, search, bookmarks and permalink redirects.
- **Original access:** confirm original crops and their full-size links in the crop-enabled build. A `View original` toggle is applicable to accepted redraws; with zero accepted transcriptions, do not mark that redraw/toggle path passed merely because crops render. Record it as not yet exercised.
- **Answers:** collapsed initially, exact official-key string preserved (including MSQ sets and NAT ranges), missing-key wording present when applicable, discrepancies visible without leaking answers early. Confirm the existing solution still answers the exact original wording. Report any altered interpretation.

Save screenshots for failures and representative layout checks. Include the URL, question ID, width, theme and browser version. Screenshots alone do not constitute complete transcription verification.

## 5. Print drafts and PDFs

The `--html-only` command creates **26 print HTML drafts**, not PDFs. Browse `_site/pdf/` (or `_site-crop-preview/pdf/`) and inspect both variants per subject. The questions-only variant intentionally has a self-check answer index at the end.

For actual PDFs, only on your own computer where Chromium is permitted:

```sh
python -m playwright install chromium
CHROMIUM="$(python -c 'from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()')"
python scripts/build_pdfs.py --preview --site _site --chromium "$CHROMIUM"
```

Replace `_site` with `_site-crop-preview` for crop-enabled PDFs. Linux may also need Playwright's documented system dependencies; resolve those locally if the browser reports missing libraries. Do not bypass a browser/security denial. The current PDF script launches headless Chromium with `--no-sandbox`, so run it only for this trusted local checkout and local generated content.

Open the actual generated `.pdf` files in a PDF viewer. Check all 13 subjects × two variants: readable math/figures, no clipped or missing content, A4 pagination/footer, question counts/year labels, answers versus questions-only separation, answer index, discrepancies, bookmarks, clickable navigation where intended, and accessibility/tagging. Record missing bookmarks/navigation as defects rather than assuming the generator supplies them. PDFs remain drafts until inspected; generation success alone is not acceptance. The PDF build consumes normal site content, not the draft comparison page.

## 6. Send findings

Copy this form for each issue or explicitly reviewed range:

```text
Checkout commit:
Paper / question ID(s):
Page: comparison / site / print HTML / actual PDF
URL or filename and physical source page:
Browser or PDF viewer + version:
Width and theme:
Result: pass for stated checks / issue / blocked / not exercised
Expected from source:
Observed:
Checks completed (wording, math, options, figure, solution, layout):
Screenshot attachment(s):
```

A useful batch reply is “CS-2026-S2 Q1–Q10 checked against full source pages; Q7 has [specific issue]; remaining questions not reviewed.” Do not change every entry to `verified` after a spot check. Promotion requires the separate per-question review, a date and specific checks recorded, and confirmation that the solution matches the original. No public deployment follows from this manual review.
