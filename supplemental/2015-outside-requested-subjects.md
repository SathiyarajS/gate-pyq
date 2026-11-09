

# GATE 2015 CS1: Q11 (printed CS Q11)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **6**, and locate printed **CS 11** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 6](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** g(x)=1−x and h(x)=x/(x−1). Simplify g(h(x))/h(g(x)). A h(x)/g(x); B −1/x; C g(x)/h(x); D x/(1−x)^2.

## Solution

Substitute before simplifying: g(h(x))=1−x/(x−1)=−1/(x−1), whereas h(g(x))=(1−x)/((1−x)−1)=(x−1)/x. Division gives −x/(x−1)^2. Option D has the same squared denominator but the wrong sign. The original composition needs x≠1 and x≠0; simplification must not silently restore excluded inputs.

Baseline derivation and retained qualifications: For x≠0, 1, g(h(x))=−1/(x−1) and h(g(x))=(x−1)/x. Their ratio is−x/(x−1)^2=h(x)/g(x), A. The exclusions are needed for the displayed compositions and ratio.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q12 (printed CS Q12)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **6**, and locate printed **CS 12** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 6](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate lim as x→∞ of x^(1/x). A ∞; B 0; C 1; D not defined.

## Solution

A variable base with a vanishing exponent is an indeterminate form, so simply calling the exponent zero is not a valid derivation. Take natural logs: ln(x^(1/x))=ln(x)/x. By l'Hôpital's rule this tends to (1/x)/1=0. Continuity of exp then gives exp(0)=1.

Baseline derivation and retained qualifications: Write x^(1/x)=exp((ln x)/x). The exponent tends to 0 as x tends to infinity, so the limit is 1, C.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q16 (printed CS Q16)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **8**, and locate printed **CS 16** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 8](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Match P condition coverage, Q equivalence class partitioning, R volume testing, S alpha testing with i black-box, ii system, iii white-box, iv performance testing. A P-ii Q-iii R-i S-iv; B P-iii Q-iv R-ii S-i; C P-iii Q-i R-iv S-ii; D P-iii Q-i R-ii S-iv.

## Solution

Condition coverage examines internal Boolean decisions, so it requires code structure. Equivalence partitioning selects representative inputs from behaviorally similar classes without inspecting code. Volume testing studies behavior under large data volumes. Alpha testing evaluates the integrated system in the developer's controlled environment. These distinctions give the paper's intended classification C.

Baseline derivation and retained qualifications: Condition coverage is white-box, equivalence partitioning is black-box, volume testing concerns performance, and alpha testing is system testing. Hence P-iii, Q-i, R-iv, S-ii, C.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q25 (printed CS Q25)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **10**, and locate printed **CS 25** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 10](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Which claims are false? I XML supports structured content beyond HTML's limitations; II XML is case-insensitive while HTML is case-sensitive; III XML supports user-defined tags while HTML uses predefined tags; IV XML tags need not be closed but HTML tags must be. A II only; B I only; C II and IV; D III and IV.

## Solution

XML distinguishes names differing in letter case: an opening <Item> cannot be closed by </item>. Every XML element must be properly closed, either by a matching end tag or empty-element syntax. Ordinary HTML syntax is case-insensitive for element names and permits certain omitted end tags. II and IV reverse these relevant distinctions; the question uses conventional HTML rather than XHTML syntax.

Baseline derivation and retained qualifications: XML names are case-sensitive; ordinary HTML element names are case-insensitive. XML requires properly closed elements, including self-closing syntax, while HTML permits omission of certain end tags. Thus II and IV are false, C. XML supports application-defined names; HTML uses its vocabulary.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q33 (printed CS Q33)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **12**, and locate printed **CS 33** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 12](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 5

**Derived answer:** 5

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A=[[2,2],[4,9]]=LU, where L is lower triangular and both U diagonal entries equal 1. Find L's lower diagonal entry l22.

## Solution

Write L=[[a,0],[b,c]] and U=[[1,d],[0,1]]. Their product is [[a,ad],[b,bd+c]]. Matching entries gives a=2, 2d=2, b=4, and 4d+c=9, hence d=1,c=5. The unit diagonal is imposed on U, not L; assuming the common alternative convention of unit-diagonal L would solve a different decomposition.

Baseline derivation and retained qualifications: Let L=[[a, 0],[b, c]] and U=[[1, d],[0, 1]]. Equating LU with[[2, 2],[4, 9]] gives a=2, d=1, b=4, c=9−4=5. Thus l22=5.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q38 (printed CS Q38)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **14**, and locate printed **CS 38** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 14](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 5

**Derived answer:** 5

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Find cyclomatic complexity of: while(first<=last){if(array[middle]<search) first=middle+1; else if(array[middle]==search) found=TRUE; else last=middle-1; middle=(first+last)/2;} if(first>last) notPresent=TRUE;.

## Solution

For a single connected control-flow graph with binary conditions, McCabe complexity is one plus the number of decisions. Count while, if(<), else-if(==), and the final if(>): four decisions, hence five. An unconditional else is not an additional test; assignments are not branches. The code can fail to terminate after finding the value, but that semantic defect does not remove a syntactic decision from its control-flow graph.

Baseline derivation and retained qualifications: The control-flow graph has four binary decisions: the while condition, the first if, the else-if, and the final if. For one connected entry/exit graph, cyclomatic complexity is decisions+1=5. This graph count does not require every syntactic path to be feasible or terminating.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q58 (printed CS Q58)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **21**, and locate printed **CS 58** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 21](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** -1

**Derived answer:** −1

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate integral from 1/π to 2/π of cos(1/x)/x² dx.

## Solution

Let u=1/x, so du=−dx/x². The lower x bound gives u=π and the upper gives u=π/2, reversing order. Therefore the integral is −∫ from π to π/2 cos(u)du=sin(π)−sin(π/2)=−1. The negative answer is plausible because cos(1/x) is nonpositive on this interval; losing the substitution minus sign would give the wrong sign.

Baseline derivation and retained qualifications: An antiderivative of cos(1/x)/x² is−sin(1/x). Evaluating from 1/π to 2/π gives−sin(π/2)+sin(π)=−1. The limits and squared denominator were visually checked.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS1: Q59 (printed CS Q59)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **22**, and locate printed **CS 59** in **CS-2015-S1**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 22](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Matrix A=[[1,4],[b,a]] has eigenvalues −1 and 7. Find (a,b). A (6,4); B (4,6); C (3,5); D (5,3).

## Solution

The sum of eigenvalues equals the trace, so 1+a=6 and a=5. Their product equals determinant, so a−4b=−7. Substitute a=5 to obtain b=3. As a check, the characteristic polynomial is λ²−6λ−7=(λ−7)(λ+1), recovering both given eigenvalues without computing eigenvectors.

Baseline derivation and retained qualifications: The trace is 1+a=(−1)+7=6, so a=5. The determinant is a−4b=(−1)*7=−7, so 5−4b=−7 and b=3. Thus D.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q15 (printed CS Q15)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **31**, and locate printed **CS 15** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 31](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 6

**Derived answer:** 6

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Find the larger eigenvalue of matrix[[4, 5], [2, 1]].

## Solution

For[[4, 5], [2, 1]], the characteristic polynomial is λ²−5λ−6=(λ−6)(λ+1). The larger eigenvalue is 6.

Teaching detail:
Eigenvalues satisfy det(A−λI)=0. Here (4−λ)(1−λ)−10=λ²−5λ−6. Factor it as(λ−6)(λ+1), giving 6 and−1. Their sum 5 matches the matrix trace and their product−6 matches its determinant, providing independent consistency checks. The larger real eigenvalue is 6.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q25 (printed CS Q25)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **34**, and locate printed **CS 25** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 34](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** An SRS should avoid discussing which? A user-interface issues; B nonfunctional requirements; C design specification; D third-party software interfaces.

## Solution

An SRS describes required behavior, interfaces and nonfunctional constraints, not the internal design used to implement them. Therefore design specification, C.

Teaching detail:
Requirements state what externally observable behavior and constraints must be met; design specifies how the implementation will realize them. User-interface behavior, performance or reliability constraints, and required external interfaces can all be legitimate requirements. Selecting internal modules, algorithms or architecture belongs in design rather than being unnecessarily prescribed by the SRS. Thus C is the category to avoid, not all discussion of interfaces.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q29 (printed CS Q29)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **36**, and locate printed **CS 29** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 36](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A under exponent notation convention

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Basic COCOMO uses effort E, development time D, KLOC and constants a_b, b_b, c_b, d_b. Choose formulas: A E=a_b KLOC^b_b, D=c_b E^d_b; B D=a_b KLOC^b_b, E=c_b D^d_b; C E=a_b exp(b_b), D=c_b KLOC^d_b; D E=a_b exp(d_b), D=c_b KLOC^b_b. Source writes “exp” after bases to denote powers; literal exp notation is qualified in solution.

## Solution

Basic COCOMO uses E=a_b·KLOC^(b_b) and D=c_b·E^(d_b). The source writes exp(b_b) and exp(d_b) after the bases, intending exponentiation; with that convention A. If exp literally denotes e raised to its argument, the printed formulas would not be the standard model.

Teaching detail:
COCOMO first estimates person-month effort from code size using a calibrated power law E=a_b·KLOC^b_b. It then estimates calendar duration from effort by D=c_b·E^d_b. The constants depend on project mode. Swapping E and D changes the model: effort and elapsed months are different quantities and not interchangeable. The printed exp notation must be read as the intended exponent placement; the conventional exponential function e^x would yield different equations.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q51 (printed CS Q51)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **45**, and locate printed **CS 51** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 45](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A root-finding procedure stores successive estimates xa, xb and fb=f(xb). Each iteration computes xt, then sets xa=xb, xb=xt, fb=f(xb). Identify the secant update among the displayed alternatives. The correct candidate C is xb−(xb−xa)fb/[fb−f(xa)]. Options: A xb−(fb−f(xa))fb/(xb−xa); B xa−(fa−f(xa))fa/(xb−xa); C xb−(xb−xa)fb/(fb−f(xa)); D xa−(xb−xa)fa/(fb−f(xa)). The procedure does not define fa.

## Solution

The secant through(xa, f(xa)) and(xb, fb) has slope(fb−f(xa))/(xb−xa). Setting its linear approximation to zero gives xt=xb−(xb−xa)*fb/(fb−f(xa)), option C. This uses quantities defined by the procedure and requires a nonzero denominator. An equivalent formula anchored at xa would require fa=f(xa), but fa is not initialized in the displayed procedure.

Teaching detail:
The secant line through (xa, f(xa)) and (xb, fb) has slope (fb−f(xa))/(xb−xa). Its x-intercept solves 0=fb+slope·(xt−xb). Rearranging gives xt=xb−fb(xb−xa)/(fb−f(xa)), exactly C. The stored fb is the current endpoint value, so replacing its numerator by an unrelated function value would not describe this line. The denominator must be nonzero; as with ordinary secant iteration, convergence is not guaranteed for arbitrary starting points.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q56 (printed CS Q56)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **48**, and locate printed **CS 56** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 48](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For f(x)=x^(−1/3) on −1≤x≤1, assess I continuity throughout the interval, II unboundedness, and III nonzero finite area between the curve and x-axis. Options: A II only; B III only; C II and III only; D I, II and III.

## Solution

For real x, x^(−1/3)=1/cuberoot(x) is undefined at 0 and unbounded near it, so I is false and II true. The geometric area is the improper integral 2*integral(0..1)x^(−1/3)dx=2*(3/2)=3, positive and finite. Thus II and III, C; signed cancellation across zero would not be the geometric area.

Teaching detail:
At x=0 the function is undefined and its magnitude grows without bound as x approaches zero, so I is false and II is true. Geometric area uses absolute value, not cancellation of the odd function’s signed integral. On the positive half, ∫₀¹ x^(−1/3)dx=[(3/2)x^(2/3)]₀¹=3/2, finite despite the singularity. The negative half contributes the same area, for total 3. Therefore III is true. A divergent function value at one endpoint does not automatically make an improper integral diverge.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q57 (printed CS Q57)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **48**, and locate printed **CS 57** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 48](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 0

**Derived answer:** 0

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Start with matrix [[3, 4, 45], [7, 9, 105], [13, 2, 195]]. Add row 3 to row 2, then subtract column 3 from column 1. Find the determinant of the resulting matrix.

## Solution

The third column is 15 times the first: 45=15*3, 105=15*7, 195=15*13. The original determinant is therefore 0. Adding one row to another and subtracting one column from another preserve determinant, so the resulting determinant remains 0.

Teaching detail:
Before doing arithmetic, observe that the third column is exactly 15 times the first: 45=15·3, 105=15·7 and 195=15·13. Hence the original determinant is zero. Adding one row to another does not change a determinant; subtracting one column from another also preserves it. After the specified column operation, column 1 is −14 times its former value and remains proportional to column 3, so dependence remains directly visible. The requested determinant is therefore 0 without expanding nine cofactors.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS2: Q64 (printed CS Q64)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **50**, and locate printed **CS 64** in **CS-2015-S2**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 50](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Which statement about code inspection and walkthrough is true? A inspection is carried out once code has been unit tested; B inspection and walkthrough are synonyms; C inspection checks adherence to coding standards; D walkthrough is usually conducted by an independent test team.

## Solution

Formal code inspection includes checking adherence to coding standards, C. Inspection is static and need not wait until unit testing; a walkthrough is typically author-led and is not synonymous with formal inspection or necessarily performed by an independent test team.

Teaching detail:
An inspection is a systematic static review against defect classes and a checklist, which can include naming, formatting, safety and other coding standards. It need not wait for execution or unit testing, so A imposes an unnecessary ordering. A walkthrough is usually author-led and less formal, so it is not simply a synonym or necessarily an independent-test-team activity. Therefore C is the defensible general assertion. These are software-engineering concepts retained as supplemental coverage outside the requested subject taxonomy.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q17 (printed CS Q17)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **59**, and locate printed **CS 17** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 59](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 612 to 613

**Derived answer:** 612.06

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Calculate the function point metric for a software project with external inputs I=30, external outputs O=60, external inquiries E=23, files F=8, and external interfaces N=2. Their respective complexity weights are 4,5,4,10,7. Of fourteen value-adjustment factors, four are not applicable (value 0), four have value 3, and the remaining six have value 4. Use the standard adjusted function-point formula.

## Solution

1. The method first multiplies each information-domain count by its complexity weight and sums to obtain unadjusted function points. It then multiplies that total by 0.65+0.01 times the sum of the fourteen adjustment ratings. Four plus four factors account for eight ratings, leaving six ratings of value 4.

2. Unadjusted points=30·4+60·5+23·4+8·10+2·7=606. Adjustment sum=4·0+4·3+6·4=36. The factor is 0.65+0.01·36=1.01, giving606·1.01=612.06, within the official612 to 613 range.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q18 (printed CS Q18)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **59**, and locate printed **CS 18** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 59](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B conceptually, after fixing HTML attribute syntax

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A server stores ten pages at http://www.yourname.com/var.html, with var=1,...,10. Page W1 (var=1) is saved locally for editing/testing, while the other pages stay on the server. W1 contains relative links of the form “var.html”. Which addition makes all relative links resolve to the server pages? Printed options (including their malformed attribute punctuation): (A) <a href: “http://www.yourname.com/”, href: “...var.html”>; (B) <base href: “http://www.yourname.com/”>; (C) <a href: “http://www.yourname.com/”>; (D) <base href: “http://www.yourname.com/”, range: “...var.html”>. Distinguish the intended element from valid HTML syntax.

## Solution

1. A base element sets the base URL used to resolve relative links, so the intended B is <base href="http://www.yourname.com/">.

2. Anchor elements only make individual links. The printed options use href: rather than href=; literal B therefore is not the required valid HTML attribute assignment. Retain the official conceptual answer with the syntax correction explicit.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** CS-2015-S3-Q18-HTML-SYNTAX



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q23 (printed CS Q23)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **61**, and locate printed **CS 23** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 61](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** The matrix A has rows (1,−1,2), (0,1,0), (1,2,1). One eigenvalue is 1. Which set gives all eigenvectors for that eigenvalue? Each option uses nonzero real α: (A) {α(4,2,1)}; (B) {α(−4,2,1)}; (C) {α(√2,0,1)}; (D) {α(−√2,0,1)}.

## Solution

1. Explicitly, A−I has rows (0,−1,2), (0,0,0), (1,2,0). Its middle equation imposes no extra constraint. Taking the free coordinate z=t gives v=t(−4,2,1); exclude t=0 because an eigenvector must be nonzero.

2. Solving(A−I)v=0 gives−y+2z=0 and x+2y=0. Therefore y=2z, x=−4z, so the nonzero eigenvectors are scalar multiples of(−4, 2, 1), B.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q24 (printed CS Q24)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **61**, and locate printed **CS 24** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 61](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Evaluate lim as x→∞ of (1+x²) raised to the power e^(−x). Options: (A) 0; (B) 1/2; (C) 1; (D) ∞.

## Solution

1. This is a ∞⁰ form, so neither the base nor the exponent alone determines the answer. Exponential growth dominates logarithmic growth: ln(1+x²)/e^x tends to 0. Continuity of exp then gives exp(0)=1.

2. Take logarithms: ln[(1+x²)^(e^(−x))]=ln(1+x²)/e^x→0. Exponentiating gives limit1, C.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q33 (printed CS Q33)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **64**, and locate printed **CS 33** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 64](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 1 mark(s).

**Official answer:** 28

**Derived answer:** 28

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A program is deliberately seeded with 100 artificial faults. Testing detects 159 faults in total, including 75 seeded faults. Assuming real and seeded faults have the same nature and distribution, estimate the number of undetected real faults.

## Solution

1. The fraction 75/100 estimates the detection probability, not the fraction of detected faults that are artificial. First separate the 159 detected faults into 75 artificial and 84 real, then use the common detection-rate assumption only on the real population.

2. The detected seeded fraction is 75/100=0.75. Detected real faults number159−75=84. Under equal detectability, estimated total real faults=84/0.75=112, leaving112−84=28 undetected.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q36 (printed CS Q36)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **65**, and locate printed **CS 36** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 65](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** NAT, 2 mark(s).

**Official answer:** 308 to 310

**Derived answer:** 309.33

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** A motorbike starts from rest. Its measured velocities v in km/min at times t in minutes are t=(2,4,6,8,10,12,14,16,18,20), v=(10,18,25,29,32,20,11,5,2,0). Thus the initial point is (t,v)=(0,0). Approximate distance traveled in the first 20 minutes using composite Simpson's 1/3 rule and round to two decimal places.

## Solution

1. Starting from rest supplies v(0)=0.

2. With ten equal subintervals of width h=2, composite Simpson’s rule uses endpoint weights 1, odd-index weights 4, and even-index weights 2. The odd-index velocity sum is 10+25+32+11+2=80; the even-index sum is 18+29+20+5=72. Hence distance ≈ (2/3)[0+0+4·80+2·72]=(2/3)·464=309.333333 km, rounded to 309.33 km. This is inside the official 308–310 interval. The baseline derived_answer 308.67 was an arithmetic error. The arithmetic correction to 309.33 was independently checked against the source table; the official scoring range is unchanged.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q52 (printed CS Q52)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **73**, and locate printed **CS 52** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 73](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For real coefficients p,q,r, the homogeneous system px+qy+rz=0; qx+ry+pz=0; rx+py+qz=0 has a nontrivial solution. Which condition must hold? (A) p−q+r=0 or p=q=−r; (B) p+q−r=0 or p=−q=r; (C) p+q+r=0 or p=q=r; (D) p−q+r=0 or p=−q=−r. The real-coefficient convention is needed for the sum-of-squares characterization.

## Solution

1. A nontrivial homogeneous solution requires determinant zero.

2. The determinant is minus(p³+q³+r³−3pqr), which factors as −(p+q+r)((p−q)²+(q−r)²+(r−p)²)/2. Over real coefficients this vanishes exactly when p+q+r=0 or p=q=r, C. The real-domain convention matters for the sum-of-squares implication.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q54 (printed CS Q54)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **74**, and locate printed **CS 54** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 74](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** For every nonzero real x, a function f satisfies a f(x)+b f(1/x)=1/x−25, where a≠b. Find ∫ from 1 to 2 of f(x) dx. Options: (A) [a(ln2−25)+47b/2]/(a²−b²); (B) [a(2ln2−25)−47b/2]/(a²−b²); (C) [a(2ln2−25)+47b/2]/(a²−b²); (D) [a(ln2−25)−47b/2]/(a²−b²). Explain why the denominator is nonzero for an existing such function.

## Solution

1. Replace x by 1/x to obtain a f(1/x)+b f(x)=x−25.

2. Eliminate f(1/x): f(x)=[a/x−bx−25a+25b]/(a²−b²). Integrating from 1 to 2 yields[a(ln2−25)+(47/2)b]/(a²−b²), A. The source states a≠b. Existence of f at x=1 also forces a+b≠0, since (a+b)f(1)=−24. Together these ensure a²−b² is nonzero.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2015 CS3: Q58 (printed CS Q58)

<!-- original-source-access:start -->
**Actual source access:** [Open official-linked CS.zip](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view). Extract **CS/CS2015.pdf**, open physical PDF page **76**, and locate printed **CS 58** in **CS-2015-S3**. This is ZIP/member navigation, not a direct question-page link.
<!-- original-source-access:end -->

**Question:** [Official archived paper page 76](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Open archive member CS/CS2015.pdf inside the linked official CS.zip. Page numbers refer to the extracted PDF, not the Drive preview.

**Paraphrased problem context:** Find McCabe cyclomatic complexities of X,Y,Z in that order. Program X:
sumcal(int maxint,int value) {
 int result=0,i=0;
 if(value<0) { value=-value; }
 while((i<value) AND (result<=maxint)) { i=i+1; result=result+1; }
 if(result<=maxint) { printf(result); } else { printf("large"); }
 printf("end of program");
}
The shown control-flow graph Y has eight vertically ordered nodes v1,...,v8, edges vi→v(i+1) for i=1,...,7, and back edges v3→v1, v6→v4, v8→v1. Graph Z is serial composition of the graph of X followed by the graph of Y. Options: (A) 4,4,7; (B) 3,4,7; (C) 4,4,8; (D) 4,3,8. State the convention for counting the compound while condition.

## Solution

1. Treat each compound source-level condition as one decision: X has its first if, the while, and the final if, so complexity4.

2. The shown Y graph has 8 vertices and 10 edges, giving E−N+2=4. Serial composition adds complexities minus1, so Z=4+4−1=7. Thus A. Expanding the short-circuit AND into separate predicate nodes would increase X to 5 and Z to 8; the official answer uses source-statement predicate counting rather than that expanded control-flow model.

**Verification:** Independent second derivation review passed; [official published key](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

