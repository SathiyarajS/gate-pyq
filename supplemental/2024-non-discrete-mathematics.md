

# GATE 2024 CS1: Q11

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=8), physical page **8**, printed **CS 11**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=8); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** Let f(x)=max{x,x³} for every real x. At exactly which points is f not differentiable? A {−1,1,2}; B {−2,−1,1}; C {0,1}; D {−1,0,1}.

## Solution

Approach: A maximum of smooth branches can have a corner where the winning branch changes. Find the crossings, then compare one-sided derivatives.
1. Solve x³=x: x(x−1)(x+1)=0, giving candidates −1, 0 and 1. Away from these points the larger expression is one fixed polynomial and is differentiable.
2. Testing the intervals gives f(x)=x for x<−1, f(x)=x³ for −1<x<0, f(x)=x for 0<x<1, and f(x)=x³ for x>1.
3. At −1, the left derivative is 1 and the right derivative is 3(−1)²=3. They differ.
4. At 0, the left derivative is 0 and the right derivative is 1. At 1, the left derivative is 1 and the right derivative is 3. These also differ.
Answer: D, {−1,0,1}. Equal function values at a crossing ensure continuity here, but do not ensure equal slopes.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS1: Q12

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=8), physical page **8**, printed **CS 12**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=8); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** Find the product of all eigenvalues of the matrix with rows (1,2,3), (4,5,6), (7,8,9). Options: A −1; B 0; C 1; D 2.

## Solution

Approach: The product of a square matrix's eigenvalues, counting algebraic multiplicities, equals its determinant. There is no need to solve its characteristic cubic.
1. Denote the rows by R1, R2 and R3. Observe R2−R1=(3,3,3) and R3−R2=(3,3,3).
2. Therefore R1−2R2+R3=0. This is a nontrivial linear dependence among the rows, so the matrix is singular and its determinant is zero.
3. Hence at least one eigenvalue is zero, making their product zero.
Answer: B. A direct determinant check gives 1(45−48)−2(36−42)+3(32−35)=−3+12−9=0. The sum of eigenvalues would instead be the trace 1+5+9=15; that is a different quantity.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS1: Q14

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=9), physical page **9**, printed **CS 14**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 9](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=9); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** A permutation of {1,2,…,n}, n≥4, is chosen uniformly. X means 1 occurs before 2; Y means 3 occurs before 4. Which statement is true? A X and Y are mutually exclusive. B They are independent. C At least one must occur. D X is more likely than Y.

## Solution

Approach: Use symmetry of label swaps; other elements and their positions do not affect the two order comparisons.
1. Swapping labels 1 and 2 pairs every permutation satisfying X with one not satisfying X. Thus P(X)=1/2. Similarly, swapping 3 and 4 shows P(Y)=1/2.
2. The first swap does not change Y, and the second does not change X. Starting from any permutation, independently applying these swaps produces all four truth combinations (X,Y), (X,not Y), (not X,Y), and (not X,not Y), each equally often.
3. Therefore P(X∩Y)=1/4=P(X)P(Y), proving independence.
Answer: B. The order 1,2,3,4 shows both events can occur, disproving mutual exclusivity. The order 2,1,4,3 shows both can fail, disproving C. Their equal probabilities disprove D.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS1: Q27

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=18), physical page **18**, printed **CS 27**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 18](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=18); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 1 mark(s).

**Official answer:** B;C

**Derived answer:** B;C

**Paraphrased problem context:** P(A)=0.3, P(B)=0.5 and P(A∩B)=0.1. Select all true claims: A A and B are independent; B P(A∪B)=0.7; C P(A∩Bᶜ)=0.2; D P(Aᶜ∩Bᶜ)=0.4.

## Solution

