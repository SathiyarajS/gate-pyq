# GATE 2026 CS1: Q11

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=10), physical page **10**, printed **CS 11**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=10).

**Paraphrased problem context:** An urn starts with one red and one blue ball. Each step selects a ball uniformly, then returns it together with one additional ball of its color. Find the probability of equal red and blue counts after two steps. Options: 1/4, 1/3, 1/2, 2/3.

**Type / marks:** MCQ, 1.

**Official answer:** B

**Derived answer:** 1/3

## Solution

Givens and goal
An urn starts with one red and one blue ball. Each step selects a ball uniformly, then returns it together with one additional ball of its color. Find the probability of equal red and blue counts after two steps. Options: 1/4, 1/3, 1/2, 2/3.

Approach
Track the changing composition after the first draw; the two draws are not independent.

Step-by-step solution
1. Each step adds exactly one ball, so after two steps there are four balls. Equal color counts mean two red and two blue, which requires adding one ball of each color.
2. Thus the selected colors must be RB or BR. For RB, the first red has probability 1/2. The urn then contains two red and one blue, so the conditional probability of blue is 1/3. Therefore Pr(RB)=(1/2)(1/3)=1/6.
3. Symmetrically, Pr(BR)=(1/2)(1/3)=1/6. These ordered events are disjoint, giving total probability 1/6+1/6=1/3, option B.
4. As a check, RR has probability (1/2)(2/3)=1/3 and BB has the same probability. The four sequence probabilities sum to 1. The tempting result 1/2 comes from incorrectly retaining a 1/2 chance for each color on the second draw.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS1: Q13

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=11), physical page **11**, printed **CS 13**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=11).

**Paraphrased problem context:** For n>1, find the largest possible multiplicity of one eigenvalue of a real n-by-n matrix. Options: n, n−1, 1, n+1.

**Type / marks:** MCQ, 1.

**Official answer:** A

**Derived answer:** n

## Solution

Givens and goal
For n>1, find the largest possible multiplicity of one eigenvalue of a real n-by-n matrix. Options: n, n−1, 1, n+1.

Approach
Prove an upper bound from the characteristic polynomial, then exhibit a matrix attaining it.

Step-by-step solution
1. The characteristic polynomial det(λI−M) has degree n. Algebraic multiplicity counts how many times a root occurs in that polynomial, so no eigenvalue can have algebraic multiplicity larger than n.
2. The identity matrix I_n attains this bound: det(λI−I_n)=(λ−1)^n. Its eigenvalue 1 occurs with multiplicity n.
3. Therefore n is both an upper bound and achievable, giving option A. The choices n−1 and 1 are too small for I_n; n+1 is impossible for a degree-n polynomial.
4. If “multiplicity” were read as geometric multiplicity, the maximum is still n: the eigenspace {v:I_nv=v} is all of R^n and has dimension n. The algebraic/geometric distinction matters for some matrices, but not for this maximum.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS1: Q20

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=16), physical page **16**, printed **CS 20**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=16).

**Paraphrased problem context:** An n-by-n real matrix M, n>1, has e₂=(0,1,0,…,0) in its null space. Decide which claims must hold: A det(M)=1; B det(M)=0; C rank(M)=1; D its null space contains at least two nonzero vectors.

**Type / marks:** MSQ, 1.

**Official answer:** B;D

**Derived answer:** Singular matrix; at least two nonzero null vectors

## Solution

Givens and goal
An n-by-n real matrix M, n>1, has e₂=(0,1,0,…,0) in its null space. Decide which claims must hold: A det(M)=1; B det(M)=0; C rank(M)=1; D its null space contains at least two nonzero vectors.

Approach
Use Me₂=0 to infer singularity, then use closure of a vector space under scalar multiplication.

Step-by-step solution
1. Multiplication by e₂ selects M’s second column. Since Me₂=0, that column is the zero vector. In particular, M maps a nonzero input to zero and cannot be invertible.
2. A square matrix is singular exactly when its determinant is zero, so B is true and A is false. Equivalently, a zero column immediately forces determinant zero.
3. Null spaces are vector spaces. Since e₂ is in the null space, M(2e₂)=2Me₂=0 as well. The vectors e₂ and 2e₂ are distinct and nonzero, proving D. They need not be linearly independent; the statement asks only for two vectors.
4. Rank is not fixed by this information. The zero matrix satisfies the premise and has rank 0. The diagonal matrix diag(1,0,1,…,1) has rank n−1 and also satisfies it. Therefore C is not always true.
5. The guaranteed conclusion is rank(M)≤n−1 and nullity(M)≥1, with infinitely many nonzero null vectors over R. Select B and D.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS1: Q32

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=23), physical page **23**, printed **CS 32**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=23).

