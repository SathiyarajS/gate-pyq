

# GATE 2016 CS1: Q13 (printed CS Q3)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **4**, and locate printed **CS 3** in **CS-2016-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 4](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 1.0 : 1.0

**Derived answer:** 1

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate lim as x approaches 4 of sin(x−4)/(x−4), with angles in radians.

## Solution

Substitute u=x−4. The limit is lim(u→0) sin(u)/u=1, with angles in radians.

Direct substitution gives 0/0, which is indeterminate rather than the numerical answer 0. The substitution u=x−4 moves the approach point to 0 and exposes the standard sine limit. Equivalently, differentiability of sine at 0 gives sin u=u+O(u^3), so the quotient approaches 1 from either side. The radians convention matters: a sine measured in degrees has derivative π/180 at zero instead.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2016 CS1: Q14 (printed CS Q4)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **4**, and locate printed **CS 4** in **CS-2016-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 4](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.5 : 0.5

**Derived answer:** 0.5

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A probability density equals 1/x^2 on [a,1] and zero outside. Find a.

## Solution

Normalize the density: integral from a to 1 of x^−2 dx=1/a−1=1, yielding a=1/2. The support cannot cross zero because the integral there diverges.

A probability density must be nonnegative and have total area 1. Here its integral is [−1/x]_a^1=−1+1/a, provided 0<a<1. Solving the normalization equation gives a=1/2, and substituting back yields 2−1=1. An interval containing zero would make this improper integral diverge, so algebraic manipulations across that singularity would not define a probability distribution.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2016 CS1: Q15 (printed CS Q5)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **4**, and locate printed **CS 5** in **CS-2016-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 4](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 15.0 : 15.0

**Derived answer:** 15

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Two eigenvalues of a real 3×3 matrix P are 2+i and 3, where i^2=−1. Find det(P).

## Solution

A real matrix has conjugate nonreal eigenvalues, so alongside 2+i it has 2−i. The determinant is their product times 3: (4+1)·3=15.

The characteristic polynomial of a real matrix has real coefficients. Therefore if a nonreal number is a root, its complex conjugate is also a root with the same multiplicity. A3×3 matrix has three eigenvalues counting multiplicity, so the missing one is fixed as 2−i. Their product is the determinant; their sum would instead give the trace. Multiplying the conjugate pair first cancels the imaginary terms and yields 5, then multiplying by 3 gives 15.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2016 CS2: Q12 (printed CS Q2)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **26**, and locate printed **CS 2** in **CS-2016-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 26](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 9.0 : 9.0

**Derived answer:** 9

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Let f be a polynomial and g=f′. If degree(f(x)+f(−x))=10, find degree(g(x)−g(−x)).

## Solution

f(x)+f(−x) isolates twice the even-degree part of f, whose highest degree is 10. Differentiating gives g(x)−g(−x), and the nonzero degree 10 leading term becomes degree 9. Therefore9.

Write f(x)=Σa_k x^k. Adding f(−x) cancels odd powers and doubles even powers; a10 is therefore nonzero and all higher even coefficients vanish. The derivative difference cancels derivative terms from odd original powers and doubles those from even original powers. Even a higher odd degree of f cannot affect the answer.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2016 CS2: Q14 (printed CS Q4)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **26**, and locate printed **CS 4** in **CS-2016-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 26](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For systems of m linear equations in n variables: I if m<n all such systems have a solution; II if m>n none has a solution; III if m=n there exists a system with a solution. A all three; B II and III only; C III only; D none.

## Solution

I fails for an inconsistent underdetermined system, for example 0x+0y=1. II fails for a consistent overdetermined system, for example x=1 and 2x=2. III holds, for example the identity coefficient matrix with any right-hand side. Thus only III, C.

Compare ranks, not just numbers of equations: solvability requires rank(A)=rank([A|b]). Having extra variables permits free variables only after consistency is established. Having extra equations can still be consistent when those equations are redundant. The existential wording in III needs only one example, such as x1=…=xn=0.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2016 CS2: Q16 (printed CS Q6)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2016.pdf**, open physical PDF page **27**, and locate printed **CS 6** in **CS-2016-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 27](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.124 : 0.126

**Derived answer:** 0.125

**Source access:** Open archive member CS/CS2016.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Matrix A has eigenvalues 1,2,4. Find det((A^(−1))^T).

## Solution

det(A)=1·2·4=8. Inversion reciprocates the determinant and transpose preserves it, so det((A^−1)^T)=1/8=0.125.

No eigenvalue is zero, so A is invertible. The eigenvalues of A inverse are reciprocals 1,1/2,1/4, whose product is 1/8. Transposition leaves the characteristic polynomial, and hence the determinant, unchanged. The decimal 0.125 belongs to the preserved official tolerance interval.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

