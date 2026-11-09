

# GATE 2022 CS: Q20

**Question:** [Official archived paper page 16](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=16); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

## Solution

For A of size m×n and B of size n×m, trace(AB)=Σ_iΣ_j A_ij B_ji=Σ_jΣ_i B_ji A_ij=trace(BA). Both products are square even when their sizes differ. Hence both stated equalities hold, C.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2022 CS: Q34

**Question:** [Official archived paper page 23](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=23); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** -0.5 to -0.5

**Derived answer:** -0.5

## Solution

At x=0 numerator and denominator both vanish. Using e^(2x)=1+2x+O(x²), x/(1−e^(2x))=x/(−2x+O(x²)) tends to −1/2. Thus −0.5.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.


# GATE 2022 CS: Q45

**Question:** [Official archived paper page 30](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=30); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D for unit-diagonal L; C also possible without normalization

## Solution

Gaussian elimination with unit diagonal L gives L=[[1, 0, 0],[1, 1, 0],[2,−1/2, 1]] and U=[[1, 1,−2],[0, 2, 1],[0, 0,−1/2]]. Solving gives (x1, x2, x3)=(0, 2,−1), so L32=−1/2, U33=−1/2, x1=0, official D. However the source does not specify a unit diagonal for L. Replacing L33 by −1/4 and U33 by 2 keeps LU equal to the original coefficient matrix and leaves L32=−1/2, x1=0. That realizes option C as well. Thus uniqueness depends on the unstated Doolittle normalization; the key is retained with that ambiguity open.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** CS-2022-Q45-LU-NORMALIZATION


# GATE 2022 CS: Q53

**Question:** [Official archived paper page 35](https://gate2026.iitg.ac.in/doc/download/2022/cs_2022.pdf#page=35); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** A,C,D

**Derived answer:** A,C,D

## Solution

Multiply each offered vector by the displayed matrix. For A, the result is (-1, 1, 0, 1), equal to the original vector (eigenvalue 1). For B, the result is (-7,-5, 12, 25), not proportional to (1, 0,-1, 0), so B fails. For C the result is (-3, 0, 6, 6)=3(-1, 0, 2, 2), and for D it is (0, 3,-9, 0)=3(0, 1,-3, 0). Thus A, C, D are eigenvectors. All matrix and vector entries were visually checked and the products recomputed independently.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2022/cs_2022.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.
