

# GATE 2021 CS1: Q28 (printed CS Q18)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=20), physical page **20**, printed **CS 18**, variant **CS-2021-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 20](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=20); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.35 to 0.39

**Derived answer:** 0.37

**Paraphrased problem context:** A component lifetime X is exponentially distributed with parameter 2. Find P(X>E[X]), rounded to two decimal places.

## Solution

For an exponential lifetime with rateλ, E[X]=1/λ and P(X>t)=e^(−λt). Therefore P(X>E[X])=e^(−1)≈0.367879, rounding to 0.37, within the official 0.35–0.39 range. The result is the same if parameter2 is expressed as a scale rather than rate.

With rate λ=2 the mean is 1/2, so integrate the density: ∫_(1/2)^∞ 2e^(−2x)dx=e^(−1). Equivalently use the survival function. If the printed 'parameter 2' were interpreted as scale θ=2, the mean would be 2 and survival at that mean would still be e^(−2/2)=e^(−1). This invariant removes the rate-versus-scale convention issue for this particular question.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS1: Q30 (printed CS Q20)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=21), physical page **21**, printed **CS 20**, variant **CS-2021-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 21](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=21); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.25 to 0.25

**Derived answer:** 0.25

**Paraphrased problem context:** Evaluate lim(x→−3) (√(2x+22)−4)/(x+3), rounded to two decimal places.

## Solution

Rationalize the numerator: (√(2x+22)−4)/(x+3)=2/(√(2x+22)+4) for x≠−3. Taking x→−3 gives 2/(4+4)=1/4=0.25.

Direct substitution yields 0/0, an indeterminate form rather than an answer. Multiply numerator and denominator by √(2x+22)+4. The numerator becomes 2x+22−16=2(x+3), which cancels for x≠−3 in a punctured neighborhood. The remaining expression is continuous at −3. The derivative interpretation also works: the numerator is f(x)−f(−3) for f(x)=√(2x+22), so the limit is f'(−3)=1/4.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS1: Q45 (printed CS Q35)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=29), physical page **29**, printed **CS 35**, variant **CS-2021-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 29](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=29); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** S1: There exist random variables X,Y for which (E[(X−E[X])(Y−E[Y])])²>Var[X]Var[Y]. S2: For all X,Y, Cov[X,Y]=E[|X−E[X]| |Y−E[Y]|]. Which is correct? A both true; B S1 true/S2 false; C S1 false/S2 true; D both false. Variances/covariances are understood to exist.

## Solution

For finite second moments, Cauchy–Schwarz gives Cov(X, Y)²≤Var(X)Var(Y), contradicting S1’s strict greater-than claim. S2 incorrectly inserts absolute values. For a nonconstant mean-zero random variable X and Y=−X, covariance is−Var(X), while the proposed expectation of absolute deviations is+Var(X). Both statements are false, D.

Let U=X−E[X], V=Y−E[Y]. Cauchy–Schwarz says |E[UV]|≤√(E[U²]E[V²]); squaring establishes the opposite of S1's strict inequality. For S2 take X equally likely ±1 and Y=−X. Means are zero, Cov(X,Y)=E[−X²]=−1, while E[|X||Y|]=1. The sign information removed by absolute values is essential to covariance.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS1: Q62 (printed CS Q52)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=40), physical page **40**, printed **CS 52**, variant **CS-2021-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 40](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=40); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 3 to 3

**Derived answer:** 3

**Paraphrased problem context:** Find the largest eigenvalue of the 4×4 matrix whose diagonal entries are 0 and all off-diagonal entries are 1: rows (0,1,1,1),(1,0,1,1),(1,1,0,1),(1,1,1,0).

## Solution

The matrix is J-I, where J is the 4-by-4 all-ones matrix. The all-ones vector has eigenvalue 4 for J and therefore eigenvalue 3 for J-I. Every vector whose coordinates sum to zero has eigenvalue 0 for J and -1 for J-I; that subspace has dimension three. The full spectrum is 3,-1,-1,-1, so the largest eigenvalue is 3.

For any vector v, Jv is the vector whose four entries are sum(v). Thus v=(1,1,1,1) gives (J−I)v=3v. Every zero-sum vector gives (J−I)v=−v; examples (1,−1,0,0),(0,1,−1,0),(0,0,1,−1) form a basis for that three-dimensional subspace. These four independent eigenvectors account for the whole 4×4 matrix. The trace check 3−1−1−1=0 matches the zero diagonal.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS1: Q64 (printed CS Q54)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=41), physical page **41**, printed **CS 54**, variant **CS-2021-S1**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 41](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.04 to 0.04

**Derived answer:** 0.04

**Paraphrased problem context:** A sender transmits H with probability .1 and L with probability .9. Channel edge probabilities are P(received H|sent H)=.3, P(received L|sent H)=.7, P(received H|sent L)=.8, P(received L|sent L)=.2. Given that H was received, find the probability H was sent, rounded to two decimals.

## Solution

Bayes rule gives P(sent H given received H)=P(received H given sent H)P(sent H)/P(received H). The diagram gives 0.3 for H-to-H and 0.8 for L-to-H. The numerator is 0.3*0.1=0.03, and the denominator is 0.3*0.1+0.8*0.9=0.75. The conditional probability is 0.03/0.75=0.04.

Among an imagined 1000 transmissions, 100 are H and 900 are L. Expected received-H counts are 30 from sent-H and 720 from sent-L. Conditioning on received H therefore selects a population of 750, of which only 30 originated as H: 30/750=.04. The reversed conditional P(received H|sent H)=.3 is not the requested P(sent H|received H), because the prior probabilities differ greatly.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q32 (printed CS Q22)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=65), physical page **65**, printed **CS 22**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 65](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=65); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 15.00 to 16.00

