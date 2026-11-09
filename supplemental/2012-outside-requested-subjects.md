

# GATE 2012 CS: Q19 (printed CS Q9)

**Question:** [Official archived paper page 3](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Open archive member CS/CS2012.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Consider the function f(x) = sin(x) in the interval x ∈ [π/4, 7π/4]. The number and location(s) of the
        local minima of this function are
        (A) One, at π/2
        (B) One, at 3π/2
        (C) Two, at π/2 and 3π/2
        (D) Two, at π/4 and 3π/2

## Solution

On the restricted domain [π/4, 7π/4], the left endpoint π/4 is a one-sided local minimum because sin x increases immediately to its right. The interior stationary points satisfy cos x=0: π/2 is a maximum and 3π/2 is a minimum. The right endpoint is not a minimum because sin x increases toward it from the left. Thus the restricted-domain convention yields two local minima, π/4 and 3π/2, D. If local extrema are defined to exclude endpoints, only the interior minimum remains; the official key uses the former convention.

Worked check / additional reasoning: A local minimum on a domain means comparison with nearby points belonging to that domain. At the left endpoint there are no allowed comparison points to its left. At 7π/4 there are smaller nearby values to the left, so it is not a minimum.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2012 CS: Q21 (printed CS Q11)

**Question:** [Official archived paper page 3](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Open archive member CS/CS2012.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Let A=[[1,1],[1,−1]]. Find the eigenvalues of A^19.
(A) ±1024 (B) ±1024√2 (C) ±4√2 (D) ±512√2.

## Solution

For A=[[1, 1],[1,−1]], direct multiplication gives A²=2I. Its eigenvalues are √2 and −√2, and powering A raises each eigenvalue to the nineteenth power. Therefore they are ±(√2)^19=±2^9√2=±512√2. Hence D.

Worked check / additional reasoning: The characteristic polynomial is det(A−λI)=(1−λ)(−1−λ)−1=λ²−2. Also A^19=(A²)^9A=512A, so multiplying A’s two eigenvalues by 512 gives the same result without repeated matrix multiplication.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2012 CS: Q38 (printed CS Q28)

**Question:** [Official archived paper page 6](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Open archive member CS/CS2012.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** The bisection method is applied to compute a zero of the function f(x) = x⁴ – x³ – x² – 4 in the
        interval [1,9]. The method converges to a solution after ––––– iterations.
        (A) 1                    (B) 3                    (C) 5                   (D) 7

## Solution

Let f(x)=x⁴−x³−x²−4. Initially f(1)=−5 and f(9)>0. The first midpoint is 5 with f(5)=471>0, leaving [1, 5]. The second is 3 with f(3)=41>0, leaving [1, 3]. The third is 2 with f(2)=16−8−4−4=0. Therefore an exact root is found after three midpoint evaluations, B; no unspecified tolerance is needed.

Worked check / additional reasoning: The sign checks select the half-interval containing a root because f is continuous. The successive midpoint sequence is 5,3,2; counting the initial endpoints as iterations would miscount the actual bisection steps.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

