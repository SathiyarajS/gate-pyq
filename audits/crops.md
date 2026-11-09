# Crop preparation audit (private local work)

Status: **draft preparation only; Phase 1 is not complete.** No publication,
source-rights conclusion, original-fidelity claim, or transcription certification.

## Coverage

- page_fallback: 2396
- candidate_questions: 3406
- text_marker_candidate: 1083
- overlap_pairs: 8422
- verified_questions: 0
- pending_visual_review_questions: 3406
- Source PDFs resolved: 40 / 40, serving 46 papers.
- Previously recorded SHA-256 matches: 35 sources (question record or committed manifest).
- Locally recorded ZIP-member SHA-256 only: 5 sources; no independent expected hash is available.
- Record versus committed manifest SHA conflicts found: 0.
- Source PDFs with captured MuPDF parser warnings: 20. Warnings include missing XObject resources in legacy reproductions. Opening a PDF does not establish that its figures survived.
- Three sample questions visually inspected in one paper; the 3-per-paper target remains incomplete for 45 papers (135 additional minimum sample checks), and all 3,406 require full crop approval.

See `crop-source-map.json` for URLs, archive members, SHA-256, portable paths, page/text counts and parser warnings; `crop-summary.json` for per-paper counts. Workstation paths are kept separately in ignored `.local-source-cache/source-paths.json` and must be regenerated on another machine. The renderer prefers normal repository source paths, with `--source-cache` as an optional local override. No PDF was added to publication assets.

## Sample visual QA

Opened rendered 216-DPI WebP images, 2026-11-09:

- CS-2026-S2-Q1: initial marker incorrectly selected the “Q.1 – Q.5 Carry ONE mark Each” heading and cut off the question. Updated detection to reject question-range/marks headings. Re-rendered and opened the replacement: the actual Q.1 stem and options A–D are visible. Excess blank area and footer remain and must be trimmed during final QA. Still draft.
- CS-2026-S2-Q31: own number, the two equations, and the NAT prompt are legible. Still draft; the sample is not an independent full-source certification.
- CS-2026-S2-Q61: own number, function body, prompt and syntax-error note are legible. Still draft; no transcription or solution re-verification performed.

## Commands and safeguards

```
python scripts/locate_crops.py
python scripts/locate_crops.py --ocr  # optional, slower Tesseract pass
python scripts/render_crops.py --allow-draft --question CS-2026-S2-Q1
python scripts/compare_transcription.py CS-2026-S2
```

The locator hashes local PDFs and resolves exact URL/archive references. Referenced ZIP members are extracted only to a temporary local cache. Existing verified crops cause it to refuse replacement. Text and optional OCR markers create proposals, not approvals. Unmatched pages, shared contexts and continuation pages retain full-page draft bounds to avoid silently discarding a stem or figure. Header/footer trimming and ambiguous subparts remain manual work. Overlaps are reported, not clipped: linked items and common stems may legitimately overlap. Do not blindly enforce a non-overlap rule that removes shared information.

The renderer rechecks source hashes, preflights page/bbox validity and refuses draft crops by default. `--allow-draft` is for explicit private QA only. It produces WebP with PNG fallback and a dimension/status manifest. It tolerates only 0.02 PDF point rounding at page edges. Comparison HTML escapes transcription markup and displays the stored text literally; it is a review scaffold, not a finished KaTeX/SVG redrawing renderer.

## Tests actually performed

- All three Python scripts compile.
- Locator completed across all 3,406 records with all referenced physical pages resolved.
- Three chosen draft images rendered successfully at 3× and were opened visually.
- Default renderer rejected draft Q1 with a nonzero exit code.
- Comparison page generated for CS-2026-S2, reporting absent transcriptions rather than inventing them.
- OCR support is implemented but has not been run over the corpus. PNG fallback was not forced.

## Pending acceptance work

Review all proposed boxes against full original pages, run/check OCR or hand-box scans, resolve marker/number omissions, trim headers/footers, audit missing figures and multipart/common-stem context, and record explicit approval only after review. Render all approved crops and finish minimum sample checks for every paper. Transcription comparison and independent verification remain future work. Do not use draft crops for a claim of complete originals.
