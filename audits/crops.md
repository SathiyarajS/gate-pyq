# Crop preparation audit (private local work)

Status: **130 crops independently reviewed; Phase 1 is not complete.** No publication,
source-rights conclusion, original-fidelity claim, or transcription certification.

## Current coverage

- 130 questions across CS-2026-S1 and CS-2026-S2 independently crop-reviewed; 3,276 remain pending.
- 130 manually bounded crops, 953 marker candidates and 2,396 full-page candidates.
- 8,390 overlap pairs remain in the draft corpus; the 130 reviewed crops have zero overlaps.
- 40 source PDFs resolved for 46 papers; 35 match previously recorded hashes and 5 ZIP-member hashes are locally recorded only.
- 20 source PDFs have parser warnings. Parse success does not establish intact figures.
- CS-2026-S2: all 42 original pages and all 65 proposed boundaries independently visually inspected. Every final 216-DPI WebP independently regenerated and matched byte-for-byte; actual outputs Q1–Q4 additionally visually sampled. See the paper and render-check audits for exact scope.
- Other 44 papers require source/crop visual QA. No full transcription certification or public redistribution clearance is implied.

See `crop-source-map.json` for URLs, archive members, SHA-256, portable paths, page/text counts and parser warnings; `crop-summary.json` for per-paper counts. Workstation paths are kept separately in ignored `.local-source-cache/source-paths.json` and must be regenerated on another machine. The renderer prefers normal repository source paths, with `--source-cache` as an optional local override. No PDF was added to publication assets.

## Historical initial sample QA (superseded for CS-2026-S2)

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

The locator hashes local PDFs and resolves exact URL/archive references. Referenced ZIP members are extracted only to a temporary local cache. Existing verified or manually reviewed draft crops cause it to refuse replacement. Text and optional OCR markers create proposals, not approvals. Unmatched pages, shared contexts and continuation pages retain full-page draft bounds to avoid silently discarding a stem or figure. Header/footer trimming and ambiguous subparts remain manual work. Overlaps are reported, not clipped: linked items and common stems may legitimately overlap. Do not blindly enforce a non-overlap rule that removes shared information.

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

## Complete first pass: CS-2026-S2

All 65 crops refined to official table boundaries and visually inspected across all 42 source pages, then checked again as actual rendered WebP images in 17 contact sheets. Headers, footers and adjacent questions are excluded. No continuations or shared-data blocks were observed; all 65 fit their recorded single physical page. Zero overlap pairs remain in this paper. Some source-table whitespace is intentionally retained.

Each remains `status: draft`, with `review_status: independent_visual_review_pending`. No item was marked verified. `crops-CS-2026-S2.json` records exact PDF boxes, source pixels, image dimensions and SHA-256 evidence. This supersedes the three-sample-only CS2 milestone above. Independent review remains pending for all 65; 3,341 other questions still need their first complete crop pass. The generic pipeline is unchanged.

Latest method counts: {"page_fallback": 2396, "text_marker_candidate": 1018, "manual_table_boundary_review": 65}. Global remaining overlap pairs: 8404.

## CS-2026-S1 review

All 46 source pages and 65 bounds checked by author and a separate reviewer. Initial table detection cut Q32 and Q58 before their complete formulas/prompts; both were extended and independently rechecked on regenerated source renders. Actual corrected Q32/Q58 outputs also visually checked. No other corrections. Crop boundaries only, not transcription, answers, final-key status or distribution rights. See crops-CS-2026-S1.json.
