from itertools import product
from collections import deque
# Q11 K-map.
gray=[(0,0),(0,1),(1,1),(1,0)];grid=[[0,None,0,None],[None,1,None,1],[0,None,1,0],[0,1,None,0]]
for i,(y,z) in enumerate(gray):
 for j,(w,x) in enumerate(gray):
  if grid[i][j] is not None:assert bool((x and y)or(not y and z))==bool(grid[i][j])
# Q21 FIFO anomaly.
refs=[1,2,3,4,1,2,5,1,2,3,4,5]
def fifo(n):
 q=deque();fault=0
 for x in refs:
  if x not in q:
   fault+=1
   if len(q)==n:q.popleft()
   q.append(x)
 return fault
assert (fifo(3),fifo(4))==(9,10)
assert sum(x%2==0 and len(set(str(x)))==4 for x in range(1000,10000))==2296
assert 4096-539==int('DE5',16)
s=1;states=[]
for _ in range(7):
 states.append(s);q0=s&1;q1=(s>>1)&1;q2=(s>>2)&1
 s=4*q1+2*q0+(q1^q2)
assert states==[1,2,5,3,7,6,4] and s==1
for x,y in product(range(2),repeat=2):
 g=1-x;f=g*(1-y)+x*y
 assert f==int(x==y)
print('2001 K-map, FIFO, counting, two-complement, mux and state-cycle checks passed')
