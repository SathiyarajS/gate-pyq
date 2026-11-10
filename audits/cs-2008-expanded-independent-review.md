# Independent review of CS-2008 expanded contribution

## Outcome

Reviewed all 85 questions, all four options per question, and the complete solutions against all 18 physical pages of `/workspace/shared/gate-old-readiness/2008.pdf`. The source has no answer key. This review establishes source fidelity and mathematical/teaching adequacy, not official scoring correctness. The contribution is suitable for integration with its explicit source-defect qualifications and the two authorized Q60 protected-field exceptions below. No repository or external service was modified.

A substantive new defect was found and corrected: Q60 silently repaired the printed `z=*ppz` to `z=**ppz`. The scan was checked again by rendering physical page 12 directly from the PDF at 3000-pixel scale. It unambiguously prints one asterisk in the assignment. Source SHA-256: f01fcd02a9a5544d1f89959eca288fe967bb537ed00513b46e5fe8f9f97f7202. No alternate source or official key is claimed.

## Logged edits

1. Q60 question code: restored `**ppz += 1; z=*ppz;` exactly in dereference semantics. The solution now distinguishes the printed pointer-to-int constraint violation from the intended repaired calculation 7+7+5=19. The source's historical `void main()` convention does not fix the pointer assignment.
2. Q60 `derived_answer`: old `B`; new `B only if z=*ppz is repaired to z=**ppz; no portable numeric answer as printed`. This protected-field exception was expressly requested by the integrating parent after the new source finding.
3. Q60 `discrepancy_ids`: old `[]`; new `["CS-2008-Q60-source-code"]`. This is the second expressly requested protected-field exception. The new discrepancy is an unresolved source-code defect, not an official-key mismatch. `verification_status` remains `independently_solved`; `official_answer` remains null. `expansion_review.status` is `reviewed_source_defect` and its scope documents the condition.
4. Q54 solution: added a concrete limitation of statement V. Merely returning a global/noncapturing function does not rule out stack activation records; A is the intended answer under an escaping nested-closure assumption. Existing Q54 discrepancy metadata remains untouched.
5. Updated the contribution builder so these changes survive regeneration; regenerated JSON and Markdown. Updated its checker with exact, narrow Q60 exceptions rather than allowing arbitrary answer or discrepancy changes. Added an independent executable check and JSON results under this audit directory. Markdown explicitly warns about Q60 and no longer claims every baseline field is unchanged.

All other original fields outside the allowed transcription/solution/review fields are unchanged against repository questions.json. In particular all other derived answers, existing discrepancy IDs, official answers, source metadata, and earlier baseline-review metadata are preserved. Most expansion_review flags remain pending for integration; this external audit supplies the independent full review and should not be confused with the earlier baseline independent_review fields.

## Complete source coverage

- Page 1: paper instructions, Q1–20 versus Q21–85 marks, common-data and linked-pair structure checked.
- Page 2, Q1–7: limit, set complements, all matrix-system coefficients, IEEE choices, K-map row/column Gray order and don't-cares, each complemented literal in four K-map options, radix equation, graph complexity choices checked. K-map corners and second four-cell group match the source.
- Page 3, Q8–13: AND-then-OR circuit and minterm lists, prime-length language, four decidability statements, handle descriptions, optimization choices, complement-RE premise checked.
- Page 4, Q14–20: TCP sizes, quantifier negations, index choices, socket calls, nested conditional, BFS edges including QN and MR, and Unix choices checked. The queue trace produces QMNPRO.
- Page 5, Q21–28: integral limits/integrand/tolerance, Newton formula, planar choices, odd/even ranges, quartic coefficients, Boolean complements, transition probabilities and all four matrices checked.
- Page 6, Q29–35: normal tails and variance versus deviation, Q30 printed parentheses/quantifiers, propositional terms, disk and architecture statements/options checked.
- Page 7, Q36–43: all hazard and register-window statements, TLB options, growth functions, majority choices, B-tree order/insertion count, spanning-tree premise, and all four inequality recurrences checked.
- Page 8, Q44–48: encoding choices, every directed weighted edge of Q45, postorder/distinct-key premise, batch insertion permission, and recursive-enumerability choices checked. Negative edges do not break this particular Dijkstra execution.
- Page 9, Q49–51: both component automata and all sixteen offered product rows, all grammar statements/options, and matching models including cross-count exponents and copy/palindrome grammars checked. Product option A really has the wrong final row.
- Page 10, Q52–53: all start/final states and transition labels in all four NFAs, all four regular expressions and four matchings, and independent/equal/unequal count language restrictions checked. Textual graph equivalents are complete.
- Page 11, Q54–59: all five runtime statements, parser types, slow-start choices, subnet mask, token bucket quantities, and listener/client operation order checked. The answer explanations explicitly identify intended runtime/network assumptions.
- Page 12, Q60–62: pointer declarations and individual stars checked at higher resolution, full string-reversal body/main/options checked, and every linked-list assignment/guard checked. Q60 corrected as logged. Q61 correctly notes that its base case also prints the newline. The pairwise value swaps preserve all links.
- Page 13, Q63–66: both counting and binary semaphore algorithms, inequalities and release order, all I/O and deadlock choices, and fork loop checked. The semaphore solution appropriately avoids claiming whole-algorithm correctness and gives a lost-wakeup schedule.
- Page 14, Q67–70: all bit ranges and sizes, relational-algebra projections and nested set differences, schema attributes/FDs, and index block/pointer sizes checked.
- Page 15, Q71–73: the full common data (cache/page/block sizes, ways, address width, array dimensions and element size, row-major order, alignment, empty cache/no prefetch/no other references), loop and options checked. Each record repeats sufficient common data; write-allocation ambiguity is preserved.
- Page 16, Q74–76: both complete recurrence implementations and initializations, all big-Theta options, values at 8, and delay-slot choices checked. Coefficients multiply results, not recursive call counts.
- Page 17, Q77–81: all register dependencies, no-consecutive-zero wording, floor-subscript distractors, x5 options, all DP index bounds/OR/AND options, and one-way implication wording checked. Shared data is repeated sufficiently for independent reading.
- Page 18, Q82–85: ER arrows toward P, total participation lines, weak N/double identifying relationship and dashed partial key N1 checked; text faithfully encodes them. Every binary-search line, input option and proposed repair checked.

