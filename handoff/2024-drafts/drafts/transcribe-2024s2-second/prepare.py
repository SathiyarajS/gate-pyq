import json,re,hashlib,unicodedata,pathlib
D=pathlib.Path(__file__).parent
raw=(D/'source.txt').read_text()
raw=re.sub(r'\n=== PAGE \d+ ===\nComputer Science and Information Technology Set 2 \(CS2\) \nPage \d+ of 40 \nOrganizing Institute: IISc, Bengaluru \n','\n',raw)
qs={int(n):t for n,t in re.findall(r'Q\.(\d+)\s*\n(.*?)(?=Q\.\d+\s*\n|\Z)',raw,re.S)}
sourcehash='b5012f2e7da399f4129e9ac5c1713493e3374ba9c9d30d600383dc535b3b5072'
existing=json.load(open(D/'existing.json'));out={}
for q in existing:
 n=int(q['source_question_number']); chunks=re.split(r'\(([ABCD])\)\s*\n',qs[n]);stem=' '.join(chunks[0].split());opts={chunks[i]:' '.join(chunks[i+1].split()) for i in range(1,len(chunks),2)}
 out[q['question_id']]={'stem':stem,'options':opts,'figures':[],'status':'draft','checked_pages':[q['source_page']],'notes':'Prepared from text extraction and visually checked against canonical source page. Independent source/figure review and manual production-rendered comparison remain pending. Existing solution checked for compatibility; see solution-review.json.','source_sha256':sourcehash}
def put(n,stem=None,options=None,fig=False):
 e=out[f'CS-2024-S2-Q{n}']
 if stem is not None:e['stem']=stem
 if options is not None:e['options']=dict(zip('ABCD',options))
 if fig:e['figures']=[f'figures/CS-2024-S2-Q{n}-1.svg']
