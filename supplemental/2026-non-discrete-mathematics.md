

**Scope note:** Non-discrete Engineering Mathematics is outside the 12 requested subjects; solution retained as supplemental coverage.

# GATE 2026 CS1: Q11

**Status:** Partial coverage. Independently derived and published official-key matched; peer review and final-key revision check pending.

**Question summary (paraphrased):** An urn starts with one ball of each of two colours. Twice, draw uniformly and return the ball with an extra matching ball. Find the probability of equal colour counts.

**Type / marks:** MCQ, 1 mark.

**Official answer:** B

## Solution

The final urn contains four balls. Equality requires one extra red and one extra blue, so the two selected colours must differ.

For red then blue: the first draw is red with probability 1/2. After reinforcement the urn has two red balls and one blue ball, so the second draw is blue with probability 1/3. This ordered event has probability 1/6.

By colour symmetry, blue then red also has probability 1/6. The events are disjoint, giving 1/6 + 1/6 = 1/3.

**Common pitfall:** The draws are not independent fair colour choices: reinforcement changes the second-draw probability.

**Discrepancy:** None identified in this derivation.

**Sources:** [Official paper page 10](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=10); [published official key page 1](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1). Accessed 2026-11-09. Final/revised status is not established.


**Scope note:** Non-discrete Engineering Mathematics is outside the 12 requested subjects; solution retained as supplemental coverage.

# GATE 2026 CS1: Q13

**Status:** Partial coverage. Independently derived and published official-key matched; peer review and final-key revision check pending.

**Question summary (paraphrased):** For real n-by-n matrices, n > 1, determine the largest possible multiplicity of a single eigenvalue.

**Type / marks:** MCQ, 1 mark.

**Official answer:** A

## Solution

The characteristic polynomial has degree n. Consequently, the algebraic multiplicity of any root is at most n.

Choose the identity matrix I_n. Its characteristic polynomial is (lambda - 1)^n, so the eigenvalue 1 has algebraic multiplicity n. Thus the upper bound is attained.

Even if multiplicity were interpreted geometrically, the answer remains n: every vector belongs to the eigenspace of I_n for eigenvalue 1.

**Common pitfall:** Distinct eigenvalues are not required; a repeated eigenvalue can account for the entire characteristic polynomial.

**Discrepancy:** None identified in this derivation.

**Sources:** [Official paper page 11](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=11); [published official key page 1](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1). Accessed 2026-11-09. Final/revised status is not established.


**Scope note:** Non-discrete Engineering Mathematics is outside the 12 requested subjects; solution retained as supplemental coverage.

# GATE 2026 CS1: Q20

**Status:** Partial coverage. Independently derived and published official-key matched; peer review and final-key revision check pending.

**Question summary (paraphrased):** A real n-by-n matrix, n>1, annihilates e2. Decide the guaranteed claims: determinant 1; determinant 0; rank 1; at least two nonzero null vectors.

**Type / marks:** MSQ, 1 mark.

**Official answer:** B;D

## Solution

The vector e2 is nonzero and M e2 = 0. Therefore M has a nontrivial null space and is singular. Its determinant is 0: B is true and A is false.

Null spaces are closed under scalar multiplication. Both e2 and 2e2 are distinct nonzero vectors in the null space, so D is true. This does not require them to be linearly independent.

The rank is not fixed at 1. The zero matrix satisfies the premise but has rank 0. More generally the premise only forces rank at most n-1, so C is not guaranteed.

**Common pitfall:** Two distinct nonzero null vectors need not be independent. Nullity 1 already supplies infinitely many nonzero vectors over the real field.

**Discrepancy:** None identified in this derivation.

**Sources:** [Official paper page 16](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=16); [published official key page 1](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1). Accessed 2026-11-09. Final/revised status is not established.
