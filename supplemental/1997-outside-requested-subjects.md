

# GATE 1997: Q2 (printed A Q1.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Essential problem context (paraphrased):** Apply Newton–Raphson to x²−2=0 starting at−1. Does it converge to−1, +sqrt (2), −sqrt (2), or fail?

## Solution

Newton’s update is x_next=x−(x²−2)/(2x)=(x+2/x)/2. From−1 it gives−1.5, then approximately−1.416667. Negative iterates remain negative. Put u=−x>0; then u_next=(u+2/u)/2. After the first step u≥sqrt (2), and this iteration decreases toward sqrt (2), since its only positive fixed point is sqrt (2). Hence the original iterates approach−sqrt (2), C, rather than crossing to the positive root.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1997: Q3 (printed A Q1.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: −48

**Essential problem context (paraphrased):** Find determinant of the upper-triangular matrix with rows (6, −8, 1, 1), (0, 2, 4, 6), (0, 0, 4, 8), (0, 0, 0, −1).

## Solution

The determinant of an upper-triangular matrix is the product of its diagonal entries. This follows by expanding repeatedly along the first column, whose entries below the diagonal are zero. Here the product is 6·2·4·(−1)=−48. The off-diagonal entries do not affect this determinant, so B is correct. Adding diagonal entries would compute the trace, a different quantity.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1997: Q26 (printed A Q4.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: 10

**Essential problem context (paraphrased):** Find maximum of f (x)=2x²−2x+6 on[0, 2], among 6, 10, 12, 5.5.

## Solution

Differentiate: f′(x)=4x−2 vanishes at x=1/2. Since f″=4>0, this point is a minimum, with value 5.5. The maximum on the closed interval must therefore occur at an endpoint. Evaluate f (0)=6 and f (2)=8−4+6=10. The larger is 10, B. Choosing the stationary value without determining whether it is a maximum would give the wrong distractor.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1997: Q27 (printed A Q4.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: A’s second column

**Essential problem context (paraphrased):** I12 is obtained by swapping rows 1 and 2 of the identity. What is the first column of AI12 relative to A?

## Solution

The first column of I12 is the second standard basis vector e2. Therefore the first column of AI12 is A e2, which is exactly A’s second column. Right multiplication by this permutation matrix swaps columns 1 and 2 of A. Left multiplication would swap rows instead. Thus C. The direction of multiplication is essential; simply recalling that I12 was built by a row swap does not mean its right action swaps rows.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1997: Q28 (printed A Q4.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** Underdetermined as printed; intended zero-slope sequence is 0, 0, h²f (0), h²[2f (0)+f (h)]

**Essential problem context (paraphrased):** For y″(t)=f (t), the source gives y (0)=0 and asks for the first four forward-Euler y values at step h. Forum prints an extra initial second-derivative condition.

## Solution

Introduce v=y′. Forward Euler gives y[k+1]=y[k]+h v[k] and v[k+1]=v[k]+h f (kh). With v (0)=v0, the four grid values y(0), y(h), y(2h), y(3h) are 0, hv0, 2hv0+h²f (0), 3hv0+2h²f (0)+h²f (h). Thus the missing initial first derivative matters. Setting v0=0 gives the intended sequence near B, but both reproductions’ B omit the h² factor multiplying f (h). Forum’s printed initial y″(0)=0 is not a replacement for y′(0)=0. Neither the missing condition nor coefficient is silently repaired.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1997-Q28-EULER-MISSING-SLOPE-AND-COEFFICIENT


# GATE 1997: Q29 (printed A Q4.4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: 2

**Essential problem context (paraphrased):** p (0)=5, p (1)=4, p (2)=9, p (3)=20. Find minimum degree among 1, 2, 3, 4.

## Solution

Successive first differences are−1, 5, 11. Their differences are 6, 6, constant and nonzero, so the data cannot come from a linear polynomial and suggest a quadratic with leading coefficient 6/2=3. Write p (x)=3x²+bx+c. From p (0)=5, get c=5; p (1)=4 gives b=−4. Then p (2)=12−8+5=9 and p (3)=27−12+5=20. The quadratic exists and degree 1 is impossible, so the minimum is 2, B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1997: Q35 (printed A Q4.10)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203902/GATE1997.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: 600 by the supplied bound

**Essential problem context (paraphrased):** Approximate ln7=integral from 1 to 7 of 1/x using uniform trapezoids. Given bound (b−a)h² max|f″|/12, find minimum count guaranteeing error≤10^−4.

## Solution

For f (x)=1/x, f″(x)=2/x³, whose maximum on[1, 7] is 2. With N trapezoids, h=6/N. The error bound becomes (6/12)·(36/N²)·2=36/N². Requiring 36/N²≤10^−4 gives N²≥360000 and N≥600. Thus C is the smallest integer certified by this bound. The actual error can be smaller than the bound; the question asks a guarantee from the supplied estimate, not the smallest empirically sufficient count.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
