# GATE CSE Previous Year Questions (1991–2026)

Work in progress: 3335 source-numbered entries across 45 CS papers, with 3097 in the requested subjects and 238 supplemental entries. Available derivations have independent second review; 1 entries remain unresolved because source material is missing. Available relevant figures were visually inspected. Official scoring fields reconcile where a key was located; 1645 entries have no located official key, including the unresolved source gaps; the others have independent derivations. Wording/model issues are disclosed. Entries are source-linked solutions, not complete question transcriptions. Legacy entries identified as third-party reproductions have unverified original-source fidelity/completeness. The 36-year collection is not complete.

## Subjects
| # | Subject |
|---|---------|
| 01 | [Digital Logic](subjects/01-digital-logic) |
| 02 | [Computer Organization and Architecture](subjects/02-computer-organization-architecture) |
| 03 | [Programming in C](subjects/03-programming-in-c) |
| 04 | [Data Structures](subjects/04-data-structures) |
| 05 | [Algorithms](subjects/05-algorithms) |
| 06 | [Theory of Computation](subjects/06-theory-of-computation) |
| 07 | [Compiler Design](subjects/07-compiler-design) |
| 08 | [Operating Systems](subjects/08-operating-systems) |
| 09 | [Database Management Systems](subjects/09-database-management-systems) |
| 10 | [Computer Networks](subjects/10-computer-networks) |
| 11 | [General Aptitude](subjects/11-general-aptitude) |
| 12 | [Discrete Mathematics](subjects/12-discrete-mathematics) |

## Ground rules
1. **No missing questions.** Each year/paper (including multiple sets, e.g. 2014–2026 sessions) is reconciled against the official paper's question count. Paper-level counts and source status live in `data/papers.json`. Every numbered item must be accounted for, including items outside the requested subjects. A paper is complete only after source reconciliation and independent solution review.
2. **No wrong answers.** Every solution is derived independently and compared with the official answer key (including revised/final keys). Mismatch → resolve or log as a discrepancy; never silently pick one.
3. **Discrepancies are always recorded**: question errors, ambiguity, missing figures, key changes, disputed keys, bonus/dropped questions. Each is in the question's `Discrepancy` field and indexed in [DISCREPANCIES.md](DISCREPANCIES.md).
4. Questions are uncategorised-by-subject cross-cutting? Assign to the single best-fit subject; note cross-references.
5. Preserve source wording, code, tables and figures faithfully where permitted, with marks and actual historical question format. Do not copy third-party explanations; write solutions independently.

## Scope assumption
"Previous 36 years" = **1991–2026**, inclusive, following the current working scope. Separate historical IT papers are not silently included; their inclusion requires an explicit scope decision.

## Workflow
Per subject/year: collect official paper + key → add questions via [template](templates/question.md) → solve and verify → update tracker → log discrepancies → commit (`<subject>: <year> done`).

Sources of truth: official GATE papers/keys (IIT organising institute sites, gate.iitk.ac.in archives). Third-party sites (e.g. GATE Overflow) may be used for cross-checking only.


## Current status and quality gates

The repository is scaffolding, not a complete question bank. Unknown counts remain null; they must not be reported as zero questions in a paper. An empty discrepancy log does not mean no discrepancies exist.

`data/papers.json` lists 46 candidate CS papers for 36 years. Session inventory is provisional until reconciled against source papers. General Aptitude is included where present (from 2010); earlier years are not missing GA. Separate IT papers and non-discrete engineering mathematics require explicit scope handling. Every source question must receive either an included subject or a documented exclusion reason so omitted material cannot disappear silently.

Run `python 3 scripts/validate.py` to check record structure. Run `python 3 scripts/validate.py --require-complete` for the release gate; it intentionally fails until every paper, question, source and solution has been verified. Passing structural validation alone is not evidence of answer correctness.

For each question, record a unique ID, paper/session ID, source question number, source page, subject, preserved question and figure references, independent solution, derived answer, exact official answer or accepted range, key revision, verification status, and discrepancy IDs. An unavailable official key must remain explicitly unverified. See `data/README.md`.


Detailed step-by-step expansion and a separate explanation-quality audit are in progress. Existing answer reviews do not certify explanatory depth; see [QUALITY.md](QUALITY.md).

Explanation-depth review: 1580 entries have independently reviewed teaching expansions; 1755 remain pending. This is separate from answer review and complete question/source access. See [QUALITY.md](QUALITY.md).
