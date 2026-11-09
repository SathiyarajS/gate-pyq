

# GATE 2025 CS1: Q23

**Question:** [Official archived paper page 23](https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf#page=23); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 1 mark(s).

**Official answer:** A;D

**Derived answer:** A;D

**Paraphrased problem context:** For real k, consider x+ky=1 and kx+y=−1. Select true claims: A exactly one k gives no solution; B infinitely many k give no solution; C exactly one k gives a unique solution; D exactly one k gives infinitely many solutions.

## Solution

Approach: Use the determinant to locate exceptional parameter values, then test consistency at those values.
The coefficient matrix is [[1,k],[k,1]], with determinant 1−k². For every k other than 1 or −1, this determinant is nonzero, so the system has a unique solution. There are infinitely many such k, which disproves C.
At k=1, the equations become x+y=1 and x+y=−1. Their left sides agree but their right sides do not, so no solution exists.
At k=−1, the equations become x−y=1 and −x+y=−1. The second is the first multiplied by −1, leaving one equation in two variables. All pairs (x,y)=(1+t,t) solve it, so there are infinitely many solutions.
There is exactly one inconsistent value and exactly one infinitely-solvable value, giving A and D. The record remains in its existing supplemental/excluded subject classification; the mathematics is included for paper completeness.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; model and counting conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS1: Q31

**Question:** [Official archived paper page 31](https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf#page=31); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** -2.1 to -1.9

**Derived answer:** -2.0

**Paraphrased problem context:** Let f(x)=ax+b for x<1 and f(x)=x³+x²+1 for x≥1. If f is differentiable everywhere, find b to one decimal place.

## Solution

Approach: Both pieces are polynomials, so only the join x=1 can cause a problem. Differentiability requires both continuity and matching one-sided derivatives there.
The right-hand value is f(1)=1+1+1=3. The left-hand limit is a+b. Continuity therefore requires a+b=3.
The derivative on the left is a. The derivative on the right is 3x²+2x, whose value at 1 is 5. Matching the slopes gives a=5. Substituting into the continuity equation yields b=3−5=−2.
Thus enter −2.0. Matching derivatives alone would determine a but leave b undetermined; the continuity condition is essential. Once both conditions hold, the polynomial pieces join differentiably and there are no other problematic points. The official accepted interval −2.1 to −1.9 remains unchanged. This supplemental calculus item retains its existing excluded subject label.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; model and counting conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS1: Q32

**Question:** [Official archived paper page 32](https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf#page=32); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.49 to 0.51

**Derived answer:** 0.50

**Paraphrased problem context:** A box contains four fair coins and one coin that always produces heads. Choose one of the five coins uniformly and toss that same coin twice. Given two heads, find the probability the chosen coin is the fake coin, to two decimal places.

## Solution

Approach: Use Bayes’ rule because observing heads changes the relative plausibility of the two kinds of coin.
Let F denote the fake coin and H denote the observed pair of heads. Before tossing, P(F)=1/5 and P(not F)=4/5. The fake always gives heads, so P(H|F)=1. With a fair coin, independent tosses give P(H|not F)=(1/2)²=1/4.
The total probability of two heads is P(H)=(1/5)×1+(4/5)×(1/4)=2/5. Consequently P(F|H)=P(F and H)/P(H)=(1/5)/(2/5)=1/2=0.50.
Two heads do not prove that the coin is fake: the combined four-coin fair alternative has exactly as much probability mass for this observation as the fake alternative. The official range 0.49–0.51 and the existing supplemental/excluded classification are retained.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; model and counting conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS1: Q41

**Question:** [Official archived paper page 41](https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** Let A=[[1,1],[1,−1]]. What are the eigenvalues of A^13? A 1,−1; B 2√2,−2√2; C 4√2,−4√2; D 64√2,−64√2.

## Solution

Approach: Look for a simple low power of the matrix before attempting thirteen multiplications.
Multiplying A by itself gives [[2,0],[0,2]]=2I. Therefore A^13=(A²)^6A=(2I)^6A=64A.
The characteristic equation of A is det(A−λI)=(1−λ)(−1−λ)−1=λ²−2=0, so its eigenvalues are √2 and −√2. Multiplying a matrix by 64 multiplies each eigenvalue by 64, giving 64√2 and −64√2 for A^13. Thus D is correct.
Equivalently, the eigenvalues of A^13 are (±√2)^13=±2^6√2. The negative eigenvalue remains negative because the exponent is odd. This gives a useful check on both sign and magnitude. Their sum is zero, consistent with trace(A^13)=64 trace(A)=0. The linear-algebra question remains in the existing supplemental/excluded subject classification.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; model and counting conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS1: Q58

**Question:** [Official archived paper page 58](https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf#page=58); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.300 to 0.302

**Derived answer:** 0.302

**Paraphrased problem context:** A continuous random variable has density p(x)=Cx² for 1≤x≤4 and p(x)=0 elsewhere. Find P(2≤X≤3) rounded to three decimal places.

## Solution

Approach: First determine C by total probability one, then integrate the normalized density over the desired interval.
Normalization requires 1=∫₁⁴Cx² dx=C[x³/3]₁⁴=C(64−1)/3=21C, hence C=1/21. This positive constant also ensures that the density is non-negative throughout its support.
Therefore P(2≤X≤3)=∫₂³x²/21 dx=[x³/63]₂³=(27−8)/63=19/63≈0.3015873016. To three decimal places this is 0.302, within the preserved official interval 0.300–0.302.
Because this is a continuous distribution, including or excluding either endpoint does not change the probability. The density is not uniform, so dividing interval lengths, (3−2)/(4−1)=1/3, would be incorrect. The density weights larger x more heavily. This calculus/probability item is retained for paper completeness while preserving its existing supplemental/excluded subject classification.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; model and counting conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q11

**Question:** [Official archived paper page 11](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=11); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Paraphrased problem context:** For A=[[1,2],[2,−1]], determine A^8.
Options: A. 25I; B. 125I; C. 625I; D. 3125I, where I is the 2×2 identity matrix.

## Solution

Square the matrix first rather than multiplying eight copies in sequence:
A²=[[1·1+2·2, 1·2+2·(−1)], [2·1+(−1)·2, 2·2+(−1)·(−1)]]
   =[[5,0],[0,5]]=5I.

Powers of the same matrix associate, so A^8=(A²)^4=(5I)^4=5^4 I=625I. Thus the diagonal entries are both 625 and the off-diagonal entries are zero. Notice that squaring 5I four times is not what is required: (A²)^4 means four factors of 5I. The other listed scalar multiples are neighboring powers of 5 but correspond to different even powers of A. Answer: C.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q12

**Question:** [Official archived paper page 11](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=11); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Paraphrased problem context:** Find x>1 satisfying ∫ from 1 to x of t ln(t) dt = 1/4.
Options: A. √e; B. e; C. e²; D. e^(−1).

## Solution

Use integration by parts with u=ln t and dv=t dt. Then du=dt/t and v=t²/2, giving
∫t ln t dt=(t²/2)ln t−(1/2)∫t dt=(t²/2)ln t−t²/4.
At t=1, this antiderivative equals −1/4. Therefore the definite integral is (x²/2)ln x−x²/4+1/4.

Set this expression equal to 1/4 and cancel the constants:
x²(2 ln x−1)/4=0.
The requirement x>1 rules out x=0 and gives ln x=1/2, hence x=e^(1/2)=√e. It satisfies x>1. The integrand t ln t is positive for t>1, so the definite integral is strictly increasing on the allowed interval, making this solution unique. D violates the domain restriction; B and C produce larger integrals. Answer: A.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q14

**Question:** [Official archived paper page 13](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=13); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Paraphrased problem context:** Nonsingular 3×3 matrices L,M,N satisfy L²=L^(−1), M=L^8, and N=L². Find det(M−N).
Options: A. 0; B. 1; C. 2; D. 3.

## Solution

Because L is invertible, multiply L²=L^(−1) by L to obtain L³=I. Its powers therefore repeat with period dividing three. Reduce the exponent 8 modulo 3:
L^8=(L³)² L²=I²L²=L².
Thus M=N, and M−N is the 3×3 zero matrix. Its determinant is zero, giving A.

Do not replace det(M−N) by det M−det N: determinants are not additive in that way. Also, the fact that M and N individually are nonsingular does not make their difference nonsingular. In this problem their difference is the clearest possible singular matrix, even though both original matrices have inverses.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q44

**Question:** [Official archived paper page 33](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=33); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A;B;C

**Derived answer:** A;B;C

**Paraphrased problem context:** A real 3×3 system PX=Q has an LU factorization P=LU. L is unit lower triangular, L=[[1,0,0],[l21,1,0],[l31,l32,1]], and U is upper triangular with diagonal u11,u22,u33. Select true statements.
A. Solve LY=Q first, then UX=Y, to solve PX=Q.
B. If P is invertible, both L and U are invertible.
C. If P is singular, some diagonal entry of U is zero.
D. If P is symmetric, both L and U are symmetric.

## Solution

Since PX=LU X, introduce Y=UX. The system becomes LY=Q followed by UX=Y, so A is valid. L has diagonal ones and is always invertible, making the first system solvable by forward substitution. The second is solved by backward substitution when U is nonsingular; if U is singular, its equations instead determine consistency and any free variables. A does not imply every original system has a unique solution.

The determinant of a triangular matrix is the product of its diagonal entries. Thus det L=1 and det P=det L·det U=u11u22u33. If P is invertible, this product is nonzero and both factors are invertible, proving B. If P is singular, the product is zero, so at least one diagonal entry of U is zero, proving C.

For D, take L=[[1,0,0],[1,1,0],[0,0,1]] and U=[[1,1,0],[0,1,0],[0,0,1]]. Their product P=[[1,1,0],[1,2,0],[0,0,1]] is symmetric, but L and U are not symmetric. Symmetry may relate suitable factors to each other's transposes; it does not make each triangular factor symmetric. Select A,B,C.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q64

**Question:** [Official archived paper page 47](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=47); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.5 to 0.5

**Derived answer:** 0.5

**Paraphrased problem context:** A monic quadratic over the complex numbers is called square-invariant when (x−α)(x−β)=(x−α²)(x−β²). Choose uniformly from all distinct such polynomials. What is the probability that its two roots are equal? Give one decimal place.

## Solution

Equality of monic polynomials implies equality of their root multisets, including multiplicity: {α,β}={α²,β²}. Squaring must therefore either fix both roots or swap them.

If it fixes each root, α²=α and β²=β, so each root is 0 or 1. Ignoring order, the possible multisets are {0,0},{0,1},{1,1}, giving x², x²−x, and (x−1)².

If it swaps two distinct roots, α²=β and β²=α. Substitute to get α^4=α, or α(α³−1)=0. The values α=0 or 1 would force β=α and do not give a distinct swapped pair. The remaining choices are the two nontrivial cube roots of unity ω,ω², which swap under squaring. Together they give one polynomial, (x−ω)(x−ω²)=x²+x+1, because ω+ω²=−1 and ω³=1.

There are therefore four distinct eligible polynomials, not four ordered root pairs. Exactly two, x² and (x−1)², have equal roots. Under uniform choice from these four polynomials, the probability is 2/4=0.5. The complex domain is essential for including x²+x+1. Answer: 0.5.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2025 CS2: Q65

**Question:** [Official archived paper page 48](https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf#page=48); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.70 to 0.80

**Derived answer:** 0.74

**Paraphrased problem context:** Choose a cut point U uniformly in (0,1), splitting the unit interval into two pieces. Let L be the length of the piece that contains the fixed point 0.4. Find E[L], to two decimal places. The event U=0.4 has probability zero.

## Solution

Condition on which side of 0.4 the random cut falls. If 0<U<0.4, the point 0.4 belongs to the right piece (U,1), whose length is 1−U. If 0.4<U<1, it belongs to the left piece (0,U), whose length is U. Since U has uniform density 1,
E[L]=∫_0^0.4(1−u)du + ∫_0.4^1 u du.

The first integral is [u−u²/2]_0^0.4=0.4−0.08=0.32. The second is [u²/2]_0.4^1=0.5−0.08=0.42. Adding them gives 0.74.

Alternatively, conditional means are E[1−U | U<0.4]=1−0.2=0.8 and E[U | U>0.4]=(0.4+1)/2=0.7. Weight by probabilities 0.4 and 0.6 to obtain 0.4·0.8+0.6·0.7=0.74. Do not average the two lengths with equal probability: the containing piece is selected by a fixed location, not by a fair choice between the pieces. The result is within the official range 0.70–0.80. Answer: 0.74.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

