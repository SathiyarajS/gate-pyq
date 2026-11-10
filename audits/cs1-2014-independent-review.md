# Independent source, correctness and teaching-depth review: CS-2014-S1

## Verdict

PASS for the expanded contribution's essential-context access and teaching correctness, with the explicit source qualifications below retained. This is not blanket certification that every published single-choice answer is mathematically unique. No blocking new transcription, mathematical, diagram, code, or teaching defect was found. No contribution or repository content was modified. The contribution's pending review metadata remains unchanged for the integrating parent to manage.

Reviewed `/workspace/shared/contributions/cs1-2014-expanded.json` and matching Markdown, against `/tmp/gate-2014-CS.pdf`, physically inspected pages 6–22 (all sixteen question pages and the key). GA 1–10 normalize to Q1–10; CS 1–55 normalize to Q11–65. All options and numeric givens were checked visually, including graph arrows, NFA/DFA loops and accepting states, multiplexer input/select order and overbars, Banker's matrix, process table, C code, SQL, and Venn diagrams. The prose code equivalents retain execution semantics under the stated assumptions. Source anchors are consistent.

All 65 official answers/ranges were separately transcribed from page 22 and matched. All protected fields match the current repository baseline exactly. Both the author checker and independent review checker pass. The independent checker is `cs1-2014-independent-review.py` in this directory; it additionally checks the linear system, determinant interior value, Banker's safety orders, enumerated dice/grid counts, and Boolean truth tables. Source/key records and discrepancies were not changed.

## Per-question review ledger

Every entry below passed source fidelity and essential-context teaching depth. “Qualified” means the solution correctly distinguishes its convention from a literal unconditional claim.

