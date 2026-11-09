

# GATE 2004: Q1 (printed CS Q1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C

**Paraphrased problem context:** What is the goal of structured programming?
Options:
(A) Have well-indented programs
(B) Infer the flow of control from compiled code
(C) Infer the flow of control from program text
(D) Avoid using GOTO statements

## Solution

1. Structured control constructs make the program’s control flow understandable from its source text, C. Indentation helps readability but is not the defining goal, and eliminating every GOTO is a technique rather than the underlying purpose.

2. This general programming-methodology item is retained as supplemental.

3. Teaching check: Sequence, selection and iteration expose control structure directly in the source. Indentation is cosmetic: a well-indented unstructured jump sequence still requires reconstructing its control-flow graph. Conversely, the educational goal is understandability, not a syntactic ban treated as an end in itself.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q27 (printed CS Q27)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** A,B,C,D are n×n matrices with nonzero determinants and ABCD=I. What is B^−1?
Options:
(A) D^−1 C^−1 A^−1
(B) CDA
(C) ADC
(D) It need not exist

## Solution

1. From ABCD=I, multiply on the left by A^-1 to get BCD=A^-1, then on the right by A to get B(CDA)=I. Since B is invertible, B^-1=CDA, B.

2. Factor order matters for matrices.

3. Teaching check: Use multiplication on the correct side: B(CDA)=ABCD conjugated by A, namely A^−1 I A=I. Matrix products generally do not commute. The formula for the inverse of a product reverses factor order and cannot be applied by casually rearranging ABCD.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q28 (printed CS Q28)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Evaluate (113+(−111))+7.51 and 113+((−111)+7.51), rounding to three significant decimal digits after each floating-point operation.
Options:
(A) 9.51 and 10.0
(B) 10.0 and 9.51
(C) 9.51 and 9.51
(D) 10.0 and 10.0

## Solution

1. For the first association,113+(−111)=2 exactly, then2+7.51=9.51. For the second,−111+7.51=−103.49 rounds to−103 with three significant digits;113+(−103)=10.0.

2. Thus9.51 and10.0, A. Rounding is applied after each operation, not merely at the end.

3. Teaching check: Three digits means three significant digits, not three decimal places. The intermediate −103.49 becomes −103, losing 0.49 before the final addition. Floating-point addition is therefore not associative even though exact real-number addition is.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q34 (printed CS Q34)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** An employee system has superclass Employee and subclasses Manager, Engineer and Secretary. Each employee has name, unique ID and salary; salary depends on category. Choose the best design for getName, getId and computeSalary (called getSalary in the numbered statements). (i) Implement getId in superclass; (ii) implement getId in subclass; (iii) getName abstract in superclass; (iv) implement getName in superclass; (v) implement getName in subclass; (vi) getSalary abstract in superclass; (vii) implement getSalary in superclass; (viii) implement getSalary in subclass.
Options:
(A) i,iv,vi,viii
(B) i,iv,vii
(C) i,iii,v,vi,viii
(D) ii,v,viii

## Solution

1. The common name and identifier accessors can be implemented once in Employee, statements i and iv. Salary computation varies by employee category, so declare it abstract in Employee and implement it in each category subclass, vi and viii.

2. Thus A is the best listed design. The narrative says computeSalary while the numbered statements say getSalary; the intended varying salary operation is treated consistently.

3. Teaching check: Inheritance should share the common accessors while polymorphism handles category-specific salary rules. An abstract salary method specifies the common interface without imposing one implementation. Making getName abstract duplicates a behavior that the problem gives no reason to vary.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q71 (printed CS Q71)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=10), physical page 10. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** None

**Paraphrased problem context:** How many solutions has the system? GFG: −x+5y=1; x−y=2; x−3y=3. GateForum differs: −x+5y=−1; x−y=2; x+3y=3. Both readings are retained rather than merging their signs.
Options:
(A) Infinitely many
(B) Two distinct solutions
(C) Unique
(D) None

## Solution

1. The GFG rendering reads −x+5y=1, x−y=2, x−3y=3. The first two give y=3/4 and x=11/4, which yield x−3y=1/2, not 3: no solution (D).

2. GateForum instead prints −x+5y=−1, x−y=2, x+3y=3. Its first two give (x,y)=(9/4,1/4), satisfying the third: a unique solution (C).

3. The source disagreement prevents an unconditional option.

4. Teaching check: Solve two independent equations and substitute into the third rather than counting equations. More equations than unknowns may be inconsistent or redundant. Here changing two signs changes exactly that distinction, so preserving separate source readings is essential.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q80 (printed CS Q80)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=11), physical page 11. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Choose a point uniformly from the rectangle with corners (0,0),(1,0),(1,2),(0,2). If p is its distance from the origin, what is E[p²]?
Options:
(A) 2/3
(B) 1
(C) 4/3
(D) 5/3

## Solution

1. Uniform sampling over [0,1]×[0,2] makes X and Y uniform on their respective intervals. Since p²=X²+Y², E[p²]=E[X²]+E[Y²]=(integral from 0 to1 of x² dx)+(1/2)(integral from 0 to2 of y² dy)=1/3+4/3=5/3, D.

2. This asks for E[p²], not the square of E[p].

3. Teaching check: Uniformity over the rectangle gives density 1/2, so E[Y²]=(1/2)∫₀²y²dy, not simply ∫₀²y²dy. Linearity gives E[X²+Y²] without needing to integrate sqrt(X²+Y²), which would answer a different question.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2004: Q90 (printed CS Q90)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203330/GATE2004.pdf#page=12), physical page 12. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Match styles P=functional, Q=logic, R=object-oriented, S=imperative with characteristics: (1) command-based, procedural; (2) imperative, abstract data types; (3) side-effect-free, declarative, expression evaluation; (4) declarative, clausal representation, theorem proving.
Options:
(A) P-2,Q-3,R-4,S-1
(B) P-4,Q-3,R-2,S-1
(C) P-3,Q-4,R-1,S-2
(D) P-3,Q-4,R-2,S-1

## Solution

1. Functional programming matches side-effect-free declarative expression evaluation (P→3). Logic programming matches declarative clauses and theorem proving (Q→4).

2. In this classification object-oriented programming matches imperative programming with abstract data types (R→2), while imperative programming matches command-based procedural computation (S→1). Thus P-3,Q-4,R-2,S-1 is D.

3. These are textbook paradigm characterizations, not claims that every language implementing a paradigm has only those features.

4. Teaching check: Match the most diagnostic feature first: theorem proving belongs to logic, and expression evaluation without side effects to functional programming. Those two matches fix P and Q, leaving abstract-data-type encapsulation for object orientation and procedural commands for imperative programming.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

