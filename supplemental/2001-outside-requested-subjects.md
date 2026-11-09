

# GATE 2001: Q1 (printed A Q1.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203551/GATE2001.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A for n≥2; C if n=1

**Essential problem context (paraphrased):** For n×n matrices, assess two possibility claims: two singular matrices may have a nonsingular sum; two nonsingular matrices may have a singular sum. Options A/B/C/D mean respectively both true, only the first true, only the second true, neither true.

## Solution

Step 1: Test the existential claims with examples. For n=2, diag(1,0) and diag(0,1) are singular but their sum I is nonsingular. For larger n, split the identity diagonal between two complementary nonempty blocks.

Step 2: I and −I are nonsingular, while I+(−I)=0 is singular. Thus both possibilities occur, giving A in the intended dimension range.

Qualification: For n=1 the only singular scalar matrix is zero, and adding two zeros remains singular. Then S1 is false and S2 true, giving C. The problem does not explicitly exclude this boundary case.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2001-Q1-DIMENSION-ONE-BOUNDARY
