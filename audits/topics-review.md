# Topic assignment review

**Status: candidate taxonomy for private preview; full review is NOT complete.**

Coverage: all 3,406 source records assigned exactly once. 348 assignments have been read individually against the complete available title, paraphrased question text, and solution. 3058 assignments remain candidates. Do not describe Phase 3 topic review or the final release topic gate as passed.

## Scope and method

- The 12 stored subjects are preserved. All 238 excluded records are retained in `13-other-topics`.
- Each subject has 9–11 syllabus-oriented topics including an explicit Other / Mixed Topics catch-all.
- Initial candidates use weighted textual evidence from title, stem, and solution. This is a candidate-generation aid only; keyword matching alone does not count as review.
- Manual review covered every initial catch-all (101 records), chronological first/middle/last samples within all 13 subjects, and low-margin candidates. Overlapping selections are counted once.
- A separate reviewer inspected four subjects: digital logic, theory of computation, discrete mathematics, and other topics. The primary review covered the other nine subjects.
- Review means checking the best topic for the stated problem and its reasoning. It does not certify mathematical correctness, exact source transcription, original diagrams, or official-key fidelity. No source PDFs/images were checked for this taxonomy.
- No source question, answer, subject, or solution was rewritten. Blank titles are treated as absent; stem and solution supply the context.

## Machine-readable review state

`data/topics.json` retains the requested `topics` and `assign` members and adds `review`: a question-ID map whose values are `reviewed` or `candidate`. Every assignment has an explicit review state. A preview may display candidates with a clear warning; a release build must reject any state other than `reviewed`, in addition to enforcing coverage and valid topic IDs.

## Counts

| Subject | Questions | Topics | Reviewed | Candidate | Other |
|---|---:|---:|---:|---:|---:|
| 01-digital-logic | 241 | 9 | 37 | 204 | 3 |
| 02-computer-organization-architecture | 329 | 10 | 6 | 323 | 0 |
| 03-programming-in-c | 150 | 9 | 6 | 144 | 0 |
| 04-data-structures | 217 | 9 | 11 | 206 | 1 |
| 05-algorithms | 272 | 10 | 167 | 105 | 3 |
| 06-theory-of-computation | 279 | 9 | 22 | 257 | 2 |
| 07-compiler-design | 241 | 9 | 12 | 229 | 2 |
| 08-operating-systems | 302 | 9 | 9 | 293 | 0 |
| 09-database-management-systems | 250 | 9 | 12 | 238 | 0 |
| 10-computer-networks | 196 | 10 | 11 | 185 | 0 |
| 11-general-aptitude | 270 | 10 | 9 | 261 | 0 |
| 12-discrete-mathematics | 421 | 11 | 18 | 403 | 1 |
| 13-other-topics | 238 | 9 | 28 | 210 | 5 |

## Representative review decisions

- TLB address partitioning is Memory Organization & Address Translation, not cache merely because it is set-associative.
- Identify the min-heap property rather than treating any complete binary tree as a generic traversal problem.
- Dynamic-programming fill orders belong under Dynamic Programming even when the question asks correctness.
- Stop-and-wait efficiency belongs under Data Link, Error Control & ARQ, even though propagation delay is computed.
- Foreign-key violations are relational-model integrity, not SQL merely because insert/delete operations appear.
- Set inclusion-exclusion in aptitude is Counting, Probability & Sets, not geometry because the solution mentions circles.
- Regular-expression semantics and language closure were separated from elementary substring counting. Some legacy mixed questions legitimately remain Other.
- Generic token-bucket questions are grouped with transport/congestion/traffic shaping without claiming that they specifically use TCP.

## Systematic continuation

After the initial 198-record checkpoint, chronological individual review continues subject by subject, beginning with Algorithms, Data Structures, and Programming in C. Each additional reviewed status is set only after reading the full available stem and solution. Source questions remain unchanged.

## Remaining work / release gate

- Individually read and review the remaining 3058 candidates. Low-margin and empty-title records merit early attention, but every assignment must be checked.
- Preserve exactly one topic per question. Prefer the skill being assessed over incidental words in a solution; use Other for genuine mixed/legacy material that does not fit.
- After changes, recheck subject counts, ID coverage, known topic IDs, catch-all presence, and per-question review states.
- Regenerate charts/PDF grouping only from validated assignments. Do not let the presence of complete coverage imply complete review.

## Structural validation performed

- 3,406 unique assignments, no missing or duplicate question IDs, no unknown IDs.
- Assignment membership exactly matches each source subject, including all 238 excluded records.
- Topic counts satisfy the requested 6–12 range; every subject has Other.
- Every assigned topic exists in its subject taxonomy; every assignment has a review status.
- Source questions SHA-256 at this review: `2781a752fc66e090b3aeacdee235052e4802f58532eb9b98ff5f1cc4ecfc5e08`.

