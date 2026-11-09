

# GATE 2000: Q3 (printed A Q1.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203732/GATE2000_compressed-1.pdf#page=1), physical page 1. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Essential problem context (paraphrased):** Find the determinant of the matrix with rows (2,0,0,0),(8,1,7,2),(2,0,2,0),(9,0,6,1). Options: 4,0,15,20.

## Solution

Step 1: Expand along the first row. Only its first entry contributes, so det=2·det[[1,7,2],[0,2,0],[0,6,1]].

Step 2: Expand this minor along its first column to obtain det[[2,0],[6,1]]=2·1−0·6=2.

Therefore the full determinant is 2·2=4, A. Entries below the first-column pivot do not contribute to the selected minor.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2000: Q24 (printed A Q2.1)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203732/GATE2000_compressed-1.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Essential problem context (paraphrased):** X, Y and Z are closed unit intervals. X and Z each overlap Y by length 1/2. If X∩Z has length k, must k=1, k=0, can it be every value in[0,1], or none of these?

## Solution

Step 1: Translate Y to[0,1]. A unit interval overlapping it by exactly 1/2 must start at−1/2 or+1/2. Thus each of X and Z is one of those two intervals.

Step 2: If they choose the same interval, their overlap length is 1. If they choose opposite intervals, they touch at one point and their overlap length is 0. No intermediate length occurs.

Therefore k∈{0,1}, and none of A–C describes the full possibilities: D. The problem does not explicitly require X and Z to be distinct; imposing that would leave only k=0.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2000: Q26 (printed A Q2.3)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203732/GATE2000_compressed-1.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** A

**Essential problem context (paraphrased):** Compare S=sum from i=3 to 100 of i log2 i and T=integral from 2 to 100 of x log2 x dx. Choices S>T,S=T,S<T with 2S>T,or 2S≤T.

## Solution

Step 1: The function f(x)=x log2 x is strictly increasing on[2,100], since f′(x)=log2 x+1/ln2>0.

Step 2: On each interval[i−1,i], the integral of f is strictly less than the width-one rectangle of height f(i). Summing for i=3,…,100 gives T<S.

Thus A. The sum uses right endpoints, so no antiderivative calculation or numerical approximation is needed to establish the strict inequality.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2000: Q27 (printed A Q2.4)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203732/GATE2000_compressed-1.pdf#page=4), physical page 4. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Essential problem context (paraphrased):** Find the least polynomial degree with p(1)=p(3)=p(5)=1 and p(2)=p(4)=−1. Choices1,2,3,4.

## Solution

Step 1: The polynomial changes sign between each consecutive pair 1,2,3,4,5. By continuity, it has at least one distinct zero in each of the four open intervals, so its degree is at least 4.

Step 2: Five prescribed values at distinct points admit an interpolating polynomial of degree at most 4. An explicit one is p(x)=1−(8/3)(x−3)²+(2/3)(x−3)^4: at x=3 it is 1, at x=2,4 it is−1, and at x=1,5 it is 1.

Therefore the minimum is 4, D.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
