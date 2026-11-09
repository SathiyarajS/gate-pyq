

# GATE 1999: Q23 (printed A Q1.23)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203805/GATE1999.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Essential problem context (paraphrased):** Newton–Raphson starts at x0. Does it converge always, only for polynomials, only if f(x0)<0, or none?

## Solution

Newton iteration is x_next=x−f(x)/f′(x), so zero derivatives or a poor initial point can prevent convergence. For f(x)=x³−2x+2 and x0=0, the iteration cycles 0→1→0, disproving always. Nonpolynomial smooth functions can converge near a simple root, disproving the polynomial restriction. For f(x)=x−1 with x0=2, f(x0)>0 yet one step reaches the root, disproving the sign restriction. Therefore D. Standard local convergence hypotheses concern smoothness, a simple root and sufficient initial proximity.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
