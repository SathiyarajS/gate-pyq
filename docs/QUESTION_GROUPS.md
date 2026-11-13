# Study views and review boundaries

Each subject and topic is a single page listing every question newest first
(50 per page by default in the browser, or all at once; the choice is remembered
on the device). Paper pages keep the original paper order.

Questions in a reviewed problem pattern, or in a repeat group that belongs to no
pattern, link to `/<subject>/similar/<group-id>/`, which lists every member newest
first as full practice cards. The pattern's description is behind "How these are
solved" so it does not give the method away. All but the newest member carry
`data-alt="1"`, which the "One per method" filter hides. The old `/page/N/`,
`/unique/` and `/patterns/` addresses redirect to the subject page.

## Sources and status

- All 28 legacy `data/repeats.json` pairs were rechecked against full source
  pages. Nineteen remained repeats; nine materially different tasks were rejected
  from repeat folding and considered separately as patterns. Accepted pairs now
  carry explicit `reviewed` status and per-member evidence. Rejected records stay
  in the audit trail and cannot fold questions. Missing status remains supported
  for old fixtures, but must not be used for new data.
- New `data/problem-patterns.json` groups require explicit status. Only `reviewed`
  groups affect display. Each needs a safe unique ID, same-subject members,
  representative, title, rationale and source comparison evidence for every
  member. Multiple source pages for one member are supported.
- Review evidence records source file, SHA-256, physical page and notes on actual
  constraints, requested output, figures and shared context, plus method, reviewer
  and date. Metadata is an audit trail, not proof that a review occurred.
- Membership must be checked against source pages, not accepted from paraphrase
  similarity. A group must explain why the procedure is shared and what differs.
  Same topic alone is insufficient. A changed requested metric or extra algorithm
  can be a pattern variation while disqualifying a repeat.
- Groups cannot overlap in this initial partition model; overlapping memberships
  fail the build rather than silently hiding or duplicating questions.
- A grouping review does not verify a transcription, solution or official key.
  Existing source/reproduction caveats remain applicable.

## Discovery

Run `python scripts/discover_groups.py --help` for offline candidate generation.
The script compares normalized text/math and explicit lexical reasoning signals.
These semantic hints are heuristics, not an embedding model or a review. It emits
candidate evidence, source pointers and cautions to a separate JSON output; the
site never loads that output. Review actual source pages before adding any member
to the reviewed files. Do not add transitive candidate edges to repeat groups.

## Checks

Run `python scripts/validate.py`, `python -m pytest -q tests`,
`node tests/test_transcription_math.js`, and `python scripts/build_site.py --preview`.
Test the subject list (50 per page and all), the year jump, "One per method",
individual answers, similar pages and browser Back. Every question must remain reachable;
filters and canonical links must still use the All questions view.

## Coverage

Candidate search scans all 3,406 summaries but does not prove complete semantic
coverage. Questions in no group are not claimed to be unique. Historical
reproduction defects and incomplete transcriptions prevent a guarantee of perfect
grouping or recall. A summary of the 11 November review is in
`audits/grouping/README.md`.

Run `python scripts/checks/check_study_views_browser.py` after building the site
for desktop/mobile expansion, answer isolation, bookmarks, filters and Back
regressions. CI runs this automatically where Chromium is available.