Approach: Compute the four disjoint regions of the probability space and check independence separately.
1. The overlap A∩B has probability 0.1. The part only in A has probability 0.3−0.1=0.2. This is A∩Bᶜ, so C is true.
2. The part only in B has probability 0.5−0.1=0.4. Adding the two exclusive parts and the overlap gives P(A∪B)=0.2+0.4+0.1=0.7, so B is true.
3. The region in neither event has probability 1−0.7=0.3, not 0.4. Hence D is false. The value 0.4 belongs to B without A, not to the complement of the union.
4. Independence would require P(A∩B)=P(A)P(B)=0.3×0.5=0.15. The supplied overlap is 0.1, so A is false.
Answer: B and C. As a check, the four disjoint probabilities 0.1, 0.2, 0.4 and 0.3 sum to 1.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS1: Q49

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=30), physical page **30**, printed **CS 49**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 30](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=30); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Paraphrased problem context:** For every n×m matrix A with m>n, which statements about Ax=0 are true? A There are at least m−n linearly independent solutions. B Exactly m−n independent vectors can span every solution. C Some nonzero solution has at least m−n zero coordinates. D Some solution has at least n nonzero coordinates.

## Solution

Approach: Rank-nullity gives the universal dimension guarantee, but it does not directly guarantee particular zero/nonzero coordinate patterns.
1. Let r=rank(A). Then r≤n, and dim ker(A)=m−r≥m−n. A nullspace basis therefore contains at least m−n independent solution vectors. A is true.
2. B demands a spanning set of only m−n independent vectors. If A is the zero matrix, its nullspace has dimension m, which is larger than m−n for n>0. Thus B is not universal.
3. For C, take n=2,m=3 and rows (1,0,1),(0,1,1). Solutions are x=(−t,−t,t). Every nonzero solution has all three coordinates nonzero, whereas m−n=1 zero coordinate is required. C is false.
4. For D, instead take rows (1,0,0),(0,1,0). Solutions are (0,0,t), with at most one nonzero coordinate, less than n=2. D is false.
Answer: A only. The counterexamples use different matrices because each universal statement may be refuted independently.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS1: Q63

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=35), physical page **35**, printed **CS 63**, variant **CS-2024-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 35](https://gate2026.iitg.ac.in/doc/download/2024/CS124S5.pdf#page=35); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.370 to 0.380

**Derived answer:** 0.375

**Paraphrased problem context:** A bag contains 10 red and 15 blue balls. Two are drawn uniformly without replacement. Given that the first draw is red, find the probability that both draws are red, rounded to three decimals.

## Solution

Approach: The first red draw is already known. Update the bag after that draw and compute only the remaining uncertainty.
1. Initially there are 25 balls. After the given red draw, one red ball has been removed, leaving 9 red and 15 blue balls, 24 in total.
2. Under this condition, “both balls are red” is equivalent to “the second ball is red”. Its probability is therefore 9/24=3/8=0.375.
3. A conditional-probability check gives P(first red and second red)/P(first red)=[(10/25)(9/24)]/(10/25)=9/24, confirming that the first-draw factor cancels.
Answer: 0.375, already expressed to three decimal places and within the official accepted interval 0.370–0.380. Multiplying by 10/25 without dividing by the conditioning probability would instead calculate the unconditional probability of two red draws.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS1FinalAnswerKey.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS2: Q16

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=12), physical page **12**, printed **CS 16**, variant **CS-2024-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 12](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=12); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** A continuous real function satisfies f(x)=1−f(2−x) for every real x. Find the integral of f(x) from 0 to 2. A 0; B 1; C 2; D −1.

## Solution

Approach: Pair each point x with its reflection 2−x across the midpoint 1.

1. Derivation. Let I=∫₀²f(x)dx. Substitution u=2−x gives∫₀²f(2−x)dx=I. Integrating f(x)+f(2−x)=1 therefore gives 2I=2, hence I=1, option B. Continuity ensures the integrals exist.

