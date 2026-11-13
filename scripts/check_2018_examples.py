#!/usr/bin/env python3
"""Independent finite checks for selected 2018 examples, not full proof coverage."""
from itertools import combinations, permutations, product
# Printed CS46: enumerate every assignment to the complete seven-node heap.
assert sum(all(a[(i-1)//2]<a[i] for i in range(1,7)) for a in permutations(range(1,8)))==80
# CS48: all subsets, not a greedy assumption.
w=[10,7,4,2];v=[60,28,20,24]
assert max(sum(v[i] for i in range(4) if mask>>i&1) for mask in range(16) if sum(w[i] for i in range(4) if mask>>i&1)<=11)==60
# CS49: maximal valid Boolean cubes.
on={0,2,5,7,9,11};dc={3,8,10,12,14};cubes=[]
for pat in product('01-',repeat=4):
 cover={m for m in range(16) if all(a=='-' or a==b for a,b in zip(pat,f'{m:04b}'))}
 if cover&on and cover<=on|dc:cubes.append((''.join(pat),cover))
primes=[(a,b) for a,b in cubes if not any(b<d for _,d in cubes)]
essential={a for m in on for a,b in primes if m in b and sum(m in d for _,d in primes)==1}
assert essential=={'01-1','10--','-0-0'}
# CS47: all spanning trees for each relevant x ordering/equality.
def mst_count(x):
 edges=[(0,1,4),(1,2,4),(0,2,1),(0,3,3),(2,3,4),(0,4,x),(3,4,5)]
 weights=[]
 for es in combinations(edges,4):
  seen={0}
  while True:
   more=seen|{v for u,v,_ in es if u in seen}|{u for u,v,_ in es if v in seen}
   if more==seen:break
   seen=more
  if len(seen)==5:weights.append(sum(w for _,_,w in es))
 return weights.count(min(weights))
assert mst_count(5)==4 and all(mst_count(x)==2 for x in [-100,0,1,3,4,4.5,5.5,6,100])
print('Selected 2018 finite checks passed: heaps, knapsack, prime implicants, MST count.')
