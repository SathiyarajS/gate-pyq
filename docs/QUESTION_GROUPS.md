# Study views and review boundaries

The subject's original route and JSON filters remain the **All questions** view.
Every question keeps its canonical permalink, paper ordering, answer, provenance,
and individual practice state. `/unique/` remains a compatible URL, but is now
labelled **Known repeats folded**. It does not claim exhaustive deduplication.

**Problem patterns** (`/<subject>/patterns/`) groups reasoning procedures rather
than duplicate statements. It renders the explicit representative and expandable
full question cards for every other variant. Ungrouped questions remain visible.
The first reviewed group covers SRTF schedule simulation with waiting/turnaround
metrics; it is not an exhaustive catalogue of scheduling questions or patterns.

## Sources and status

- Existing `data/repeats.json` pairs retain their historical review claim. They
  were not newly source-audited by this feature. Missing `status` means the legacy
  reviewed record; explicit `candidate` and `rejected` pairs cannot fold anything.
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
Test all three views, expanding/collapsing alternatives, individual answers,
bookmarks, pagination and browser Back. Every question must remain reachable;
filters and canonical links must still use the All questions view.
