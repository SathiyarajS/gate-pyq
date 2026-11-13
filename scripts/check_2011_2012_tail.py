#!/usr/bin/env python3
"""Selected finite checks; these do not certify all solutions or source completeness."""
from itertools import combinations
# 2011 CS50–51, from visually inspected wiring.
def step(s):
 p,q,r=s
 return r, int(not(p or r)), q*(1-r)
assert step((0,1,0))==(0,1,1)
s=(0,0,0); seen=[]
while s not in seen:
 seen.append(s);s=step(s)
assert seen==[(0,0,0),(0,1,0),(0,1,1),(1,0,0)]
# 2011 CS54: Kruskal independently checks the proposed tree weight.
for n in range(3,51):
 edges=sorted((i+j,i,j) for i in range(1,n+1) for j in range(i+1,min(i+2,n)+1))
 parent=list(range(n+1))
 def find(i):
  while parent[i]!=i:i=parent[i]
  return i
 weight=0; chosen=[]
 for w,i,j in edges:
  a,b=find(i),find(j)
  if a!=b:parent[a]=b;weight+=w;chosen.append((i,j))
 assert weight==n*n-n+1
 assert set(chosen)=={(1,2)}|{(i-2,i) for i in range(3,n+1)}
# 2012 CS42 replacement policies.
refs=[1,2,3,2,4,1,3,2,4,1]
for policy,expected in [('FIFO',6),('LRU',9),('OPT',5)]:
 cache=[];last={};faults=0
 for i,x in enumerate(refs):
  if x not in cache:
   faults+=1
   if len(cache)==3:
    if policy=='FIFO':cache.pop(0)
    elif policy=='LRU':cache.remove(min(cache,key=lambda y:last[y]))
    else:cache.remove(max(cache,key=lambda y:refs.index(y,i+1) if y in refs[i+1:] else 100))
   cache.append(x)
  last[x]=i
 assert faults==expected
assert (8+16+16**2)*128==35*1024
assert (256*1024//32)*(16+4)==160*1024
print('Selected 2011 counter/MST and 2012 replacement/size checks passed.')
