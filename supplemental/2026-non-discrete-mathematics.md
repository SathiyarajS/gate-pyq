

**Scope note:** Non-discrete Engineering Mathematics is outside the 12 requested subjects; solution retained as supplemental coverage.

# GATE 2026 CS1: Q11

**Status:** Partial coverage. Independently derived and published official-key matched; independent second derivation review passed; final-key revision check pending.

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

**Status:** Partial coverage. Independently derived and published official-key matched; independent second derivation review passed; final-key revision check pending.

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

**Status:** Partial coverage. Independently derived and published official-key matched; independent second derivation review passed; final-key revision check pending.

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


# GATE 2026 CS1: Q32

**Question:** [Official paper page 23](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=23); consult original wording and options.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 3 to 3

## Solution

For positive x, rewrite the logarithm term as c2 ln(x). As x approaches zero from the right, ln(x) diverges, while e^x tends to 1. A finite right limit therefore requires c2=0. Continuity with the value at zero then requires c1=3. Hence c1+c2=3. The formula was checked visually to distinguish the logarithm argument and exponential.

**Verification:** Source diagram/notation visually inspected; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1) compared. Independent second derivation review passed; final-key revision verification pending.

**Scope:** Supplemental non-discrete mathematics, outside the requested subject list.


# GATE 2026 CS1: Q46

**Question:** [Official paper page 35](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=35); consult original wording and options.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A;C;D

## Solution

The factors are negatives of one another, so the function is minus the square of x-|x|/2. For x>=0 it equals -x^2/4; for x<0 it equals -9x^2/4. It has a strict local (and global) maximum at zero and no local minimum. The derivative is -x/2 on the positive side, -9x/2 on the negative side, and zero at the origin, so it is continuous everywhere. Its own one-sided derivatives at zero are -1/2 and -9/2, which differ; therefore f-prime is not differentiable on all of R. Select A,C,D. The source has |x| divided by 2, not |x| squared; visual inspection resolved this extraction ambiguity.

**Verification:** Source diagram/notation visually inspected; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=2) compared. Independent second derivation review passed; final-key revision verification pending.

**Scope:** Supplemental non-discrete mathematics, outside the requested subject list.


# GATE 2026 CS1: Q58

**Question:** [Official paper page 44](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=44); consult original wording and options.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 4.24 to 4.26

## Solution

Expectation is the probability-weighted sum. Grouping outcomes by their probability gives (1+2+5+7)/6 +(3+4+6+8)/12 =15/6+21/12 =4.25. The supplied probabilities sum to 4/6+4/12=1. Preserve the official accepted interval 4.24 to 4.26 rather than narrowing it to the computed central value. The two probability groups were checked visually.

**Verification:** Source diagram/notation visually inspected; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=2) compared. Independent second derivation review passed; final-key revision verification pending.

**Scope:** Supplemental non-discrete mathematics, outside the requested subject list.


# GATE 2026 CS2: Q14

**Question:** [Official master paper page 12](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=12); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

## Solution

Compare the density with (1/(σ√(2π))) exp(−(x−μ)²/(2σ²)). The coefficient gives σ=3 and the exponent gives μ=0 and 2σ²=18. Hence X is normal with mean 0 and variance 9, option B. It is not uniform or exponential, and a Poisson variable has a discrete probability mass function rather than this density.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.


# GATE 2026 CS2: Q27

**Question:** [Official master paper page 21](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=21); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 1 mark(s).

**Official answer:** A;C

**Derived answer:** A;C

## Solution

On the symmetric interval [−1,1], the odd term −ax integrates to zero. The remaining integrals are ∫3x² dx=2 and ∫1 dx=2. Hence I(a)=4 for every real a. It is independent of a and positive (indeed for all a), so A and C are true; B and D are false.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.


# GATE 2026 CS2: Q31

**Question:** [Official master paper page 22](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=22); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 24 to 24

**Derived answer:** 24

## Solution

Multiple solutions require the two linear equations to be dependent and consistent. The determinant is a²−16, so a=4 or a=−4. Multiplying the first equation by a gives a²x+ay=ab. Comparing with 16x+ay=24 gives ab=24. The consistent pairs are (a,b)=(4,6) and (−4,−6), both yielding the requested product 24.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.


# GATE 2026 CS2: Q62

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 48 to 48

**Derived answer:** 48 to 48

## Solution

Multiplying an n-by-n matrix by a scalar multiplies each of its n rows by that scalar, so the determinant scales by its nth power. Here det(2A)=2^4 det(A)=16*3=48.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.


# GATE 2026 CS2: Q63

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.5 to 0.5

**Derived answer:** 0.5

## Solution

Conditioning on two heads among tosses 1,2,3,5 leaves toss 2 equally likely to be head or tail by symmetry. Tosses 4 and 6 remain independent fair tosses because they are not involved in that condition. If toss 2 is a head, the target event needs at least one head among 4 and 6, probability 3/4. If toss 2 is a tail, it needs both heads, probability 1/4. Averaging gives (1/2)(3/4)+(1/2)(1/4)=1/2=0.5. Exhaustive enumeration of all 64 outcomes gave 12 satisfying both events out of 24 satisfying the condition.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.


# GATE 2026 CS2: Q64

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 40 to 40

**Derived answer:** 40 to 40

## Solution

Within each interval between consecutive tenths, the output is one on the second-decimal-digit bands 2–3 and 6–7, and zero elsewhere. It switches at offsets .02,.04,.06,.08 in each tenth: four jumps. There are ten tenth-sized intervals in (0,1), yielding forty discontinuities. Boundaries between tenths have zero on both sides and add none; zero and one are outside the domain. Use the customary decimal expansion that does not end in recurring nines. At a jump boundary, choosing the other representation changes a point value but does not remove the unequal one-sided limits.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.
