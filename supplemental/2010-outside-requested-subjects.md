

# GATE 2010: Q12 (printed CS Q2)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Apply one Newton–Raphson iteration to x²−13=0, starting from x₀=3.5. What is the resulting approximation?
Options: (A) 3.575; (B) 3.677; (C) 3.667; (D) 3.607.

## Solution

For f(x)=x²−13, Newton’s update is x₁=x₀−(x₀²−13)/(2x₀). With x₀=3.5, x₁=3.5−(12.25−13)/7=3.607142857…, which rounds to 3.607, D. This is one iteration, not the exact square root.

Teaching detail: Newton’s method replaces the curve locally by its tangent: f(x₀)+f′(x₀)(x₁−x₀)=0. Here f′(x)=2x and the negative residual f(3.5)=−0.75 makes the update increase x by 0.75/7. As a reasonableness check, 3.6²=12.96<13 and 3.61²=13.0321>13, so 3.607 lies in the expected interval.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2010: Q15 (printed CS Q5)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 2. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** Evaluate lim as n→∞ of (1−1/n)^(2n).
Options: (A) 0; (B) e^(−2); (C) e^(−1/2); (D) 1.

## Solution

Let L_n=(1−1/n)^(2n). Its logarithm is 2n log(1−1/n), which tends to −2 since log(1−x)/x tends to −1 as x tends to zero. Exponentiating yields e^(−2), option B.

Teaching detail: A shorter route is the standard limit (1−1/n)^n→e^(−1); squaring it gives e^(−2). It is incorrect to replace the base by its limit 1 first and conclude 1: the exponent also tends to infinity, producing the indeterminate form 1^∞. Taking logarithms resolves that interaction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2010: Q31 (printed CS Q21)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Paraphrased problem context:** Modules A and B each have cyclomatic complexity 10. The combined flow executes A and then B in sequence, with no additional branch between them. What is the cyclomatic complexity of this sequential integration?
Options: (A) 19; (B) 21; (C) 20; (D) 10.

## Solution

For a connected single-entry/single-exit flow graph, cyclomatic complexity is the number of decision points plus one. Complexity 10 in each component means nine independent decisions each. Sequentially composing them adds their decision counts but introduces only one overall baseline path: 9+9+1=19. Equivalently V(A;B)=V(A)+V(B)−1, so A.

Teaching detail: The flow-graph formula gives the same result. Connecting A’s exit to B’s entry adds one edge while leaving N_A+N_B vertices. Thus E−N+2=(E_A−N_A+2)+(E_B−N_B+2)−1=19. Simply adding 10+10 counts the straight-through baseline path twice.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2010: Q32 (printed CS Q22)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 5. Consult original wording and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** Match software-life-cycle activities P Requirements capture, Q Design, R Implementation, S Maintenance with: 1 Module development and integration; 2 Domain analysis; 3 Structural and behavioral modeling; 4 Performance tuning.
Options: (A) P–3,Q–2,R–4,S–1; (B) P–2,Q–3,R–1,S–4; (C) P–3,Q–2,R–1,S–4; (D) P–2,Q–3,R–4,S–1.

## Solution

Requirements capture includes domain analysis (P–2); design includes structural and behavioral modeling (Q–3); implementation covers module development and integration (R–1); and maintenance includes performance tuning (S–4). Thus the matching is P–2,Q–3,R–1,S–4, option B.

Teaching detail: The pairing follows what each phase produces: requirements establish the domain problem; design models the proposed system; implementation creates and combines executable modules; maintenance improves or repairs an existing system. Performance tuning may occur elsewhere in practice, but among these offered one-to-one mappings its intended lifecycle association is maintenance.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2010: Q39 (printed CS Q29)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 6. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** The matrix A=[[2,3],[x,y]] has eigenvalues 4 and 8. Find x,y.
Options: (A) x=4,y=10; (B) x=5,y=8; (C) x=−3,y=9; (D) x=−4,y=10.

## Solution

The trace equals the eigenvalue sum: 2+y=4+8=12, giving y=10. The determinant equals the eigenvalue product: 2y−3x=4·8=32. Substituting y=10 gives x=−4. Thus x=−4,y=10, option D.

Teaching detail: Trace and determinant avoid solving the characteristic polynomial from scratch. Equivalently det(λI−A)=λ²−(2+y)λ+(2y−3x), and the desired polynomial is (λ−4)(λ−8)=λ²−12λ+32. Matching coefficients gives the same two linear equations. Substituting x=−4,y=10 verifies both invariants.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2010: Q54 (printed CS Q44)

**Question:** [Official-source archive](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view), member CS/CS2010.pdf, physical page 11. Consult original wording and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** Find a test suite covering statements S1,S2,S3,S4 in:
begin
 if(a==b) { S1; exit; }
 else if(c==d) { S2; }
 else { S3; exit; }
 S4;
end
Available test properties: T1: a,b,c,d all equal; T2: all distinct; T3: a=b and c≠d; T4: a≠b and c=d.
Options: (A) T1,T2,T3; (B) T2,T4; (C) T3,T4; (D) T1,T2,T4.

## Solution

T1 and T3 both take a==b, execute S1, then exit. T2 takes a!=b and c!=d, executes S3, then exits. T4 takes a!=b and c==d, executes S2 and then S4. Full statement coverage therefore needs T2, T4 and either T1 or T3. Of the offered suites only T1,T2,T4 meets this condition, option D.

Teaching detail: The crucial control-flow feature is exit: neither the S1 branch nor the S3 branch reaches S4. Only T4 covers S2 and S4 together. T2 is indispensable for S3, and one of T1/T3 is indispensable for S1. Thus three tests suffice and two cannot cover all three mutually exclusive branch outcomes.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

