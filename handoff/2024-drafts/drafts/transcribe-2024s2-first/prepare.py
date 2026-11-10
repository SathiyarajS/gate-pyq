import json,re,pathlib
O=pathlib.Path(__file__).parent
records=json.load(open(O/'records.json')); D={}
for rec in records:
 n=int(rec['source_question_number']); txt=(O/f"source-pages/{rec['source_page']:02}.txt").read_text();text=re.split(r'Q\.'+str(n)+r'\s*\n',txt)[1];text=re.split(r'\nQ\.\d+\s*\n',text)[0]
 parts=re.split(r'\n\(([ABCD])\)\s*\n',text); clean=lambda s:' '.join(s.split()).replace('depth- first','depth-first')
 opts={parts[i]:clean(parts[i+1]) for i in range(1,len(parts),2)}
 D[rec['question_id']]={'stem':clean(parts[0]),'options':opts,'figures':[],'status':'draft','checked_pages':[rec['source_page']],'notes':'Preparer visually compared source page wording and options after text extraction and checked existing solution. Pending independent source/figure review and manual user production comparison.','source_sha256':'b5012f2e7da399f4129e9ac5c1713493e3374ba9c9d30d600383dc535b3b5072'}
def put(n,s=None,opts=None):
 d=D[f'CS-2024-S2-Q{n}']
 if s is not None:d['stem']=s
 if opts is not None:d['options']=dict(zip('ABCD',opts))
