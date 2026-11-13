

# GATE 1996: Q6 (printed A Q1.6)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D: [f(x+h)−2f(x)+f(x−h)]/h²

**Essential problem context (paraphrased):** Choose a finite-difference approximation for f″(x) using f(x−h), f(x), f(x+h).

## Solution

Taylor expansion gives f(x±h)=f(x)±hf′(x)+h²f″(x)/2±h³f‴(x)/6+O(h⁴). Add the two expansions: the odd derivative terms cancel, leaving 2f(x)+h²f″(x)+O(h⁴). Subtract 2f(x) and divide by h² to obtain f″(x)≈[f(x+h)−2f(x)+f(x−h)]/h², with error O(h²) for a sufficiently smooth function. The denominator must be h², not h, because the first surviving derivative term is quadratic in the spacing.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q7 (printed A Q1.7)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Essential problem context (paraphrased):** Which linear-system claim is false, including the claim that m=n and b≠0 ensure a unique solution of Ax=b?

## Solution

A square coefficient matrix does not automatically have full rank. For example A is the 2×2 zero matrix and b=(1,0)ᵀ: the system has no solution despite m=n and b≠0. In general consistency requires rank(A)=rank([A|b]), and uniqueness additionally requires rank(A)=n. A homogeneous system with fewer equations than unknowns has a nontrivial nullspace over the reals; a square full-rank homogeneous system has only the zero solution. These rank facts distinguish the other standard statements from C.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q26 (printed A Q2.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: f⁻¹(u,v)=((u+v)/2,(u−v)/2)

**Essential problem context (paraphrased):** Find the inverse of f(x,y)=(x+y,x−y) on R².

## Solution

Set u=x+y and v=x−y. Adding the equations gives u+v=2x, while subtracting gives u−v=2y. Hence x=(u+v)/2 and y=(u−v)/2. Substitution back into the original map returns (u,v), verifying both coordinates rather than only guessing a similar expression. The factors of one half are essential: omitting them produces twice the desired input. The nonzero determinant −2 also confirms that this linear map is bijective.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q30 (printed A Q2.5)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: x_next=(2x³+c)/(3x²)

**Essential problem context (paraphrased):** Derive Newton–Raphson iteration to find c^(1/3), c>0.

## Solution

Apply Newton’s method to F(x)=x³−c, whose derivative is F′(x)=3x². Thus x_next=x−(x³−c)/(3x²)=(2x³+c)/(3x²). The iteration requires a nonzero current x to avoid division by zero. It uses c in the numerator, not its already-unknown cube root; substituting the root there would defeat the purpose of the iteration. A positive initial value is a standard choice for finding the positive root.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q31 (printed A Q2.6)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A: a=b or θ is an integer multiple of π

**Essential problem context (paraphrased):** For R=[[cosθ,−sinθ],[sinθ,cosθ]] and D=diag(a,b), determine when RD=DR.

## Solution

The diagonal entries of both products are a cosθ and b cosθ. Their off-diagonal entries agree exactly when −b sinθ=−a sinθ and a sinθ=b sinθ. Both reduce to (a−b)sinθ=0. Therefore either the scale factors are equal, making D a scalar matrix, or sinθ=0, meaning θ=nπ. This proves necessity as well as sufficiency. General unequal anisotropic scaling does not commute with an arbitrary rotation.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q51 (printed A Q3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=7), physical page 7. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** a=−1/2, b=3, c=−3/2, d=1/2.

**Essential problem context (paraphrased):** Let f(x)=x² for x≤1, ax²+bx+c for 1<x≤2, and x+d for x>2. Find a,b,c,d making f continuous and differentiable on the real line.

## Solution

Each branch is a polynomial, so only the joining points 1 and 2 can cause trouble. Continuity at 1 requires a+b+c=1. Equality of the left and right derivatives at 1 requires 2a+b=2, because the derivative of x² is 2x. At 2, continuity gives 4a+2b+c=2+d, while equality of derivatives gives 4a+b=1.

Subtract the derivative equation at 1 from that at 2: 2a=−1, hence a=−1/2. Then 2a+b=2 gives b=3. Substituting in a+b+c=1 gives c=−3/2. The middle branch at 2 is −2+6−3/2=5/2, so 2+d=5/2 and d=1/2.

As a direct check, the middle branch has value 1 and derivative 2 at x=1, and value 5/2 and derivative 1 at x=2. These match the adjacent branches exactly. The four linear matching conditions determine the four constants uniquely. Continuity is needed in addition to matching formal derivative formulas: derivative agreement alone would not rule out jumps in the function.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1996: Q66 (printed B Q10)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203937/GATE1996.pdf#page=8), physical page 8. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** descriptive, 5 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D=[[b11,b12],[b21−b11,b22−b12]].

**Essential problem context (paraphrased):** A and B are 2×2 matrices with AB=I. Let C=A[[1,0],[1,1]] and CD=I. Express D in terms of entries b11,b12,b21,b22 of B.

## Solution

Write M=[[1,0],[1,1]], so C=AM. Because A and B are square and AB=I, A is invertible and B=A^−1. Also det(M)=1, so M is invertible, with M^−1=[[1,0],[−1,1]]. Inverting a product reverses the order: D=C^−1=(AM)^−1=M^−1A^−1=M^−1B.

Multiply on the left explicitly. The first row of M^−1B is the first row of B, (b11,b12). The second row is the second row of B minus its first row, (b21−b11,b22−b12). Hence D has the stated entries.

For verification, M D=B, because adding D's first row to its second gives B's second row, while its first row is unchanged. Then CD=A(MD)=AB=I. This check uses only the identities in the question and avoids introducing unknown entries of A. Multiplying B by M^−1 on the right instead would subtract columns, not rows, and generally would not satisfy CD=I. The matrix order is therefore essential.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
