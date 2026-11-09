# CS 2005 independent depth and source audit

Reviewer: review_2005_solution_depth. Date: 2026-11-09.

## Outcome

PASS for all 90 expanded teaching explanations and essential question contexts, after the corrections below. This is a source-aware mathematical/editorial review, not official-key validation or verification of the original examination paper. Reproduction discrepancies and conditional answers remain explicitly qualified. No repository files were edited.

Reviewed candidate: cs-2005-expanded.json and .md. Rebuild: python /workspace/shared/gate-pyq-contributions/finish_2005_expansion.py, which runs the seven expansion builders. All review corrections live in that final builder and survive regeneration.

## Scope and evidence

Read all 90 complete question contexts and solutions. Independently visually inspected every GFG page 1–12. Cross-checked GateForum physical pages 5, 10–15, 17–18 for sensitive options, graphs, automata, code, timing diagrams, and datapath. The alternate PDF has 22 physical pages (not 20); not all 22 were independently inspected in this pass. Sources are the local 2005-gfg.pdf and 2005-gateforum.pdf under /workspace/shared/gate1991-2006-research. Remaining alternate-specific claims rely on the inherited source review, not a new all-page alternate audit.

The question text is an essential-context paraphrase, not a verbatim diplomatic transcription. Diagram connectivity, table values, relevant code and formula content are represented textually. Linked printed 81(a/b) through 85(a/b) retain normalized IDs 81–90. Author-supplied hypotheses and caveats remain distinguished from source statements.

## Corrections made

- Removed indiscriminate alphabet/digit splitting from the final spacing pass. It had broken hexadecimal literals (1AF, 0x4D3D, 0x4AE8), IPv4, and variable/state subscripts. Prose spacing now avoids these tokens; hexadecimal choices are separately labelled.
- Q5 explicitly restores integer scores.
- Q48 restores C: more than one but finitely many solutions; D: infinitely many. Previous expansion incorrectly substituted C infinite and D exactly two. The derived unique-solution answer B is unchanged.
- Q50 restores all four GateForum choices i, i+1, 2i, 2^i, plus the extra GFG constant-1 choice and shifted five-entry lettering. The earlier candidate incorrectly included 1 and omitted 2i from its intended list.
- Q59 restores option B's third handle E+E×n instead of n+E×n. Answer D unchanged.
- Q62 restores B's third value A2′ and C's full sequence A1,A2,A2′,A3,A4. Answer A unchanged.
- Q66 spells out all mapping tuples and documents the differing first tuple in D: GFG (1,b), GateForum (1,a). Answer C unchanged.
- Q78 notes that its C distractor uses the clearer GateForum BEH while GFG appears to print BEE. Answer D unchanged.

## Sensitive findings retained

Q14 ambiguity and left recursion both obstruct predictive parsing. Q29's two-attribute BCNF claim requires excluding empty-determinant dependencies. Q32 diagnostic severity depends on C mode. Q44 requires the integer domain. Q47's GFG prism has extra face diagonals but stays planar. Q48's first-row sign differs across reproductions without changing uniqueness. Q51's alternate omits a color. Q53's start state is nonfinal: exact language requires at least one a, so the broad B wording is not literally exact. Q58 both problems concern independent sets; the five-vertex test checks nonedges, not clique edges. Q60 GFG duplicate equality distractors remain documented; state counts are 6,10,6. Q61 preserves fro and argument commas with historical-C and undefined-runtime caveats. Q62 preserves coincident-edge ambiguity. Q65 preserves the instruction-fetch-boundary ambiguity. Q68 forwarding is conditional. Q69 states the CPU-occupation and unit convention. Q70 computes 26.2144% (binary) /25.6% (decimal), rather than calling 25% exact. Q72 retains the printf pointer-type defect. Q77 does not infer NOT NULL from distinct prices. Q80 explicitly identifies its constant-one datapath assumption. Q83 retains source option-letter mismatch. Q89–90 normalize the stored truncated value using zero-fill rather than freshly converting the decimal.

## Depth assessment

All 90 contain a derivation, invariant, trace, construction, counterexample, or concept-level rationale adequate to teach the selected result. Proof-bearing questions explain the mechanism rather than merely cite an answer: complement/cover duality, Catalan recurrence, closure proofs, reduction direction, parser state distinctions, pipeline scheduling, FD closure, MST exchange/minimax arguments, and scheduling optimality bounds. Straight arithmetic questions give intermediate calculations. Longer explanations intentionally preserve genuine source limitations. Some baseline/teaching-detail repetition remains editorial rather than mathematical.

## Structural checks

Exactly 90 unique sequential question IDs. Protected-field comparison with repository baseline: no changes to answers, official-answer/key fields, provenance, source URLs/hashes, marks, subjects, question types, numbering, discrepancy IDs, or verification flags. Only question_text, solution, independent_review (author reset pending), independent_depth_review, explanatory_depth_status, and solution_word_count differ. All depth-review records are passed; generic independent_review remains pending and must not be interpreted as renewed official/source verification. Minimum solution length is 54 words; length itself is not the acceptance test.

No blocker or denied operation. No official answer key was used or claimed.
