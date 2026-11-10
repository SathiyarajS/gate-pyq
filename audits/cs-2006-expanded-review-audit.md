# CS 2006 expanded-content independent review audit

Disposition: all 85 essential prompts and complete teaching solutions independently reviewed. One approved answer qualification (Q39), one tightened proof (Q51), and one equivalent grammar-notation consistency fix (Q84). No official paper or key authenticated. Original-source fidelity remains unverified; mathematical review is not official scoring verification.

## Evidence and actual scope

Read every candidate question, all 340 options, shared contexts and all solution steps. Visually inspected GFG physical pages 1–13 and GateForum pages 1–29 (29 is blank). Checked the four Q8 circuits; Q28 truth table; Q35 mux, Q36 complement bars, Q37 feedback, Q38 hazard bars, Q39 sign-bit bars, Q47 weighted graph, Q49/53/55–61 code, Q67–69 SQL/query plans, Q78–79 barrier code, Q80–81 traversal code, Q82–83 LAN wiring/forwarding tables, and Q84 grammar. Text extraction of GateForum is largely corrupted, so visual renders, not extracted glyphs, established notation.

Source files: /workspace/shared/gate1991-2006-research/2006-gfg.pdf and 2006-gateforum.pdf. Source URLs remain in each record. GFG pages were inspected using existing 2006-p1.png through 2006-p13.png. GateForum was rendered independently at 95 dpi; Q39 page 11 was additionally inspected at 200 dpi. Review evidence copies are in /workspace/shared/contributions/cs-2006-review-evidence/.

## Approved protected-field exception

CS-2006-Q39 derived_answer:
- Old: B
- New: B only under separate-literal complement reading; printed grouped bar is ambiguous

Parent approval received before editing: “Please preserve literal spanning-bar source and change derived_answer to the proposed conditional wording, with exact old/new exception audit, after checking both reproductions.” Both sources visibly place a continuous bar over the product of the operand sign bits in B. Literal ab¬c+¬(ab)c incorrectly signals overflow for four-bit −8+1=−7. The intended standard formula ab¬c+¬a¬bc is correct. Prompt, option B, and solution now distinguish the two readings. This is a source-notation qualification, not an official-key correction. No other protected field changed. Existing discrepancy IDs, review flags, official-null fields, provenance hashes, marks and subjects remain unchanged; the new issue is recorded in the existing editable essential_question_review rather than inventing a registry discrepancy ID.

## Other exact content amendments

Q51 old reasoning inferred Θ(2^h)=Θ(log n) from h=Θ(log log n), which alone is insufficient. New proof derives h=floor(log₂ log₂ n)+1 for n≥2 using iterated floor roots, then T=2^(h+1)−1 and log₂ n<2^h≤2log₂ n. Answer B unchanged.

Q84 solution production B→bB|b changed to B→Bb|b, matching its prompt and GateForum. Both generate the same positive unary b strings and have identical derivation lengths. No answer change.

Fresh review fields now indicate reviewed, not pending; inherited earlier review remains intact. Builder imports review_cs_2006_expanded.py so regeneration preserves amendments. Checker permits exactly the Q39 derived-answer exception and verifies everything else protected byte-for-value.

## Preserved limitations

Q1, Q38, Q40, Q47, Q66 and Q85 source variations remain explicit. Q17 nonunique traversal options; Q18 empty sample; Q49 strict bound; Q53 minus-one postconditions; Q70 two false closures; Q79 incomplete conceptual barrier repair; Q83 learning-table qualification remain. Q8 storage timing, Q14 swap model, Q24 empty sets, Q44 RTT serialization, Q56 Fortran model, Q64 time discretization and Q80 alignment are not silently promoted to official facts.

## Per-question findings

