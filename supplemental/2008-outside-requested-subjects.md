

# GATE 2008: Q1 (printed CS Q1)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

## Solution

Divide numerator and denominator by x. As x→∞, sin(x)/x and cos(x)/x both tend to0, so the ratio tends to1, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2008: Q3 (printed CS Q3)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** All real α except5; no exact listed option

## Solution

Subtract the first equation from the second and third. The remaining coefficient rows are(0,1,1) and(0,3,α−2), so the determinant is α−5. A unique solution exists exactly when α≠5. At α=5 the third reduced equation is three times the second, including its right side, so solutions are nonunique. None of the printed choices gives the exhaustive set R minus{5}:0,1,−1 all work but are not the only possibilities, while any real number incorrectly includes5. No official key has been located; this is a source/options discrepancy, not a claimed official-key correction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2008-Q3-MISSING-ALPHA-CHOICE


# GATE 2008: Q21 (printed CS Q21)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A is the conventional sufficient bound; literal minimum is not represented

## Solution

For f(x)=xe^x on[1,2], f″(x)=(x+2)e^x is increasing, with maximum4e². The composite trapezoidal bound is |E_n|≤4e²/(12n²)=e²/(3n²). Requiring this upper bound≤10^−6/3 gives n≥1000e, corresponding to A; an integer subdivision count would be ceil(1000e)=2719. This is a sufficient worst-derivative bound, not the exact minimum demanded by the wording. Direct high-precision evaluation gives error3.33057431918×10^−7 at n=2046, already within the tolerance and substantially below2719. At n=2045 the error is3.33383240096×10^−7. Thus A describes the standard error-bound calculation, not a literal minimal integer answer. No official key is asserted.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2008-Q21-SUFFICIENT-BOUND-NOT-MINIMUM


# GATE 2008: Q22 (printed CS Q22)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

## Solution

Apply Newton’s method to f(x)=x²−R: x_next=x−(x²−R)/(2x)=(x+R/x)/2. Thus it computes√R, C, under the usual R>0 and positive starting-value convergence conditions.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2008: Q25 (printed CS Q25)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

## Solution

For f=3x^4−16x³+24x²+37, f′=12x(x−2)². The derivative changes from negative to positive at0, giving a local minimum. At2 it vanishes without a sign change, so2 is a stationary nonextremum. There is exactly one extremum, B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2008: Q28 (printed CS Q28)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

## Solution

Test det(M−I). For the four displayed matrices, these determinants are0,1,1 and4 respectively. Only the first has eigenvalue1, so the count is one, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2008: Q29 (printed CS Q29)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2008.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

## Solution

X has mean1 and standard deviation2, so P(X≤−1)=Φ(−1). If Y has mean−1 and standard deviation s>0, P(Y≥2)=1−Φ(3/s)=Φ(−3/s). Strict monotonicity of Φ gives−3/s=−1, so s=3, A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
