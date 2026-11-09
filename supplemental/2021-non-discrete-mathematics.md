

# GATE 2021 CS1: Q28 (printed CS Q18)

**Question:** [Official archived paper page 20](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=20); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.35 to 0.39

**Derived answer:** 0.37

## Solution

For an exponential lifetime with rateλ, E[X]=1/λ and P(X>t)=e^(−λt). Therefore P(X>E[X])=e^(−1)≈0.367879, rounding to 0.37, within the official0.35–0.39 range. The result is the same if parameter2 is expressed as a scale rather than rate.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS1: Q30 (printed CS Q20)

**Question:** [Official archived paper page 21](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=21); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.25 to 0.25

**Derived answer:** 0.25

## Solution

Rationalize the numerator: (√(2x+22)−4)/(x+3)=2/(√(2x+22)+4) for x≠−3. Taking x→−3 gives 2/(4+4)=1/4=0.25.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS1: Q45 (printed CS Q35)

**Question:** [Official archived paper page 29](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=29); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

## Solution

For finite second moments, Cauchy–Schwarz gives Cov(X, Y)²≤Var(X)Var(Y), contradicting S1’s strict greater-than claim. S2 incorrectly inserts absolute values. For a nonconstant mean-zero random variable X and Y=−X, covariance is−Var(X), while the proposed expectation of absolute deviations is+Var(X). Both statements are false, D.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS1: Q62 (printed CS Q52)

**Question:** [Official archived paper page 40](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=40); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 3 to 3

**Derived answer:** 3

## Solution

The matrix is J-I, where J is the 4-by-4 all-ones matrix. The all-ones vector has eigenvalue 4 for J and therefore eigenvalue 3 for J-I. Every vector whose coordinates sum to zero has eigenvalue 0 for J and -1 for J-I; that subspace has dimension three. The full spectrum is 3,-1,-1,-1, so the largest eigenvalue is 3.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS1: Q64 (printed CS Q54)

**Question:** [Official archived paper page 41](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=41); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0.04 to 0.04

**Derived answer:** 0.04

## Solution

Bayes rule gives P(sent H given received H)=P(received H given sent H)P(sent H)/P(received H). The diagram gives 0.3 for H-to-H and 0.8 for L-to-H. The numerator is 0.3*0.1=0.03, and the denominator is 0.3*0.1+0.8*0.9=0.75. The conditional probability is 0.03/0.75=0.04.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=3) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q32 (printed CS Q22)

**Question:** [Official archived paper page 65](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=65); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 15.00 to 16.00

**Derived answer:** 15.49

## Solution

For X~Binomial(1000, 0.4), variance is np(1−p)=1000·0.4·0.6=240. Standard deviation is√240≈15.4919, or15.49 to two decimals, within the official15.00–16.00 range.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q34 (printed CS Q24)

**Question:** [Official archived paper page 66](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 4 to 4

**Derived answer:** 4

## Solution

The nullspace is contained in the span of one nonzero vector, so its dimension is at most1. A4×5 matrix has rank at most4 and therefore nullity at least1. Hence nullity=1 and rank=5−1=4.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q35 (printed CS Q25)

**Question:** [Official archived paper page 66](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=66); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 19 to 19

**Derived answer:** 19

## Solution

The mean value theorem gives f(3)−f(−3)=6f′(c)≤12 for some c∈(−3, 3). Since f(−3)=7, f(3)≤19. The linear function f(x)=2x+13 attains equality, so 19 is the tight upper bound.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q39 (printed CS Q29)

**Question:** [Official archived paper page 70](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=70); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

## Solution

Attempting A first gives expected marks0.8·10+(0.8·0.5)·20=16. Attempting B first gives 0.5·20+(0.5·0.8)·10=14. The product terms use the stated independence. Hence A then B maximizes the expectation at 16, D.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q43 (printed CS Q33)

**Question:** [Official archived paper page 73](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=73); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

## Solution

Let Rk be the number of red balls after k draws and N=r+b. Given Rk, the expected red count after one more draw is Rk+Rk/(N+k). Therefore E[R_(k+1)/(N+k+1)|Rk]=Rk/(N+k). The expected red proportion remains r/N through all trials. The probability of red on trial4 is E[R3/(N+3)]=r/(r+b), A.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=5) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2021 CS2: Q47 (printed CS Q37)

**Question:** [Official archived paper page 76](https://gate2026.iitg.ac.in/doc/download/2021/cs_2021.pdf#page=76); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** B

**Derived answer:** B

## Solution

The displayed operation is the standard inner product. Pairwise orthogonal nonzero vectors are linearly independent: dotting a zero linear combination with any member forces its coefficient to vanish. In dimension10 there can be at most10 such vectors. The ten standard basis vectors attain that bound, so 10, B.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2021/cs_merged_2021.pdf#page=6) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.