## Individually reviewed IDs

These IDs are also enumerated by `review: reviewed` in the JSON. All IDs not listed remain unreviewed candidates.

### 01-digital-logic

CS-1991-Q1, CS-1991-Q20, CS-1991-Q38, CS-1991-Q40, CS-1991-Q42, CS-1993-Q18, CS-1994-Q44, CS-1994-Q48, CS-1994-Q49, CS-1995-Q48, CS-1996-Q57, CS-1997-Q39, CS-1997-Q88, CS-1998-Q15, CS-1998-Q42, CS-1998-Q59, CS-2001-Q37, CS-2001-Q69, CS-2003-Q11, CS-2003-Q47, CS-2005-Q16, CS-2005-Q63, CS-2006-Q36, CS-2006-Q40, CS-2007-Q9, CS-2008-Q6, CS-2009-Q27, CS-2010-Q41, CS-2012-Q29, CS-2013-Q31, CS-2014-S1-Q18, CS-2014-S2-Q18, CS-2017-S2-Q34, CS-2021-S2-Q28, CS-2023-Q32, CS-2023-Q44, CS-2026-S2-Q59

### 02-computer-organization-architecture

CS-1991-Q2, CS-1992-Q14, CS-1997-Q37, CS-1998-Q45, CS-2006-Q62, CS-2026-S2-Q57

### 03-programming-in-c

CS-1991-Q34, CS-1997-Q56, CS-2000-Q85, CS-2015-S1-Q65, CS-2015-S2-Q24, CS-2026-S2-Q61

### 04-data-structures

CS-1991-Q8, CS-1991-Q63, CS-1992-Q17, CS-1994-Q11, CS-1997-Q30, CS-2000-Q14, CS-2004-Q43, CS-2006-Q77, CS-2012-Q57, CS-2015-S2-Q48, CS-2026-S2-Q50

### 05-algorithms

CS-1991-Q6, CS-1991-Q7, CS-1991-Q10, CS-1991-Q25, CS-1991-Q27, CS-1991-Q62, CS-1992-Q9, CS-1992-Q16, CS-1992-Q19, CS-1992-Q37, CS-1992-Q46, CS-1992-Q47, CS-1992-Q48, CS-1993-Q43, CS-1993-Q48, CS-1993-Q51, CS-1994-Q7, CS-1994-Q19, CS-1994-Q22, CS-1994-Q23, CS-1994-Q53, CS-1994-Q78, CS-1994-Q79, CS-1994-Q80, CS-1995-Q5, CS-1995-Q16, CS-1995-Q28, CS-1995-Q47, CS-1995-Q52, CS-1995-Q65, CS-1995-Q82, CS-1996-Q11, CS-1996-Q37, CS-1996-Q38, CS-1996-Q40, CS-1996-Q75, CS-1996-Q76, CS-1996-Q77, CS-1996-Q78, CS-1996-Q79, CS-1997-Q5, CS-1997-Q31, CS-1997-Q54, CS-1997-Q55, CS-1997-Q71, CS-1997-Q74, CS-1998-Q21, CS-1998-Q22, CS-1998-Q23, CS-1999-Q12, CS-1999-Q13, CS-1999-Q14, CS-1999-Q16, CS-1999-Q45, CS-1999-Q46, CS-1999-Q63, CS-1999-Q67, CS-2000-Q15, CS-2000-Q38, CS-2000-Q40, CS-2000-Q41, CS-2000-Q42, CS-2000-Q75, CS-2000-Q76, CS-2000-Q80, CS-2000-Q81, CS-2000-Q82, CS-2000-Q83, CS-2001-Q14, CS-2001-Q16, CS-2001-Q39, CS-2001-Q81, CS-2001-Q82, CS-2001-Q83, CS-2001-Q84, CS-2002-Q3, CS-2002-Q35, CS-2002-Q36, CS-2002-Q70, CS-2002-Q71, CS-2002-Q72, CS-2003-Q20, CS-2003-Q21, CS-2003-Q22, CS-2003-Q35, CS-2003-Q62, CS-2003-Q66, CS-2003-Q67, CS-2003-Q68, CS-2003-Q69, CS-2003-Q70, CS-2004-Q29, CS-2004-Q39, CS-2004-Q42, CS-2004-Q44, CS-2004-Q82, CS-2004-Q83, CS-2004-Q84, CS-2004-Q85, CS-2005-Q7, CS-2005-Q37, CS-2005-Q38, CS-2005-Q39, CS-2005-Q58, CS-2005-Q81, CS-2005-Q82, CS-2005-Q83, CS-2005-Q84, CS-2005-Q87, CS-2005-Q88, CS-2006-Q1, CS-2006-Q11, CS-2006-Q12, CS-2006-Q14, CS-2006-Q17, CS-2006-Q47, CS-2006-Q48, CS-2006-Q51, CS-2006-Q52, CS-2006-Q54, CS-2007-Q5, CS-2007-Q14, CS-2007-Q41, CS-2007-Q44, CS-2007-Q45, CS-2007-Q49, CS-2007-Q50, CS-2007-Q51, CS-2007-Q76, CS-2007-Q77, CS-2008-Q7, CS-2008-Q19, CS-2008-Q39, CS-2008-Q40, CS-2008-Q43, CS-2008-Q44, CS-2008-Q45, CS-2008-Q74, CS-2008-Q80, CS-2008-Q81, CS-2009-Q11, CS-2009-Q13, CS-2009-Q14, CS-2009-Q35, CS-2009-Q38, CS-2009-Q39, CS-2009-Q53, CS-2009-Q54, CS-2010-Q22, CS-2010-Q44, CS-2010-Q60, CS-2010-Q61, CS-2011-Q35, CS-2011-Q47, CS-2011-Q48, CS-2011-Q64, CS-2011-Q65, CS-2012-Q26, CS-2012-Q28, CS-2012-Q39, CS-2012-Q49, CS-2012-Q50, CS-2013-Q16, CS-2015-S3-Q63, CS-2022-Q11, CS-2025-S2-Q20, CS-2026-S2-Q39

