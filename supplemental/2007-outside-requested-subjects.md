

# GATE 2007: Q1 (printed CS Q1)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2007.pdf**, open physical PDF page **2**, and locate printed **CS 1** in **CS-2007**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2007.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** For f(x)=|x|, consider P: f is continuous for every real x; Q: f is differentiable for every real x. Which statement is true?
Options:
(A) P true, Q false
(B) P false, Q true
(C) Both true
(D) Both false

## Solution

1. Approach. Write |x| as -x for x<0 and x for x≥0. The values from both sides approach zero at the joining point, but the slopes differ there.

2. Derivation and interpretation. The absolute-value function is continuous everywhere. At 0 its left derivative is −1 and right derivative +1, so it is not differentiable there. Thus P is true and Q false, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2007: Q25 (printed CS Q25)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2007.pdf**, open physical PDF page **5**, and locate printed **CS 25** in **CS-2007**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2007.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** A is a 4×4 matrix with eigenvalues −5,−2,1,4, and I is the 4×4 identity. Which option is an eigenvalue of the 8×8 block matrix [[A,I],[I,A]]?
Options:
(A) −5
(B) −7
(C) 2
(D) 1

## Solution

1. Approach. Apply the block matrix separately to (v,v) and (v,−v), where Av=λv. This reduces the eight-dimensional eigenvalue calculation to adding and subtracting one from each eigenvalue of A.

2. Derivation and interpretation. For Av=λv, the block vectors (v,v) and (v,−v) are eigenvectors of [[A,I],[I,A]] with eigenvalues λ+1 and λ−1. The eight values are −4,−6,−1,−3,2,0,5,3. Among the options only 2 occurs, C.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2007: Q27 (printed CS Q27)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2007.pdf**, open physical PDF page **6**, and locate printed **CS 27** in **CS-2007**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2007.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Let X={x∈R³:x1+x2+x3=0}, with vectors understood as columns. Which statement is true?
Options:
(A) {(1,−1,0),(1,0,−1)} is a basis of X
(B) Those two vectors are independent but do not span X
(C) X is not a subspace of R³
(D) None of these

## Solution

1. Approach. The single homogeneous equation removes one degree of freedom from R³. Verify membership, linear independence, and spanning rather than assuming two vectors automatically form a basis.

2. Derivation and interpretation. The vectors (1,−1,0) and (1,0,−1) lie in X and are linearly independent. Any (x1,x2,x3) with x1+x2+x3=0 equals −x2(1,−1,0)−x3(1,0,−1). They span X and form a basis, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2007: Q28 (printed CS Q28)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2007.pdf**, open physical PDF page **6**, and locate printed **CS 28** in **CS-2007**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2007.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Newton–Raphson iteration gives x_(n+1)=x_n/2+9/(8x_n), starting at x0=0.5. To what value does the sequence converge?
Options:
(A) 1.5
(B) √2
(C) 1.6
(D) 1.4

## Solution

1. Approach. A limit must satisfy the fixed-point equation, but that equation alone does not prove convergence or choose a sign. Positive iterates select the positive root; monotonicity after the first step verifies convergence.

2. Derivation and interpretation. Rewrite the iteration as x_next=(x+(9/4)/x)/2, Newton’s square-root iteration for 9/4. Starting at .5>0, the first step is 2.5; subsequent iterates stay above 1.5 and decrease to the positive fixed point. Solving x=x/2+9/(8x) yields x²=9/4, so the limit is 1.5, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

