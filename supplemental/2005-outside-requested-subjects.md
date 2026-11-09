

# GATE 2005: Q3 (printed CS Q3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203225/GATE2005.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** Common property of logic and functional languages? A procedural; B based on lambda calculus; C declarative; D use Horn clauses.

## Solution

Logic programming states logical relations, while functional programming expresses computations through functions rather than imperative state-changing instruction sequences. Both are conventionally classified as declarative, C. Lambda calculus is the usual basis for functional programming; Horn clauses are associated with logic programming, not both paradigms.

Teaching detail:
Logic programs describe facts/rules and functional programs compose function expressions. Both conventionally emphasize what result or relation is specified rather than a sequence of mutable-state commands, hence declarative. Functional foundations commonly use lambda calculus; Horn clauses are associated with logic programming. Neither foundation is common to both simply because both are declarative.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2005: Q4 (printed CS Q4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203225/GATE2005.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B under the conventional classification

**Paraphrased problem context:** Which are essential conventional OOP features? I abstraction/encapsulation; II strict typing; III type safety with subtype rule; IV polymorphism with inheritance. A I/II; B I/IV; C I/II/IV; D I/III/IV.

## Solution

Abstraction/encapsulation and subtype polymorphism with inheritance are standard object-oriented features, statements i and iv. Object-oriented languages can be dynamically typed and need not enforce the particular strict typing/type-safety requirements in ii and iii. Thus B. This is the conventional feature taxonomy, not a theorem that every language called object-oriented must use class inheritance.

Teaching detail:
Encapsulation groups state with operations and hides representation, while polymorphism allows a common interface to have different implementations. These are I and IV in the question’s conventional taxonomy. Dynamic object-oriented languages show that strict static typing is not required; the specific type-safety/subtyping rule is also not universal. The classification is pedagogical, not a mathematical definition excluding prototype-based OOP.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2005: Q12 (printed CS Q12)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203225/GATE2005.pdf#page=2), physical page 2. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** For continuous probability density f of X, express P(a<X≤b): A f(b−a); B f(b)−f(a); C ∫_a^b f(x)dx; D ∫_a^b x f(x)dx.

## Solution

For a≤b, probability P(a<X≤b)=∫_a^b f(x)dx, C. Individual endpoints have probability zero for a continuous distribution. The integral of xf(x) instead contributes to an expectation.

Teaching detail:
A density is integrated over an interval to obtain probability, so P(a<X≤b)=∫_a^b f(x)dx. A single point has probability zero for a continuous density, making endpoint inclusion immaterial here. The expression f(b)−f(a) uses density values rather than cumulative probabilities; multiplying by x would instead compute a truncated first moment. Hence C.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2005: Q48 (printed CS Q48)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203225/GATE2005.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** Determine the solution count of 2x1−x2−3x3=1, 3x1+2x2+5x3=2, −x1+4x2+x3=3: A no solution; B unique; C more than one but finitely many; D infinitely many. The alternate reproduction changes the first −3x3 to +3x3.

## Solution

GFG prints the first equation as 2x1−x2−3x3=1; the other rows are (3, 2, 5) and (−1, 4, 1). Its coefficient determinant is −70, so the solution is unique (B), specifically (37/70, 67/70,−3/10). GateForum changes −3x3 to +3x3; that determinant is 14 and also gives a unique solution, (−25/14,−1/14, 3/2). The option conclusion agrees, but the equation and numeric solution do not; original fidelity is unverified.

Teaching detail:
For a square linear system, a nonzero determinant means the coefficient map is invertible, so every right-hand side has exactly one preimage. Expanding the GFG determinant gives 2(2−20)+1(3+5)−3(12+2)=−70. This proves uniqueness without needing the actual solution. Substituting the stated triple checks the arithmetic. Replacing −3 by +3 changes the determinant to 14, still nonzero, so the alternative source gives the same choice but different numeric coordinates.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2005-Q48-COEFFICIENT-SIGN



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2005: Q49 (printed CS Q49)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203225/GATE2005.pdf#page=6), physical page 6. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** Find the eigenvalues of [[2,−1],[−4, 5]]. A −1, 1; B 1, 6; C 2, 5; D 4,−1.

## Solution

det(λI−A)=(λ−2)(λ−5)−4=λ²−7λ+6=(λ−1)(λ−6). The eigenvalues are 1 and 6, option B.

Teaching detail:
An eigenvalue λ makes A−λI singular. The characteristic polynomial is (2−λ)(5−λ)−4, since the off-diagonal product is positive 4. Expanding yields λ²−7λ+6=(λ−1)(λ−6). The sum 7 equals the trace and product 6 equals the determinant, providing two quick independent checks. Reading the diagonal 2, 5 as eigenvalues would only be valid for triangular matrices, not this matrix.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

