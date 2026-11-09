# Independent source, correctness and depth review: CS-2014-S3

## Outcome

All 65 expanded records pass essential-context source fidelity and teaching-depth review, with the qualifications below. This is not blanket certification of inherited official-key claims. All 16 question pages (physical 51–66) and the complete session-3 key (67) were rendered and visually inspected independently. Every answer/range matches the printed key. All solution text was read and reasoning checked. No answer, verification status, discrepancy ID, marks, subject, exclusion reason, page anchor or URL was changed. Pending review metadata is deliberately left for parent integration; this audit supplies the independent result.

The contribution contains 2,361 stem words and 5,243 solution words. All answers have substantive method, intermediate reasoning, and a conclusion rather than padded answer assertions. Mathematical proofs are proportionate to examination level. In particular Q46 states the non-DCFL theorem as known rather than pretending its midpoint intuition is a complete proof.

## Verified correction

Q51–65 contained **both** source_archive_member and source_access_note with `CS/CS3014.pdf`. The accompanying Markdown incorrectly claimed source_archive_member was already correct. The actual archive `/tmp/gate-official-CS.zip` contains `CS/CS2014.pdf` and no CS3014 member. Extracted member bytes exactly equal the inspected `/tmp/gate-2014-CS.pdf` (2,494,424 bytes; SHA-256 ffff763b2bde2242dfb7bac952947e2fee791ce99c23642907e76cd6b22641c9).

Corrected these 30 metadata values in contribution JSON only, plus the explanatory Markdown, reproducible builder and checker. The checker permits only this exact string substitution in those two fields, not arbitrary source metadata drift. Repository files were not edited. The companion JSON contains every old/new field value. All other protected fields remain baseline-identical.

## Full coverage ledger

- Q1–10, pages 51–52: All option letters and choices checked. Table rows total 44; total marks 133. GDP factor 107/120 yields 10.833% decrease. Graph values 2.5,3,2,1,1.5 confirmed visually. Octal difference 3142 checked. Linguistic inference and conditional constructions support the intended answers, subject to Q1 below.
- Q11–14, page 53: Contraposition; preimage intersection and counterexamples; subgroup divisibility; trace/determinant counterexample diag(3,-1,-1) all valid. Options faithful.
- Q15–19, page 54: Dimension bound and attainment correct. Integral absolute-value splitting gives 4π. Minterm required-one/don't-care separation and all complemented option literals match the page; two implicants give XNOR in Q,S. Multiplexer and slowest-stage period reasoning correct.
- Q20–22, page 55: Double matrix swap restores A. Polynomial is precisely X⁵+4X³+6X+5; six-operation refactoring is valid. Tree has R's three children T,U,V and U's child W; its nonbinary nature and assumed traversal convention are explicitly handled.
- Q23–27, page 56: Grid topology includes connector's upper pendant and right-middle pendant, with no diagonal edges. Simple-path/DFS correspondence and bipartite upper bound 19 are sound; a snake through both nine-vertex grids attains it. Central position is not median rank; quadratic worst case valid. Regex a*b*(ba)*a* and missing bab checked. Countability and optimizer reuse correct.
- Q28–32, page 57: Recursion qualification appropriate; high cohesion/low coupling correct. LRU trace faults at 1,2,3,4,8,9. Projection/selection nesting and all options faithfully represented. Prime means membership in at least one candidate key.
- Q33–36, page 58: Physical bit timing distinguished from data-link framing. Unstuffing deletes exactly the first zero after five ones. IPv4 fragment qualification explicit. All four prefix/interface pairs verified; /15 longest match gives interface 1.
- Q37–40, page 59: 32+10+8 fixed-field allocation yields 256 seconds. Fragment payload arithmetic 1480+1480+1424 and offset 370 correct. Both schedules transcribed exactly; S1 order T2,T3,T1 and S2 cycle T1↔T2 valid. Anti-join relational expression correctly distinguishes own/all dependents.
- Q41–45, page 60: Resource bound 7; SRTF schedule and waiting times 15,0,3,4; serial TLB weighted mean 122 ms all correct. DAG reduction accurately requires algebraic cancellation; ambiguity undecidability and other CFG decisions correctly distinguished.
- Q46–49, page 61: All language exponents/reversals and example 2CNF formula checked visually. DCFL choices, immediate-successor DP recurrence, SCC criterion, and O(log n+m) traversal all correct under stated models. Original second logarithm is log n, faithfully retained.
- Q50–51, page 62: All denominators are 100³ as transcribed. Chaining permits repeat slots. Recursive leftmost-child/right-sibling control flow and leaf-count interpretation verified against code.
- Q52–54, page 63: Two independent comparisons and do-while semantics faithfully retained. Equality terminates search correctly. Branch stage numbering and penalties give 1.54 within printed 1.50–1.60 range. Cache weighted mean and aggregate-only range distinction correct.
- Q55–58, page 64: Independently traced wire jump and JK inputs: J2=not Q1, K2=Q0; J1=Q2, K1=not Q2; J0=Q1, K0=not Q0. Next states 100,110,111 correct. Trapezoidal/Simpson statements, ∫x²cos x=-2π and complementary-event maximum 1/4 correct with explicit scope qualifications.
- Q59–62, page 65: Odd cardinality 2015 forces a fixed point in an involution; surjectivity and counterexample correct. Group relations yield commuting involutions and tight bound 4. Forest floor/ceiling distractors checked. Disconnected Euler formula used correctly to prove universal face lower bound.
- Q63–65, page 66: Negated universal formula, exact SQL predicate and Boolean complemented answer options checked. NULL caveat valid; XOR expression has three occurrences each of P,Q and reduces to XNOR.
- Page 67: Independently checked all 65 official entries, including numerical ranges and per-section numbering/marks.