- Q1: Horner three products; cubic/quadratic reproduction conflict and special coefficients preserved.
- Q2: Power-set cardinality and independent function images give 2^(xyz).
- Q3: 3 inverse 7; 2 and 8 nonunits; closure counterexample retained.
- Q4: Reflexive partial-order convention distinguished from strict partial order.
- Q5: TTL loop prevention distinguished from time guarantee.
- Q6: Remaining times at arrivals 8 and 4; only two switches.
- Q7: LR closure does not advance dots; listed kernels separate.
- Q8: All four circuit inversion/clock/output connections verified; latch versus edge sampling caveat retained.
- Q9: 24-bit to three-byte conversion and implicit byte addressing stated.
- Q10: Leaf scan supplies matching linear bounds.
- Q11: Weight lower bound 2(n−1) attained by consecutive-vertex path.
- Q12: FIFO layers implement unit-weight Dijkstra in O(V+E).
- Q13: Right-child chain maximum index 2^n−1 verified.
- Q14: Swap-count convention and shift-based insertion exception explicit.
- Q15: Comma sequencing and exact halving sum checked computationally.
- Q16: Reduction directions yield R NP-hard, not necessarily NP-complete.
- Q17: Right-to-left constant-space method and left-to-right stack alternative both recognized.
- Q18: Empty subset probability and conditional expectation are explicitly distinguished.
- Q19: L1 grammar verified; L2 pumping directions and L3 triple-block argument adequate.
- Q20: Commit/undo-redo semantics and printed 1200 versus 12000 retained.
- Q21: Binomial count divided by 4^n correct.
- Q22: Both set expressions reduce to E intersection F minus G.
- Q23: Nonzero null vector and infinite affine solution line; dependent rows need not coincide.
- Q24: Intersection/union symmetry and nonempty-minimum precondition correct.
- Q25: Double incidence count yields 3n even with repeated subsets.
- Q26: Species union and sufficient implication direction correct.
- Q27: One assignment refutes both proposed tautologies.
- Q28: All truth-table rows and negation scopes checked.
- Q29: Prefix bounded imbalance finite-state versus final-only unbounded cancellation distinguished.
- Q30: 35-state residue update gives constructive regularity proof.
- Q31: Three-vertex path gadget forces Hamiltonian traversal; search-to-decision convention stated.
- Q32: Generated language is (ab+ba)*; ambiguity and aabb counterexample correct.
- Q33: Sigma-star and empty regular languages distinguish non-guarantee from universal falsehood.
- Q34: Numerical semigroup gaps and nine distinguishable unary states verified.
- Q35: Mux figure/select inputs and complemented y checked in both reproductions.
- Q36: Seven-term carry generate checked on 64 inputs; GateForum spanning bars retained in distractors.
- Q37: Feedback diagram and simultaneous nine-clock trace verified.
- Q38: All six ON adjacencies verified; A missing 13–15; C both bar readings invalid; D source mismatch unresolved.
- Q39: NEW correction: continuous bar over ab in both sources requires conditional B; signed-overflow counterexample and full truth check added.
- Q40: Current Gray indices and all next-bit ON sets checked; A minterm 3/5 difference retained.
- Q41: 32 chunks need two 92-ns rounds; decoder charged each round per text.
- Q42: Two branch fetch stalls give CPI 1.4 and 1.4 seconds.
- Q43: One-hot mask correct; unsigned C qualification protects bit 31.
- Q44: Bandwidth-delay product 40 packets; serialization convention noted.
- Q45: Each host applies its own /17 or /18 mask; asymmetry verified.
- Q46: Global attempts 5,10,15 lost; 16-attempt full-window trace checked conceptually.
- Q47: All 11 graph edges verified; GFG af versus GateForum df and D weight inversion explicit.
- Q48: DFS leaf neighbors form ancestor chain; highest ancestor yields containing cycle.
- Q49: Exact pushes n+t and pops t+d expose strict bound and unsuccessful-delete defects.
- Q50: Boolean XOR is symmetric difference; printed expression checked.
- Q51: Tightened proof to exact h=floor(log2 log2 n)+1 and T=2^(h+1)−1.
- Q52: Balanced median recursion includes selection cost; duplicate-key qualification retained.
- Q53: Code increment invariant k=i+j disproves printed −1 postconditions in both reproductions.
- Q54: Earliest prefix differences and direct-index bounded range; exhaustive check through length five.
- Q55: Both function bodies verified; alias example produces returns 3 and 2.
- Q56: Expression temporary traced separately from ib; actual Fortran limitations distinguished.
- Q57: Aliasing and signed-overflow limitations retained; invalid pointers may fault.
- Q58: FIRST(FR) and FOLLOW(R) produce correct table cells.
- Q59: Print-action ordering follows grammar, not conventional arithmetic precedence.
- Q60: Loop invariants, shared 4j and strength reduction versus unproven deadness explained.
- Q61: Atomic mutual exclusion distinguished from scheduler progress on one CPU.
- Q62: 20 VPN bits minus five set bits gives 15-bit tag.
- Q63: Equal address widths do not remove isolation need; can simplify cache remains qualified.
- Q64: Unit-time LRTF timeline computationally reproduced; completions 12,13,14.
- Q65: Overlapped initial I/O and final completion horizon produce idle 5/47.
- Q66: GateForum min versus GFG max verified; necessary versus sufficient resource conditions distinguished.
- Q67: Tie counting and inner-join omission of maxima checked; agreement only on empty database explicit.
- Q68: SQL result multiplicities and paid key prove B; no implicit DISTINCT.
- Q69: Both query-plan figures checked; bag projection duplicates and nonuniversal timing claims explained.
- Q70: All four closures recomputed; C and D false in both sources.
- Q71: Empty/singleton isolated; size-two vertices have proper-superset neighbors.
- Q72: Degree formula excludes self at k=2; ratio maximum k=3,4 checked.
- Q73: Pair-union paths connect all nonisolated vertices.
- Q74: Two-way parallel 18-bit comparison plus mux gives 2.4 ns.
- Q75: Direct-map 17-bit comparison gives 1.7 ns.
- Q76: Ternary parent-child indices reject A/B/C and accept D.
- Q77: Each of four insertion paths checked and final array reproduced.
- Q78: Explicit arrival-count 4 deadlock interleaving valid under pseudocode model.
- Q79: Conceptual entry gate not falsely presented as executable complete repair.
- Q80: Row-major 16 elements/block gives 16384 misses under aligned assumption.
- Q81: Column stride 32 cache lines cycles eight indices; simulation confirms all misses.
- Q82: All six LAN-port groups verified from both diagrams; B3 designated tie and DFS subtree order correct.
- Q83: All table groups checked including D typo; one broadcast does not learn every destination.
- Q84: Unequal-count decomposition correct; standardized solution B→Bb to match written GateForum production.
- Q85: Counts include start and epsilon steps; GFG duplicated option versus GateForum +3 retained.

## Deterministic validation

Ran build_cs_2006_expanded.py and check_cs_2006_expanded.py successfully. Existing checks cover Q15,28,34–38,40,54,64,70–73,76–77,80–81, including exhaustive binary-array pairs through length five, n=6 subset graph, 64 carry input patterns, and both full 512×512 cache traversals. Added all 256 four-bit signed input pairs for Q39 and the grouped-bar counterexample; Q51 exact depth checked for n=2 through 9999. These tests supplement, not replace, the item-by-item review above.
