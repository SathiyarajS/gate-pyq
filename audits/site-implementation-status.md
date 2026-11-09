# Private site implementation status

This working implementation follows `CODEX_INSTRUCTIONS.md` while retaining the latest source-access audit. It is not a public deployment or a claim of complete original-question fidelity.

## Integration base

- Existing `site` additions: source-fetch workflow, script, source manifest, and implementation instructions at f1e7f858c3dc736d76dac1139f8b05b399a660d8.
- Latest question-bank/access base: 59a17ab318a917b1d81c95f8267a1353047c53d9 on `work/gate-source-audit`.
- Source binaries already on `site` must be preserved during additive publication. Local source caches and generated outputs are not automatically publication inputs.

## Safety and fidelity boundaries

- No repository visibility change, public deployment, Pages settings change, new credential, or workflow-permission expansion is part of this checkpoint.
- Source access does not establish a bulk republication license. Cropping and redrawing work is local/draft until provenance, fidelity and applicable distribution permissions are resolved.
- A preview may show clearly labelled essential-question paraphrases with original source links. This does not satisfy the final crop/verbatim acceptance gate.
- Historical question types, more than four options, shared stems, nested subparts, official marks-to-all and alternative accepted ranges must be preserved. A conditional independent answer is not an unconditional practice grading key.
- Candidate topic assignments and automatically detected crop boxes must not be labelled independently reviewed without actual review.
- Original-paper completeness, final-key revision uncertainties and known source defects remain visible.

## Completed preparation

- Latest access metadata retained without changing question answers.
- Added structured discrepancy rows for the recovered 1993 diagram and sufficient-condition ambiguity, 2006 complement-bar scope, and 2008 pointer assignment defect. Existing explanatory narrative remains.
- Structural question-bank validation passes for 46 paper variants and 3,406 entries.

## Pending acceptance

Private preview implementation, topic review, source/crop QA, PDF generation, responsive/accessibility testing, complete original transcription and independent visual verification remain distinct gates. Public deployment is not authorized by this status file.

## Private preparation checkpoint (not a finished phase)

- Local preview build: 3,406 entries, 46 paper views, 13 subject groups. Source questions/answers are semantically identical to the published access checkpoint.
- Topic coverage complete; checkpoint review status is 348 individually reviewed and 3,058 candidates. Full topic review remains underway.
- All 40 unique source PDFs resolve locally. Crop manifest contains 3,479 draft page entries for all 3,406 questions; 1,083 marker proposals and 2,396 full-page fallbacks, with 8,422 overlap pairs flagged. Zero crops are certified. Shared contexts require deliberate exceptions to naive non-overlap rules.
- Added a local print exporter and generated 26 print-HTML drafts, clearly labelled paraphrase previews. PDF files are not claimed.
- Chromium cannot launch because the runtime rejects socket creation, including one approved elevated attempt. Interactive browser QA, responsive screenshots and Chromium PDF rendering are blocked in this environment. Static HTML/JavaScript checks do not substitute for them.
- No source PDFs, generated crops, generated site, screenshots, or print exports are added by this checkpoint. Existing source binaries on the remote site branch are preserved unchanged.
- No deployment workflow or permission expansion was added. The existing Claude source-fetch script/workflow is unchanged, so this checkpoint does not intentionally trigger it.

For a reproducible clean preview, use a new empty output directory with `python scripts/build_site.py --preview --output <directory>`. Incremental reuse can leave stale pages when topic assignments change. The final release command deliberately remains blocked.
