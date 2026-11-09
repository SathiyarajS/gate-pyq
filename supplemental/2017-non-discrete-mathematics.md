

# GATE 2017 CS2: Q20 (printed CS Q10)

**Question:** [Official archived paper page 5](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2-2017.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Let f(x)=R sin(πx/2)+S, with f′(1/2)=√2 and ∫₀¹ f(x)dx=2R/π. Find (R,S). A:(2/π,16/π). B:(2/π,0). C:(4/π,0). D:(4/π,16/π).

## Solution

1. Differentiate with respect to x, treating R and S as constants: f′(x)=R(π/2)cos(πx/2). At x=1/2, cos(π/4)=√2/2, so Rπ√2/4=√2. Cancel √2 to obtain R=4/π.

2. Integrate the original function: ∫₀¹ R sin(πx/2)dx=R[-(2/π)cos(πx/2)]₀¹=2R/π. The constant term contributes S.

3. The given integral equality therefore becomes 2R/π+S=2R/π, forcing S=0. The pair is (4/π,0), option C. The derivative condition alone cannot determine S.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS2: Q32 (printed CS Q22)

**Question:** [Official archived paper page 9](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 2.0 to 2.0

**Derived answer:** 2

**Source access:** Open archive member CS/CS2-2017.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** P=[[1,1,-1],[2,-3,4],[3,-2,3]] and Q=[[-1,-2,-1],[6,12,6],[5,10,5]]. Find rank(P+Q).

## Solution

1. Add corresponding entries to obtain A=P+Q=[[0,-1,-2],[8,9,10],[8,8,8]]. Rank concerns the number of independent rows or columns of this sum, not the sum of the separate ranks.

2. Row 3 equals row 1 plus row 2: (0,-1,-2)+(8,9,10)=(8,8,8). Therefore the three rows are dependent and rank(A)≤2.

3. Rows 1 and 2 are independent since the first coordinate of row 1 is zero while that of row 2 is 8, and row 1 is nonzero. Equivalently, the upper-left 2×2 minor has determinant 0·9-(-1)·8=8≠0. Thus rank(A)=2.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS2: Q36 (printed CS Q26)

**Question:** [Official archived paper page 10](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2-2017.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** P and Q may apply for a job. Given Pr(P)=1/4, Pr(P|Q)=1/2 and Pr(Q|P)=1/3, find Pr(not P | not Q). A:4/5. B:5/6. C:7/8. D:11/12.

## Solution

1. Conditional probability gives Pr(P∩Q)=Pr(Q|P)Pr(P)=(1/3)(1/4)=1/12. Use the other conditional to find Pr(Q): (1/12)/Pr(Q)=1/2, so Pr(Q)=1/6.

2. Inclusion-exclusion gives Pr(P∪Q)=1/4+1/6-1/12=1/3. Therefore the probability of neither event is Pr(not P∩not Q)=2/3.

3. Conditioning on not Q restricts the denominator to Pr(not Q)=5/6. Hence the requested probability is (2/3)/(5/6)=4/5, A. Independence was not given and must not be assumed; in fact the supplied conditional probabilities do not equal the unconditional ones.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS2: Q41 (printed CS Q31)

**Question:** [Official archived paper page 12](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Open archive member CS/CS2-2017.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For a discrete random variable X with probabilities p_j on j=0,…,N, define g_X(z)=Σ(j=0 to N)p_j z^j. Suppose g_Y(z)=(1−β+βz)^N with β∈[0,1]. Find E[Y]. A:Nβ(1−β). B:Nβ. C:N(1−β). D:not expressible from N and β alone.

## Solution

1. Differentiate the definition of the probability generating function: g′_Y(z)=Σ(j=1 to N)j p_j z^(j-1). Evaluating at z=1 leaves Σj p_j, exactly E[Y].

2. By the chain rule, differentiating the supplied polynomial gives g′_Y(z)=Nβ(1−β+βz)^(N-1). At z=1 the parenthesized expression is 1, so g′_Y(1)=Nβ.

3. Therefore B is correct. The generating function also identifies a binomial distribution, whose variance is Nβ(1−β), the distractor A. The mean formula remains valid for β=0 or 1 and for the degenerate N=0 case.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS2: Q62 (printed CS Q52)

**Question:** [Official archived paper page 21](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 5.0 to 5.0

**Derived answer:** 5

**Source access:** Open archive member CS/CS2-2017.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A real 3×3 matrix has characteristic polynomial λ³−4λ²+aλ+30. One eigenvalue is 2. Find the largest absolute value among its eigenvalues.

## Solution

1. An eigenvalue is a root of the characteristic polynomial. Substitute λ=2: 8-16+2a+30=0, so 2a+22=0 and a=-11.

2. The polynomial becomes λ³-4λ²-11λ+30. Divide by λ-2 to obtain λ²-2λ-15, which factors as (λ-5)(λ+3). The eigenvalues are therefore 2,5,-3.

3. Take absolute values before comparing: 2,5,3. Their maximum is 5. The requested quantity is the spectral radius, not the largest magnitude coefficient or the sum of eigenvalues. As a check the roots sum to 4 and their product is -30, consistent with the polynomial.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS1: Q13 (printed CS Q3)

**Question:** [Official archived paper page 3](https://web.archive.org/web/20170712112248id_/http://www.gate.iitg.ac.in:80/2017questions/CS1.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Archived July2017 original official paper and key. Page numbers refer to the paper PDF; key is a separate two-page PDF.

**Paraphrased problem context:** Let a1,...,an be column vectors in R^n and let scalars c1,...,cn, not all zero, satisfy Σ ci ai=0. Set A=[a1,...,an] and b=Σ ai. For Ax=b choose: A unique solution x=J (all-ones vector); B no solution; C infinitely many solutions; D finitely many solutions.

## Solution

1. A linear combination of columns is a matrix-vector product. Thus c≠0 and Ac=0, so A has nontrivial nullspace. Singularity alone does not tell us whether Ax=b is consistent.

2. Here b is specifically the sum of the columns. Therefore AJ=b for J=(1,...,1), establishing consistency.

3. For each real t, A(J+tc)=AJ+tAc=b. Since c≠0, different t give distinct solutions. There are infinitely many, C, not merely the known solution J.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20170712112242id_/http://www.gate.iitg.ac.in:80/2017answers/CS1.pdf) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS1: Q29 (printed CS Q19)

**Question:** [Official archived paper page 10](https://web.archive.org/web/20170712112248id_/http://www.gate.iitg.ac.in:80/2017questions/CS1.pdf#page=10); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.0 to 0.0

**Derived answer:** 0

**Source access:** Archived July2017 original official paper and key. Page numbers refer to the paper PDF; key is a separate two-page PDF.

**Paraphrased problem context:** X is Gaussian with mean 0 and variance σ². Let Y=max(X,0). Find the median of Y.

## Solution

1. For positive variance, symmetry of a zero-mean Gaussian gives P(X≤0)=1/2. The map max(X,0) sends every negative input to exactly zero.

2. Thus Y has no negative values and has probability 1/2 concentrated at zero. A median m satisfies P(Y≤m)≥1/2 and P(Y≥m)≥1/2; m=0 satisfies both.

3. For m<0 the first probability is zero; for m>0 the second is less than 1/2. Hence the median is 0. If variance is zero, Y is identically zero and the same answer holds.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20170712112242id_/http://www.gate.iitg.ac.in:80/2017answers/CS1.pdf) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS1: Q38 (printed CS Q28)

**Question:** [Official archived paper page 14](https://web.archive.org/web/20170712112248id_/http://www.gate.iitg.ac.in:80/2017questions/CS1.pdf#page=14); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Archived July2017 original official paper and key. Page numbers refer to the paper PDF; key is a separate two-page PDF.

**Paraphrased problem context:** Evaluate lim(x→1) (x^7−2x^5+1)/(x^3−3x²+2). A 0; B −1; C 1; D does not exist.

## Solution

1. Direct substitution gives numerator 1−2+1=0 and denominator 1−3+2=0, an indeterminate 0/0 rather than a value of zero.

2. Differentiate numerator and denominator: 7x^6−10x^4 and 3x²−6x. At x=1 both equal −3.

3. The denominator derivative is nonzero near 1, so the standard 0/0 limit rule applies. The limit is (−3)/(−3)=1, option C. Equivalently both polynomials have a common simple factor x−1 that cancels.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20170712112242id_/http://www.gate.iitg.ac.in:80/2017answers/CS1.pdf) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS1: Q40 (printed CS Q30)

**Question:** [Official archived paper page 14](https://web.archive.org/web/20170712112248id_/http://www.gate.iitg.ac.in:80/2017questions/CS1.pdf#page=14); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A for nondegenerate internal bisector

**Source access:** Archived July2017 original official paper and key. Page numbers refer to the paper PDF; key is a separate two-page PDF.

**Paraphrased problem context:** Nonzero vectors u,v in R² satisfy ||u||=2||v||. What α makes w=u+αv bisect their angle? A 2; B 1/2; C 1; D −1/2. The intended case is the internal bisector of a nonstraight angle.

## Solution

1. Simply adding u and v weights their directions unequally because their lengths differ. First normalize: û=u/||u|| and v̂=v/||v||.

2. The vector û+v̂ makes equal angles with the two unit vectors: its dot product with each is 1+û·v̂, and their norms are equal. Thus it points along the internal bisector when nonzero.

3. Multiply by ||u|| to obtain u+(||u||/||v||)v=u+2v. Therefore α=2, A. Zero vectors or opposite directions make this construction degenerate and are not the intended case.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20170712112242id_/http://www.gate.iitg.ac.in:80/2017answers/CS1.pdf) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2017 CS1: Q41 (printed CS Q31)

**Question:** [Official archived paper page 14](https://web.archive.org/web/20170712112248id_/http://www.gate.iitg.ac.in:80/2017questions/CS1.pdf#page=14); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Archived July2017 original official paper and key. Page numbers refer to the paper PDF; key is a separate two-page PDF.

**Paraphrased problem context:** A is an n×n real symmetric rank-2 matrix satisfying ΣiΣj Aij²=50. I: an eigenvalue must lie in [−5,5]. II: the eigenvalue of largest magnitude must be strictly greater than 5. Which necessarily hold? A both; B I only; C II only; D neither.

## Solution

1. For a real symmetric matrix, orthogonal diagonalization preserves the squared Frobenius norm: ΣAij²=trace(AᵀA)=Σλi². Rank 2 means exactly two eigenvalues are nonzero.

2. Thus λ1²+λ2²=50. If both had magnitude greater than 5, their squares would sum to more than 50, impossible. At least one is in [−5,5], proving I; any additional zero eigenvalues also satisfy it.

3. For II, A=diag(5,5) satisfies all premises but has largest eigenvalue magnitude exactly 5. Strictly greater is therefore not guaranteed. Answer B.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20170712112242id_/http://www.gate.iitg.ac.in:80/2017answers/CS1.pdf) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

