

# GATE 2002: Q1 (printed A Q1.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203519/GATE2002.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Essential problem context (paraphrased):** Find the rank of the matrix [[1, 1], [0, 0]].
(A) 4; (B) 2; (C) 1; (D) 0.

## Solution

Step 1: Count independent rows, not nonzero entries.

Step 2: The row (1,1) spans every row of the matrix, so the row-space dimension is one. Rank cannot be negative; rank two would require two independent rows, while rank zero would require the zero matrix.

Conclusion and qualifications: The first row is nonzero and the second row is zero. There is exactly one linearly independent row, so the rank is 1, C.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2002: Q2 (printed A Q1.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203519/GATE2002.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Essential problem context (paraphrased):** For which polynomial degrees does the trapezoidal integration rule give an exact result?
(A) 0 but not 1; (B) 1 but not 0; (C) 0 or 1; (D) 2.

## Solution

Step 1: Check what the trapezoidal formula integrates.

Step 2: On [a,b], the approximation is (b−a)(f(a)+f(b))/2. Substituting f(x)=c gives c(b−a), and substituting f(x)=mx+c gives m(b²−a²)/2+c(b−a), both exact integrals. For f(x)=x² on [0,1], it gives 1/2 instead of 1/3, ruling out degree two.

Conclusion and qualifications: The trapezoidal rule integrates the straight line joining the endpoint values. It is exact for every polynomial of degree 0 or 1, C. A quadratic such as x² already has a nonzero error on a nondegenerate interval.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2002: Q40 (printed A Q2.15)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203519/GATE2002.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Essential problem context (paraphrased):** The Newton–Raphson iteration Xₙ₊₁ = Xₙ/2 + 3/(2Xₙ) can solve which equation?
(A) X²=3; (B) X³=3; (C) X²=2; (D) X³=2.

## Solution

Step 1: Derive the Newton step from the candidate equation.

Step 2: For x²−3=0, derivative 2x gives x_next=x−(x²−3)/(2x). Splitting the fraction gives x−x/2+3/(2x)=x/2+3/(2x). A cubic would instead involve a derivative 3x² and a2x/3 term, so it cannot produce the displayed iteration.

Conclusion and qualifications: For g(x)=x²−3, Newton’s formula is x−g(x)/g′(x)=x−(x²−3)/(2x)=x/2+3/(2x). This is the displayed iteration, so it solves x²=3, A, with a suitable nonzero initial value.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2002: Q56 (printed B Q5(a))

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203519/GATE2002.pdf#page=7), physical page 7. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 1, 2, −2, −1

**Essential problem context (paraphrased):** Find the eigenvalues of A with rows [1,2,34,49], [0,2,43,94], [0,0,−2,104], [0,0,0,−1].

## Solution

1. Read the matrix, including its zero structure:

```text
A = [1  2  34   49]
    [0  2  43   94]
    [0  0  -2  104]
    [0  0   0   -1]
```

All entries below the main diagonal are zero, so A is upper triangular.

2. Form λI − A. It is also upper triangular, with diagonal entries λ−1, λ−2, λ+2, and λ+1. The determinant of a triangular matrix is the product of its diagonal entries; the displayed entries above the diagonal do not contribute additional factors.

3. Compute the characteristic polynomial: det(λI − A) = (λ−1)(λ−2)(λ+2)(λ+1) = (λ²−1)(λ²−4).

4. Set the determinant to zero. Each factor supplies one eigenvalue, giving λ ∈ {1,2,−2,−1}, each with algebraic multiplicity one.

5. As a consistency check, the eigenvalues sum to 0, matching the trace 1+2−2−1. Their product is 4, matching the product of the diagonal entries and hence det(A). This leaf is supplemental linear algebra rather than one of the requested twelve subjects.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
