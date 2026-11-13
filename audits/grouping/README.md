# Grouping review summary

The study groups shown on the site live in two files, and each accepted group or
pair there carries its own evidence: source file, page, SHA-256 and notes for
every member.

- `data/problem-patterns.json`: 376 reviewed problem patterns covering 1,232
  questions (questions solved with the same method).
- `data/repeats.json`: 36 accepted repeat pairs (the same question, or the same
  question with changed values) and 34 rejected pair records, which never fold.

## How they were made (11 November 2026)

Candidates came from comparing every question's summary text. Each proposed
member was then compared against the source pages before being accepted. A
consistency pass applied one rule to every repeat pair: the same setup and the
same requested answer, with only given values allowed to change. Generic
"compute this" questions on different data (SRTF tables, CRC, eigenvalues of
different matrices) are patterns, not repeats.

Questions that are in no group are not claimed to be unique; the search cannot
guarantee every relationship was found. CS-2010-Q56 stayed ungrouped because its
archived scan is too faint to read the resource subscripts.

The per-question working files from that review (6.7 MB) were not kept in the
repository; they are in the history of pull request #2 (`feat/question-study-views`).
