

# GATE 1994: Q2 (printed A Q1.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204113/GATE1994.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Essential problem context (paraphrased):** For real symmetric n×n matrices A,B, which identity is guaranteed: AAᵀ=I, A=A⁻¹, AB=BA, or (AB)ᵀ=BA?

## Solution

Transpose reverses product order: (AB)ᵀ=BᵀAᵀ. Symmetry gives Bᵀ=B and Aᵀ=A, so the product transpose is BA. Symmetry alone does not imply orthogonality or self-inverse behavior; for example 2I refutes both. Two symmetric matrices also need not commute, as unequal diagonal scaling and a coordinate-swap matrix demonstrate. Hence only D follows for all such A and B, including singular matrices for which A⁻¹ may not exist.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1994: Q3 (printed A Q1.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204113/GATE1994.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B: y_(n+1)=y_n+h f(x_(n+1),y_(n+1))

**Essential problem context (paraphrased):** For y′=f(x,y), which update is backward Euler?

## Solution

Integrating the derivative over one step gives the change in y. Backward Euler approximates that derivative using the right endpoint of the step, so y_(n+1)−y_n≈h f(x_(n+1),y_(n+1)). This produces the stated implicit equation, which may require solving for the new y. Forward Euler instead evaluates f at the known left endpoint (x_n,y_n). A formula with two-step values or an unrelated scaling is not the first-order backward Euler method.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1994: Q9 (printed A Q1.9)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204113/GATE1994.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: 2

**Essential problem context (paraphrased):** Find the rank of [[0,0,3],[9,3,5],[3,1,1]].

## Solution

The first column is three times the second, so at most two columns are independent and rank is at most two. The second and third columns are independent: their first coordinates are 0 and 3, respectively, while the second column is nonzero. Alternatively the minor from rows 1,3 and columns 2,3 is 0·1−3·1=−3, nonzero. Thus rank is at least two as well, proving rank exactly two.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1994: Q38 (printed A Q3.4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204113/GATE1994.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** matching, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** i–b,ii–c,iii–d,iv–a

**Essential problem context (paraphrased):** Match Newton–Raphson, Runge–Kutta, Gauss–Seidel, Simpson’s rule with root finding, ODEs, linear systems and integration.

## Solution

Newton–Raphson updates a root estimate using a function and its derivative. Runge–Kutta methods advance an ODE solution by combining several slope evaluations. Gauss–Seidel iteratively solves a linear system using newly updated components within each sweep. Simpson’s rule approximates a definite integral by fitting quadratic interpolants. Therefore the respective matches are root finding, ordinary differential equations, systems of linear equations and integration. These identify the methods’ standard purposes, not claims that each is the only available method for that task.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1994: Q46 (printed A Q3.12)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204113/GATE1994.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** short-answer, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** [[1/2,−1/2,1/2],[0,0,1],[1/2,1/2,−1/2]]

**Essential problem context (paraphrased):** Find the inverse of M=[[1,0,1],[-1,1,1],[0,1,0]].

## Solution

Solve Mx=b. The third row gives x2=b3. The first gives x1+x3=b1, while the second gives −x1+x3=b2−b3. Adding the last two equations gives x3=(b1+b2−b3)/2; subtracting gives x1=(b1−b2+b3)/2. Thus the coefficients of b in x are exactly the displayed inverse matrix. This also proves uniqueness for every b, hence invertibility, without relying only on a numerical inverse calculation. Multiplying M by the displayed matrix returns the identity.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