**Paraphrased problem context:** For x>0, f(x)=c₁e^x−c₂ln(1/x); for x≤0, f(x)=3. The constants are real. Continuity at zero is required. Find c₁+c₂ as an integer.

**Type / marks:** NAT, 1.

**Official answer:** 3 to 3

**Derived answer:** 3 to 3

## Solution

Givens and goal
For x>0, f(x)=c₁e^x−c₂ln(1/x); for x≤0, f(x)=3. The constants are real. Continuity at zero is required. Find c₁+c₂ as an integer.

Approach
Compare the right-hand limit with f(0), first eliminating any divergent contribution.

Step-by-step solution
1. Since f(0)=3 and f is constant 3 on the negative half-line, the value and left-hand limit already agree. Only the limit as x→0+ needs to be imposed.
2. Use ln(1/x)=−ln x to rewrite the positive branch as c₁e^x+c₂ln x. As x→0+, e^x→1 while ln x→−∞.
3. If c₂>0, the logarithmic term tends to −∞; if c₂<0, it tends to +∞. The exponential term has finite limit c₁ and cannot cancel either divergence. A finite right-hand limit therefore requires c₂=0.
4. With c₂=0, the right-hand limit is c₁. Continuity requires c₁=3, so c₁+c₂=3.
5. Checking the resulting function confirms it: its right branch is 3e^x and tends to 3 at zero. There is no need for the derivatives on the two sides to agree because the question asks only for continuity.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=1) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS1: Q46

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=35), physical page **35**, printed **CS 46**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=35).

**Paraphrased problem context:** For real x, f(x)=(|x|/2−x)(x−|x|/2). Determine which are true: A f has a local maximum; B f has a local minimum; C f′ is continuous on R; D f′ is not differentiable everywhere on R.

**Type / marks:** MSQ, 2.

**Official answer:** A;C;D

**Derived answer:** A;C;D

## Solution

Givens and goal
For real x, f(x)=(|x|/2−x)(x−|x|/2). Determine which are true: A f has a local maximum; B f has a local minimum; C f′ is continuous on R; D f′ is not differentiable everywhere on R.

Approach
Remove the absolute value separately on each side of zero, then inspect the function, its derivative, and the derivative’s one-sided slopes at zero.

Step-by-step solution
1. The two factors are negatives, so f(x)=−(x−|x|/2)^2. If x≥0, |x|=x and f(x)=−x²/4. If x<0, |x|=−x and f(x)=−9x²/4.
2. Both branches are negative away from zero and f(0)=0. Thus zero is a strict local and global maximum, making A true. The negative branch is strictly increasing toward zero, and the positive branch strictly decreases away from zero. No point is a local minimum, so B is false.
3. For x<0, f′(x)=−9x/2; for x>0, f′(x)=−x/2. At zero compute the difference quotient: f(h)/h equals −9h/4 from the left and −h/4 from the right. Both tend to 0, so f′(0)=0.
4. The one-sided limits of f′ at zero are also 0, and each branch is continuous elsewhere. Therefore f′ is continuous over all R, proving C.
5. To differentiate f′ at zero, divide f′(h)−f′(0) by h. The left limit is −9/2 and the right limit is −1/2. These differ, so f′ is not differentiable at zero. D is true.
6. Select A, C and D. Continuity of a derivative does not imply that derivative is itself differentiable. Here f is continuously differentiable but not twice differentiable at the joining point.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=2) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS1: Q58

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=44), physical page **44**, printed **CS 58**, variant **CS-2026-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Original question:** [Complete wording, options and figures](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf#page=44).

**Paraphrased problem context:** X takes values 1,…,8. Values 1,2,5,7 each have probability 1/6; values 3,4,6,8 each have probability 1/12. Find E[X] rounded to two decimals.

**Type / marks:** NAT, 2.

**Official answer:** 4.24 to 4.26

**Derived answer:** 4.25

## Solution

Givens and goal
X takes values 1,…,8. Values 1,2,5,7 each have probability 1/6; values 3,4,6,8 each have probability 1/12. Find E[X] rounded to two decimals.

Approach
Check normalization and evaluate the probability-weighted sum, grouping equal-probability outcomes.

Step-by-step solution
1. There are four values in each probability group. Their total mass is 4(1/6)+4(1/12)=2/3+1/3=1, so the stated distribution is normalized.
2. By definition E[X]=Σ_x x·Pr(X=x). The first group contributes (1+2+5+7)/6=15/6=2.5.
3. The second group contributes (3+4+6+8)/12=21/12=1.75.
4. Summing gives E[X]=2.5+1.75=4.25. This is already exact to two decimal places.
5. The unweighted average of 1 through 8 is 4.5, but that would assume equal probabilities of 1/8. Here the lower-sum first group carries twice the probability per value, so 4.25 is consistent with the extra weight on that group.

Result: 4.25. The published accepted numerical interval is 4.24 to 4.26, which is broader than the exact computed central value.

**Verification:** Independent answer and expanded teaching-depth review passed; [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf#page=2) compared. Final-key revision and complete question transcription remain uncertified.

**Discrepancy references:** See stated model assumptions.

# GATE 2026 CS2: Q14

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=12), physical page **12**, printed **CS 14**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 12](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=12); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** For every real x, f(x)=[1/(3√(2π))]exp(−x²/18) is a probability density. Is X A exponential, B normal, C Poisson, or D uniform?

