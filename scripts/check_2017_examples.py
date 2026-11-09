"""Recompute selected2017 examples independently of stored answer strings."""
from itertools import product,combinations
# CS2 logical options A and B coincide on every valuation.
for p,q,r in product([False,True],repeat=3):
 a=(not p and r) and (r or (p and q))
 b=(not p and r) and (not(p and q) or not r)
 assert a==b==(not p and r)
# CS2 conflict-serializable transaction interleavings.
count=0
for t1pos in combinations(range(8),4):
 seq=[1 if i in t1pos else 2 for i in range(8)]
 one=[i for i,t in enumerate(seq) if t==1];two=[i for i,t in enumerate(seq) if t==2]
 count+=(one[3]<two[0] or two[1]<one[2])
assert count==54
# CS1 two-way LRU conflicts, separate compulsory misses.
sets={};seen=set();comp=conf=0
seq=[0,128,256,128,0,128,256,128,1,129,257,129,1,129,257,129]*10
for block in seq:
 s=sets.setdefault(block%128,[])
 if block not in s:
  if block not in seen:comp+=1
  else:conf+=1
  if len(s)==2:s.pop(0)
 else:s.remove(block)
 s.append(block);seen.add(block)
assert (comp,conf)==(6,76)
assert sum(any(i%d==0 for d in [3,5,7]) for i in range(1,501))==271
assert (35*11)%192==1
print('2017 logic equivalence, interleavings, LRU, inclusion-exclusion and modular inverse checks passed.')
