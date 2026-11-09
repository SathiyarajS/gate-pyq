

# GATE 2023 CS: Q18

**Question:** [Official archived paper page 15](https://gate2026.iitg.ac.in/doc/download/2023/cs_2023.pdf#page=15); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Paraphrased problem context:** Let A have rows (1,2,3,4),(4,1,2,3),(3,4,1,2),(2,3,4,1). Let B have rows (3,4,1,2),(4,1,2,3),(1,2,3,4),(2,3,4,1). Which holds? A det A=det B; B det B=−det A; C det A=0; D det(AB)=det A+det B.

## Solution

B is obtained from A by exchanging rows1 and 3, which negates the determinant. Direct elimination gives det(A)=−160 and det(B)=160, so neither is zero or equal. Also det(AB)=det(A)det(B)=−25600, not their sum0. Thus only B. Matrix entries and swapped rows were visually checked.

Teaching detail. A row swap reverses the alternating sign in the determinant definition. It does not depend on the actual values of the other rows, so the visible swap gives the answer immediately. To confirm the exclusions, subtract suitable multiples of row 1 to reduce the determinant to a 3×3 determinant: rows (−7,−10,−13),(−2,−8,−10),(−1,−2,−7) give −160. Determinants multiply under matrix multiplication; they do not add. The explicit nonzero check prevents mistakenly treating A as another true statement.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2023/CS_ANS_GATE2023.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2023 CS: Q28

**Question:** [Official archived paper page 26](https://gate2026.iitg.ac.in/doc/download/2023/cs_2023.pdf#page=26); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 1 mark(s).

**Official answer:** B, D

**Derived answer:** B;D

**Paraphrased problem context:** For f(x)=x³+15x²−33x−36, select true statements: A no local maximum; B a local maximum exists; C no local minimum; D a local minimum exists.

## Solution

Differentiate: f′(x)=3x²+30x−33=3(x−1)(x+11). The derivative changes from positive to negative at−11 and from negative to positive at 1, giving a local maximum and minimum respectively. Equivalently f″(−11)=−36 and f″(1)=36. Therefore B, D.

Teaching detail. A stationary point alone need not be an extremum, so the sign change or second derivative must be checked. Here f′ is positive for x<−11, negative for −11<x<1, and positive for x>1. Therefore the curve rises then falls at −11 and falls then rises at 1. The second derivative gives the same conclusion since neither value is zero. These are local extrema; an odd-degree cubic is unbounded in both directions and has no global maximum or minimum over all real numbers.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2023/CS_ANS_GATE2023.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2023 CS: Q31

**Question:** [Official archived paper page 29](https://gate2026.iitg.ac.in/doc/download/2023/cs_2023.pdf#page=29); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 0 to 0

**Derived answer:** 0

**Paraphrased problem context:** Evaluate the triple integral of 4x²y−z³ over −3≤x≤3, −2≤y≤2, −1≤z≤1, in the order dz dy dx, rounded to the nearest integer.

## Solution

The integral is over the symmetric box x∈[−3, 3], y∈[−2, 2], z∈[−1, 1]. The term4x²y is odd in y and integrates to 0 over its symmetric limits. The term−z³ is odd in z and also integrates to 0. Their sum therefore has integral0, already an integer.

Teaching detail. One can integrate in the stated order to verify the symmetry shortcut. The z integral of −z³ is zero, while integrating 4x²y over a z-interval of length 2 gives 8x²y. Integrating this over y from −2 to 2 gives zero for every fixed x, and the remaining x integration stays zero. Oddness is used in the variable whose bounds are symmetric; the fact that x² is even causes no problem. No rounding uncertainty remains because the value is exactly zero.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2023/CS_ANS_GATE2023.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2023 CS: Q53

**Question:** [Official archived paper page 56](https://gate2026.iitg.ac.in/doc/download/2023/cs_2023.pdf#page=56); consult original wording, diagrams and choices.

**Type / marks:** MSQ, 2 mark(s).

**Official answer:** C, D

**Derived answer:** C, D

**Paraphrased problem context:** Two fair coins are tossed independently. A={HH}, B={HH,HT} (first head), C={HH,TH} (second head). Select true claims: A events A,B independent; B events A,C independent; C events B,C independent; D P(B|C)=P(B).

## Solution

The four outcomes HH, HT, TH, TT are equally likely. P(A)=1/4, P(B)=P(C)=1/2. Since A is a subset of B and of C, P(A intersection B)=P(A intersection C)=1/4, whereas P(A)P(B)=P(A)P(C)=1/8; neither pair is independent. But P(B intersection C)=1/4=P(B)P(C), and P(B given C)=1/2=P(B). Hence C and D.

Teaching detail. Independence asks whether learning one event changes the other's probability, not whether the events overlap. Knowing C leaves the first coin fair, so the two equally likely remaining outcomes HH,TH give P(B|C)=1/2. By contrast, learning A guarantees B, giving P(B|A)=1 rather than P(B)=1/2. The same reasoning applies to C. The direct product checks in the solution are valid because all four outcomes have probability 1/4 under the standard independent fair-coin experiment.

**Verification:** Independent second derivation review passed; [official published key](https://gate2026.iitg.ac.in/doc/download/Answer_keys2023/CS_ANS_GATE2023.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

