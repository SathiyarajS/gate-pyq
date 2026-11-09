from collections import defaultdict
from itertools import product
import re
# Independent symbolic check of the six-operation polynomial counterexample.
import sympy as s
x=s.symbols('x'); t=x*x;t=t+2;t=t*t;t=t+2;t=t*x;t=t+5
assert s.expand(t)==x**5+4*x**3+6*x+5
# Literal undirected graph from source p56, two 3x3 grids, connector and two leaves.
g=defaultdict(set)
def edge(a,b):g[a].add(b);g[b].add(a)
for side in ('L','R'):
 for i,j in product(range(3),repeat=2):
  if i<2:edge((side,i,j),(side,i+1,j))
  if j<2:edge((side,i,j),(side,i,j+1))
edge(('L',2,2),'C');edge('C',('R',2,0));edge('C','top');edge(('R',1,2),'right')
best=[]
def visit(v,path,seen):
 global best
 if len(path)>len(best):best=path[:]
 for w in g[v]-seen:visit(w,path+[w],seen|{w})
for v in g:visit(v,[v],{v})
assert len(best)==19
print('Longest simple path / attainable DFS stack depth:',len(best),best)
for n in range(4):
 absent=[''.join(w) for w in product('ab',repeat=n) if not re.fullmatch('a*b*(ba)*a*',''.join(w))]
 print('Regex missing strings at length',n,absent)
 if n<3:assert not absent
 else:assert 'bab' in absent
print('Six-operation expansion verified:',s.expand(t))
