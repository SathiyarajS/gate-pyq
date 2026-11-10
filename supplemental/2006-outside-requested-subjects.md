

# GATE 2006: Q23 (printed CS Q23)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203119/GATE2006.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** F is an n×n real matrix, b an n×1 real vector. Distinct vectors u,v satisfy Fu=b and Fv=b. Which is not necessarily true?
Options:
(A) det(F)=0
(B) Fx=b has infinitely many solutions
(C) A nonzero x satisfies Fx=0
(D) F must have two identical rows

## Solution

1. Since u≠v and Fu=Fv, the nonzero vector u−v lies in the null space. Hence F is singular and det F=0.

2. Every u+t(v−u), t real, is another solution, yielding infinitely many. Singularity does not force identical rows: F=[[1,2],[2,4]] is a counterexample.

3. Therefore D is false as a necessary assertion.

4. Teaching check: Subtract the two equations to obtain F(u−v)=0, with u−v nonzero. Linearity then lets any scalar multiple of this null vector be added to one solution. Dependent rows need not be identical rows, so determinant zero does not establish option D.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