### 06-theory-of-computation

CS-1991-Q32, CS-1991-Q70, CS-1992-Q27, CS-1992-Q68, CS-1994-Q15, CS-1994-Q34, CS-1994-Q72, CS-1995-Q45, CS-1995-Q49, CS-1996-Q34, CS-1997-Q44, CS-1998-Q9, CS-1998-Q12, CS-1999-Q65, CS-2008-Q51, CS-2012-Q35, CS-2013-Q18, CS-2015-S2-Q60, CS-2016-S1-Q26, CS-2016-S1-Q28, CS-2019-Q25, CS-2026-S2-Q48

### 07-compiler-design

CS-1991-Q11, CS-1993-Q30, CS-1993-Q31, CS-1993-Q32, CS-1994-Q5, CS-1994-Q67, CS-1995-Q4, CS-1995-Q36, CS-1997-Q8, CS-2004-Q9, CS-2016-S1-Q29, CS-2026-S2-Q45

### 08-operating-systems

CS-1991-Q12, CS-1993-Q33, CS-1994-Q21, CS-1994-Q82, CS-1996-Q18, CS-1998-Q51, CS-2002-Q45, CS-2007-Q56, CS-2026-S2-Q55

### 09-database-management-systems

CS-1991-Q58, CS-1997-Q50, CS-1998-Q33, CS-1998-Q55, CS-2000-Q47, CS-2004-Q51, CS-2009-Q56, CS-2014-S2-Q32, CS-2017-S1-Q26, CS-2021-S1-Q33, CS-2024-S1-Q35, CS-2026-S2-Q46

### 10-computer-networks

CS-1992-Q2, CS-1995-Q12, CS-2007-Q65, CS-2008-Q58, CS-2014-S3-Q34, CS-2015-S2-Q34, CS-2016-S1-Q64, CS-2017-S1-Q54, CS-2020-Q48, CS-2025-S1-Q56, CS-2026-S2-Q65

### 11-general-aptitude

CS-2010-Q1, CS-2010-Q4, CS-2011-Q9, CS-2015-S2-Q3, CS-2015-S3-Q4, CS-2015-S3-Q5, CS-2016-S2-Q6, CS-2017-S2-Q6, CS-2026-S2-Q10

### 12-discrete-mathematics

CS-1991-Q13, CS-1993-Q54, CS-1994-Q26, CS-1994-Q30, CS-1995-Q66, CS-1996-Q2, CS-1997-Q69, CS-1997-Q70, CS-1998-Q8, CS-2000-Q1, CS-2000-Q2, CS-2000-Q56, CS-2001-Q29, CS-2003-Q31, CS-2005-Q47, CS-2015-S1-Q41, CS-2024-S1-Q52, CS-2026-S2-Q36

### 13-other-topics

CS-1993-Q1, CS-1993-Q2, CS-1993-Q3, CS-1993-Q5, CS-1993-Q9, CS-1993-Q11, CS-1993-Q15, CS-1993-Q16, CS-1993-Q17, CS-1995-Q22, CS-1995-Q23, CS-1995-Q33, CS-1995-Q43, CS-1996-Q26, CS-1996-Q31, CS-1998-Q67, CS-2000-Q24, CS-2004-Q1, CS-2004-Q28, CS-2004-Q71, CS-2014-S1-Q14, CS-2014-S1-Q15, CS-2014-S2-Q15, CS-2015-S1-Q11, CS-2015-S1-Q33, CS-2015-S2-Q51, CS-2022-Q20, CS-2026-S2-Q64