- Q1–3: B, C, C. Idiom and contextual contrast explained; all distractors preserved.
- Q4: 96. Expansion subtracts the cross term 2, without unnecessarily solving for z.
- Q5: Qualified. Four distinct solutions require distinct positive roots. Repeated positive roots give two distinct solutions. Source contains no distinctness premise; qualification independently confirmed.
- Q6–7: C, B. Inference and necessary-assumption reasoning do not reverse causality or require all illnesses to be genetic.
- Q8: Qualified 850. Both discounts interpreted on the same total; sequential 855 explicitly distinguished. Source supports the key's additive interpretation, but does not resolve every everyday usage of discount wording.
- Q9: 48%. Table entries/categories visually checked; complementary scooter-owner count agrees.
- Q10: 6. Unordered pairs of corner segments correspond to six distinct interior triangular planes.
- Q11: D. Correct quantifier and implication negation.
- Q12: 0.25. Uniform-cut integral and symmetry correct.
- Q13: Confirmed source/key nonuniqueness. B and C preserve mutual reachability. Source C says path length at most two, so includes all original edges. Added edges abbreviate original paths; key B alone is incomplete.
- Q14: 1. Unique values (-11/5,19/5,7/5) satisfy all four equations.
- Q15: 0. Symmetry and distinct eigenvalues supply orthogonality; positive definiteness is unnecessary.
- Q16: C. Rolle plus nonzero interior determinant proves both derivative claims. The given pi/4 determinant was symbolically checked.
- Q17: A. Algebra and essential implicant argument correct; source overbars and all options preserved.
- Q18–19: 5 and 16383. Positional notation and opcode/register/immediate allocations correct.
- Q20: Qualified D. Source is legacy implicit-int main; valid pointer destination and successful-input/no-overflow assumptions are explicit.
- Q21–22: C and 1. Matrix DFS row scans and postorder subtree-size computation establish linear/quadratic costs appropriately.
- Q23: C. Every source arrow matches the prose graph; precisely PSRQ and SPRQ are valid.
- Q24: Qualified C. Standard pivot comparison model gives 10 versus at most 7. Implementation dependence is not hidden.
- Q25: C. Modulo-three construction and nonregular distractor reasoning valid; natural-number convention addressed.
- Q26: A. NFA transition set matches figure; active sets after 0011 correctly exclude q3.
- Q27–28: D and B. Constant folding distinguished from reuse; model-feature mapping justified.
- Q29: 3. Services 100,105,110 before 90; dynamic seek distances checked.
- Q30: Qualified D. Shared code and traditional many-to-one blocking assumption clearly separated.
- Q31: B. EFH closure and mandatory attributes show minimality.
- Q32: Interpretation-dependent, not certified as a definite key error. Composite-key arity makes S2 false. An assertion can express referential allowed-state constraints, but not cascading update actions by itself. This supports A under constraint-only equivalence and potentially D under full behavioral equivalence. Source does not specify that distinction; contribution responsibly leaves it unresolved.
- Q33: Qualified D. Textbook local-overhead/convergence comparison is presented as a model, not a theorem for every implementation; split horizon limitation explained.
- Q34–35: C and A. Hash/encryption classification and fresh HTTP/TCP dependency order correct; historical algorithm security and connection-reuse qualifications included.
- Q36: 28 or 30 microseconds. Ring propagation is 10; nine versus ten holding periods depends on timer origin. Both fit the actual key range.
- Q37: 1100 ms. Classic timeout reset, three slow-start rounds and eight additive rounds correct under stated accounting.
- Q38: 5 bits. Utilization window ceiling 12 and selective-repeat sequence space at least 24 correct with either KB convention.
- Q39: D. Conflict edges/cycles and serial order T2,T3,T1 verified.
- Q40: Qualified A. Proposed cover loses AB→E. Two-attribute BCNF proof needs nonempty determinants; empty-determinant counterexample is valid and retained.
- Q41: B. Exact matrices/requests visually checked; independently enumerated safety confirms REQ1 unsafe, REQ2 safe.
- Q42: 7.2 ms. SRTF timeline and turnaround values 8,2,7,14,5 verified.
- Q43: 7. Farthest-future replacement trace correct; hits are not counted as faults.
- Q44: D. Visually confirmed shift terminal is > and queried symbol is <; no competing reductions.
- Q45: C. Dovetailing recognizers yields a decider; relevant distinction explained.
- Q46: B. Exact DFA and expressions preserved. Strings ending in 1 are recognized; 0101 disproves expression II.
- Q47: 12. Excess weight 13 encodes bags 1,3,4, not sample-count product.
- Q48: Confirmed convention issue. Polynomial CLIQUE implies P=NP. Under standard many-one completeness, empty/universal languages prevent literal equality with NPC, so C is mathematically defensible and D requires excluding trivial languages or a different reduction convention. Venn alternatives are conveyed in text; no protected key edit.
- Q49: 148. Pairwise construction gives 50+49+49. The optimal lower bound is correctly stated, though its adversary proof is only sketched; sufficient for this essential-context teaching level.
- Q50: A. Nine residues, empty chains, and denominator for average checked.
- Q51: A. Full-array initialization handles all-negative inputs; every nonempty contiguous subarray enumerated. C's valid-array/index/no-overflow assumptions acknowledged.
- Q52: C. Counts j(n−j) triples and derives (n−1)n(n+1)/6 exactly.
- Q53: Qualified 4. Average stall penalty and steady-state assumption explicit; finite-N formula distinguished.
- Q54: Confirmed insufficient premise. Source says A≥k, but the guaranteed LRU reuse hit needs fewer than A competing same-set distinct blocks. x,y,x,y with A=k=1 is a valid counterexample. Cold-start assumption is also required for exactly n compulsory misses.
- Q55: A. Select order P,Q and data 0,1,R,not R match figure. Minimal SOP and isolated minterm reasoning checked.
- Q56: -2. Product-rule derivatives and identity correct.
- Q57: Confirmed nonunique answer. Source D contains the minus sign. Difference f(y)−f(y+1) and sum f(y)+f(2−y) both change signs from -2 to 2, proving A and D.
- Q58: 10. Deficit enumeration and stars-and-bars agree under fair independent dice model.
- Q59: 89. Ordered composition recurrence and empty-sequence base case correct.
- Q60: 16. Both function-count exponentiation levels handled correctly.
- Q61: 506. Horizontal/vertical/diagonal count independently enumerated; self-loops excluded.
- Q62: C. Nonisolated-vertex argument correct; explicit realizations validate other options.
- Q63: B. Exact-two truth table and source equivalence/negation signs checked.
- Q64: Qualified B. Row-value IN query has intended semantics including ties, after quoted/renamed identifiers. Literal source uses unquoted hyphens, including USING(dept-id), so syntax caveat is supported.
- Q65: 1.6 GHz. Time/CPI ratios and equal instruction-count assumption correct.

## Depth and presentation notes

All solutions have a genuine setup and a worked reasoning step, rather than an answer with padding. The repeated section labels are generic but do not substitute for reasoning. Simple aptitude/identification items appropriately remain short. Complex items contain the relevant invariant, recurrence, trace, algebra, counterexample or convention. Minor inherited missing spaces in some prose/algebra do not affect mathematical access and were not edited. Q49's lower-bound proof could be expanded for a proof-focused textbook, but is not a correctness blocker or a reason to withhold this expansion.

No new discrepancy IDs are proposed. Existing ambiguity disclosures must survive integration. Do not label Q32 as a definitively wrong official key or silently collapse Q13/Q48/Q54/Q57 into an unqualified official answer.
