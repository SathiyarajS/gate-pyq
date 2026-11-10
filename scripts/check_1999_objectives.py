from itertools import product,permutations
from math import comb
for n in range(7):
 for k in range(7):
  count=sum(x.count(0)==n and x.count(1)==k and all(not(x[i]==x[i+1]==1) for i in range(len(x)-1)) for x in product((0,1),repeat=n+k))
  assert count==(comb(n+1,k) if k<=n+1 else 0)
maprows=[[0,0,1,0],[None,None,1,None],[0,1,1,0],[0,1,1,0]]
gray=[(0,0),(0,1),(1,1),(1,0)]
for i,(a,b) in enumerate(gray):
 for j,(c,d) in enumerate(gray):
  if maprows[i][j] is not None:assert int(d and(c or a))==maprows[i][j]
bits=[(199>>i)&1 for i in range(8)]
d=[(bits[i-1] if i else 0)-bits[i] for i in range(8)]
assert sum(x*2**i for i,x in enumerate(d))==-57
assert d[::-1]==[0,-1,0,0,1,0,0,-1]
assert [(a,b,c) for a,b,c in product((0,1),repeat=3) if int(c and not(b and not(a and 1)))==1]==[(0,0,1),(1,0,1),(1,1,1)]
def trial(a,b,c):
 seen=set()
 while (a,b,c) not in seen:
  seen.add((a,b,c))
  if a>=b and c<b:return b
  if a>=b:b,c=c,b
  else:a,b=b,a
 return None
for t in permutations((1,2,3)):assert trial(*t)==2
assert trial(2,1,1) is None
print('Binary gap counts, K-map, Booth digits, feedback states and Trial cases passed.')
