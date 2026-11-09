# Independent private-preview review

Reviewed the local generated preview against CODEX_INSTRUCTIONS.md and audits/site-implementation-status.md. This review does not authorize publication or certify exact source fidelity.

## Initial preparation snapshot (historical result)

A clean rebuild was independently checked: 4,233 HTML files including 26 print drafts, 3,406 unique canonical subject records and 3,406 unique paper-view records. Zero structural/link/metadata errors. The JavaScript and print-HTML checks below also passed on this frozen output. Topic review remains partial (348 reviewed, 3,058 candidates), not certified complete.

## Verified

- All 3,406 question IDs appear exactly once across canonical subject pages and exactly once in paper views. Topic duplicates and permalink redirects are deliberately outside canonical coverage counts.
- Static site question answers are native details elements, collapsed by default. All recorded official-answer strings, no-key labels, independent answers where different, discrepancy badges, years, source-access notes, key-revision caveats, provenance, historical numbering notes and shared context checked against generated subject fragments.
- Internal links and fragment targets checked across generated HTML. Report JSON records exact page count and errors.
- Initial omission of source/key/numbering qualifications was reported and corrected by the builder. Historical group marks and subparts now appear in provenance details.
- Source HTML is escaped before formatting. Script/image injection smoke tests and unsafe URL-scheme rejection passed.
- JavaScript VM tests cover ordinary MCQ, options beyond D, MSQ sets, exact NAT ranges, no key, conditional text, marks-to-all, alternative MCQ answers and disjoint NAT ranges. Unsupported official formats deliberately return self-check, never an incorrect numeric/letter comparison. This is a safe preview limitation, not complete practice functionality.
- All 13 subjects' PDF HTML exports checked: questions-only variants contain no detailed-solution blocks, answer-index entry counts match each subject, and full variants retain all 3,406 detailed solutions. This is HTML verification, not PDF verification.
- Blocked-localStorage initialization and nested subject-page base/link resolution passed isolated JavaScript tests. Full DOM interaction was not exercised.
- Preview text explicitly says paraphrase, unverified draft topics and no certified original crops/redraws. Source links are labelled as source links rather than a false original-image display.

## Execution blocker and exact limits

Chromium did not start: process_singleton_posix.cc socket() failed with Operation not permitted. One approved require_escalated attempt encountered the same runtime restriction. No further launch attempts were made. No screenshots were produced or visually inspected. Mobile 360 px, desktop 1280 px, light/dark layouts, interactive search/filter/bookmarks/timer behavior, browser accessibility, screenshot quality, PDF rendering, bookmarks and page layout remain unverified. CSS includes responsive rules but these are not proof of responsive rendering.

The generator does not clear its output directory on rebuild. A clean output directory is recommended after topic or route changes to avoid stale unlinked pages.

At this initial checkpoint, Pagefind, math typesetting, exact original crops, independently reviewed topics, verified redraws and finished PDF acceptance remained pending. Stored question data was not edited by this reviewer. Latest access metadata presence in generated fragments was checked; provenance correctness and every underlying source were not independently re-audited.

## Reproducible checks

- `python audits/site-preview-review.py`
- `node audits/site-preview-review-js.cjs`
- `python audits/site-preview-review-pdf-html.py` (requires the build dependencies)
- Browser script retained as `audits/site-preview-review-browser.py` for an environment that permits Chromium. Its results must not be assumed until execution succeeds and the screenshots are actually inspected.

## Enhanced checkpoint follow-up

A new clean build passed with 7,634 HTML files (including 3,406 search documents and 26 print drafts), exact 3,406 canonical subject and paper records, and zero static errors. All 3,406 topic assignments now have individual text/solution-based review. Real KaTeX and Pagefind parser/index checks pass; see enhanced-preview-review.md. Crop metadata records 65 independent source-boundary/render checks, but the preview remains paraphrase-based. Browser, accessibility, PDF layout, full original presentation, source fidelity and rights limitations above still apply.
