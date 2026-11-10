

# GATE 2003: Q24 (printed CS Q24)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=3), physical page 3. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D under the standard polymorphic-language distinction

**Paraphrased problem context:** Which typing statement is false? A. In statically typed languages each program variable has a fixed type; B. In untyped languages values do not have types; C. In dynamically typed languages variables have no types; D. In all statically typed languages each variable is associated with values of only a single type during execution.

## Solution

1. Static type and runtime class are different concepts. A variable declared as a superclass reference retains that declared type while holding references to multiple subclasses. This gives a counterexample to D without implying that the compiler changes the declared type of the variable.

2. A variable in a statically typed language can have one declared static type while referring at different times to values of different compatible runtime subtypes. For example an Animal reference may refer to Dog and Cat objects. Thus D’s claim that values must have only a single runtime type in all statically typed languages is false. The other statements use the conventional distinction between declared variable types, dynamically typed values and untyped formalisms; that terminology is not uniform across every language theory.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2003: Q41 (printed CS Q41)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** B

**Paraphrased problem context:** The equations are 2x+y−4z=α, 4x+3y−12z=5, and x+2y−8z=7. The second and third coefficient columns are linearly dependent. For how many values of α are there infinitely many solutions? A. 0; B. 1; C. 2; D. Infinitely many.

## Solution

1. The dependence of columns suggests combining y and z, not setting either to zero. Substitute u=y−4z; the last two equations have a nonsingular 2×2 coefficient matrix and determine x,u uniquely. The first then imposes one consistency condition on α. Once it holds, every real z gives a corresponding y, hence a one-parameter infinite solution set.

2. Put u=y−4 z. The last two equations become 4 x+3 u=5 and x+2 u=7, giving x=−11/5 and u=23/5. The first equation is then consistent only for α=2 x+u=1/5. At that value z is free and y=u+4 z, giving infinitely many solutions. Thus exactly one value of α works, option B.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2003: Q42 (printed CS Q42)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=5), physical page 5. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D under the plotted segments

**Paraphrased problem context:** A piecewise-linear f has drawn vertices (0,1), (0.5,0.5), approximately (0.8,−1), (1.55,0.5), and (2.05,1), with first and last straight segments extended. Marked roots are 0.6 and 1.3. Starting points x₀, x₁, x₂ lie respectively in the first descending segment, the steep descending segment, and the final rising segment. Newton–Raphson is started separately from each. Which roots result, in that order? A. (1.3,0.6,0.6); B. (0.6,0.6,1.3); C. (1.3,1.3,0.6); D. (1.3,0.6,1.3). Source defect: the lower vertex is actually labeled (−1.0,0.8), contrary to its plotted location; use the drawn-segment interpretation explicitly rather than silently correcting the label.

## Solution

1. Newton’s formula is x_next=x−f(x)/f′(x). On a straight segment f(x)=ax+b this simplifies to −b/a, the intercept of its extended line, independent of the starting point within that segment. Consequently one must follow the segment containing each new iterate, not simply choose the visually nearest root. The first segment has equation 1−x and the last has equation x−1.05.

2. Newton iteration on a linear segment jumps to that segment’s extended x-intercept. Starting at x₀ on the leftmost segment gives x=1, which is on the rising middle segment and then gives the root 1.3. Starting at x₁ on the steep descending segment gives the root 0.6 immediately. Starting at x₂ on the rightmost segment gives 1.05, then 1.3 on the rising middle segment. Therefore the plotted-segment interpretation gives (1.3,0.6,1.3), D. The lower-vertex label appears as (−1.0,0.8) in both reproductions, inconsistent with its plotted position; the graph instead places it near (0.8,−1.0). The result uses the visibly drawn segments and marked roots, not that reversed coordinate label.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2003-Q42-SOURCE-OR-MODEL



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2003: Q60 (printed CS Q60)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=8), physical page 8. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** C if the runtimes are independent; otherwise underdetermined

**Paraphrased problem context:** A program executes two modules sequentially. Their execution times have probability densities f1(t),f2(t). Which expression gives the density of total execution time?
A. f1(t)+f2(t)
B. ∫[0,t] f1(x)f2(x) dx
C. ∫[0,t] f1(x)f2(t−x) dx
D. max{f1(t),f2(t)} [GateForum; GFG instead prints max{f1(t)+f2(t)}.]
The statement does not explicitly assert independence.

## Solution

1. Let T=T1+T2. A contribution to density near t with T1=x must have T2 near t−x, not x. Nonnegative runtimes restrict x to [0,t].
2. If T1,T2 are independent, their joint density is f1(x)f2(y). Integrating along x+y=t yields ∫[0,t]f1(x)f2(t−x)dx, C.
3. Marginal densities alone do not supply that product. For example, if both times are uniform on [0,1], independent times give a triangular sum density, whereas T2=T1 gives a uniform sum on [0,2]. Sequential execution permits either dependency.
4. Therefore C is conditional on independence; the literal problem is underdetermined. One cannot infer independence merely because the modules run one after another.

Baseline derivation and caveats (retained): For independent nonnegative runtimes T₁,T₂, the density of T₁+T₂ is the convolution f(t)=∫₀ᵗ f₁(x)f₂(t−x) dx, option C. Sequential execution alone does not imply independence. In general the answer is ∫₀ᵗ f₁₂(x,t−x) dx using a joint density, when one exists, and marginal densities f₁,f₂ do not determine it. The same marginal distributions can give different sums under different dependencies, so C requires an extra independence assumption not stated in either reproduction.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** CS-2003-Q60-SOURCE-OR-MODEL



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2003: Q75 (printed CS Q75)

**Question:** [Third-party reproduction](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20211005203452/GATE2003.pdf#page=11), physical page 11. Consult the reproduced wording and choices. Original official provenance and completeness have not been established.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** Not available; no official key located.

**Independently derived answer:** D

**Paraphrased problem context:** A hypothetical object-oriented language supports inheritance and dynamic binding; do not assume Java or C++ semantics beyond those facts.
class P { void f(int i) { print(i); } }
class Q subclass of P { void f(int i) { print(2*i); } }
Execute:
P x=new Q();
Q y=new Q();
P z=new Q();
x.f(1); ((P)y).f(1); z.f(1);
The cast (P)y changes the reference type to P. What is printed?
A. 1 2 1  B. 2 1 1  C. 2 1 2  D. 2 2 2

## Solution

1. Each allocation is new Q(), so all three runtime objects have class Q even where the declared reference type is P.
2. Dynamic binding selects an override from the runtime class of the receiving object. The first call therefore invokes Q.f and prints 2×1=2.
3. Casting y to P affects its static reference type, not the object's runtime class. The second call still invokes Q.f, printing 2; z likewise points to a Q and prints 2.
4. Output 2 2 2 matches D. Static binding would be a different language rule from the one expressly stipulated.

Baseline derivation and caveats (retained): Each allocated object is an instance of Q, including those referenced through a variable or cast of type P. With the stipulated dynamic binding, each call therefore selects Q's overriding method. For argument 1 that method prints 2, giving 2 2 2, option D. An upcast changes the reference's static type, not the runtime object or dynamically selected override.

**Verification:** Independent second derivation and visual source review passed. No official scoring comparison or complete question transcription is claimed.

**Discrepancy / qualification:** See model assumptions in solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