2. Explanation and checks. For the reflected integral let u=2−x, so dx=−du. The limits x=0 and x=2 become u=2 and u=0; reversing them cancels the minus sign. Thus both integrals have the same value although f itself need not be constant. The relation fixes f(1)=1/2 and fixes the interval average at 1/2, yielding area 2×1/2=1. Solving for a particular function is unnecessary. For example, f(x)=x/2 satisfies the identity and integrates to one, illustrating that the required value does not depend on f being constant.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS2FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS2: Q18

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=13), physical page **13**, printed **CS 18**, variant **CS-2024-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 13](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=13); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** Six independent unbiased dice are rolled. What is the probability all six face values are different? A 1/324; B 5/324; C 7/324; D 11/324.

## Solution

Approach: Count outcomes for distinguishable dice, or expose the dice one at a time.

1. Derivation. There are6⁶ equally likely outcomes for six labelled fair dice. All six faces are distinct exactly when the outcome is a permutation of 1 through6, giving6! possibilities. Probability=720/46656=5/324, option B.

2. Explanation and checks. The sequential calculation is (6/6)(5/6)(4/6)(3/6)(2/6)(1/6), because every new die must avoid all previously observed faces. This equals 6!/6^6. The dice may be rolled simultaneously, but labeling them for counting does not change their probabilities. There is only one unordered multiset containing all six faces, yet it corresponds to 720 ordered outcomes, so using 1/6^6 would undercount favorable outcomes.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS2FinalAnswerKey.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS2: Q44

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=31), physical page **31**, printed **CS 44**, variant **CS-2024-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 31](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=31); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** Random variables x,y lie in [0,1], may be dependent, and z=xy. Which always holds? A E[z]=E[x]E[y]; B E[z]≤E[x]E[y]; C E[z]≥E[x]E[y]; D E[z]≤E[x].

## Solution

Approach: Use a bound true for each outcome, which remains true after taking an expectation.

1. Derivation. Since0≤y≤1 and x≥0, pointwise xy≤x. Taking expectations preserves the inequality, giving E[xy]≤E[x], option D. No independence is assumed. If x=y is a fair0/1 variable, E[xy]=1/2>E[x]E[y]=1/4; if y=1−x, E[xy]=0<1/4. These examples rule out universal equality and both fixed comparisons with the product of means.

2. Explanation and checks. Multiplication by a number between zero and one cannot increase a nonnegative quantity, so xy≤x in every outcome; similarly xy≤y. No factorization of expectation is needed. To test the other answers take x equal to 0 or 1 with probability one half each. Choosing y=x makes the variables positively associated, while y=1−x makes them mutually exclusive. Their means remain one half in both examples, yet their product means differ, ruling out any universal product-of-means comparison.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS2FinalAnswerKey.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2024 CS2: Q47

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=32), physical page **32**, printed **CS 47**, variant **CS-2024-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 32](https://gate2026.iitg.ac.in/doc/download/2024/CS224S6.pdf#page=32); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A;B

**Derived answer:** A;B

**Paraphrased problem context:** B is obtained by swapping two rows of a real n×n matrix A. Select true statements: A det(B)=−det(A); B invertibility of A implies invertibility of B; C symmetry of A implies symmetry of B; D zero trace of A implies zero trace of B.

## Solution

Approach: Use the determinant rule for the positive claims and small explicit matrices to refute universal claims.

1. Derivation. A single row swap negates the determinant, proving A. If det(A) is nonzero then det(B)=−det(A) is nonzero as well, proving B. Symmetry is not preserved: swapping rows of diag(1, 2) gives[[0, 2],[1, 0]], which is not symmetric. Zero trace is not preserved: A=[[1, 2],[3,−1]] has trace0, but its row-swapped matrix has trace5. Answer A, B.

2. Explanation and checks. A row swap is multiplication on the left by an invertible permutation matrix P, so B=PA and B^−1=A^−1 P^−1 whenever A is invertible. This supplies another proof of B. In contrast symmetry would naturally be preserved by applying the same permutation to rows and columns, PAP^T, not by a row permutation alone. Trace invariance also applies to similarity transformations, not arbitrary independent row operations. The two counterexamples in the derivation make these distinctions concrete.

**Verification:** Independent second derivation review passed; [official Final Answer Key](https://gate2026.iitg.ac.in/doc/download/2024/CS2FinalAnswerKey.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

