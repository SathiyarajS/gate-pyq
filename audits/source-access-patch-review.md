# Source-access patch review

Reviewed 2026-11-09 against frozen published snapshot `/tmp/gate-tree-3406-depth3406-contexts-v2.json` and the supplied original-question access audit. Result: PASS for navigation/metadata integration. No external writes or new source fetching performed.

- All 3,406 question IDs, ordering, answers, explanations, source page numbers, printed numbering, sections, and other protected question fields match baseline.
- Only intended field changes occur: 1,985 added original-source access records, 19 added pending-artwork audit records, 661 question-text status corrections, the CS-2019-Q10 diagram-accessibility correction, and 279 additive source-transcription verification-scope clarifications.
- Validated all 1,985 panels against their question record and variant. Counts: 15 ZIP variants / 1,010 records; 12 live-official PDF variants / 780 records; three archived-official PDF variants / 195 records.
- Every route matches the supplied audit. ZIP links have no page fragment; exact member, physical page, printed section/question, and variant are explicit. Direct/archived PDF links retain physical-page fragments. Combined-paper page ranges remain distinct and do not restart at variant boundaries.
- Removing added panels reproduces all baseline solution Markdown except the intended CS-2019-Q10 accessibility paragraph. That paragraph links the reviewed artifact and removes the stale pending-redraw assertion; answer and explanation text remain unchanged.
- Both new SOURCE_ACCESS.md relative links resolve. The corrected 2019 paragraph's ../../question-access path also resolves.
- Exactly 19 panels identify local artwork as pending. Unknown artwork is explicitly distinguished from missing artwork. Source availability and republication/accessibility limitations are disclosed without claiming complete original transcription.
- scripts/validate.py passes: 46 candidate papers, 3,406 entries. Re-running scripts/build_source_access.py leaves every tracked workspace file byte-identical.

## Limits

This review verifies routing against existing provenance and supplied audit, not a fresh visual inspection of 1,985 questions. ZIP member names and archived URLs are inherited provenance, not newly downloaded/verified bytes. The 2021 reader-size and 2023 timeout limitations remain correctly qualified. Rights to republish complete papers are not established.

## Review changes

No implementation fixes were necessary. Added only this review and its machine-readable companion, source-access-patch-review.json. Running the generator caused no file-content changes.

## Final additive scope clarification

Verified exactly 279 records have legacy source_transcription_verified=true and the new source_transcription_verification_scope clarification. No other records carry that scope text. The clarification limits the legacy flag to essential source context/option interpretation and explicitly does not certify complete verbatim wording or artwork. Recomparison against baseline confirms no additional protected-field changes.