## Inherited discrepancies and qualifications independently evaluated

- Q1: Progressive aspect is grammatically possible. D is an intended edit, not an unconditional grammatical theorem. Keep the discrepancy; the explanation does not erase it.
- Q21: The explicit six-operation computation disproves unrestricted minimum 7. Verified by expansion and evaluation at all integers -100 through 100. Six is only an upper bound; no unsupported optimality assertion.
- Q22: Source tree is genuinely nonbinary. The first-child/node/remaining-children extension produces option A; generic binary inorder alone does not specify it.
- Q28: General activation-record model supports D; bounded/tail-recursive special cases justify the retained caution.
- Q35/Q38: Received fragment versus reassembled datagram and unfragmented original assumptions remain important; numerical interpretation is correct.
- Q37: 256 follows conventional disjoint address/counter/time fields. It is not a uniqueness theorem for every imaginable ID encoding, and timestamps wrap.
- Q43/Q53: Serial single-level page-table lookup and steady-state pipeline assumptions are stated rather than concealed.
- Q44: Six-node/six-edge DAG uses cancellation and commutativity. Pure syntactic construction gives eight/ten. Do not reinterpret it as unconditional floating-point optimization.
- Q54: Overall 0.9 hit ratio alone allows mean 1.6+0.02w for w=0..20 write misses. The key 1.68 additionally assumes the intended class split. Qualification is mathematically correct.
- Q56: Convex trapezoidal overestimate uses forward limits; reversing limits reverses the error inequality. Intended C preserved.
- Q58: Maximum 1/4 is attainable among probability models satisfying the constraints, not necessarily in every fixed probability space.
- Q64: NULL-rated customers evade rating <> GOOD. Literal query means no known non-GOOD rating, so the non-NULL qualification is necessary.

No further substantive correction was needed. Source official revision designation remains unverified. These qualifications should remain visible during integration rather than be converted into unconditional verified claims.

## Reproducible checks

`contributions/check_cs3_2014_expanded.py` passes after the precise metadata exception. Additional independent checks exercised Q21 polynomial arithmetic; every length-0/1/2 regex word and missing bab; all nondecreasing arrays of lengths 1–7 over values 0..3 with search targets -1..4; three synchronous JK transitions; and all four XOR truth assignments. Computational results are in the companion audit JSON. Visual review, not OCR alone, established source fidelity.
