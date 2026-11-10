

# GATE 2020 CS: Q11 (printed CS Q1)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=3), physical page **3**, printed **CS 1**, variant **CS-2020**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 3](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Paraphrased problem context:** Which functions increase throughout [0,1]? I e^(−x); II x²−sin x; III √(x³+1). Options: A III only; B II only; C II and III; D I and III.

## Solution

Worked explanation

For a differentiable function, a negative derivative anywhere in the interior rules out increasing throughout the interval. Function I has derivative −e^(−x)<0 everywhere. For II, continuity of 2x−cos x and its value −1 at zero imply negativity on some interval immediately to the right of zero. Function III has derivative 3x²/(2√(x³+1)), positive for x>0 and zero only at the endpoint. A zero derivative at one endpoint does not prevent strict increase: for x<y, x³+1<y³+1, and square root preserves this inequality.

Derivation and answer

The derivative of e^(−x) is negative. The derivative of x²−sin x is 2x−cos x, which is−1 at 0 and remains negative nearby, so that function is not increasing throughout the interval. The third function√(x³+1) is strictly increasing on[0, 1] since both x³ and square root are strictly increasing there. Only III, A.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=17) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2020 CS: Q37 (printed CS Q27)

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=9), physical page **9**, printed **CS 27**, variant **CS-2020**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 9](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=9); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Paraphrased problem context:** For real n×n matrices A,B, test I rank(AB)=rank(A)rank(B); II det(AB)=det(A)det(B); III rank(A+B)≤rank(A)+rank(B); IV det(A+B)≤det(A)+det(B). A I,II; B I,IV; C II,III; D III,IV.

## Solution

Worked explanation

The product determinant identity is valid even for singular matrices. For the rank inequality, every column of A+B is a sum of a column of A and a column of B, so its span lies in col(A)+col(B). The dimension of a sum of subspaces is at most the sum of their dimensions, proving III. To refute universal assertions, one legal counterexample suffices: choose 2×2 identities. AB=I has rank 2, not 4, and A+B=2I has determinant 4, exceeding det A+det B=2. Rank multiplication is not the correct rule; a useful correct bound is rank(AB)≤min(rank A,rank B).

Derivation and answer

Determinants multiply, so II is true. The column space of A+B is contained in the sum of the column spaces of A and B, proving rank(A+B)≤rank(A)+rank(B), III. With A=B=I2, rank(AB)=2 differs from 2·2=4, refuting I, while det(A+B)=4 exceeds 1+1=2, refuting IV. Thus C.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/2020/cs_2020.pdf#page=17) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

