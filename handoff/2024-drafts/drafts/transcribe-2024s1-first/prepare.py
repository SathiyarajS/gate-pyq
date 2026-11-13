import json,re,pathlib,unicodedata
O=pathlib.Path(__file__).parent;R=O.parent/'gate-pyq';src=json.load(open(O/'source.json')); crops=json.load(open(R/'data/crops.json'))
t=(O/'extracted.txt').read_text(); t=re.sub(r'PAGE \d+\n.*?Organizing Institute: IISc Bengaluru\s*','',t,flags=re.S);t=re.sub(r'(General Aptitude \(GA\)|Q\.\d+ – Q\.\d+ Carry (ONE|TWO) mark[s]? Each)\s*','',t)
parts=re.split(r'Q\.(\d+)\s*\n',t);out={}
def norm(t):
 return re.sub(r'\s+',' ',t).strip()
for i in range(1,len(parts),2):
 n=int(parts[i]);q=f'CS-2024-S1-Q{n}';chunks=re.split(r'\(([A-D])\)\s*\n',parts[i+1]);opts={chunks[j]:norm(chunks[j+1]) for j in range(1,len(chunks),2)}
 out[q]={'stem':norm(chunks[0]),'options':opts,'figures':[],'status':'draft','checked_pages':sorted({x['page'] for x in crops[q]}),'notes':'Extracted text corrected against rendered canonical source pages by transcribe_2024_s1_first. Independent source/figure review and manual production-rendered comparison pending.','source_sha256':src['source_sha256']}
def edit(n,stem=None,opts=None):
 q=out[f'CS-2024-S1-Q{n}'];
 if stem is not None:q['stem']=stem
 if opts is not None:q['options']=dict(zip('ABCD',opts))
