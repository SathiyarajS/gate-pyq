

# GATE 2014 CS1: Q12 (printed CS Q2)

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0.24 to 0.27

**Derived answer:** 0.25

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A unit-length stick is cut once at a uniformly random point. Find the expected length of the shorter piece.

## Solution

1. Method and setup. Let X be the cut position measured from the left endpoint. The two lengths are X and 1−X. The shorter length is X on [0,1/2] and 1−X on [1/2,1]; the two halves contribute equally to the expectation.

2. Work through the result and its assumptions. For a uniform cut X on[0, 1], the shorter length is min(X, 1−X). Symmetry gives E=2∫₀^(1/2)x dx=1/4, within the accepted range.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q14 (printed CS Q4)

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 1 to 1

**Derived answer:** 1

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Find the number of solutions of 3x+2y=1, 4x+7z=1, x+y+z=3, and x−2y+7z=0.

## Solution

1. Method and setup. Eliminate y and z using y=(1−3x)/2 and z=(1−4x)/7. Substitution into x+y+z=3 gives (9−15x)/14=3, hence x=−11/5. These three equations uniquely determine all variables; the fourth must then be checked for consistency, not treated as an automatic contradiction.

2. Work through the result and its assumptions. The first three equations give x=−11/5, y=19/5, z=7/5 uniquely. Substitution into the fourth gives(−11−38+49)/5=0. Hence the consistent system has exactly one solution.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q15 (printed CS Q5)

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0 to 0

**Derived answer:** 0

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For a real symmetric positive-definite 4×4 matrix, what is the dot product of eigenvectors associated with any two distinct eigenvalues?

## Solution

1. Method and setup. Write Au=λu and Av=μv. Symmetry means Aᵀ=A, allowing the matrix to move from one side of an inner product to the other. Positive definiteness ensures positive eigenvalues but is not needed for the orthogonality conclusion; symmetry and λ≠μ are enough.

2. Work through the result and its assumptions. For symmetric A, eigenvectors u, v with distinct eigenvalues λ,μ satisfy λuᵀv=(Au)ᵀv=uᵀAv=μuᵀv. Therefore(λ−μ)uᵀv=0 and their dot product is 0.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q16 (printed CS Q6)

