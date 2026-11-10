

# GATE 1995: Q21 (printed A Q1.21)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: exactly one

**Essential problem context (paraphrased):** How many solutions does x=cos x have on [0,π]?

## Solution

Define g(x)=x−cos x, a continuous function. It satisfies g(0)=−1 and g(π)=π+1>0, so the intermediate value theorem gives at least one zero. On [0,π], g′(x)=1+sin x≥1, so g is strictly increasing and can have at most one zero. Combining existence and uniqueness proves exactly one solution. A graph can suggest this result, but the derivative and endpoint signs establish it rigorously.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q22 (printed A Q1.22)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D: ellipse

**Essential problem context (paraphrased):** A curve has dy/dx=−2x/y wherever the slope is defined. Is it a line, parabola, circle or ellipse?

## Solution

Multiply by y and separate variables: y dy=−2x dx. Integration gives y²/2=−x²+C, or 2x²+y²=C′. For a nondegenerate real curve C′>0, this is an ellipse with unequal axis coefficients, not a circle. C′=0 would give only a point, and C′<0 no real curve; the premise of an actual smooth curve excludes these degeneracies. At points with y=0 the displayed slope is undefined, corresponding to the ellipse’s vertical tangents.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q23 (printed A Q1.23)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: 9

**Essential problem context (paraphrased):** For which listed k∈{0,2,9,3} does 4x²−8xy+ky²=0 fail to represent two real lines through the origin?

## Solution

View the homogeneous quadratic as a quadratic in x/y. Its discriminant is (−8)²−4·4·k=16(4−k). Real line factors exist when k≤4. The choices 0,2,3 all satisfy that condition, while 9 does not. In fact 4x²−8xy+9y²=4(x−y)²+5y² vanishes only at the origin, not along a pair of real lines. The qualification “real” is important because complex factors exist even for a negative discriminant.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q24 (printed A Q1.24)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A: 1

**Essential problem context (paraphrased):** Every row of an (n+1)×(n+1) matrix is (1,a,a²,…,a^n), for real a. Find its rank.

## Solution

All rows are identical, so the row space is spanned by a single vector and its dimension is at most one. That vector is nonzero for every a because its first coordinate is 1. Hence the dimension is at least one, proving rank exactly one. In particular a=0 does not make the matrix zero: its first column remains all ones. The result is independent of a and of the number of repeated rows.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q33 (printed A Q2.8)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: −1,1−2ω,1−2ω²

**Essential problem context (paraphrased):** If 1,ω,ω² are cube roots of unity, find roots of (x−1)³+8=0.

## Solution

The equation says (x−1)³=−8. Since (−2)³=−8, all three cube roots are −2 times the cube roots of unity: −2,−2ω,−2ω². Adding 1 yields −1,1−2ω,1−2ω². Each substitution cubes back to −8 because ω³=1. Changing the sign to plus 2 would solve the equation with +8 on the other side instead, so the negative sign is essential.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q38 (printed A Q2.13)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A: (i+j+k)/sqrt(3)

**Essential problem context (paraphrased):** Find a unit vector perpendicular to a=2i−3j+k and b=i+j−2k.

## Solution

Their cross product is (5,5,5): its components are (−3)(−2)−1·1, 1·1−2(−2), and 2·1−(−3)·1. Its length is 5sqrt(3), so normalization gives (1,1,1)/sqrt(3). Direct checks give a·(1,1,1)=0 and b·(1,1,1)=0. The negative vector is also a valid unit normal, but among the listed alternatives the positive normalized one is A. A divisor of 3 would not give unit length. GateForum changes the first vector to (2,−2,1); its cross product with (1,1,−2) is (3,5,4), so neither sign of the unit vector (3,5,4)/sqrt(50) matches the listed choices. The answer A therefore follows the GFG −3 coefficient, not that alternate variant.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1995-Q38-VECTOR-COEFFICIENT-VARIANCE


# GATE 1995: Q40 (printed A Q2.15)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: x_next=(x²+b)/(2x)

**Essential problem context (paraphrased):** What is the Newton–Raphson iteration for the positive square root of b?

## Solution

Set f(x)=x²−b and f′(x)=2x. Newton’s formula gives x_next=x−f(x)/f′(x)=x−(x²−b)/(2x)=(x²+b)/(2x). Starting with positive x and b keeps the iterates positive and approaches the positive root. The denominator must not be zero. The alternative form (x+b/x)/2 makes clear that each step averages the current estimate with the reciprocal-scaled estimate b/x. This is GFG option B; GateForum renders B as a malformed expression rather than the same formula, so the expression itself is the reliable answer across the source discrepancy.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1995-Q40-NEWTON-OPTION-CORRUPTION


# GATE 1995: Q43 (printed A Q2.18)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: C1e^−x+C2e^−2x

**Essential problem context (paraphrased):** Find the general solution of y″+3y′+2y=0.

## Solution

Try y=e^(rx). Substitution gives the characteristic equation r²+3r+2=0, which factors as (r+1)(r+2)=0. The two distinct roots are −1 and −2, giving independent solutions e^−x and e^−2x. Linearity yields their arbitrary linear combination C1e^−x+C2e^−2x. Positive exponential roots would not satisfy the characteristic equation, and an x multiplier is needed only for a repeated root, which is absent here.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1995: Q58 (printed A Q7(b))

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 1 for the GFG expression; literal GateForum expression is undefined.

**Essential problem context (paraphrased):** Without power-series expansion, compute lim(x→0) sin(x)/x, with x in radians. GFG prints denominator x; GateForum prints denominator 0.

## Solution

For 0<x<π/2, the unit-circle area comparison gives sin x < x < tan x. Divide the first inequality by positive x, and rearrange the second to obtain cos x < sin x/x < 1. As x→0 from the right, both bounding functions tend to 1. The squeeze theorem therefore gives the right-hand limit 1 without a power series.

The quotient is even away from zero: sin(−x)/(−x)=sin x/x. Its left-hand limit equals the right-hand limit, so the two-sided limit is 1. The function need not be defined at x=0 for this limit to exist. Radian measure is essential to the value 1.

GateForum’s literal sin(x)/0 is undefined for every nearby x, so it does not describe this standard real-valued limit. The answer 1 belongs to the denominator-x reproduction; it is not an evaluation of division by zero.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1995-LIMIT-SOURCE


# GATE 1995: Q85 (printed B Q25(a))

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204046/GATE1995.pdf#page=8), physical page 8. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** Minimum1, attained at x=1.

**Essential problem context (paraphrased):** Find the minimum value of 3−4x+2x², taking x to range over the real numbers.

## Solution

Complete the square rather than guessing a stationary point: 3−4x+2x²=2(x²−2x)+3=2[(x−1)²−1]+3=2(x−1)²+1. For every real x, the square is nonnegative, so the expression is at least 1. At x=1 the square is zero, so the lower bound is attained. Thus1 is the global minimum, and x=1 is the unique minimizer.

As a check, differentiating gives f′(x)=4x−4, whose sole zero is x=1. The second derivative is 4>0 everywhere, confirming strict convexity and the minimum. The completed-square proof is stronger than simply solving f′=0: it directly establishes a lower bound over the full domain and proves attainment.

The source does not explicitly specify a domain for x; the conventional real-variable interpretation is used. If x were restricted to integers the same answer still holds because 1 is an allowed integer. A different restricted domain excluding 1 would need a separate analysis. The requested minimum value is 1, whereas x=1 is where that value occurs.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
