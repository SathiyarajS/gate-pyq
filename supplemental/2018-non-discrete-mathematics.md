

# GATE 2018 CS: Q25 (printed CS Q15)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2018.pdf**, open physical PDF page **8**, and locate printed **CS 15** in **CS-2018**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.021 to 0.024

**Derived answer:** 0.023

**Source access:** Open archive member CS/CS2018.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Each of two players independently rolls a fair six-faced die per trial; ties cause a retry. Find the probability that the game first has a winner on trial 3, rounded to three decimals.

## Solution

Method and intermediate reasoning:

Of the 36 equally likely ordered roll pairs, six are ties: (1,1) through (6,6). The other 30 yield a winner, regardless of which player wins. To reach trial 3, the first two trials must both tie; the third must be non-tied. Independence permits multiplying these three probabilities. Do not multiply by an extra factor 2 for the two players: the decisive probability already includes both possible winners.

Derivation, answer and qualifications:

A trial ties with probability 6/36=1/6 and is decisive with probability 5/6. Winning first on trial 3 requires two ties then a decisive roll, probability(1/6)²(5/6)=5/216≈0.023148, rounded 0.023.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2018 CS: Q26 (printed CS Q16)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2018.pdf**, open physical PDF page **8**, and locate printed **CS 16** in **CS-2018**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.27 to 0.30

**Derived answer:** 0.289

**Source access:** Open archive member CS/CS2018.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate ∫ from 0 to π/4 of x cos(x²) dx, using π=3.14 and rounding to three decimals.

## Solution

Method and intermediate reasoning:

The derivative of the inner argument x² is 2x, so the factor x dx is half of du. The transformed upper bound is (3.14/4)²=0.616225, not 3.14/4. Thus the integral is one half of the sine of 0.616225 radians. The integrand is positive throughout this interval, consistent with a positive answer smaller than ∫x dx=0.3081125.

Derivation, answer and qualifications:

Substitute u=x², du=2x dx. The integral is(1/2)sin(x²) evaluated at 0 andπ/4, hence(1/2)sin((3.14/4)²)≈0.288979, rounded 0.289.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2018 CS: Q27 (printed CS Q17)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2018.pdf**, open physical PDF page **8**, and locate printed **CS 17** in **CS-2018**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 3 to 3

**Derived answer:** 3

**Source access:** Open archive member CS/CS2018.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Let u=(1,2)^T, v=(1,1)^T and A=uv^T. Find the largest eigenvalue.

## Solution

Method and intermediate reasoning:

Write out the matrix to make the outer-product order explicit: A=[[1,1],[2,2]]. Its characteristic polynomial is (1−λ)(2−λ)−2=λ²−3λ=λ(λ−3), giving eigenvalues 0 and 3. This independently confirms the rank-one shortcut below. The scalar v^Tu is not the same matrix as uv^T; it supplies the nonzero eigenvalue because applying A to u returns a scalar multiple of u.

Derivation, answer and qualifications:

A=uv^T has rank 1. Its nonzero eigenvalue is v^Tu=1+2=3, since Au=u(v^Tu)=3u. The other eigenvalue is 0, so the largest is 3.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2018 CS: Q36 (printed CS Q26)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2018.pdf**, open physical PDF page **10**, and locate printed **CS 26** in **CS-2018**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 10](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Open archive member CS/CS2018.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A 2×2 matrix P has only eigenvectors parallel to (1,4)^T. Which statements are necessary? I P is singular; II its eigenvalue repeats; III P is not diagonalizable. A I,III; B II only; C I,II; D II,III.

## Solution

Method and intermediate reasoning:

Diagonalization in dimension two requires a basis of two linearly independent eigenvectors; the given one-dimensional eigenspace cannot provide it. Distinct eigenvalues would yield independent eigenvectors, so they must coincide. Repeated does not mean zero: take S=[[1,0],[4,1]] and J=[[1,1],[0,1]]. Then SJS^−1=[[-3,1],[-16,5]] has determinant 1, while its eigenvectors satisfy y=4x. This explicit nonsingular example refutes I.

Derivation, answer and qualifications:

A2×2 matrix with only one eigenvector direction cannot be diagonalized, proving III. Two distinct eigenvalues would supply independent eigenvectors, so its eigenvalue must be repeated, II. Invertibility is not ruled out: any similarity transform of the nonsingular Jordan block [[1, 1],[0, 1]] with its first basis vector(1, 4) has exactly that eigenvector direction. Thus II and III, D.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

