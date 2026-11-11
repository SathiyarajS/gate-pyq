# Study views and review boundaries

The subject's original route and JSON filters remain the **All questions** view.
Every question keeps its canonical permalink, paper ordering, answer, provenance,
and individual practice state. `/unique/` remains a compatible URL, but is now
labelled **Known repeats folded**. It does not claim exhaustive deduplication.

**Problem patterns** (`/<subject>/patterns/`) groups reasoning procedures rather
than duplicate statements. It renders the explicit representative and expandable
full question cards for every other variant. Ungrouped questions remain visible.
Source-reviewed groups span scheduling, automata, dependencies, recurrences,
probability, caches, pipelines and networks. This remains an incomplete catalogue.
The review coverage and exclusions are recorded in `audits/grouping/`.

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
Test all three views, expanding/collapsing alternatives, individual answers,
bookmarks, pagination and browser Back. Every question must remain reachable;
filters and canonical links must still use the All questions view.

## Agent-managed verification

The user is not asked to review these groups manually. Accepted changes require
source-page review and automated data, retention and browser checks. Candidate
search scans all 3,406 summaries, but does not prove complete semantic coverage.
Source-reviewed counts refer to inspected questions, not proof that every pair
among them was exhaustively compared. Historical reproduction defects and
incomplete transcriptions prevent a guarantee of perfect grouping or recall.

Run `python scripts/checks/check_study_views_browser.py` after building the site
for desktop/mobile expansion, answer isolation, bookmarks, filters and Back
regressions. CI runs this automatically where Chromium is available.

## Systematic full-corpus pass

`audits/grouping/full-corpus/manifest.json` accounts for every canonical question,
including pending, source-blocked, ambiguous and no-reviewed-match records.
Regenerate it with `python scripts/group_review_progress.py --write`. Candidate
review alone never counts as full-subject completion. Primary subject reports
record a method fingerprint and source evidence per question. A subject reaches
the completion gate only after independent source checking of proposed group
members and required corrections; this does not imply a second transcription
review of all ungrouped questions. Proposals awaiting that gate are not integrated
into the pattern data. No-reviewed-match means no accepted counterpart was found,
not proof of uniqueness. Source-blocked records cannot count as completed.


The 11 November full-corpus pass assessed all 3,406 questions, with zero pending
primary or independent group reviews. 3,405 have readable source evidence; one
remains source-blocked after alternate-source investigation. The accepted
partition has 376 patterns covering 1,231 questions, and 45 accepted repeat pairs.
The full-corpus README documents the blocker and exact count definitions.
Unmatched and ambiguous questions remain visible, without a uniqueness claim.
