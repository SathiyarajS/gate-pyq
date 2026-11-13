

# GATE 1993: Q1 (printed A Q1.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B,D

**Essential problem context (paraphrased):** For M=[[0,0,α],[0,0,0],[0,0,0]], α≠0, which listed vectors are eigenvectors: (0,0,α),(α,0,0),(0,0,1),(0,α,0)?

## Solution

The matrix is nilpotent: M²=0, so its only eigenvalue is zero. For v=(x,y,z), Mv=(αz,0,0), which vanishes exactly when z=0. Thus every nonzero vector in the xy-plane is a zero-eigenvalue eigenvector. The second and fourth candidates satisfy this condition and are nonzero because α≠0. The first and third have nonzero z and their images are not scalar multiples of themselves. Hence B and D, not merely one option.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q2 (printed A Q1.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B under the standard linear-ODE terminology

**Essential problem context (paraphrased):** Classify y″+y′+sin y=0 among linear,nonlinear,homogeneous,degree two.

## Solution

A linear differential equation contains y and its derivatives only to first powers with coefficients depending on the independent variable. The term sin y violates that requirement, making this equation nonlinear. Its order is two, but its highest derivative occurs to power one, so its differential degree is one, not two. “Homogeneous” in the standard homogeneous-linear-ODE sense is not applicable to this nonlinear equation. Merely having zero on the right is not enough to infer the linear homogeneity property; a different informal use of that word should be stated separately.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1993-Q2-NONLINEAR-HOMOGENEITY-TERMINOLOGY


# GATE 1993: Q3 (printed A Q1.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A,B,C

**Essential problem context (paraphrased):** For which polynomial degrees 1,2,3,4 is Simpson’s rule exact?

## Solution

Simpson’s rule integrates every polynomial of degree at most three exactly. One way to see the extra cubic exactness is to center the interval: the odd cubic term integrates to zero and is canceled by the symmetric sample weights, while the rule integrates constants, linear and quadratic terms exactly. Its error involves the fourth derivative, which vanishes for degrees one through three. A general quartic has nonzero error, so degree four is not guaranteed. As a multiple-select question, all of A,B,C are required.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q5 (printed A Q1.5)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C: π²/8

**Essential problem context (paraphrased):** Using the supplied Fourier series or otherwise, evaluate 1+1/3²+1/5²+1/7²+… among π²/4,π²/6,π²/8,π²/12.

## Solution

Let S=Σ(n≥1)1/n²=π²/6. The even-index terms sum to Σ1/(2n)²=S/4. Subtracting them from S leaves precisely the positive odd-index terms, so the required sum is 3S/4=π²/8. This agrees with evaluating the displayed Fourier series at its endpoint using the appropriate midpoint value. The source’s piecewise interval typography is damaged, but the requested numerical series itself is explicit and determines the result independently.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q6 (printed A Q1.6)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B on the literal x⁵/2 reading; B,D if D intended x^(5/2)

**Essential problem context (paraphrased):** Assess integrals A ∫₀¹ sin x/(1−cos x) dx; B ∫₀∞ cos x/(1+x) dx; C ∫₀∞ x/(1+x²) dx; D ∫₀¹ (1−cos x)/(x⁵/2) dx as displayed.

## Solution

Near zero, sin x/(1−cos x) is asymptotic to 2/x, so A diverges. Integral B converges by Dirichlet’s test: an antiderivative of cos x is bounded and 1/(1+x) decreases to zero. C has antiderivative (1/2)log(1+x²), unbounded at infinity. The displayed D denominator is stacked x⁵ over 2; literally its integrand behaves as x^−3, hence diverges. If the intended typography was x^(5/2), it behaves as (1/2)x^−1/2 and converges instead. Both reproductions retain this ambiguity, so a unique D selection is not claimed.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1993-Q6-IMPROPER-INTEGRAL-EXPONENT


# GATE 1993: Q7 (printed A Q1.7)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MSQ, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A: no local extrema

**Essential problem context (paraphrased):** For f(x,y)=x²y−3xy+2y+x, determine the number of local maxima and minima.

## Solution

The partial derivatives are f_x=(2x−3)y+1 and f_y=x²−3x+2=(x−1)(x−2). Stationarity therefore requires x=1,y=1 or x=2,y=−1. The Hessian has f_xx=2y, f_xy=2x−3 and f_yy=0. Its determinant is −(2x−3)²=−1 at either point, so both are saddle points. Since a differentiable function on R² can have an interior local extremum only at a stationary point, there are no local maxima or minima.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q8 (printed A Q2.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 1

**Essential problem context (paraphrased):** Evaluate lim(x→0)[x(e^x−1)+2(cos x−1)]/[x(1−cos x)].

## Solution

Expand e^x−1=x+x²/2+x³/6+O(x⁴) and cos x−1=−x²/2+x⁴/24+O(x⁶). Multiplying the first by x and the second by two cancels their x² terms, leaving x³/2+O(x⁴). The denominator is x³/2+O(x⁵). Dividing gives a ratio tending to one. Keeping only first-order expansions would miss the cancellation and fail to identify the first nonzero terms.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q9 (printed A Q2.2)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 1/3

**Essential problem context (paraphrased):** Find the radius of convergence in x of Σ(m≥0)(3m)!/(m!)³ · x^(3m).

## Solution

For successive nonzero terms, the absolute ratio is [(3m+3)(3m+2)(3m+1)/(m+1)³]|x|³, tending to 27|x|³. The ratio test gives convergence for 27|x|³<1 and divergence when it exceeds one. Therefore |x|<1/3 is the convergence interior and the radius is 1/3. Treating x³ as a new variable gives radius 1/27 in that variable, but the question asks the radius in x, requiring the cube root.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q10 (printed A Q2.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** −i−k under ω=(1/2)curl V

**Essential problem context (paraphrased):** For V=(x²y,xyz,−yz²), find local angular velocity at (1,1,−1).

## Solution

The local rigid-rotation component of a velocity field has angular velocity half its curl. Compute curl V=(∂(−yz²)/∂y−∂(xyz)/∂z, ∂(x²y)/∂z−∂(−yz²)/∂x, ∂(xyz)/∂x−∂(x²y)/∂y)=(-z²−xy,0,yz−x²). At (1,1,−1) this is (−2,0,−2). Dividing by two gives (−1,0,−1). The full curl is vorticity, not angular velocity; omitting the factor one half would answer a different quantity.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q11 (printed A Q2.4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 0.005

**Essential problem context (paraphrased):** For y′=x−y,y(0)=0,h=0.1, compute y(0.1) to three decimal places using RK2.

## Solution

Using Heun’s RK2 form, k1=h f(0,0)=0. The endpoint predictor is y+k1=0 at x=0.1, so k2=0.1·(0.1−0)=0.01. The corrected value is y+(k1+k2)/2=0.005. The midpoint RK2 variant gives the same first step: its midpoint slope is 0.05 and h times that is 0.005. The exact value 0.1−1+e^−0.1≈0.004837 also rounds to 0.005, providing a consistency check rather than replacing the requested numerical method.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q13 (printed A Q2.6)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** Literal expression unresolved; 1/2 if the inner differential is repaired to dy and the outer to dx

**Essential problem context (paraphrased):** The source prints ∫₀¹ ∫₀^(1/x) x/(1+y²) dx dy. Evaluate if possible without silently changing the differentials.

## Solution

As printed, the inner integration variable x also appears in its own upper bound 1/x, so this is not a well-defined ordinary iterated integral with fixed outer parameter y. One plausible repair is ∫₀¹∫₀^(1/x) x/(1+y²) dy dx. That becomes ∫₀¹ x arctan(1/x) dx. Integration by parts gives [x² arctan(1/x)/2]₀¹+(1/2)∫₀¹ x²/(1+x²) dx=π/8+(1/2)(1−π/4)=1/2. This is a conditional repaired result, not a verified interpretation; another repair of the bound could change the value.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-1993-Q13-MALFORMED-INTEGRAL


# GATE 1993: Q14 (printed A Q2.7)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** I₄

**Essential problem context (paraphrased):** For A=[[1,0,0,1],[0,−1,0,−1],[0,0,i,i],[0,0,0,−i]], find A⁴.

## Solution

The triangular matrix has diagonal eigenvalues 1,−1,i,−i, all distinct. Its characteristic polynomial is (t−1)(t+1)(t−i)(t+i)=t⁴−1. Cayley–Hamilton therefore gives A⁴−I=0 directly, including the off-diagonal entries; one cannot justify the full matrix power by looking only at the diagonal. Thus A⁴ is the 4×4 identity. The result can also be verified by multiplication, but the characteristic polynomial explains why all off-diagonal contributions cancel.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q15 (printed A Q2.8)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** 1

**Essential problem context (paraphrased):** For V=(x cos²y,x²e^z,z sin²y), find outward flux through the surface of a unit cube with coordinate-parallel edges.

## Solution

Use the divergence theorem. The divergence is ∂(x cos²y)/∂x+∂(x²e^z)/∂y+∂(z sin²y)/∂z=cos²y+0+sin²y=1. Integrating over the cube multiplies this constant by its volume, one, so outward flux is one. The middle component has no y dependence and contributes zero to divergence. Outward orientation is the conventional normal on a closed surface; reversing every normal would reverse the flux sign.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q16 (printed A Q2.9)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** λ=kπ; k≥1 for a positive interval length

**Essential problem context (paraphrased):** For y″+y=0 with y(0)=y(λ)=0, give λ allowing a nontrivial solution.

## Solution

The general solution is y=A cos x+B sin x. At zero, the boundary condition forces A=0. A nontrivial solution therefore requires B≠0, and the second condition becomes sin λ=0. Thus λ is an integer multiple of π. If λ denotes a positive interval length, take k=1,2,…; if the source allows λ=0 or negative endpoints, the algebraic zero condition includes those multiples too. This distinction states the usual boundary-value convention instead of inventing a range restriction.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 1993: Q17 (printed A Q2.10)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005204139/GATE1993.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** fill-in, Unallocated leaf; group total None mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** −1/[(s²+1)(e^(πs)−1)], Re(s)>0

**Essential problem context (paraphrased):** A 2π-periodic function is zero on (0,π) and sin t on (π,2π), repeated thereafter. Find its Laplace transform.

## Solution

For a periodic function of period T, the Laplace transform is the transform over one period divided by 1−e^(−sT). Here the numerator is ∫π^(2π)e^(−st)sin t dt=−(e^(−πs)+e^(−2πs))/(s²+1). Divide by 1−e^(−2πs) and factor the difference of squares to obtain −e^(−πs)/[(s²+1)(1−e^(−πs))], the stated form. Its negative sign is consistent with every nonzero pulse lying below the axis. Boundary-point values do not affect the integral.

**Verification:** Independent review of the stated derivation or unresolved-source explanation passed; a missing-source entry is not a solved answer. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