put(36,'''What is the output of the following C program?

```c
#include <stdio.h>
int main() {
    double a[2]={20.0, 25.0}, *p, *q;
    p = a;
    q = p + 1;
    printf(”%d,%d”, (int)(q – p), (int)(*q – *p));
    return 0;}
```
[sic]''')
put(39,'''You are given a set $V$ of distinct integers. A binary search tree $T$ is created by inserting all elements of $V$ one by one, starting with an empty tree. The tree $T$ follows the convention that, at each node, all values stored in the left subtree of the node are smaller than the value stored at the node. You are not aware of the sequence in which these values were inserted into $T$, and you do not have access to $T$.

Which one of the following statements is TRUE?''',[f'{tr} of $T$ can be determined from $V$' for tr in ['Inorder traversal','Root node','Preorder traversal','Postorder traversal']])
put(40,r'''Consider the following context-free grammar where the start symbol is $S$ and the set of terminals is $\{a,b,c,d\}$.

$$S\to AaAb\mid BbBa$$
$$A\to cS\mid\epsilon$$
$$B\to dS\mid\epsilon$$

The following is a partially-filled LL(1) parsing table.

| | $a$ | $b$ | $c$ | $d$ | $\$$ |
| --- | --- | --- | --- | --- | --- |
| $S$ | $S\to AaAb$ | $S\to BbBa$ | (1) | (2) | |
| $A$ | $A\to\epsilon$ | (3) | $A\to cS$ | | |
| $B$ | (4) | $B\to\epsilon$ | | $B\to dS$ | |

Which one of the following options represents the CORRECT combination for the numbered cells in the parsing table?

*Note: In the options, “blank” denotes that the corresponding cell is empty.*''',[r'(1) $S\to AaAb$  (2) $S\to BbBa$  (3) $A\to\epsilon$  (4) $B\to\epsilon$',r'(1) $S\to BbBa$  (2) $S\to AaAb$  (3) $A\to\epsilon$  (4) $B\to\epsilon$',r'(1) $S\to AaAb$  (2) $S\to BbBa$  (3) blank  (4) blank',r'(1) $S\to BbBa$  (2) $S\to AaAb$  (3) blank  (4) blank'])
put(41,r'''Let $M$ be the 5-state NFA with $\epsilon$-transitions shown in the diagram below.

Which one of the following regular expressions represents the language accepted by $M$ ?''',[r'$(00)^*+1(11)^*$',r'$0^*+(1+0(00)^*)(11)^*$',r'$(00)^*+(1+(00)^*)(11)^*$',r'$0^++1(11)^*+0(11)^*$'],True)
put(42,'''Consider an array X that contains n positive integers. A subarray of X is defined to be a sequence of array locations with consecutive indices.

The C code snippet given below has been written to compute the length of the longest subarray of X that contains at most two distinct integers. The code has two missing expressions labelled $(P)$ and $(Q)$.

```c
int first=0, second=0, len1=0, len2=0, maxlen=0;
for (int i=0; i < n; i++) {
  if (X[i] == first) {
    len2++; len1++;
  } else if (X[i] == second) {
    len2++;
    len1 = ___(P)___;
    second = first;
  } else {
    len2 = ___(Q)___;
    len1 = 1; second = first;
  }
  if (len2 > maxlen) {
    maxlen = len2;
  }
  first = X[i];
}
```

Which one of the following options gives the CORRECT missing expressions?

(**Hint:** At the end of the i-th iteration, the value of `len1` is the length of the longest subarray ending with `X[i]` that contains all equal values, and `len2` is the length of the longest subarray ending with `X[i]` that contains at most two distinct values.)''',['$(P)$ `len1+1`  $(Q)$ `len2+1`','$(P)$ `1`  $(Q)$ `len1+1`','$(P)$ `1`  $(Q)$ `len2+1`','$(P)$ `len2+1`  $(Q)$ `len1+1`'])
put(43,r'''Consider the following expression: $x[i]=(p+r)*-s[i]+u/w$. The following sequence shows the list of triples representing the given expression, with entries missing for triples (1), (3), and (6).

| | | | |
| --- | --- | --- | --- |
| (0) | $+$ | $p$ | $r$ |
| (1) | | | |
| (2) | uminus | (1) | |
| (3) | | | |
| (4) | $/$ | $u$ | $w$ |
| (5) | $+$ | (3) | (4) |
| (6) | | | |
| (7) | $=$ | (6) | (5) |

Which one of the following options fills in the missing entries CORRECTLY?''',[r'(1) =[] $s$ $i$    (3) * (0) (2)    (6) []= $x$ $i$',r'(1) []= $s$ $i$    (3) − (0) (2)    (6) =[] $x$ (5)',r'(1) =[] $s$ $i$    (3) * (0) (2)    (6) []= $x$ (5)',r'(1) []= $s$ $i$    (3) − (0) (2)    (6) =[] $x$ $i$'])
put(44,r'''Let $x$ and $y$ be random variables, not necessarily independent, that take real values in the interval $[0,1]$. Let $z=xy$ and let the mean values of $x,y,z$ be $\bar{x},\bar{y},\bar{z}$, respectively. Which one of the following statements is TRUE?''',[r'$\bar{z}=\bar{x}\bar{y}$',r'$\bar{z}\le\bar{x}\bar{y}$',r'$\bar{z}\ge\bar{x}\bar{y}$',r'$\bar{z}\le\bar{x}$'])
put(45,r'''The relation schema, $\text{Person}(\underline{\text{pid}},\text{city})$, describes the city of residence for every person uniquely identified by `pid`. The following relational algebra operators are available: `selection`, `projection`, `cross product`, and `rename`.

To find the list of cities where at least 3 persons reside, using the above operators, the minimum number of `cross product` operations that must be used is''')
put(46,'''Consider a multi-threaded program with two threads `T1` and `T2`. The threads share two semaphores: `s1` (initialized to 1) and `s2` (initialized to 0). The threads also share a global variable `x` (initialized to 0). The threads execute the code shown below.

```c
// code of T1
wait(s1);
x = x+1;
print(x);
wait(s2);
signal(s1);
```

```c
// code of T2
wait(s1);
x = x+1;
print(x);
signal(s2);
signal(s1);
```

Which of the following outcomes is/are possible when threads `T1` and `T2` execute concurrently?''')
put(47,r'''Let $A$ be an $n\times n$ matrix over the set of all real numbers $\mathbb{R}$. Let $B$ be a matrix obtained from $A$ by swapping two rows. Which of the following statements is/are TRUE?''',['The determinant of $B$ is the negative of the determinant of $A$','If $A$ is invertible, then $B$ is also invertible','If $A$ is symmetric, then $B$ is also symmetric','If the trace of $A$ is zero, then the trace of $B$ is also zero'])
put(48,'''Let `S1` and `S2` be two stacks. `S1` has capacity of 4 elements. `S2` has capacity of 2 elements. `S1` already has 4 elements: 100, 200, 300, and 400, whereas `S2` is empty, as shown below.

Only the following three operations are available:

`PushToS2`: Pop the top element from `S1` and push it on `S2`.

`PushToS1`: Pop the top element from `S2` and push it on `S1`.

`GenerateOutput`: Pop the top element from `S1` and output it to the user.

Note that the pop operation is not allowed on an empty stack and the push operation is not allowed on a full stack.

Which of the following output sequences can be generated by using the above operations?''',fig=True)
put(50,r'''Consider 4-variable functions $f1$, $f2$, $f3$, $f4$ expressed in sum-of-minterms form as given below.

$$f1=\sum(0,2,3,5,7,8,11,13)$$
$$f2=\sum(1,3,5,7,11,13,15)$$
$$f3=\sum(0,1,4,11)$$
$$f4=\sum(0,2,6,13)$$

With respect to the circuit given above, which of the following options is/are CORRECT?''',[r'$Y=\sum(0,1,2,11,13)$',r'$Y=\prod(3,4,5,6,7,8,9,10,12,14,15)$',r'$Y=\sum(0,1,2,3,4,5,6,7)$',r'$Y=\prod(8,9,10,11,12,13,14,15)$'],True)
put(51,'''Let $G$ be an undirected connected graph in which every edge has a positive integer weight. Suppose that every spanning tree in $G$ has *even* weight. Which of the following statements is/are TRUE for every such graph $G$ ?''',['All edges in $G$ have even weight','All edges in $G$ have even weight **OR** all edges in $G$ have odd weight','In each cycle $C$ in $G$, all edges in $C$ have even weight','In each cycle $C$ in $G$, either all edges in $C$ have even weight **OR** all edges in $C$ have odd weight'])
put(52,r'''Consider a context-free grammar $G$ with the following 3 rules.

$$S\to aS,\ S\to aSbS,\ S\to c$$

Let $w\in L(G)$. Let $n_a(w),n_b(w),n_c(w)$ denote the number of times $a,b,c$ occur in $w$, respectively. Which of the following statements is/are TRUE?''',[r'$n_a(w)>n_b(w)$',r'$n_a(w)>n_c(w)-2$',r'$n_c(w)=n_b(w)+1$',r'$n_c(w)=n_b(w)*2$'])
put(55,'''Consider an Ethernet segment with a transmission speed of $10^8$ bits/sec and a maximum segment length of 500 meters. If the speed of propagation of the signal in the medium is $2\times10^8$ meters/sec, then the minimum frame size *(in bits)* required for collision detection is _________'''.replace('\t','\\t'))
put(56,r'''A functional dependency $F:X\to Y$ is termed as a *useful functional dependency* if and only if it satisfies all the following three conditions:

- $X$ is not the empty set.
- $Y$ is not the empty set.
- Intersection of $X$ and $Y$ is the empty set.

For a relation $R$ with 4 attributes, the total number of possible useful functional dependencies is ________''')
put(59,'The number of distinct minimum-weight spanning trees of the following graph is _________',fig=True)
put(60,'The chromatic number of a graph is the minimum number of colours used in a *proper colouring* of the graph. The chromatic number of the following graph is _________',fig=True)
put(61,r'''A processor uses a 32-bit instruction format and supports byte-addressable memory access. The ISA of the processor has 150 distinct instructions. The instructions are equally divided into two types, namely R-type and I-type, whose formats are shown below.

In the OPCODE, 1 bit is used to distinguish between I-type and R-type instructions and the remaining bits indicate the operation. The processor has 50 architectural registers, and all register fields in the instructions are of equal size.

Let $X$ be the number of bits used to encode the UNUSED field, $Y$ be the number of bits used to encode the OPCODE field, and $Z$ be the number of bits used to encode the immediate value/address field. The value of $X+2Y+Z$ is ________''',fig=True)
put(62,r'''Let $L_1$ be the language represented by the regular expression $b^*ab^*(ab^*ab^*)^*$ and $L_2=\{w\in(a+b)^*\mid |w|\le4\}$, where $|w|$ denotes the length of string $w$. The number of strings in $L_2$ which are also in $L_1$ is ___________''')
put(63,r'''Let $Z_n$ be the group of integers $\{0,1,2,\ldots,n-1\}$ with addition modulo $n$ as the group operation. The number of elements in the group $Z_2\times Z_3\times Z_4$ that are their own inverses is ________''')
put(64,r'''Consider a 32-bit system with 4 KB page size and page table entries of size 4 bytes each. Assume 1 KB = $2^{10}$ bytes. The OS uses a 2-level page table for memory management, with the page table containing an outer page directory and an inner page table. The OS allocates a page for the outer page directory upon process creation. The OS uses demand paging when allocating memory for the inner page table, i.e., a page of the inner page table is allocated only if it contains at least one valid page table entry.

An active process in this system accesses 2000 unique pages during its execution, and none of the pages are swapped out to disk. After it completes the page accesses, let $X$ denote the minimum and $Y$ denote the maximum number of pages across the two levels of the page table of the process.

The value of $X+Y$ is ________''')
put(65,r'''Consider the following augmented grammar, which is to be parsed with a SLR parser. The set of terminals is $\{a,b,c,d,\#,@\}$

$$S'\to S$$
$$S\to SS\mid Aa\mid bAc\mid Bc\mid bBa$$
$$A\to d\#$$
$$B\to @$$

Let $I_0=CLOSURE(\{S'\to\bullet S\})$. The number of items in the set $GOTO(I_0,S)$ is ___________''')
out['CS-2024-S2-Q36']['notes']+=' Source visibly uses typographic quotation marks and en dashes in C code. [sic] is outside the code block to preserve code lines; proposed question-error row records this. Intended answer B assumes ASCII C punctuation.'
out['CS-2024-S2-Q42']['notes']+=' Printed underlined blanks around (P)/(Q) are encoded as underscores in the code block; code indentation is two spaces per level.'
(D/'CS-2024-S2-Q36-Q65.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