edit(2,r'If two distinct non-zero real variables $x$ and $y$ are such that $(x+y)$ is proportional to $(x-y)$ then the value of $\frac{x}{y}$',[r'depends on $xy$',r'depends only on $x$ and not on $y$',r'depends only on $y$ and not on $x$','is a constant'])
edit(4,opts=['21%',r'$14\frac{2}{7}\%$','10%','30%'])
edit(5,r'For positive non-zero real variables $p$ and $q$, if\n$$\log(p^2+q^2)=\log p+\log q+2\log 3\ ,$$\nthen, the value of $\frac{p^4+q^4}{p^2q^2}$ is'.replace(r'\n','\n'))
edit(6,'In the given text, the blanks are numbered (i)−(iv). Select the best match for all the blanks.\n\nSteve was advised to keep his head ___(i)___ before heading ___(ii)___ to bat;\nfor, while he had a head ___(iii)___ batting, he could only do so with a cool head\n___(iv)___ his shoulders.')
edit(7,opts=[r'$1/\pi$',r'$2/\pi$',r'$3/\pi$',r'$4/\pi$'])
edit(8,'The pie chart presents the percentage contribution of different macronutrients to a typical 2,000 kcal diet of a person.\n\nThe typical energy density (kcal/g) of these macronutrients is given in the table.\n\n| Macronutrient | Energy density (kcal/g) |\n|---|---|\n| Carbohydrates | 4 |\n| Proteins | 4 |\n| Unsaturated fat | 9 |\n| Saturated fat | 9 |\n| Trans fat | 9 |\n\nThe total fat (all three types), in grams, this person consumes is', ['44.4','77.8','100','3,600'])
edit(11,r'Let $f:\mathbb{R}\to\mathbb{R}$ be a function such that $f(x)=\max\{x,x^3\},\ x\in\mathbb{R}$, where $\mathbb{R}$ is the set of all real numbers. The set of all points where $f(x)$ is NOT differentiable is',[r'$\{-1,1,2\}$',r'$\{-2,-1,1\}$',r'$\{0,1\}$',r'$\{-1,0,1\}$'])
edit(12,r'The product of all eigenvalues of the matrix $\begin{bmatrix}1&2&3\\4&5&6\\7&8&9\end{bmatrix}$ is')
edit(13,out['CS-2024-S1-Q13']['stem'].replace('𝐴',' $A$ ').replace('𝐵',' $B$ '),[r'$A+B$',r'$A-B$',r'$B-A$',r'$2*B$'])
edit(14,r'Consider a permutation sampled uniformly at random from the set of all permutations of $\{1,2,3,\cdots,n\}$ for some $n\geq4$. Let $X$ be the event that 1 occurs before 2 in the permutation, and $Y$ the event that 3 occurs before 4. Which one of the following statements is TRUE?', ['The events $X$ and $Y$ are mutually exclusive','The events $X$ and $Y$ are independent','Either event $X$ or $Y$ must occur','Event $X$ is more likely than event $Y$'])
edit(17,out['CS-2024-S1-Q17']['stem'].replace(' N,',' $N$,'),[r'both $O(N)$ and $\Omega(N)$',r'$O(N)$ but not $\Omega(N)$',r'$\Omega(N)$ but not $O(N)$',r'neither $O(N)$ nor $\Omega(N)$'])
edit(18,'Consider the following C program:\n\n```c\n#include <stdio.h>\nint main(){\n   int a = 6;\n   int b = 0;\n   while(a < 10) {\n      a = a / 12 + 1;\n      a += b;}\n   printf(”%d”, a);\n   return 0;}\n```\n[sic: typographic double quotation marks in source.]\n\nWhich one of the following statements is CORRECT?')
edit(19,"Consider the following C program:\n\n```c\n#include <stdio.h>\nvoid fX();\nint main(){\n   fX();\n   return 0;}\n\n  void fX(){\n   char a;\n   if((a=getchar()) != ’\\n’)\n       fX();\n   if(a != ’\\n’)\n       putchar(a);}\n```\n[sic: typographic single quotation marks in source.]\n\nAssume that the input to the program from the command line is 1234 followed by a newline character. Which one of the following statements is CORRECT?")
edit(23,r'Let $L_1,L_2$ be two regular languages and $L_3$ a language which is not regular. Which of the following statements is/are *always* TRUE?',[r'$L_1=L_2$ if and only if $L_1\cap\overline{L_2}=\phi$',r'$L_1\cup L_3$ is not regular',r'$\overline{L_3}$ is not regular',r'$\overline{L_1}\cup\overline{L_2}$ is regular'])
edit(27,r'Let $A$ and $B$ be two events in a probability space with $P(A)=0.3$, $P(B)=0.5$, and $P(A\cap B)=0.1$. Which of the following statements is/are TRUE?', ['The two events $A$ and $B$ are independent',r'$P(A\cup B)=0.7$',r'$P(A\cap B^c)=0.2$, where $B^c$ is the complement of the event $B$',r'$P(A^c\cap B^c)=0.4$, where $A^c$ and $B^c$ are the complements of the events $A$ and $B$, respectively'])
for n in [28,29]:
 for field in ['stem']:
  s=out[f'CS-2024-S1-Q{n}'][field]
  for a,b in [('𝑁𝑃',r'$N_P$'),('𝑁𝑄',r'$N_Q$'),('𝒀','$Y$'),('𝑿','$X$')]:s=s.replace(a,b)
  out[f'CS-2024-S1-Q{n}'][field]=s
 for k,s in out[f'CS-2024-S1-Q{n}']['options'].items():
  for a,b in [('𝑁𝑃',r'$N_P$'),('𝑁𝑄',r'$N_Q$'),('𝒀','$Y$'),('𝑿','$X$')]:s=s.replace(a,b)
  out[f'CS-2024-S1-Q{n}']['options'][k]=s
edit(32,r'Let $A$ and $B$ be non-empty finite sets such that there exist one-to-one and onto functions (i) from $A$ to $B$ and (ii) from $A\times A$ to $A\cup B$. The number of possible values of $|A|$ is __________')
edit(33,'Consider the operator precedence and associativity rules for the *integer* arithmetic operators given in the table below.\n\n| Operator | Precedence | Associativity |\n|---|---|---|\n| $+$ | Highest | Left |\n| $-$ | High | Right |\n| $*$ | Medium | Right |\n| $/$ | Low | Right |\n\nThe value of the expression $3+1+5*2/7+2-4-7-6/2$ as per the above rules is __________')
edit(35,'Consider the following two relations, **R(A,B)** and **S(A,C)**:\n\n**R**\n\n| A | B |\n|---|---|\n| 10 | 20 |\n| 20 | 30 |\n| 30 | 40 |\n| 30 | 50 |\n| 50 | 95 |\n\n**S**\n\n| A | C |\n|---|---|\n| 10 | 90 |\n| 30 | 45 |\n| 40 | 80 |\n\nThe total number of tuples obtained by evaluating the following expression\n$$\\sigma_{B<C}(R\\bowtie_{R.A=S.A}S)$$\nis _________')
for n in [8,10,20,28]:out[f'CS-2024-S1-Q{n}']['figures']=[f'figures/CS-2024-S1-Q{n}-1.svg']
json.dump(out,open(O/'CS-2024-S1-Q1-35.json','w'),indent=2,ensure_ascii=False)
