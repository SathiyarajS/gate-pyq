

# GATE 1998: Q2 (printed A Q1.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Essential problem context (paraphrased):** Solve the classification for x+2y=5, 4x+8y=12, 3x+6y+3z=15: unique, no solution, finitely many, or infinitely many?

## Solution

Multiply the first equation by 4 to obtain 4x+8y=20. The second requires the same left-hand side to equal 12, which is impossible. Hence the first two equations already contradict each other; adding the third cannot restore consistency. The system has no solution, B. The plus sign before 8y matters: changing it to minus would create a different system, so the raster rather than OCR was used.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q3 (printed A Q1.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Essential problem context (paraphrased):** Which applies to bisection: few iterations guaranteed, all continuous functions guaranteed, always faster than Newton, or correct determination of function signs?

## Solution

Bisection maintains an interval whose endpoint values have opposite signs and replaces one endpoint by the midpoint. Selecting the correct half therefore depends on reliable sign determination; an erroneous sign can discard the root. This is D. Continuity alone is insufficient without a bracket containing a sign change, and the number of iterations grows with the logarithm of the requested accuracy. Newton may converge quadratically near a simple root, so bisection is not universally faster. These distinctions rule out A, B, C.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q4 (printed A Q1.4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Essential problem context (paraphrased):** For y=|x| on[−1, 1], classify continuity and differentiability.

## Solution

On each side of zero the function is linear: −x for x<0 and x for x>0. Both one-sided limits at zero equal 0, the function value, so it is continuous throughout the interval. But its left derivative at zero is−1 and its right derivative is+1. They disagree, so it is not differentiable at zero. Thus it is continuous but not differentiable everywhere, B. Differentiability away from zero does not remove the corner.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q36 (printed A Q2.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A: 3

**Essential problem context (paraphrased):** Find rank of rows (1, 4, 8, 7), (0, 0, 3, 0), (4, 2, 3, 1), (3, 12, 24, 21). Options 3, 1, 2, 4.

## Solution

The fourth row is three times the first, so rank is at most 3. To show the remaining rows are independent, take their minor using the first three columns. Expansion along the second row gives determinant−3·det[[1, 4], [4, 2]]=−3·(2−16)=42, which is nonzero. Thus rank is at least 3. Combining the bounds proves rank 3, option A. A zero full determinant alone would only show rank below 4, not determine its exact value.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q37 (printed A Q2.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: a−b

**Essential problem context (paraphrased):** For determinant with rows (1, a, bc), (1, b, ca), (1, c, ab), choose a factor from a+b, a−b, a+b+c, abc.

## Solution

Set a=b. Then the first two rows become identical, so the determinant vanishes identically as a polynomial in the remaining variables. By the polynomial factor theorem, a−b divides it. More explicitly, subtract the first row from the other two and factor (b−a) and (c−a); the remaining 2×2 determinant is c−b, giving (b−a)(c−a)(c−b). This confirms the requested factor B. The argument does not require dividing by a possibly zero variable.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q65 (printed B Q8(a))

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** Interior maximum at x=1 and minimum at x=3. Values are C+4 and C; endpoints are one-sided local extrema relative to [0,6].

**Essential problem context (paraphrased):** Find local maxima and minima on 0≤x≤6 for f(x)=x³−6x²+9x+C. GFG prints C=−15; GateForum prints C=+15.

## Solution

Keep the disputed constant as C. Since differentiation removes it, both reproductions have identical stationary positions: f′(x)=3x²−12x+9=3(x−1)(x−3). Hence f′=0 at x=1 and x=3. The second derivative f″(x)=6x−12 is negative at 1 and positive at 3, so the interior local maximum is (1,C+4) and the interior local minimum is (3,C).

The derivative signs give the complete explanation: f increases on (0,1), decreases on (1,3), and increases on (3,6). Thus these are genuine turning points, not just horizontal tangencies. With GFG's constant −15, they are (1,−11) and (3,−15). With GateForum's constant +15, they are (1,19) and (3,15). The disagreement shifts the whole graph vertically by 30 and does not change its shape.

Because the stated domain is closed, endpoints deserve explicit treatment. Under the relative-domain definition of a local extremum, x=0 is a one-sided local minimum and x=6 a one-sided local maximum. Their values are f(0)=C and f(6)=C+54. Under the classroom convention that “local extrema” refers only to interior stationary points, report just x=1 and x=3, while still recording the endpoint behavior.

For global extrema on the closed interval, compare all four candidates: values C, C+4, C, C+54 at x=0,1,3,6. The global minimum C occurs at both 0 and 3, and the global maximum C+54 occurs at 6. This endpoint check prevents incorrectly treating the interior local maximum as the absolute maximum.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1998-Q65-CUBIC-CONSTANT-VARIANT


# GATE 1998: Q66 (printed B Q8(b))

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 0.

**Essential problem context (paraphrased):** Evaluate the definite integral of x cos x from −π to π.

## Solution

Let g(x)=x cos x. Since cosine is even, g(−x)=−x cos(−x)=−x cos x=−g(x), so g is odd. Its integral over the symmetric interval [−π,π] therefore cancels pairwise and equals zero.

Integration by parts provides an independent derivation. Take u=x and dv=cos x dx, giving du=dx and v=sin x. Then ∫x cos x dx=x sin x−∫sin x dx=x sin x+cos x+C. At π this antiderivative has value π·0+(−1)=−1; at −π it has value (−π)·0+(−1)=−1. Subtracting lower from upper again gives 0.

The printed bounds are −π and π, not an indefinite integral or the interval [0,π]. On [0,π] the value would be −2. The sign and symmetry of the lower bound are consequently essential to the result.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1998: Q67 (printed B Q9)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203837/GATE1998.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** n(n−1)(2n+5)/6 paired multiply-add operations including RHS updates and back substitution; leading term n³/3.

**Essential problem context (paraphrased):** Derive the number of operations to solve n linear equations in n unknowns by Gaussian elimination, counting one multiplication followed by an addition as one operation.

## Solution

Assume a dense nonsingular system Ax=b, successful pivots, ordinary forward elimination followed by back substitution, and no work saved by special structure. Count an update u←u−m·v as one multiplication-addition pair. Divisions and pivot search/comparison are separate because the question's paired-operation definition does not explicitly include them.

At pivot k, for k=1,...,n−1, there are n−k rows below the pivot. Each needs n−k updates to its remaining coefficient entries and one update to its right-hand-side value. Thus this stage uses (n−k)(n−k+1) paired operations. Summing with j=n−k gives

E=Σ_(j=1)^(n−1) j(j+1)
 = (n−1)n(2n−1)/6 + (n−1)n/2
 = n(n−1)(n+1)/3.

In back substitution, solving row i subtracts the contributions from the n−i already known variables. This contributes B=Σ_(i=1)^n(n−i)=n(n−1)/2 paired updates. Consequently

E+B=n(n−1)(2n+5)/6
   = n³/3+n²/2−5n/6.

For n=2 there are two elimination updates, one to the remaining coefficient and one to the right-hand side, followed by one back-substitution update: three in total, matching the formula. For n=1 there are no such pairs, although one division is still necessary.

The elimination multipliers require n(n−1)/2 divisions, and back substitution requires n more, totaling n(n+1)/2 divisions. If a convention counts each division as one extra operation, the combined count becomes (n³+3n²−n)/3. If only the coefficient-matrix elimination is requested, its pair count is Σj² rather than the full solve count. Actual floating-point operation counts often count multiplication and addition separately, producing leading cost 2n³/3. Under the printed paired-operation convention, the leading cost is n³/3, with the exact lower-order terms dependent on which phases and divisions are included.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1998-Q67-GAUSSIAN-OPERATION-CONVENTION
