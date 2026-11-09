

# GATE 2019 CS: Q19 (printed CS Q9)

**Question:** [Official archived paper page 5](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=5); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** For a square matrix X, compare I: X is invertible; II: det(X) is nonzero. Choices: A only I implies II; B only II implies I; C neither implication; D the two statements are equivalent.

## Solution

Method: prove each implication separately for an ordinary square matrix over the real or complex numbers.

1. Suppose X is invertible. Then XX^−1 = I. Taking determinants gives det(X)·det(X^−1) = det(I) = 1. A product equal to 1 cannot have a zero factor, so det(X) ≠ 0. Hence I implies II.
2. Conversely, suppose det(X) ≠ 0. The adjugate identity says X·adj(X) = det(X)I. Dividing by the nonzero determinant gives X·[adj(X)/det(X)] = I and similarly on the other side.
3. Therefore adj(X)/det(X) is an inverse of X, proving II implies I. Equivalently, a nonzero determinant means full rank and no nonzero vector in the nullspace.

Result: D, I and II are equivalent. The square-matrix assumption matters because ordinary two-sided invertibility and this determinant criterion are not defined in the same way for rectangular matrices.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=17) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2019 CS: Q23 (printed CS Q13)

**Question:** [Official archived paper page 6](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=6); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Paraphrased problem context:** Evaluate lim as x approaches 3 of (x^4−81)/(2x²−5x−3). Choices: A 1; B 53/12; C 108/7; D the limit does not exist.

## Solution

Method: resolve the 0/0 form by factoring; a limit depends on nearby values, so cancellation away from x=3 is legitimate.

1. Direct substitution gives numerator 3^4 − 81 = 0 and denominator 18 − 15 − 3 = 0. This indeterminate form does not itself mean the limit fails to exist.
2. Factor the numerator twice: x^4 − 81 = (x²−9)(x²+9) = (x−3)(x+3)(x²+9).
3. Factor the denominator: 2x² − 5x − 3 = (x−3)(2x+1).
4. For x≠3, cancel x−3. The quotient becomes (x+3)(x²+9)/(2x+1), whose denominator at 3 is 7, not zero.
5. Substitute into this continuous simplified expression: (3+3)(9+9)/(6+1) = 6×18/7 = 108/7.

Result: C. As an independent check, differentiating numerator and denominator in this 0/0 case gives 4·3³/(4·3−5) = 108/7 by l'Hôpital's rule; factoring is sufficient and requires less machinery.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=17) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2019 CS: Q32 (printed CS Q22)

**Question:** [Official archived paper page 8](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=8); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.502 to 0.504

**Derived answer:** 0.503

**Paraphrased problem context:** Choose two numbers independently and uniformly from {1,…,13}. Represent each as a four-bit unsigned binary number, including leading zeros. Find the probability that their most significant bits agree, rounded to three decimal places.

## Solution

Method: partition the sample space by the value of the leftmost four-bit position.

1. In four-bit unsigned representation, the most significant bit has weight 8. Numbers 1 through 7 have MSB 0; there are seven. Numbers 8 through 13 have MSB 1; there are six. Zero is not in the sampling set.
2. The MSBs agree in two disjoint cases: both draws come from the seven-number group, or both from the six-number group.
3. Independent draws give probability (7/13)² for the first case and (6/13)² for the second. The desired sum is (49+36)/169=85/169.
4. Numerically 85/169≈0.50295858, which rounds to 0.503.

Result: 0.503. Independence permits the same number to be drawn twice. Treating the draws as without replacement would change both denominators and the probability.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=18) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2019 CS: Q54 (printed CS Q44)

**Question:** [Official archived paper page 14](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=14); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 12 to 12

**Derived answer:** 12

**Paraphrased problem context:** R has rows (1,2,4,8), (1,3,9,27), (1,4,16,64), (1,5,25,125). Find the absolute value of the product of its eigenvalues.

## Solution

1. For any square matrix, the determinant equals the product of its eigenvalues, counted with algebraic multiplicity. Thus the requested value is |det R|; finding each eigenvalue individually is unnecessary.
2. Each row has the pattern (1,t,t²,t³), with t=2,3,4,5. This is a Vandermonde matrix. Its determinant is the product of (t_j−t_i) over every pair i<j.
3. There are six such pairs. Their differences are 3−2=1, 4−2=2, 5−2=3, 4−3=1, 5−3=2, and 5−4=1.
4. Multiply: det R=1×2×3×1×2×1=12. Because the t values appear in increasing order, the determinant is positive; the requested absolute value is therefore also 12.
5. The Vandermonde shortcut applies because columns are successive powers of the same row parameter, not merely because the entries increase. Standard elimination would give the same determinant, but numerical eigenvalue approximation introduces needless work and error.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=19) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2019 CS: Q57 (printed CS Q47)

**Question:** [Official archived paper page 14](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=14); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.8 to 0.8

**Derived answer:** 0.8

**Paraphrased problem context:** Y is uniformly distributed on (1,6). Find the probability that 3x²+6Yx+3Y+6 has only real roots, rounded to one decimal place.

## Solution

1. A real quadratic ax²+bx+c with a≠0 has real roots exactly when its discriminant Δ=b²−4ac is nonnegative. Here a=3, b=6Y, c=3Y+6.
2. Substitute and simplify: Δ=(6Y)²−4×3×(3Y+6)=36Y²−36Y−72=36(Y−2)(Y+1).
3. Throughout the support 1<Y<6, the factor Y+1 is positive. Thus Δ≥0 exactly when Y−2≥0, namely Y≥2. Intersecting with the support gives [2,6).
4. Uniform probability is favorable interval length divided by total interval length: (6−2)/(6−1)=4/5=0.8. This already has the requested one-decimal precision.
5. At Y=2 the quadratic has a repeated real root. Including or excluding that single boundary point does not change probability for a continuous uniform variable. The question asks for real roots, not positive roots; the negative sign of their sum is irrelevant.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2019/cs_2019.pdf#page=19) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

