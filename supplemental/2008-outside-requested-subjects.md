

# GATE 2008: Q1 (printed CS Q1)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Evaluate lim(x→∞) (x−sin x)/(x+cos x).

(A) 1
(B) −1
(C) ∞
(D) −∞

## Solution

1. Divide both terms by x, obtaining (1−sin(x)/x)/(1+cos(x)/x).
2. Since |sin x|≤1 and |cos x|≤1, both divided trigonometric terms tend to zero by squeezing.
3. The denominator tends to 1, not zero, so the quotient limit is 1: A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q3 (printed CS Q3)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** All real α except5; no exact listed option

**Paraphrased problem context:** The equations x₁+x₂+2x₃=1, x₁+2x₂+3x₃=2, x₁+4x₂+αx₃=4 have a unique solution. The only possible value(s) of α is/are:

(A) 0
(B) Either 0 or 1
(C) One of 0,1,−1
(D) Any real number

## Solution

1. Subtract the first equation from the second and third. The remaining coefficient rows are(0,1,1) and(0,3,α−2), so the determinant is α−5.
2. A unique solution exists exactly when α≠5. At α=5 the third reduced equation is three times the second, including its right side, so solutions are nonunique.
3. None of the printed choices gives the exhaustive set R minus{5}:0,1,−1 all work but are not the only possibilities, while any real number incorrectly includes5. No official key has been located; this is a source/options discrepancy, not a claimed official-key correction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2008-Q3-MISSING-ALPHA-CHOICE



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q21 (printed CS Q21)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A is the conventional sufficient bound; literal minimum is not represented

**Paraphrased problem context:** What minimum number of equal subintervals is needed to approximate ∫₁² xe^x dx with error at most (1/3)×10^−6 using the trapezoidal rule?

(A) 1000e
(B) 1000
(C) 100e
(D) 100

## Solution

1. For f(x)=xe^x on[1,2], f″(x)=(x+2)e^x is increasing, with maximum4e². The composite trapezoidal bound is |E_n|≤4e²/(12n²)=e²/(3n²). Requiring this upper bound≤10^−6/3 gives n≥1000e, corresponding to A; an integer subdivision count would be ceil(1000e)=2719.
2. This is a sufficient worst-derivative bound, not the exact minimum demanded by the wording. Direct high-precision evaluation gives error3.33057431918×10^−7 at n=2046, already within the tolerance and substantially below2719. At n=2045 the error is3.33383240096×10^−7.
3. Thus A describes the standard error-bound calculation, not a literal minimal integer answer. No official key is asserted.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2008-Q21-SUFFICIENT-BOUND-NOT-MINIMUM



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q22 (printed CS Q22)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** The Newton–Raphson iteration xₙ₊₁=(xₙ+R/xₙ)/2 computes which quantity?

(A) Square of R
(B) Reciprocal of R
(C) Square root of R
(D) Logarithm of R

## Solution

1. Newton iteration for f(x)=0 is x_next=x−f(x)/f′(x).
2. Set f(x)=x²−R; then f′(x)=2x and x_next=x−(x²−R)/(2x)=(x+R/x)/2.
3. Thus the fixed point satisfies x²=R. For R>0 and positive initial x, it computes the positive square root, C; zero starting values are invalid.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q25 (printed CS Q25)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** An extremum is a local minimum or maximum. How many distinct extrema does 3x⁴−16x³+24x²+37 have?

(A) 0
(B) 1
(C) 2
(D) 3

## Solution

1. Differentiate: f′(x)=12x³−48x²+48x=12x(x−2)². Stationary points are 0 and 2.
2. The squared factor is nonnegative. The derivative is negative before 0 and positive after 0 except where it vanishes at 2. Hence 0 is a local minimum.
3. At 2 the derivative remains positive on both sides, so there is no extremum there. The count is one, B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q28 (printed CS Q28)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** How many of these matrices have eigenvalue 1? [[1,0],[0,0]], [[0,1],[0,0]], [[1,−1],[1,1]], [[−1,0],[1,−1]].

(A) One
(B) Two
(C) Three
(D) Four

## Solution

1. A matrix has eigenvalue 1 exactly when M−I is singular.
2. Subtract the identity from the four matrices and compute their determinants. In order they are 0,1,1,4.
3. Only the first determinant vanishes, giving one matrix, A. The remaining eigenvalues need not be computed.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2008: Q29 (printed CS Q29)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** X is normal with mean +1 and variance 4. Y is normal with mean −1 and unknown variance. If P(X≤−1)=P(Y≥2), what is the standard deviation of Y?

(A) 3
(B) 2
(C) √2
(D) 1

## Solution

1. X has standard deviation √4=2. Standardization gives P(X≤−1)=Φ((−1−1)/2)=Φ(−1).
2. Write Y’s positive standard deviation as s. Then P(Y≥2)=1−Φ((2+1)/s)=Φ(−3/s), using normal symmetry.
3. Φ is strictly increasing, so equality implies −3/s=−1 and s=3, A. The requested quantity is standard deviation, not variance 9.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

