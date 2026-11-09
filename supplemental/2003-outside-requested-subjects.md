

# GATE 2003: Q24 (printed CS Q24)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D under the standard polymorphic-language distinction

## Solution

A variable in a statically typed language can have one declared static type while referring at different times to values of different compatible runtime subtypes. For example an Animal reference may refer to Dog and Cat objects. Thus D’s claim that values must have only a single runtime type in all statically typed languages is false. The other statements use the conventional distinction between declared variable types, dynamically typed values and untyped formalisms; that terminology is not uniform across every language theory.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2003: Q41 (printed CS Q41)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

## Solution

Put u=y−4z. The last two equations become 4x+3u=5 and x+2u=7, giving x=−11/5 and u=23/5. The first equation is then consistent only for α=2x+u=1/5. At that value z is free and y=u+4z, giving infinitely many solutions. Thus exactly one value of α works, option B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.


# GATE 2003: Q42 (printed CS Q42)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D under the plotted segments

## Solution

Newton iteration on a linear segment jumps to that segment’s extended x-intercept. Starting at x₀ on the leftmost segment gives x=1, which is on the rising middle segment and then gives the root 1.3. Starting at x₁ on the steep descending segment gives the root 0.6 immediately. Starting at x₂ on the rightmost segment gives 1.05, then 1.3 on the rising middle segment. Therefore the plotted-segment interpretation gives (1.3,0.6,1.3), D. The lower-vertex label appears as (−1.0,0.8) in both reproductions, inconsistent with its plotted position; the graph instead places it near (0.8,−1.0). The result uses the visibly drawn segments and marked roots, not that reversed coordinate label.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2003-Q42-SOURCE-OR-MODEL


# GATE 2003: Q60 (printed CS Q60)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=8), physical page 8. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C if the runtimes are independent; otherwise underdetermined

## Solution

For independent nonnegative runtimes T₁,T₂, the density of T₁+T₂ is the convolution f(t)=∫₀ᵗ f₁(x)f₂(t−x) dx, option C. Sequential execution alone does not imply independence. In general the answer is ∫₀ᵗ f₁₂(x,t−x) dx using a joint density, when one exists, and marginal densities f₁,f₂ do not determine it. The same marginal distributions can give different sums under different dependencies, so C requires an extra independence assumption not stated in either reproduction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2003-Q60-SOURCE-OR-MODEL


# GATE 2003: Q75 (printed CS Q75)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=11), physical page 11. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

## Solution

Each allocated object is an instance of Q, including those referenced through a variable or cast of type P. With the stipulated dynamic binding, each call therefore selects Q's overriding method. For argument 1 that method prints 2, giving 2 2 2, option D. An upcast changes the reference's static type, not the runtime object or dynamically selected override.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.
