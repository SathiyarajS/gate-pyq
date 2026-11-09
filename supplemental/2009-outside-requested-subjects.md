

# GATE 2009: Q19 (printed CS Q19)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 4. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Rank coupling strongest to weakest: I content, II common, III control, IV stamp, V data. A I-II-III-IV-V; B V-IV-III-II-I; C I-III-V-II-IV; D IV-II-V-III-I.

## Solution

From strongest to weakest, content coupling reaches into another module’s internals; common coupling shares global state; control coupling passes control flags; stamp coupling passes a larger composite record; data coupling passes only needed data values. Thus I, II, III, IV, V, option A.

Teaching detail:
The ordering measures how much one module relies on another’s implementation. Content coupling directly accesses internals and is most intrusive. Common coupling shares globals; control coupling tells another module which action to take; stamp coupling passes a composite structure with more fields than needed; data coupling passes only the required values. Thus I-II-III-IV-V is the conventional ranking, A. This software-engineering topic is retained as supplemental coverage.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2009: Q20 (printed CS Q20)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 4. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** An HTML table has three rows. Row 1 contains ab with rowspan 2 and cd with colspan 2. Row 2 contains ef and gh with rowspan 2. Row 3 contains ik with colspan 2. Count visible cell regions per column and per row: A (2, 2, 3)/(2, 3, 2); B (2, 2, 3)/(2, 2, 3); C (2, 3, 2)/(2, 3, 2); D (2, 3, 2)/(2, 2, 3).

## Solution

The logical 3×3 grid is [ab, cd, cd], [ab, ef, gh], [ik, ik, gh]. Counting distinct vertically separated cells in each column gives 2, 3, 2. Counting distinct horizontally separated cells in each row likewise gives 2, 3, 2. Thus C. These counts refer to the visible cell regions after spans, not the number of underlying grid coordinates.

Teaching detail:
Expand the spans onto a three-by-three logical grid: row 1 ab, cd, cd; row 2 ab, ef, gh; row 3 ik, ik, gh. In column 1 the first two slots form one ab cell and the last is ik, giving 2 regions. Column 2 has cd, ef, ik, giving 3. Column 3 has cd then a two-row gh, giving 2. The same horizontal counting gives 2, 3, 2 by row. The question counts distinct drawn regions, not the three underlying grid positions in each direction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2009: Q25 (printed CS Q25)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Evaluate ∫₀^(π/4)(1−tan x)/(1+tan x) dx. A 0; B 1; C ln2; D(1/2)ln2.

## Solution

The integrand equals tan(π/4−x). Substitute u=π/4−x to obtain the integral of tan u from 0 toπ/4. Its antiderivative is−ln(cos u), giving−ln(1/√2)=½ln2, D.

Teaching detail:
Use tan(α−β)=(tanα−tanβ)/(1+tanαtanβ) with α=π/4. The integrand becomes tan(π/4−x). Set u=π/4−x; reversing the bounds cancels the minus from dx, leaving ∫₀^(π/4)tan u du. The antiderivative −ln(cos u) evaluates to−ln(1/√2)+ln1=(1/2)ln2. The interval contains no pole, so the substitution is valid throughout.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2009: Q49 (printed CS Q49)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** DFD assertions: I context diagram represents system as one bubble; II external entities must be identified at every level; III control information should not appear; IV stores may connect directly to another store or external entity. A II/III; B I/II/IV; C I/III; D I/II/III.

## Solution

I is true: the context diagram represents the entire system as a single process or bubble and shows its boundary interactions. II is false: external entities need not be repeated at every decomposition level; lower-level DFDs elaborate relevant processes and flows. III is true in conventional DFD notation: a DFD models data transformation and movement, not execution-control information. IV is false: a data store cannot directly exchange data with another store or an external entity; a process must intervene. Therefore I and III, option C. Supplemental topic: software engineering / structured analysis, outside the collection’s twelve core subject buckets.

Teaching detail:
A context diagram deliberately hides internal decomposition behind one process, so I describes its purpose. Lower-level diagrams refine relevant flows and need not duplicate every external entity, refuting II. Ordinary DFD arrows describe data rather than the temporal order or branching control of execution, supporting III. Data must pass through a transforming process between a store and another store/entity, refuting IV. These conventions select C; real-time DFD extensions require additional notation.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2009: Q50 (printed CS Q50)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Cyclomatic complexity assertions: I equals maximum independent circuits; II equals decisions+1; III gives independent paths for basis-path tests. A I/II; B II/III; C I/III; D all. Interpret circuit augmentation and binary-decision conventions explicitly.

## Solution

Under the standard software-testing convention all three statements are true, option D. For a connected module with E control-flow edges and N nodes, V(G)=E−N+2. Adding a virtual exit-to-entry edge gives a strongly connected/closed flow graph whose cycle-space dimension is (E+1)−N+1=E−N+2, explaining statement I’s independent-circuit interpretation. For binary predicates V(G)=number of decisions+1 (II), and V(G) gives the number of independent paths in a basis-path test set (III). The circuit wording presupposes this conventional augmentation; the raw unaugmented graph has ordinary undirected cycle rank E−N+1. Likewise a multiway branch contributes outdegree−1 rather than one unless reduced to binary decisions. Supplemental topic: software engineering / testing, outside the twelve core subject buckets.

Teaching detail:
For a connected single-entry/single-exit module, V=E−N+2. The independent-cycle interpretation uses a virtual edge from exit back to entry; omitting that augmentation gives cycle rank E−N+1 instead. Each binary predicate adds one independent alternative, yielding decisions+1, and those alternatives form a basis of test paths. Thus all three hold under the intended testing convention. Multiway decisions contribute more than one unless decomposed into binary predicates, so the wording is not an unrestricted graph theorem.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

