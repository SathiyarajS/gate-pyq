

# GATE 2011 CS: Q15 (printed CS Q5)

**Question:** [Official archived paper page 2](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=2); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** B

**Derived answer:** B

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** Software can be developed in L1 or L2. L2 needs twice as many lines of code as L1. For either language development effort is LOC/10000 man-years. Development cost per man-year is Rs 1000000 for L1 and Rs 750000 for L2. Maintenance lasts five years, at Rs 100000 per year for L1 and Rs 50000 per year for L2. For what L1 LOC do total development plus maintenance costs agree?

(A) 4000
(B) 5000
(C) 4333
(D) 4667

## Solution

Let L1 require x lines and L2 require2x. Their development costs are100x and 150x rupees, respectively. Five-year maintenance costs are500000 and 250000. Equating100x+500000=150x+250000 gives x=5000, B.

The LOC-to-effort conversion must be done separately for each language: x/10000 man-years for L1 versus 2x/10000 for L2. Multiplying by their respective annual development rates produces 100x and 150x. L2 is dearer to develop by 50x but cheaper to maintain by Rs 250000 over five years. Equality therefore occurs when that extra development cost exactly cancels the maintenance saving. At x=5000 both totals are Rs 1000000.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q17 (printed CS Q7)

**Question:** [Official archived paper page 3](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** Digital-signal-processing software is expected to contain 40000 lines of code. In basic COCOMO, the multiplicative effort factor is 2.8 and the exponent is 1.20. Estimate development effort in person-months.

(A) 234.25
(B) 932.50
(C) 287.80
(D) 122.40

## Solution

The basic effort formula is a(KLOC)^b. Here KLOC=40000/1000=40, so effort=2.8×40^1.20≈234.23 person-months, approximately the listed234.25, A.

COCOMO uses thousands of lines, not raw LOC, as its size input. Substituting 40000 directly would overestimate effort by a factor 1000^1.2. With the correct input, 40^1.2=40×40^0.2≈83.65, and multiplying by 2.8 gives about 234.2. Person-months measure total labor effort, not elapsed calendar months: assigning several people does not make this a schedule estimate without an additional scheduling model.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q19 (printed CS Q9)

**Question:** [Official archived paper page 3](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** Which action is NOT supported by pure HTML pages, without server-side or client-side scripting?

(A) Embed web objects from different sites in one page
(B) Automatically refresh a page after a specified interval
(C) Automatically redirect to another page upon download
(D) Display the client's current time as part of the page

## Solution

HTML can embed remote objects and use refresh metadata for timed refresh or redirection. It has no mechanism by itself to read and display the client’s current clock time. That normally requires scripting or another active component, so D.

A static timestamp written into HTML is not the client's current time. Remote image/object URLs satisfy A, and a refresh directive can reload a document or navigate to a specified URL, satisfying B and C in the intended browser model. Reading the local clock and inserting its live value requires computation beyond HTML markup, for example JavaScript Date and DOM updates. That distinction between document description and active computation selects D.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q20 (printed CS Q10)

**Question:** [Official archived paper page 3](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=3); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 1 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** Which item is NOT desired in a good Software Requirements Specification document?

(A) Functional requirements
(B) Non-functional requirements
(C) Goals of implementation
(D) Algorithms for software implementation

## Solution

An SRS specifies required behavior, quality constraints and goals. Particular algorithms for implementing those requirements belong to design/implementation, not the requirements specification itself. Thus D.

Functional requirements describe what services the system must provide. Non-functional requirements describe qualities or constraints, such as response time or reliability. Goals clarify the intended outcome. Choosing a sorting algorithm or a particular implementation procedure generally prescribes how to build the system, so it belongs in design rather than the requested requirements specification. This is the standard separation tested here, not a claim that a real contract can never impose an implementation constraint.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q41 (printed CS Q31)

**Question:** [Official archived paper page 8](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=8); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** D

**Derived answer:** D

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** For i=√(-1), evaluate the definite integral from 0 to π/2 of (cos x+i sin x)/(cos x-i sin x) dx.

(A) 0
(B) 2
(C) -i
(D) i

## Solution

Euler’s formula gives(cos x+i sin x)/(cos x−i sin x)=e^(2ix). Integrating from 0 toπ/2 gives[e^(2ix)/(2i)]_0^(π/2)=(−1−1)/(2i)=i, D.

The denominator e^(-ix) is never zero for real x, so the quotient simplification is valid throughout the interval. An alternative real-imaginary check is to integrate cos(2x)+i sin(2x). The cosine integral is [sin(2x)/2] from 0 to π/2, hence zero; the sine integral is [-cos(2x)/2] over the same limits, hence one. The result therefore has real part zero and imaginary part one, confirming the sign of i.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q50 (printed CS Q40)

**Question:** [Official archived paper page 11](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=11); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** A

**Derived answer:** A

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** Find the eigenvalues of the matrix with rows (1,2,3), (0,4,7), (0,0,3).

(A) 1,4,3
(B) 3,7,3
(C) 7,3,2
(D) 1,2,3

## Solution

For an upper triangular matrix, det(A−λI) is the product of diagonal entries minus λ. Here it is(1−λ)(4−λ)(3−λ), so the eigenvalues are1, 4, 3, A.

Subtracting λI preserves triangular form. Expanding the determinant along the first column gives (1-λ) times the determinant of the lower-right 2×2 triangular block, namely (4-λ)(3-λ). Eigenvalues make this characteristic determinant zero. Off-diagonal entries 2,3,7 can affect eigenvectors but not these diagonal roots. The trace check gives 1+4+3=8, equal to the sum of the diagonal entries, and the determinant check gives product 12.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=1) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.



**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

# GATE 2011 CS: Q57 (printed CS Q47)

**Question:** [Official archived paper page 13](https://web.archive.org/web/20220204093545id_/https://gate.iitkgp.ac.in/documents/gatepapers/2011/cs_2011.pdf#page=13); consult original wording, diagrams and choices.

**Type / marks:** MCQ, 2 mark(s).

**Official answer:** C

**Derived answer:** C

**Source access:** Archived official IIT Kharagpur paper and IIT Madras key, booklet A. Physical PDF page numbers are used; code A is the matching key column. Final-revision designation is unverified.

**Paraphrased problem context:** A quadratic-root function for ax²+bx+c=0 specifies four cases: a=0 (regardless of discriminant); otherwise discriminant positive, zero or negative. Only positive/zero cases yield valid real roots, ordered root1≥root2, and return 0; invalid cases store two zeros and return -1. Test rows list (a,b,c;root1,root2;return): T1=(0,0,7;0,0;-1), T2=(0,1,3;0,0;-1), T3=(1,2,1;-1,-1;0), T4=(4,-12,9;1.5,1.5;0), T5=(1,-2,-3;3,-1;0), T6=(1,1,4;0,0;-1). Which set is nonredundant and covers the input equivalence classes?

(A) T1,T2,T3,T6
(B) T1,T3,T4,T5
(C) T2,T4,T5,T6
(D) T2,T3,T4,T5

## Solution

The specification defines four input equivalence classes: a=0 regardless of discriminant, and, for a≠0, discriminant positive, zero or negative. T1 and T2 cover the first class. T3 and T4 both have zero discriminant. T5 has discriminant 16>0, and T6 has discriminant −15<0. A nonredundant representative set must choose one of {T1, T2}, one of {T3, T4}, and both T5 and T6. Among the supplied choices, only {T2, T4, T5, T6} does so, option C.

Compute discriminants b²-4ac only after recognizing the special a=0 class. T3 gives 4-4=0 and T4 gives 144-144=0, so they are redundant for this partition despite different numerical roots. T5 gives 4+12=16; T6 gives 1-16=-15. A repeats the a=0 class and omits positive discriminant. B and D repeat the zero-discriminant class and omit negative discriminant. C contains exactly one representative of each stated category.

**Verification:** Independent second derivation review passed; [official published key](https://web.archive.org/web/20110812091059id_/http://gate.iitm.ac.in:80/gate2011/pdffiles/keycs.pdf#page=2) compared. Complete question transcription is not certified.

**Discrepancy / qualification:** No answer-key disagreement identified; conventions are stated in the solution.

**Explanation depth:** Expanded and independently reviewed for teaching detail. Original question transcription remains separately uncertified.

