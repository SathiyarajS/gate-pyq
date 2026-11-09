# CS 2004 independent essential-question and solution-depth review

## Verdict and exact scope

Accepted with stated source/model caveats for all 90 essential paraphrases and teaching solutions. This is a fresh review by a reviewer other than the expansion author. It is not verification of official wording, an official answer key, or the original examination paper. No official key was available. No protected-answer correction is proposed.

The reviewer read all 90 question stems, four options, and complete solutions in `cs-2004-expanded.json` (including inherited arguments and new teaching checks), inspected the builder and checker, and visually inspected every rendered page of both supplied secondary PDFs: GFG physical pages 1–12 and GateForum physical pages 1–23, including the cover instructions. The views used 1600-pixel-long-side page renders. The clearer GateForum rendering resolved small labels and code where GFG was blurred. The Markdown is generated from the same records; its 90-section structure was checked, but no claim of a separately rendered publication-layout review is made.

Review inputs:
- `/workspace/shared/gate1991-2006-research/2004-gfg.pdf`
- `/workspace/shared/gate1991-2006-research/2004-gateforum.pdf`
- Baseline `/workspace/shared/gate-pyq/data/questions.json`, CS-2004 records only.
- Candidate and author scripts in `/workspace/shared/contributions/`.

## Coverage and teaching-depth findings

- Q1–10: control-flow goals, pass-by-value trace, stack-space equation, full BST parent-child structure, delimiter handling, BFS queue argument, all hash outputs, grammar restrictions, linking model, and register evaluation order were reviewed. The explanations distinguish mechanisms from distractors.
- Q11–20: threading assumptions, disk queue caveat, foreign-key difference, join-size bounds, network layers/addresses, Boolean simplification, NAND forbidden state, bases, and relocation were reviewed. Q12 and Q14 appropriately do not silently invent missing assumptions.
- Q21–30: architectural frame constraint, serial overhead, logic quantifiers, closure, coin counting, symmetric-matrix degrees of freedom, ordered matrix multiplication, floating-point rounding, sorting lower bound, and SAT classification were reviewed. The variants in Q23/Q24 are explicitly qualified.
- Q31–40: recursive/static-state trace, digit invariant, string terminator, class hierarchy, traversal ambiguity, circular queue, all heap alternatives, expression associativity, layout versus asymptotics, and unsorted-list costs were reviewed. Q39/Q40 state their computational models.
- Q41–50: Euclidean invariant/termination, square-root iteration/error bound, edge height, all directed graph arcs and Dijkstra order, semantic grammar precedence, SRPT schedule, paging arithmetic, semaphore ordering, inode capacity, and normal-form closures were reviewed. Q45/Q47/Q49 preserve nontrivial qualifications.
- Q51–60: relational quantifiers, B+ node capacity, SQL grouping/subquery scope, backoff pairs, longest-prefix routes, full repeated networking context, fragmentation and goodput, BCD gates, prime implicants, and MUX expansion were reviewed. Q51 wording was clarified as described below.
- Q61–70: counter wiring/excitation, carry-lookahead assumptions, full repeated program table, byte PC, instruction cycles, cache trace, signed multiplication, microinstruction connectivity, DMA ratio, pipeline fill, and both propositional variants were reviewed.
- Q71–80: both linear systems, group table, lattice meet/join caveat, expectation, unordered colour pairs, matching bound, full graph and colouring proof, Hamming counting, graph-complement count, and squared-distance expectation were reviewed.
- Q81–90: union-cycle proof, amortized run charging, recursion tree, recurrence derivation, balanced-tree upper/lower bounds, all DFA transitions, CFG and pumping argument, grammar residue/converse proof, both enumeration conventions, and paradigm matching were reviewed.

Solutions are instructional rather than answer-only: numerical items expose intermediate calculations; algorithmic items use traces/invariants or complexity arguments; mathematical items give derivations/counterexamples. Concise conceptual items do not require artificially long derivations. Some teaching checks repeat earlier reasoning, and inherited prose retains occasional missing spaces around numerals. These are editorial polish opportunities, not evidence of an unresolved essential-data or mathematical error found in this pass.

## Corrections made and explicit limitations

1. Q51: replaced the ambiguous sentence “Subtracting these removes every girl who fails to score strictly more than at least one boy.” with “Subtracting these removes every girl for whom at least one boy has marks greater than or equal to hers.” The remaining universal conclusion was already correct. No answer changed.
2. Q26: added a source note that option C follows GFG's grouped exponent (n²+n)/2; GateForum p6 has malformed parentheses. The mathematically correct option and answer were not changed.
3. Q66: added a source note that option B is 10011100 in GFG p9 but 10111100 in GateForum p17. Both sources agree on the correct option A. No option was changed; the existing GFG reading is explicitly identified.
4. All 90 fresh review statuses now read reviewed-with-caveats. Builder and checker were updated consistently. Existing inherited review/provenance/discrepancy fields were not overwritten.

Confirmed substantive source qualifications include Q23, Q24, Q33, Q41, Q45, Q48, Q57, Q70, Q71 and Q82. GFG Q82 visually appears to use a capital O in option D, while GateForum clearly uses lowercase o; the candidate explicitly chooses GateForum's reading. Q26/Q66 are additional minor option variants. GateForum also contains typographical defects such as a missing option label in Q72; the candidate follows the legible GFG alternatives rather than reproducing every typesetting defect.

The GateForum cover instructs candidates to choose the closest numerical answer. This supports presenting Q49's power-of-two choice as an approximation, while retaining the exact inode capacity. It does not establish that an official key selected that option. Nor does it remove Q47's important two-level paging-model distinction.

The candidate intentionally contains editorial assumptions and clarifications (for example distinct traversal labels, no overflow, standard unit-cost models, initial cache state, independent draws), not a verbatim diplomatic transcription. Q73 interprets “necessary” as the minimal offered sufficient augmentation; Q75 treats colour pairs as unordered. Q89 genuinely depends on whether enumeration may repeat words. Source/model qualifications remain part of the accepted result and must not be dropped when presenting answers.

## Checks, audit, and reproducibility

The author checker passed after the edits: 90 ordered IDs, four options each, protected fields unchanged from baseline, word counts/step consistency, shared contexts present, null official answers and no original-official-verification claims. Its selected arithmetic/structural checks also passed. This rerun is supporting evidence, not the independent review itself.

Fresh reviewer checks in `review2004/independent_checks.py` passed: exact permitted-field change scope, Boolean simplification truth table, BCD threshold for all valid digits, T-flip-flop excitation cycle, DFA simulation for all words of lengths 0–8, and both Q71 linear-system checks. Proof-based items were reviewed by reasoning, not claimed to have been exhaustively machine-proved.

`cs-2004-independent-depth-changes.json` records every candidate JSON field change with before/after values (187 changes: review metadata on all 90 records plus the explicitly described local edits). Builder/checker diffs are in `review2004/builder.diff` and `review2004/checker.diff`. Pre-review snapshots and page renders are in `review2004/`. Repository files were not edited.

Reviewed final candidate SHA-256:
- JSON: 3b4930caa0b06176ead13b304f5180bf1e71620f7fe3f49b86067554042b7b25
- Markdown: 792a468aa21974217d0c929f77833931f3f8eec24e9cbbed2ef83a31392b5730