**Question:** [Official archived paper page 9](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For θ∈[π/6,π/3], let f(θ) be the determinant with rows (sin θ, cos θ, tan θ), (sin(π/6),cos(π/6),tan(π/6)), and (sin(π/3),cos(π/3),tan(π/3)). I: There exists θ strictly between the endpoints with f′(θ)=0. II: There exists θ strictly between the endpoints with f′(θ)≠0. Which are true? A: I only. B: II only. C: both. D: neither.

## Solution

1. Method and setup. The tangent function has no pole on this interval, so the determinant is continuous on the closed interval and differentiable inside it. At either endpoint two rows coincide, forcing determinant zero. Rolle’s theorem proves I. To establish II, check an interior value is nonzero; endpoint equality alone would not exclude the identically zero function.

2. Work through the result and its assumptions. The determinant vanishes at θ=π/6 and π/3 because two rows coincide, so Rolle’s theorem guarantees an interior derivative zero. It is not identically zero: direct expansion gives f(π/4)=√2(1−1/√3)−1/2≠0. The mean-value theorem between an endpoint and π/4 gives another interior point with nonzero derivative. Both I and II hold, C.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q28 (printed CS Q18)

**Question:** [Official archived paper page 11](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Match models 1 waterfall, 2 evolutionary, 3 component-based software engineering, 4 spiral development to features a incremental specifications, b unavoidable requirement compromises, c explicit recognition of risk, d inflexible project stages. A: 1-a,2-b,3-c,4-d. B: 1-d,2-a,3-b,4-c. C: 1-d,2-b,3-a,4-c. D: 1-c,2-a,3-b,4-d.

## Solution

1. Method and setup. Anchor the distinctive matches first: the spiral model organizes work around risk, whereas waterfall divides work into fixed sequential phases. Evolutionary development permits specifications to grow with successive versions. Component reuse may require adapting desired requirements to available components.

2. Work through the result and its assumptions. Waterfall fixes sequential stages(d); evolution permits incremental specifications(a); reusable components can force requirement compromises(b); spiral development explicitly treats risk(c). The mapping1-d, 2-a, 3-b, 4-c is B.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q56 (printed CS Q46)

**Question:** [Official archived paper page 19](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** -2 to -2

**Derived answer:** −2

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For f(x)=x sin x, the identity f″(x)+f(x)+t cos x=0 holds. Find constant t.

## Solution

1. Method and setup. Differentiate using the product rule twice: first differentiate both x and sin x; then differentiate both terms of the result. Adding f to f″ cancels the x sin x terms. The remaining coefficient of cos x must be zero for the identity to hold for all x.

2. Work through the result and its assumptions. For f=x sin x, f′=sin x+x cos x and f″=2cos x−x sin x. Therefore f″+f+t cos x=(2+t)cos x vanishes identically exactly when t=−2.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS1: Q57 (printed CS Q47)

**Question:** [Official archived paper page 19](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** Both A and D are guaranteed

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A continuous function f on [0,2] satisfies f(0)=f(2)=−1 and f(1)=1. Which must hold? A: Some y∈(0,1) satisfies f(y)=f(y+1). B: Every y∈(0,1) satisfies f(y)=f(2−y). C: The maximum on (0,2) is 1. D: Some y∈(0,1) satisfies f(y)=−f(2−y). The source requests one choice.

## Solution

1. Method and setup. Turn each claimed equality into a zero of a continuous auxiliary function. A difference handles A, while a sum handles D. Opposite endpoint signs force an interior zero by the intermediate value theorem. Continuity does not impose mirror symmetry or prevent values greater than 1 between the given sample points.

2. Work through the result and its assumptions. For A, define h(y)=f(y)−f(y+1). It is continuous on[0, 1], with h(0)=−2 and h(1)=2, so an interior zero exists. But D also follows: g(y)=f(y)+f(2−y) is continuous, g(0)=−2 and g(1)=2, so an interior zero gives f(y)=−f(2−y). Thus both A and D are necessarily true although the official single-choice key is A. This is a literal nonunique-answer discrepancy, not an assumed symmetry of f.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** CS-2014-S1-Q57-TWO-IVT-ANSWERS



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS2: Q14 (printed CS Q4)

**Question:** [Official archived paper page 30](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0 to 0

**Derived answer:** 0

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** The matrix A is the outer product of column vector (2,-4,7)ᵀ and row vector (1,9,5). Find det(A).

## Solution

1. Set up the reasoning. Expand the product conceptually as rows (2,18,10), (-4,-36,-20), and (7,63,35). Each row is a scalar multiple of (1,9,5).

2. Derive the result. The matrix is the outer product of a 3-vector and a row3-vector, so its rank is 1. A3×3 rank-deficient matrix has determinant0.

3. Check the interpretation. A determinant is zero whenever rows are linearly dependent. There is no need to expand nine cofactors, and det(uvᵀ) is not a product of ordinary determinants of the nonsquare factors.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS2: Q15 (printed CS Q5)

**Question:** [Official archived paper page 30](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A nonzero cubic polynomial f(x) has roots 1, 2, and 3. Which must hold? A f(0)f(4)<0; B f(0)f(4)>0; C f(0)+f(4)>0; D f(0)+f(4)<0.

## Solution

1. Set up the reasoning. All three roots exhaust the degree, so f(x)=c(x-1)(x-2)(x-3) for a nonzero real leading coefficient c. Keep c symbolic because its sign is unspecified.

2. Derive the result. Write f(x)=c(x−1)(x−2)(x−3), where real c≠0. Then f(0)=−6c and f(4)=6c, whose product is−36c²<0. Their sum is 0, so only A is forced.

3. Check the interpretation. The two endpoint values have opposite signs regardless of c, but their sum is exactly zero. Thus neither positive-sum nor negative-sum statements can be forced by the roots alone.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS2: Q29 (printed CS Q19)

**Question:** [Official archived paper page 33](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Which requirements-engineering statement is true? A A requirements document also describes efficient implementation of its listed requirements. B Functional requirements are always consistent and complete in practice. C Prototyping is a requirements-validation method. D A requirements review is conducted to find errors in system design.

## Solution

1. Set up the reasoning. Requirements validation asks whether the proposed requirements reflect users' actual needs. A prototype allows users to try representative behavior before committing to the full implementation.

2. Derive the result. Prototypes let users and developers test whether proposed requirements match needs, so they are a validation technique. Requirements specify what is wanted, not efficient implementation details; completeness is not guaranteed, and requirement reviews are not primarily design-error reviews. Thus C.

3. Check the interpretation. A confuses requirements with design, B makes an unrealistic guarantee, and D confuses review of requirements with review of a later design. C identifies a practical validation technique without claiming it proves all requirements correct.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS2: Q56 (printed CS Q46)

**Question:** [Official archived paper page 42](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Newton-Raphson starts at x0=2 for f(x)=0.75x³-2x²-2x+4=0. Consider I x3=0; II the iteration converges to a root in finitely many steps. Which holds? A only I; B only II; C both; D neither.

## Solution

1. Set up the reasoning. Use x(k+1)=xk-f(xk)/f′(xk), where f′(x)=2.25x²-4x-2. Evaluate exact values at the first two iterates to detect a possible cycle.

2. Derive the result. Let f(x)=0.75x³−2x²−2x+4, with f′(x)=2.25x²−4x−2. At x=2, f=−2 and f′=−1, so the next iterate is 0. At0, f=4 and f′=−2, so the next is 2. The sequence cycles2, 0, 2, 0,...; x3=0 but it never converges to a root. Only I holds, A.

3. Check the interpretation. At x=2 the next point is 0, and at x=0 the next point is 2. Neither is a root because their function values are -2 and 4. Returning to the same point after two iterations establishes repetition forever, not convergence.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS2: Q57 (printed CS Q47)

**Question:** [Official archived paper page 42](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 6 to 6

**Derived answer:** 6

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Find the product of the nonzero eigenvalues of the matrix with rows (1,0,0,0,1), (0,1,1,1,0), (0,1,1,1,0), (0,1,1,1,0), (1,0,0,0,1).

## Solution

1. Set up the reasoning. Reorder the coordinate indices as 1,5,2,3,4, applying the same permutation to rows and columns. This similarity transformation preserves eigenvalues and reveals two all-ones diagonal blocks.

2. Derive the result. Permuting coordinates to group indices 1, 5 and 2, 3, 4 makes the matrix block diagonal with all-one blocks J2 and J3. Their spectra are{2, 0} and{3, 0, 0}. The two nonzero eigenvalues multiply to 6.

3. Check the interpretation. An m×m all-ones block has eigenvalue m on the all-ones vector and eigenvalue zero on vectors whose coordinates sum to zero. The full matrix's determinant is zero, but the requested product excludes those zero eigenvalues.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q14 (printed CS Q4)

**Question:** [Official archived paper page 53](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For an n×n matrix with only real eigenvalues, which assertion is always true? A Positive trace and negative determinant imply at least one negative eigenvalue. B Positive trace implies all eigenvalues positive. C Positive determinant implies all eigenvalues positive. D Positive trace-times-determinant implies all eigenvalues positive.

## Solution

Step 1: The trace equals the eigenvalue sum, while the determinant equals their product, including algebraic multiplicities. Step 2: A negative product of real numbers requires a negative factor; none can be zero. Thus A is true, and its positive-trace condition is not even needed for this conclusion. Step 3: A positive sum permits negative terms, and a positive product permits an even number of negative factors. For example diag(3,−1,−1) has trace 1, determinant 3 and positive product of trace and determinant, yet two negative eigenvalues. It refutes B, C and D simultaneously.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q15 (printed CS Q5)

**Question:** [Official archived paper page 54](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 2 to 2

**Derived answer:** 2

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** V1 and V2 are four-dimensional subspaces of a six-dimensional vector space V. What is the smallest possible dimension of V1∩V2?

## Solution

Step 1: Use dim(V1+V2)=dim V1+dim V2−dim(V1∩V2). Step 2: Since V1+V2 is a subspace of V, its dimension is at most 6, so the intersection dimension is at least 4+4−6=2. Step 3: Establish attainability: for a basis e1,…,e6 of V, take V1=span(e1,e2,e3,e4) and V2=span(e3,e4,e5,e6). Their intersection is span(e3,e4), of dimension 2. Therefore the minimum is exactly 2, not merely a lower bound.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q16 (printed CS Q6)

**Question:** [Official archived paper page 54](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 4 to 4

**Derived answer:** 4

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** If the definite integral from 0 to 2π of |x sin x| dx equals kπ, find k.

## Solution

Step 1: On the integration interval x is nonnegative; sin x is nonnegative on [0,π] and nonpositive on [π,2π]. Thus split the absolute-value integral as ∫₀^π x sin x dx−∫π^2π x sin x dx. Step 2: Integration by parts gives the antiderivative −x cos x+sin x. The first ordinary integral is π, and the second is −3π. Step 3: The absolute areas add to π+3π=4π, so k=4. Integrating without splitting the absolute value would incorrectly allow cancellation.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q29 (printed CS Q19)

**Question:** [Official archived paper page 57](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For modular software design, which combination is desirable? A high cohesion/high coupling; B high cohesion/low coupling; C low cohesion/high coupling; D low cohesion/low coupling.

## Solution

Step 1: Cohesion measures how closely a module's internal responsibilities belong together. High cohesion makes its purpose focused and understandable. Step 2: Coupling measures dependencies between modules. Low coupling limits the effect of one module's changes on others and facilitates independent testing. Step 3: The desirable combination is therefore high cohesion and low coupling, B. “High” is not universally good: the two measures describe different relationships.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q56 (printed CS Q46)

**Question:** [Official archived paper page 64](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C under the usual a≤b interval convention

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For K=∫ₐᵇ x² dx, evaluate statements I: trapezoidal-rule K is always at least the exact integral; II: Simpson-rule K is always exact. A I only; B II only; C both; D neither.

## Solution

Step 1: On an ordinary forward interval a≤b, x² is convex because its second derivative is 2. Every trapezoidal chord lies on or above the curve, so summing trapezoid areas overestimates the integral; I holds. Step 2: Simpson’s rule integrates every polynomial of degree at most three exactly when its partition meets the rule's requirements. Since x² has degree two, II holds as well. Step 3: The intended answer is C. Preserve the implicit ordering qualification: reversing integration limits reverses signed errors, so I's inequality is not valid for arbitrary a>b. The source says only that a and b are given.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2014 CS3: Q57 (printed CS Q47)

**Question:** [Official archived paper page 64](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2014.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate ∫₀^π x² cos x dx. A −2π; B π; C −π; D 2π.

## Solution

Step 1: Integrate by parts with u=x² and dv=cos x dx: the integral is [x² sin x]₀^π−2∫₀^π x sin x dx. The boundary term is zero. Step 2: For the remaining integral, another integration by parts gives ∫x sin x dx=−x cos x+sin x. Between 0 and π this is π. Step 3: Therefore the original definite integral is −2π, A. The negative result is possible because cos x is negative over the second half and the x² weight is larger there.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

