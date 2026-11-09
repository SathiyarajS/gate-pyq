# Build a private working preview

This is a preparation checkpoint, not a finished or publicly deployed website. The question bank and its source-access guidance remain available independently of this preview.

## Local build

Use Python 3.12 and install `requirements-site.txt` in a writable virtual environment. Install the pinned local math/search packages with `npm ci --ignore-scripts` (Node.js 20 or newer), then run:

```sh
python scripts/validate.py
npm run build:enhanced-preview
python scripts/build_pdfs.py --preview --html-only
python audits/site-preview-review.py
node audits/site-preview-review-js.cjs
node audits/site-search-review.mjs
```

Start with an empty `_site` directory, or use a fresh `--output` directory and pass the same directory to `build_pdfs.py --site`. Topic changes can leave obsolete pages in a reused output directory. Generated output is ignored by Git.

The preview shows essential-question paraphrases, original source links, independent solutions, exact official-key strings where available, and discrepancies. It does not claim that the paraphrases are verbatim originals or that unresolved diagrams have been certified. Candidate topics are labelled separately from reviewed topics.

## Local print drafts

`--html-only` prepares two print HTML drafts for each subject, with and without detailed solutions. The questions-only draft includes a clearly labelled answer index. These are not finished PDFs.

For an environment that permits Chromium:

```sh
python scripts/build_pdfs.py --preview --chromium /path/to/chromium
```

In the current execution environment, Chromium fails at socket creation, including an approved elevated attempt. Browser screenshots, full interaction testing, PDF layout, tagging and bookmarks are therefore unverified. Do not report them as passed based on static checks.

## Original question pipeline

`data/crops.json` contains draft crop candidates, not approved source images. `scripts/render_crops.py` refuses drafts unless a local QA run explicitly enables them. Full-page fallbacks, overlaps, shared stems, continuation pages and parser warnings need visual inspection before approval. Runtime source paths belong in the ignored `.local-source-cache` directory, not public manifests.

Original paper availability does not establish permission to republish every paper or image. Keep source provenance and distribution permissions distinct from mathematical correctness and visual verification.

## Release boundary

Running `scripts/build_site.py` without `--preview` intentionally fails until its remaining acceptance gates are satisfied. Full topic review, exact original-question access/redraw verification, math/search integration, browser QA and finished PDFs are separate requirements. The original question-bank completeness gate also retains its historical source and key uncertainties.

No command above changes repository visibility, Pages settings, workflow permissions, or publishes the generated site. The existing source-fetch workflow is separate and can commit downloaded sources when its trigger paths change. Do not change those files merely to trigger a fetch without considering that side effect.

## Verified crop metadata

65 CS-2026-S2 source crops have independent boundary/render QA. Their generated images remain local, not published by this checkpoint. After resolving the original sources locally, `python scripts/render_crops.py --question CS-2026-S2-Q1` demonstrates the verified rendering path. Other papers remain draft; do not use the explicit draft override as approval. The preview still uses clearly labelled paraphrases until the full source-content presentation and rights gates are satisfied.
