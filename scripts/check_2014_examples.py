#!/usr/bin/env python3
"""Selected independent checks, not whole-paper certification."""
from itertools import product,combinations
from fractions import Fraction
import struct
# S1CS42 nested-loop count.
for n in range(1,30):
 assert sum(1 for i in range(1,n+1) for j in range(i,n+1) for k in range(j+1,n+1))==(n-1)*n*(n+1)//6
# S1CS45 multiplexer expression.
for p,q,r in product([0,1],repeat=3):
 expected=[0,1,r,1-r][2*p+q]
 assert expected==bool((not p and q) or (q and not r) or (p and not q and r))
# S1CS51 grid edges.
vs=list(product(range(12),repeat=2))
assert sum(max(abs(a-c),abs(b-d))<=1 for (a,b),(c,d) in combinations(vs,2))==506
# S2CS45 exact binary32.
assert struct.pack('>f',-14.25).hex()=='c1640000'
# S2CS48 complement count.
assert sum(all(n%p for p in [2,3,5]) for n in range(1,101))==26
# S2CS52 graph MST enumeration. Labels left low/high/center/bottom/right-high/right, and right triangle.
edges=[(0,1,2),(1,2,1),(0,2,2),(0,3,1),(3,2,1),(1,4,2),(2,4,2),(4,5,1),(2,5,2),(3,6,2),(6,7,2),(7,8,1),(6,8,2)]
weights=[]
for es in combinations(edges,8):
 parent=list(range(9))
 def find(x):
  while parent[x]!=x:x=parent[x]
  return x
 for u,v,w in es:
  a,b=find(u),find(v)
  if a==b:break
  parent[a]=b
 else:weights.append(sum(e[2] for e in es))
assert weights.count(min(weights))==6
# S3CS45 JK next-state calculation.
state=(0,0,0);states=[]
for _ in range(3):
 q2,q1,q0=state
 state=(int((not q1 and not q2) or (not q0 and q2)),q2,int(q1 or q0));states.append(state)
assert states==[(1,0,0),(1,1,0),(1,1,1)]
# S3CS55 XOR cancellation.
for p,q in product([0,1],repeat=2):assert ((1^p)^(p^q)^((p^q)^(q^0)))==1^(p^q)
print('Selected 2014 loop, Boolean, grid, binary32, probability, MST and JK checks passed.')