## Solution

Givens and goal
For every real x, f(x)=[1/(3√(2π))]exp(−x²/18) is a probability density. Is X A exponential, B normal, C Poisson, or D uniform?

Approach
Match both the exponent and the normalization factor to a standard density.

Step-by-step solution
1. The normal density with mean μ and standard deviation σ is [1/(σ√(2π))]exp(−(x−μ)²/(2σ²)). The given coefficient implies σ=3.
2. The exponent has x² rather than (x−μ)² with a nonzero shift, so μ=0. Its denominator is 18=2×9=2σ², independently confirming σ²=9.
3. Thus X is N(0,9), a normal random variable, option B. The scale parameter 3 is the standard deviation, not the variance.
4. A uniform density is constant on its support; an exponential density has a linear exponent on a one-sided support; a Poisson law assigns discrete masses to nonnegative integers. None matches this smooth two-sided Gaussian density.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2026 CS2: Q27

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=21), physical page **21**, printed **CS 27**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 21](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=21); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 1 mark(s).

**Official answer:** A;C

**Derived answer:** A;C

**Paraphrased problem context:** For real a, I(a)=integral from −1 to 1 of (3x²−ax+1) dx. Select true statements: A independent of a; B can vary with a; C positive for some a; D negative for some a.

## Solution

Givens and goal
For real a, I(a)=integral from −1 to 1 of (3x²−ax+1) dx. Select true statements: A independent of a; B can vary with a; C positive for some a; D negative for some a.

Approach
Exploit symmetry and verify by an antiderivative.

Step-by-step solution
1. The only parameter-dependent term is −ax. It is odd in x, so its integral over the symmetric interval [−1,1] is zero for every fixed a.
2. The other contributions are ∫(−1 to 1)3x² dx=[x³] from −1 to 1=2, and ∫1 dx=2. Therefore I(a)=2+0+2=4.
3. Alternatively an antiderivative is x³−ax²/2+x. Its endpoint values are 2−a/2 and −2−a/2; their difference is again 4, making the parameter cancellation explicit.
4. A is true and B false because the result never changes with a. C is true, indeed for every a rather than merely some a. D is false because 4 cannot be negative. Select A,C. The integrand itself need not be positive everywhere for this conclusion.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2026 CS2: Q31

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=22), physical page **22**, printed **CS 31**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 22](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=22); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 24 to 24

**Derived answer:** 24

**Paraphrased problem context:** The system ax+y=b and 16x+ay=24 has multiple solutions for chosen real a,b. Find ab.

## Solution

Givens and goal
The system ax+y=b and 16x+ay=24 has multiple solutions for chosen real a,b. Find ab.

Approach
Require both singular coefficients and compatible right-hand sides.

Step-by-step solution
1. The coefficient matrix is [[a,1],[16,a]], with determinant a²−16. A nonzero determinant would give a unique solution; multiple solutions therefore require a²=16, or a=4 or a=−4.
2. Multiply the first equation by a: a²x+ay=ab. Under a²=16 its left side is identical to the second equation’s left side. Consistency then requires ab=24.
3. For a=4, choose b=6. The second equation is four times the first, leaving one free variable and infinitely many solutions. For a=−4, b=−6 likewise makes it −4 times the first.
4. Both admissible cases give ab=24. Setting only the determinant to zero is insufficient: for example a=4,b=5 would make the equations inconsistent, with no solutions rather than multiple solutions.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=1) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2026 CS2: Q62

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41), physical page **41**, printed **CS 62**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 48 to 48

**Derived answer:** 48 to 48

**Paraphrased problem context:** A is a 4×4 matrix with det(A)=3. Compute det(2A).