put(1,"If ‘→’ denotes increasing order of intensity, then the meaning of the words\n[walk → jog → sprint] is analogous to [bothered → ________ → daunted].\n\nWhich one of the given options is appropriate to fill the blank?")
D['CS-2024-S2-Q2']['stem']=D['CS-2024-S2-Q2']['stem'].replace('possible combination','possible combination [sic]')
put(3,D['CS-2024-S2-Q3']['stem'].replace('1/4th',r'$1/4^{\text{th}}$'))
put(4,r'For positive non-zero real variables $x$ and $y$, if'+ '\n\n'+r'$$\ln\left(\frac{x+y}{2}\right)=\frac{1}{2}[\ln(x)+\ln(y)]$$'+'\n\n'+r'then, the value of $\frac{x}{y}+\frac{y}{x}$ is')
put(5,r'In the sequence $6, 9, 14, x, 30, 41$, a possible value of $x$ is')
put(6,'Sequence the following sentences in a coherent passage.\n\nP: This fortuitous geological event generated a colossal amount of energy and heat that resulted in the rocks rising to an average height of 4 km across the contact zone.\n\nQ: Thus, the geophysicists tend to think of the Himalayas as an active geological event rather than as a static geological feature.\n\nR: The natural process of the cooling of this massive edifice absorbed large quantities of atmospheric carbon dioxide, altering the earth’s atmosphere and making it better suited for life.\n\nS: Many millennia ago, a breakaway chunk of bedrock from the Antarctic Plate collided with the massive Eurasian Plate.')
put(8,opts=['25%','50%','77.5%','62.5%'])
put(10,D['CS-2024-S2-Q10']['stem'].replace('4 × 4',r'$4\times4$'))
put(12,'Let $p$ and $q$ be the following propositions:\n\n$p$: Fail grade can be given.\n\n$q$: Student scores more than 50% marks.\n\nConsider the statement: “Fail grade cannot be given when student scores more than 50% marks.”\n\nWhich one of the following is the CORRECT representation of the above statement in propositional logic?',[r'$q\to\neg p$',r'$q\to p$',r'$p\to q$',r'$\neg p\to q$'])
put(13,'Consider the following C program. Assume parameters to a function are evaluated from *right to left*.\n\n```c\n#include <stdio.h>\n\nint g(int p) { printf("%d", p); return p; }\nint h(int q) { printf("%d", q); return q; }\n\nvoid f(int x, int y) {\n  g(x);\n  h(y);\n}\n\nint main() {\n  f(g(10),h(20));\n}\n```\n\nWhich one of the following options is the CORRECT output of the above C program?')
def table(head,row):return '\n\n| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n| '+' | '.join(row)+' |'
put(14,'The format of a single-precision floating-point number as per the **IEEE 754** standard is:'+table(['Sign','Exponent','Mantissa'],['(1bit)','(8 bits)','(23 bits)'])+'\n\nChoose the largest floating-point number among the following options.',[table(['Sign','Exponent','Mantissa'],['0',e,m]).strip() for e,m in [('0111 1111','1111 1111 1111 1111 1111 111'),('1111 1110','1111 1111 1111 1111 1111 111'),('1111 1111','1111 1111 1111 1111 1111 111'),('0111 1111','0000 0000 0000 0000 0000 000')]])
put(15,'Let $T(n)$ be the recurrence relation defined as follows:\n\n$T(0)=1$,\n\n$T(1)=2$, and\n\n$T(n)=5T(n-1)-6T(n-2)$    for $n\\ge2$\n\nWhich one of the following statements is TRUE?',[r'$T(n)=\Theta(2^n)$',r'$T(n)=\Theta(n2^n)$',r'$T(n)=\Theta(3^n)$',r'$T(n)=\Theta(n3^n)$'])
put(16,r'Let $f(x)$ be a continuous function from $\mathbb{R}$ to $\mathbb{R}$ such that'+'\n\n$$f(x)=1-f(2-x)$$\n\n'+r'Which one of the following options is the CORRECT value of $\int_0^2 f(x)dx$ ?', ['0','1','2',r'$-1$'])
put(17,r'Let $A$ be the adjacency matrix of a simple undirected graph $G$. Suppose $A$ is its own inverse. Which one of the following statements is *always* TRUE?', ['$G$ is a cycle','$G$ is a perfect matching','$G$ is a complete graph','There is no such graph $G$'])
put(18,opts=[rf'$\frac{{{v}}}{{324}}$' for v in [1,5,7,11]])
put(21,'Consider the following two sets:\n\n| Set X | Set Y |\n| --- | --- |\n| P. Lexical Analyzer | 1. Abstract Syntax Tree |\n| Q. Syntax Analyzer | 2. Token |\n| R. Intermediate Code Generator | 3. Parse Tree |\n| S. Code Optimizer | 4. Constant Folding |\n\nWhich one of the following options is the CORRECT match from **Set X** to **Set Y** ?')
put(22,'Which one of the following regular expressions is equivalent to the language accepted by the DFA given below?', [r'$0^*1(0+10^*1)^*$',r'$0^*(10^*11)^*0^*$',r'$0^*1(010^*1)^*0^*$',r'$0(1+0^*10^*1)^*0^*$'])
D['CS-2024-S2-Q29']['options']['B']=D['CS-2024-S2-Q29']['options']['B'].replace('a L-attributed','a [sic] L-attributed')
put(30,'For a Boolean variable $x$, which of the following statements is/are FALSE?', [r'$x.1=x$',r'$x+1=x$',r'$x.x=0$',r'$x+\bar{x}=1$'])
put(31,'An instruction format has the following structure:\n\nInstruction Number: *Opcode destination reg, source reg-1, source reg-2*\n\nConsider the following sequence of instructions to be executed in a pipelined processor:\n\n```text\nI1: DIV R3, R1, R2\nI2: SUB R5, R3, R4\nI3: ADD R3, R5, R6\nI4: MUL R7, R3, R8\n```\n\nWhich of the following statements is/are TRUE?')
put(33,'Consider the following C function definition.\n\n```c\nint fX(char *a){\n\n    char *b = a;\n\n    while(*b)\n\n        b++;\n\n    return b - a;}\n```\n\nWhich of the following statements is/are TRUE?', ['The function call `fX(”abcd”)` [sic] will always return a value','Assuming a character array `c` is declared as `char c[] = ”abcd”` [sic] in `main()`, the function call `fX(c)`will always return a value','The code of the function will not compile','Assuming a character pointer `c` is declared as `char *c = ”abcd”` [sic] in `main()`, the function call `fX(c)`will always return a value'])
put(34,r'Let $P$ be the partial order defined on the set $\{1,2,3,4\}$ as follows'+'\n\n'+r'$$P=\{(x,x)\mid x\in\{1,2,3,4\}\}\cup\{(1,2),(3,2),(3,4)\}$$'+'\n\n'+r'The number of total orders on $\{1,2,3,4\}$ that contain $P$ is __________')
put(35,r'Let $A$ be an array containing integer values. The distance of $A$ is defined as the minimum number of elements in $A$ that must be replaced with another integer so that the resulting array is sorted in non-decreasing order. The distance of the array $[2, 5, 3, 1, 4, 2, 6]$ is ___________')
for n in [8,10,22]:D[f'CS-2024-S2-Q{n}']['figures']=[f'figures/CS-2024-S2-Q{n}-1.svg']
D['CS-2024-S2-Q8']['figures'].append('figures/CS-2024-S2-Q8-2.svg')
json.dump(D,open(O/'CS-2024-S2-Q1-35.json','w'),ensure_ascii=False,indent=2)
