

# GATE 2010: Q12 (printed CS Q2)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

For f(x)=x²−13, Newton’s update is x₁=x₀−(x₀²−13)/(2x₀). With x₀=3.5, x₁=3.5−(12.25−13)/7=3.607142857…, which rounds to 3.607, D. This is one iteration, not the exact square root.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2010: Q15 (printed CS Q5)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

## Solution

Let L_n=(1−1/n)^(2n). Its logarithm is 2n log(1−1/n), which tends to −2 since log(1−x)/x tends to −1 as x tends to zero. Exponentiating yields e^(−2), option B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2010: Q31 (printed CS Q21)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

## Solution

For a connected single-entry/single-exit flow graph, cyclomatic complexity is the number of decision points plus one. Complexity 10 in each component means nine independent decisions each. Sequentially composing them adds their decision counts but introduces only one overall baseline path: 9+9+1=19. Equivalently V(A;B)=V(A)+V(B)−1, so A.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2010: Q32 (printed CS Q22)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

## Solution

Requirements capture includes domain analysis (P–2); design includes structural and behavioral modeling (Q–3); implementation covers module development and integration (R–1); and maintenance includes performance tuning (S–4). Thus the matching is P–2,Q–3,R–1,S–4, option B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2010: Q39 (printed CS Q29)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

The trace equals the eigenvalue sum: 2+y=4+8=12, giving y=10. The determinant equals the eigenvalue product: 2y−3x=4·8=32. Substituting y=10 gives x=−4. Thus x=−4,y=10, option D.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2010: Q54 (printed CS Q44)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

T1 and T3 both take a==b, execute S1, then exit. T2 takes a!=b and c!=d, executes S3, then exits. T4 takes a!=b and c==d, executes S2 and then S4. Full statement coverage therefore needs T2, T4 and either T1 or T3. Of the offered suites only T1,T2,T4 meets this condition, option D.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