**Derived answer:** 15.49

**Paraphrased problem context:** A coin independently gives heads with probability 0.4 on each of 1000 tosses. X counts heads. Find standard deviation of X to two decimals.

## Solution

For X~Binomial(1000, 0.4), variance is np(1−p)=1000·0.4·0.6=240. Standard deviation is√240≈15.4919, or 15.49 to two decimals, within the official 15.00–16.00 range.

Write X as the sum of 1000 independent Bernoulli indicators. Each has variance p(1−p)=0.24; independence makes variances add. Standard deviations do not add directly. Taking the square root only after the variance sum produces the requested units, number of heads.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q34 (printed CS Q24)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66), physical page **66**, printed **CS 24**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 66](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 4 to 4

**Derived answer:** 4

**Paraphrased problem context:** P is a 4×5 matrix and every solution of Px=0 is a scalar multiple of (2,5,4,3,1)ᵀ. Find rank(P).

## Solution

The nullspace is contained in the span of one nonzero vector, so its dimension is at most 1. A4×5 matrix has rank at most 4 and therefore nullity at least 1. Hence nullity=1 and rank=5−1=4.

Rank-nullity applies to the five-column linear map: rank+nullity=5. The statement only says every solution lies in the given line, not explicitly that every point on the line is a solution. Nevertheless the 4-row rank bound forces a nonzero nullspace, completing that missing direction and ruling out nullity zero.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q35 (printed CS Q25)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66), physical page **66**, printed **CS 25**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 66](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 19 to 19

**Derived answer:** 19

**Paraphrased problem context:** f is continuous on [−3,3], differentiable on (−3,3), f′(x)≤2 everywhere inside, and f(−3)=7. Find the largest possible f(3).

## Solution

The mean value theorem gives f(3)−f(−3)=6f′(c)≤12 for some c∈(−3, 3). Since f(−3)=7, f(3)≤19. The linear function f(x)=2x+13 attains equality, so 19 is the tight upper bound.

The mean value theorem needs continuity on the closed interval and differentiability inside, both supplied. It provides an actual intermediate derivative equal to the secant slope. An upper derivative bound is not an absolute derivative bound, so the problem gives no analogous finite lower bound on f(3). The attaining linear function proves tightness.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q39 (printed CS Q29)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=70), physical page **70**, printed **CS 29**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 70](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=70); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Paraphrased problem context:** Independent questions A and B are correct with probabilities 0.8 and 0.5, worth 10 and 20 marks. A wrong first answer yields zero; a correct first and wrong second yields only first marks; both correct yield 30. Choose order and expectation: A A then B,14; B B then A,14; C B then A,22; D A then B,16.

## Solution

Attempting A first gives expected marks 0.8·10+(0.8·0.5)·20=16. Attempting B first gives 0.5·20+(0.5·0.8)·10=14. The product terms use the stated independence. Hence A then B maximizes the expectation at 16, D.

Alternatively enumerate outcomes for A first: probability 0.2 earns 0; probability 0.8×0.5 earns 10; probability 0.8×0.5 earns 30. Expectation is 4+12=16. For B first, 0.5 earns zero, 0.5×0.2 earns 20 and 0.5×0.8 earns 30, totaling 2+12=14. Expected individual question value alone does not determine the order.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q43 (printed CS Q33)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=73), physical page **73**, printed **CS 33**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 73](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=73); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Paraphrased problem context:** Urn starts with r red,b black balls. Each trial draws uniformly, replaces the ball, and adds one more of that color. Four trials occur. Probability fourth draw is red? A r/(r+b); B r/(r+b+3); C (r+3)/(r+b+3); D product of (r+i)/(r+b+i) for i=0,1,2,3.

## Solution

Let Rk be the number of red balls after k draws and N=r+b. Given Rk, the expected red count after one more draw is Rk+Rk/(N+k). Therefore E[R_(k+1)/(N+k+1)|Rk]=Rk/(N+k). The expected red proportion remains r/N through all trials. The probability of red on trial 4 is E[R3/(N+3)]=r/(r+b), A.

A direct check on the second draw already shows the pattern: (r/N)((r+1)/(N+1))+(b/N)(r/(N+1))=r/N. Reinforcement makes successive colors dependent, but leaves the marginal probability unchanged. Option D is the probability that all four draws are red, which is stronger than only the fourth being red.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2021 CS2: Q47 (printed CS Q37)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=76), physical page **76**, printed **CS 37**, variant **CS-2021-S2**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 76](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=76); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** Define s(P,Q)=Σi P[i]Q[i] for real vectors. L consists of nonzero ten-dimensional vectors with s(P,Q)=0 for every distinct pair. Maximum |L|? A 9; B 10; C 11; D 100.

## Solution

The displayed operation is the standard inner product. Pairwise orthogonal nonzero vectors are linearly independent: dotting a zero linear combination with any member forces its coefficient to vanish. In dimension 10 there can be at most 10 such vectors. The ten standard basis vectors attain that bound, so 10, B.

If Σαi vi=0, dot with vj. Orthogonality removes every term except αj||vj||². Nonzero vj implies its squared norm is positive, hence αj=0. This is linear independence, so dimension bounds the set. Nonzero is essential: the zero vector is orthogonal to everything but would not contribute an independent direction.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=6) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