## Independent correctness and depth assessment

All 85 solutions were read and their reasoning checked, not inferred from the author's checker. Short elementary items are sufficiently worked: e.g. Q2 has 27 whitespace-counted words but explicitly performs distribution and De Morgan's law; it is not merely an answer assertion. Complex items include the required derivations, dependency/queue/pointer traces, graph/table equivalents, constructive algorithms, asymptotic arguments, or counterexamples. No artificial minimum word threshold was used.

Substantive source/interpretation qualifications independently confirmed:
- Q3 determinant is alpha−5; no offered exhaustive set is exact.
- Q21 A is a sufficient derivative-bound answer, not the literal minimum. Independent 50-digit direct trapezoidal summation confirms the two stated errors at n=2045 and 2046.
- Q30 A's x quantifier is scoped only in its antecedent; the displayed formula is not the intended universal implication. Other choices also fail under ordinary first-order semantics.
- Q34, Q35 and Q38 are architecture/model-qualified rather than universal physical necessities. Q37 includes reduced instruction fetches from omitted saves/restores.
- Q40 middle candidate plus two binary searches gives logarithmic time. Q41 split bound uses leaves/internal separators and covers both overflow and preemptive conventions. Q42's two K4s sharing a vertex establish the articulation counterexample.
- Q43's C is the immediate monotone upper bound; B needs an additional worst-split argument. The supplied solution does not pretend to know arbitrary pivot-selection overhead.
- Q49 product rows independently recomputed as P:(S,R), Q:(R,S), R:(Q,P), S:(P,Q). No printed option is correct.
- Q50 correctly separates right recursion from right-linear grammar and notes the epsilon-preservation issue.
- Q52 four NFA/regex pairs additionally checked on every binary word of lengths 0–12, 32,764 pair-word checks, with no mismatch.
- Q54 intended closure interpretation retained, but general statement V now explicitly qualified.
- Q60 new source-code defect described above. No unique portable numeric result follows from the printed program. B is conditional, not official.
- Q63 initial values are 1,0, but saturating binary-semaphore implementation can lose wakeups, as explained.
- Q67 table-pointer bits depend on 2-KiB alignment; the caveat is present. Q69 Collection is BCNF and therefore 3NF; option C does not say 'only'.
- Q73 hit ratio is 50% with write allocation versus 0% without; assumption disclosed.
- Q74 runtime is Theta(phi^n), not Theta(2^n); the scanned options really use Theta.
- Q79 enumeration/recurrence gives 13, missing from choices.
- Q81 both A and C satisfy the printed one-way implication; C is the full decision cell.
- Q84 nontermination checked; Q85 A still misses x=4 in [1,...,10] because i<j stops at an unexamined singleton.

## Reproducible checks and integration artifacts

- `/workspace/shared/contributions/check_cs2008_expanded.py`: passes after exact Q60 exceptions.
- `/workspace/shared/gate-pyq-contributions/check_cs2008_independent_review.py`: passes.
- `/workspace/shared/gate-pyq-contributions/cs-2008-expanded-independent-checks.json`: quantitative results and source hash.
- `/workspace/shared/gate-pyq-contributions/cs-2008-q60-discrepancy.json`: new source discrepancy and old/new protected-field audit.
- `/workspace/shared/contributions/cs-2008-expanded.json` and `.md`: regenerated corrected deliverables.

No blocker remains for integrating this qualified contribution. The integrator must retain Q60's new discrepancy/conditional answer and must not treat the unavailable official key as verified.
