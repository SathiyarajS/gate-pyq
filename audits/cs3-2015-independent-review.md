# CS-2015-S3 independent expansion review

## Verdict

PASS after the Q54 distractor transcription fix described below. All 65 expanded records were read, their derivations independently assessed, and all 27 physical source pages 53–79 of `/tmp/gate-2015-CS.pdf` rendered and visually inspected. The review did not rely on OCR for question notation, code, diagrams, or tables. No repository or external-service edits were made.

The explicit protected-field exception for Q36 derived_answer `308.67` → `309.33` is approved. No other protected-field change is approved or present.

## Source fidelity and correction audit

- Physical page 74 shows Q54 option B with `a(2 ln 2 − 25) − 47b/2` and option D with `a(ln 2 − 25) − 47b/2`, both over `a²−b²`. The candidate had exchanged B and D's logarithmic coefficients. Corrected these distractors in `cs3-2015-expanded.json`, `cs3-2015-expanded.md`, and `build_cs3_2015_expanded.py`. Option A, its solution, the derived answer, and source key are unchanged.
- All other essential statements and options match the inspected source under the explicit explanatory paraphrases and qualifications. In particular, visually confirmed Q8's full bar-chart data, Q9's two directed rays, Q23's matrix and vectors, Q31's critical sections inside the inner loops, Q36's table, Q48's reservation table, Q51's transaction schedule, Q57's process table, and Q58's eight-node graph and three back edges.
- Q11 assigns digit '0', not a null terminator. Q18 really has the malformed attribute punctuation noted in the contribution. Q43 really prints adjacent conversions without a separator. Q54 source states a≠b; evaluating at x=1 validly supplies a+b≠0 for an existing function.

## Q36 independently verified exception

Physical page 65 supplies times 2,4,6,8,10,12,14,16,18,20 minutes, velocities 10,18,25,29,32,20,11,5,2,0 km/min, and explicitly says the bike starts from rest. Therefore v(0)=0 and the ten subintervals have width 2.

Odd-index sum = 10+25+32+11+2 = 80. Even-index sum = 18+29+20+5 = 72. Composite Simpson bracket = 4×80+2×72 = 464. Distance = (2/3)×464 = 928/3 = 309.333333… km, rounded to 309.33 km. An additional exact-rational panel-by-panel calculation gives 116/3 + 98 + 118 + 46 + 26/3 = 928/3. Thus 308.67 is an arithmetic mistake, not a source-table alternative.

The source's annotated range is 308 to 310 and remains unchanged. Both old and corrected numbers lie within that range; this does not make the old calculation correct.

## Derivations and explanatory depth

All 65 answers have sufficient problem-specific working for these questions. This is an assessment of reasoning, not a word-count threshold. Simple verbal and arithmetic questions appropriately have short explanations. Several solutions repeat their core observation between steps, but this is nonblocking style debt rather than missing reasoning.

Specifically checked the set-difference identity (Q12), NAND counterexample (Q16), adjusted function points 612.06 (Q17), tree edge count (Q21), eigenvector nullspace (Q23), heap witness and exhaustive exclusion of fewer than three swaps (Q30), five-state DFA transitions/distinguishability (Q32), fault estimator (Q33), cache split (Q34), collision round trip (Q35), recursive base-call count 25 (Q38), internal B+ node capacity 50 (Q39), polynomial reduction direction (Q41), C call sequencing and total 230 (Q42), CFL grammar/pumping reasoning (Q44), GBN window 201 and eight bits (Q47), latency lower bound and constant-gap witness (Q48), determinant factorization (Q52), switch fall-through count 10 (Q53), integral coefficients (Q54), MST increment 495 (Q55), packet timeline 1575 microseconds (Q56), scheduling turnaround comparisons (Q57), graph complexity convention (Q58), all five base pairs (Q59), maximal Boolean cubes (Q62), modular exponent trace (Q63), dense integer-angle subsequences (Q64), and grammar-specific parsing conflicts (Q65).

The preserved qualifications for Q6, Q18, Q29, Q31, Q43, Q46, Q52, Q56, Q58, and Q65 are appropriate. They prevent an intended exam answer from being presented as an unconditional claim under a different formal model.

## Mechanical checks and limitations

- Compared against `/workspace/shared/gate-pyq/data/questions.json`, not only the author's snapshot. Snapshot matches the 65 repository records exactly. Excluding the explicitly editable context/solution/review fields, the sole difference is Q36 derived_answer.
- Inspected and reran the supplied checker successfully after the Q54 fix. It includes exhaustive zero/one/two-swap exclusion for Q30, cube enumeration for Q62, and collision-state cycle means for Q48. Independently checked JSON/Markdown question and solution equality, exact word counts, unique count 65, and the rational Simpson calculation.
- The checker alone does not establish source fidelity or independent review; those were performed here. Its fixed visual-page list and pending-review labels are metadata, not automated evidence.
- Contribution records and the author's checker output still say independent review pending. This audit supplies the completed independent assessment; the integrator should apply review status consistently instead of interpreting those stale labels as a failed audit.
- The PDF is an inline-answer annotated paper. This review does not authenticate it as an official final-version answer key. That provenance limitation remains intact. The alternate PDF was available but unnecessary because every combined-source page was readable.
- No UI/rendering test of the eventual application was performed. This audit covers the contributed content and its structured/Markdown representations.

Machine-readable result and reviewed file hashes: `cs3-2015-independent-review.json`.
