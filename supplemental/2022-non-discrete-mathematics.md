

# GATE 2022 CS: Q20

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=16), physical page **16**, printed **CS 20**, variant **CS-2022**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 16](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=16); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Paraphrased problem context:** For A of size m×n, B n×m, and C,D n×n, assess 1: tr(AB)=tr(BA), and 2: tr(CD)=tr(DC). A only 1; B only 2; C both; D neither.

## Solution

For A of size m×n and B of size n×m, trace(AB)=Σ_iΣ_j A_ij B_ji=Σ_jΣ_i B_ji A_ij=trace(BA). Both products are square even when their sizes differ. Hence both stated equalities hold, C.

Teaching detail:
Trace only sums diagonal entries, not all entries. (AB)ii=Σj AijBji. Finite sums may be exchanged, and scalar factors commute, giving the diagonal sum of BA. This cyclic identity does not assert AB=BA.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2022 CS: Q34

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=23), physical page **23**, printed **CS 34**, variant **CS-2022**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 23](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=23); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** -0.5 to -0.5

**Derived answer:** -0.5

**Paraphrased problem context:** Evaluate lim as x→0 from above of x/(1−e^(2x)).

## Solution

At x=0 numerator and denominator both vanish. Using e^(2x)=1+2x+O(x²), x/(1−e^(2x))=x/(−2x+O(x²)) tends to −1/2. Thus −0.5.

Teaching detail:
Alternatively l’Hôpital gives numerator derivative 1 and denominator derivative −2e^(2x), yielding −1/2. For small positive x, e^(2x)>1, so the quotient is negative, consistent with the answer.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2022 CS: Q45

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=30), physical page **30**, printed **CS 45**, variant **CS-2022**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 30](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=30); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D for unit-diagonal L; C also possible without normalization

**Paraphrased problem context:** Solve x1+x2−2x3=4, x1+3x2−x3=7, 2x1+x2−5x3=7 using A=LU, lower/upper triangular L/U. Which tuple (L32,U33,x1) is intended? A (2,−1/2,−1); B (2,2,−1); C (−1/2,2,0); D (−1/2,−1/2,0). No diagonal normalization is explicitly stated in the source.

## Solution

Gaussian elimination with unit diagonal L gives L=[[1, 0, 0],[1, 1, 0],[2,−1/2, 1]] and U=[[1, 1,−2],[0, 2, 1],[0, 0,−1/2]]. Solving gives (x1, x2, x3)=(0, 2,−1), so L32=−1/2, U33=−1/2, x1=0, official D. However the source does not specify a unit diagonal for L. Replacing L33 by −1/4 and U33 by 2 keeps LU equal to the original coefficient matrix and leaves L32=−1/2, x1=0. That realizes option C as well. Thus uniqueness depends on the unstated Doolittle normalization; the key is retained with that ambiguity open.

Teaching detail:
Elimination details: R2←R2−R1 gives [0,2,1|3]; R3←R3−2R1 gives [0,−1,−1|−1]. Then R3←R3+(1/2)R2 gives [0,0,−1/2|1/2]. Back substitution yields x3=−1, x2=2, x1=0. The multipliers 1,2,−1/2 populate a unit-diagonal L only if that convention is imposed.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** CS-2022-Q45-LU-NORMALIZATION



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2022 CS: Q53

<!-- original-source-access:start -->
**Actual source access:** [Open actual source question in the official PDF](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=35), physical page **35**, printed **CS 53**, variant **CS-2022**. Continue to following pages for any continuation; some viewers ignore page anchors.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 35](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=35); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A,C,D

**Derived answer:** A,C,D

**Paraphrased problem context:** Which vectors are eigenvectors of M=[[-9,-6,-2,-4],[-8,-6,-3,-1],[20,15,8,5],[32,21,7,12]]? A (−1,1,0,1); B (1,0,−1,0); C (−1,0,2,2); D (0,1,−3,0).

## Solution

Multiply each offered vector by the displayed matrix. For A, the result is (-1, 1, 0, 1), equal to the original vector (eigenvalue 1). For B, the result is (-7,-5, 12, 25), not proportional to (1, 0,-1, 0), so B fails. For C the result is (-3, 0, 6, 6)=3(-1, 0, 2, 2), and for D it is (0, 3,-9, 0)=3(0, 1,-3, 0). Thus A, C, D are eigenvectors. All matrix and vector entries were visually checked and the products recomputed independently.

Teaching detail:
For example, multiplying C row by row gives 9−4−8=−3; 8−6−2=0; −20+16+10=6; −32+14+24=6. Zero coordinates must remain zero in any scalar multiple, so B is immediately ruled out by its second coordinate −5 and fourth coordinate 25.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

