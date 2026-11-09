

# GATE 2013 CS: Q13 (printed CS Q3)

**Question:** [Official archived paper page 2](https://web.archive.org/web/20130418030400id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/CS-A.pdf#page=2); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Archived official IIT Bombay booklet A. Physical PDF page numbers are used; ORS code A is the matching key column. Booklets B/C/D permute the same questions, not separate sessions.

**Paraphrased problem context:** Let Δ have rows (1, x, x²),(1, y, y²),(1, z, z²). Which determinant is not identically Δ? A rows (1, x(x+1), x+1),(1, y(y+1), y+1),(1, z(z+1), z+1). B rows (1, x+1, x²+1),(1, y+1, y²+1),(1, z+1, z²+1). C rows (0, x−y, x²−y²),(0, y−z, y²−z²),(1, z, z²). D rows (2, x+y, x²+y²),(2, y+z, y²+z²),(1, z, z²).

## Solution

Let the original columns be u, v, w. Option A has columns u, v+w, u+v. Multilinearity removes repeated-column terms and leaves det(u, w, v)=−det(u, v, w). The other options use determinant-preserving row/column additions or differences. Thus A is the expression not identically equal to the original determinant. If the original determinant happens to be0, its negative also equals it; the question is understood as asking for a general identity, not pointwise inequality for every possible entry.

Teaching detail:
For A, the new columns are u, v+w, u+v, where the old columns are u=(1, 1, 1), v=(x, y, z), w=(x², y², z²). Expanding in columns leaves only det(u, w, v), because every other term repeats u or v. One swap of v and w changes the determinant sign. B merely adds column1 to columns2 and 3. C replaces row1 by r1−r2 and row2 by r2−r3, with row3 retained; D uses r1+r2, r2+r3, r3. The respective row-transformation matrices for C and D are triangular with diagonal1, so both preserve Δ. A is the failed general identity, although −Δ=Δ at singular instances.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20130418034853id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/cs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2013 CS: Q21 (printed CS Q11)

**Question:** [Official archived paper page 3](https://web.archive.org/web/20130418030400id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/CS-A.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Archived official IIT Bombay booklet A. Physical PDF page numbers are used; ORS code A is the matching key column. Booklets B/C/D permute the same questions, not separate sessions.

**Paraphrased problem context:** Match P service-oriented computing, Q heterogeneous communicating systems, R information representation, S process description to 1 interoperability, 2 BPMN, 3 publish-find-bind, 4 XML. A P1 Q2 R3 S4; B P3 Q4 R2 S1; C P3 Q1 R4 S2; D P4 Q3 R2 S1.

## Solution

Service-oriented computing uses publish/find/bind interactions, giving P→3. Heterogeneous systems require interoperability, Q→1. Neutral data representation is provided by XML, R→4. Business-process composition corresponds to BPMN, S→2. This mapping is C.

Teaching detail:
The service workflow publishes a description, lets a client find it, then binds the client to the provider, fixing P→3. Interoperability is the ability of heterogeneous systems to communicate, fixing Q→1. XML is a structured information representation, giving R→4. BPMN explicitly denotes Business Process Model and Notation, giving S→2. Checking these four associations against the complete choices leaves C, not a mapping chosen from only one match.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20130418034853id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/cs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2013 CS: Q32 (printed CS Q22)

**Question:** [Official archived paper page 5](https://web.archive.org/web/20130418030400id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/CS-A.pdf#page=5); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Archived official IIT Bombay booklet A. Physical PDF page numbers are used; ORS code A is the matching key column. Booklets B/C/D permute the same questions, not separate sessions.

**Paraphrased problem context:** Which function is continuous at 3? A f(3)=2, f(x)=x−1 for x>3, f(x)=(x+3)/3 for x<3. B f(3)=4, f(x)=8−x otherwise. C f(x)=x+3 for x≤3 and x−4 for x>3. D f(x)=1/(x³−27) for x≠3, with no value supplied at 3.

## Solution

For option A, the left limit is(3+3)/3=2, the right limit is 3−1=2, and f(3)=2. All agree. B has limit5 but value 4; C has unequal one-sided limits6 and−1; D is undefined at 3. Hence A.

Teaching detail:
Continuity at a point needs three things: the function value must exist, both one-sided limits must agree, and their common value must equal the function value. A satisfies all three with value 2. B approaches5 but assigns4, a removable discontinuity. C approaches6 from the left and−1 from the right, a jump. D provides no finite value at 3 and its denominator vanishes there, so it cannot meet the continuity test as given.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20130418034853id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/cs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2013 CS: Q33 (printed CS Q23)

**Question:** [Official archived paper page 5](https://web.archive.org/web/20130418030400id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/CS-A.pdf#page=5); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Archived official IIT Bombay booklet A. Physical PDF page numbers are used; ORS code A is the matching key column. Booklets B/C/D permute the same questions, not separate sessions.

**Paraphrased problem context:** For x=0,.3,.6,.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, the ordinates are0,.09,.36,.81, 1.44, 2.25, 3.24, 4.41, 5.76, 7.29, 9.00. Approximate the integral from 0 to 3 using the trapezoidal rule. A8.983, B9.003, C9.017, D9.045.

## Solution

The spacing is h=.3. The nine interior ordinates sum to 25.65. The composite trapezoidal estimate is .3[(0+9)/2+25.65]=.3×30.15=9.045, D.

Teaching detail:
Each interval contributes its width times the average of its two endpoint heights. On adding ten intervals of equal width.3, each interior ordinate is counted twice inside the half-weighted sum, while endpoints appear once. Thus use .3[(f(0)+f(3))/2+Σ interior values]. The interior sum .09+.36+.81+1.44+2.25+3.24+4.41+5.76+7.29 is 25.65, giving 9.045. Although these ordinates equal x², the question asks the trapezoidal estimate, not the exact integral9.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20130418034853id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/cs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2013 CS: Q48 (printed CS Q38)

**Question:** [Official archived paper page 8](https://web.archive.org/web/20130418030400id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/CS-A.pdf#page=8); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Archived official IIT Bombay booklet A. Physical PDF page numbers are used; ORS code A is the matching key column. Booklets B/C/D permute the same questions, not separate sessions.

**Paraphrased problem context:** Two access-graph modules each have4attribute nodes. M1 has 4 methods and M2 has 3; each method accesses2 attributes of its own module. Method m in M1 additionally accesses2 attributes in M2. Move m to M2, keeping attributes fixed. Under access-density cohesion and cross-module access coupling, what changes? A neither; B cohesion rises, coupling falls; C both fall; D both rise. Filled circles in the source are methods, unfilled circles attributes.

## Solution

The diagram shows m accessing two attributes in its own module and two in the other. Moving m exchanges two internal accesses for two external ones in each direction, so the number of cross-module accesses remains2. Every method accesses two of the four attributes of its current module; internal access densities stay8/16=.5 and 6/12=.5 before the move, then6/12=.5 and 8/16=.5 after. Thus average cohesion and coupling are unchanged under this access-based measure, A.

Teaching detail:
Before moving m, internal accesses total 4×2=8in M1 and 3×2=6in M2; possible method-attribute pairs are4×4=16and3×4=12. Both densities are1/2. After moving m, the method counts exchange, so the two densities remain6/12and8/16. The two accesses from m to M2 become internal, but its two accesses to its old M1 attributes become external. Thus cross-module accesses stay2. The conclusion is tied to this access-graph measure, rather than every possible software cohesion metric.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20130418034853id_/http://www.gate.iitb.ac.in:80/gate2013/wp-content/uploads/2013/03/cs.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

