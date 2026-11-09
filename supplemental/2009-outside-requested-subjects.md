

# GATE 2009: Q19 (printed CS Q19)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 4. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

## Solution

From strongest to weakest, content coupling reaches into another module’s internals; common coupling shares global state; control coupling passes control flags; stamp coupling passes a larger composite record; data coupling passes only needed data values. Thus I,II,III,IV,V, option A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2009: Q20 (printed CS Q20)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 4. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

## Solution

The logical3×3 grid is [ab,cd,cd], [ab,ef,gh], [ik,ik,gh]. Counting distinct vertically separated cells in each column gives2,3,2. Counting distinct horizontally separated cells in each row likewise gives2,3,2. Thus C. These counts refer to the visible cell regions after spans, not the number of underlying grid coordinates.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2009: Q25 (printed CS Q25)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

The integrand equals tan(π/4−x). Substitute u=π/4−x to obtain the integral of tan u from0 toπ/4. Its antiderivative is−ln(cos u), giving−ln(1/√2)=½ln2, D.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2009: Q49 (printed CS Q49)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

## Solution

I is true: the context diagram represents the entire system as a single process or bubble and shows its boundary interactions. II is false: external entities need not be repeated at every decomposition level; lower-level DFDs elaborate relevant processes and flows. III is true in conventional DFD notation: a DFD models data transformation and movement, not execution-control information. IV is false: a data store cannot directly exchange data with another store or an external entity; a process must intervene. Therefore I and III, option C. Supplemental topic: software engineering / structured analysis, outside the collection’s twelve core subject buckets.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2009: Q50 (printed CS Q50)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2009.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

Under the standard software-testing convention all three statements are true, option D. For a connected module with E control-flow edges and N nodes, V(G)=E−N+2. Adding a virtual exit-to-entry edge gives a strongly connected/closed flow graph whose cycle-space dimension is (E+1)−N+1=E−N+2, explaining statement I’s independent-circuit interpretation. For binary predicates V(G)=number of decisions+1 (II), and V(G) gives the number of independent paths in a basis-path test set (III). The circuit wording presupposes this conventional augmentation; the raw unaugmented graph has ordinary undirected cycle rank E−N+1. Likewise a multiway branch contributes outdegree−1 rather than one unless reduced to binary decisions. Supplemental topic: software engineering / testing, outside the twelve core subject buckets.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