## Solution

Givens and goal
A is a 4×4 matrix with det(A)=3. Compute det(2A).

Approach
Apply determinant multilinearity once for each row.

Step-by-step solution
1. Multiplying a single row by a scalar c multiplies the determinant by c. This is one of the multilinearity properties of the determinant.
2. The matrix 2A multiplies every entry by 2, which is equivalent to multiplying each of its four rows by 2. Factoring a 2 out of each row therefore gives det(2A)=2×2×2×2×det(A).
3. Substitute det(A)=3: det(2A)=2⁴×3=16×3=48.
4. The tempting value 2×3=6 would be appropriate for scaling only one row, not the whole matrix. One can also verify using 2A=(2I₄)A and det(2I₄)=16, followed by determinant multiplicativity.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2026 CS2: Q63

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41), physical page **41**, printed **CS 63**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.5 to 0.5

**Derived answer:** 0.5

**Paraphrased problem context:** Six independent fair coin tosses define E1: at least two heads among tosses 2,4,6; E2: exactly two heads among tosses 1,2,3,5. Find P(E1|E2) to one decimal place.

## Solution

Givens and goal
Six independent fair coin tosses define E1: at least two heads among tosses 2,4,6; E2: exactly two heads among tosses 1,2,3,5. Find P(E1|E2) to one decimal place.

Approach
Condition on the shared toss 2, leaving tosses 4 and 6 independent.

Step-by-step solution
1. E2 concerns four positions and permits C(4,2)=6 equally likely arrangements of their two heads. Of these, C(3,1)=3 have toss 2 as a head and C(3,2)=3 have it as a tail. Therefore P(H2|E2)=P(T2|E2)=1/2.
2. Tosses 4 and 6 are not constrained by E2, so conditional on E2 they remain independent fair tosses and independent of the constrained four positions.
3. If toss 2 is a head, E1 requires at least one head among 4 and 6. Its probability is 1−P(T4T6)=1−1/4=3/4. If toss 2 is a tail, E1 requires both remaining tosses to be heads, probability 1/4.
4. By total probability, P(E1|E2)=(1/2)(3/4)+(1/2)(1/4)=1/2=0.5.
5. A direct counting check gives 6×4=24 full six-toss outcomes satisfying E2. Favorable outcomes number 3×3+3×1=12, again 12/24=0.5. The events share toss 2, so conditional reasoning should not be replaced by an unsupported assertion of independence.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2026 CS2: Q64

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41), physical page **41**, printed **CS 64**, variant **CS-2026-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official master paper page 41](https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 40 to 40

**Derived answer:** 40 to 40

**Paraphrased problem context:** For r in (0,1), f(r)=1 if the second decimal digit is 2,3,6,or 7, and 0 otherwise. Count discontinuities, using the customary decimal representation not ending in recurring nines.

## Solution

Givens and goal
For r in (0,1), f(r)=1 if the second decimal digit is 2,3,6,or 7, and 0 otherwise. Count discontinuities, using the customary decimal representation not ending in recurring nines.

Approach
Group neighboring hundredth intervals with the same output and count only actual changes.

Step-by-step solution
1. Fix a tenth interval with index k∈{0,…,9}. Write r=k/10+u with 0≤u<0.1, restricted to the open domain at the endpoints. Within this interval the second digit is j on u∈[j/100,(j+1)/100).
2. The output is 1 on u∈[0.02,0.04) and u∈[0.06,0.08), and 0 on the remaining parts. Adjacent digit bands 2 and 3 merge into one constant segment; bands 6 and 7 likewise merge.
3. The one-sided limits differ at exactly u=0.02,0.04,0.06,0.08. Each tenth interval therefore contributes four jumps at r=k/10+d/100, d∈{2,4,6,8}.
4. At the boundary between successive tenths, the output is 0 immediately to both sides: digit 9 on the left and digit 0 on the right. Hence those boundaries add no discontinuities. The domain excludes 0 and 1.
5. There are 10×4=40 distinct jump points. At every other point a small enough neighborhood stays in a constant-output region, establishing continuity there.
6. Terminating decimals also have recurring-nine representations. Without a convention the digit-based definition is ambiguous at some points. The standard non-recurring-nine convention makes f single-valued; at the jump points the alternative representation can change the assigned value but cannot equalize the unequal one-sided limits.

**Verification:** Independent second derivation review passed and [published key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf#page=2) compared. Final-key revision provenance and complete question transcription are not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; any model assumptions are stated in the solution.

**Scope:** Supplemental non-discrete Engineering Mathematics.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

