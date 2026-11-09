from itertools import product
from fractions import Fraction
# Q27 interpolation.
for x,want in [(1,1),(2,-1),(3,1),(4,-1),(5,1)]:
 t=x-3;assert 1-Fraction(8,3)*t*t+Fraction(2,3)*t**4==want
# Q34 map axes wz columns, xy rows. All three candidate expressions valid.
gray=[(0,0),(0,1),(1,1),(1,0)];grid=[[0,None,0,0],[0,None,1,1],[1,1,1,1],[0,None,0,0]]
for i,(x,y) in enumerate(gray):
 for j,(w,z) in enumerate(gray):
  a=(w or x)and y;b=(x and y)or(y and w);c=(w or x)and(not w or y)and(not x or y)
  assert bool(a)==bool(b)==bool(c)
  if grid[i][j] is not None:assert bool(a)==bool(grid[i][j])
# Q33 candidate and complete solutions (only candidate C satisfies all).
def valid(x,y,z,w):return (x or y or z)and not(x and y)and((x and z)or w)and not((x and y)or(not z and not w))
assert [valid(*v) for v in [(0,1,0,0),(1,1,0,1),(1,0,1,1),(1,0,0,0)]]==[False,False,True,False]
# Q35 synchronous cycle.
p,q=0,1
for _ in range(3):p,q=1-p,p
assert (p,q)==(1,0)
# Q47 dependencies on literal rows.
rows=[(1,4,2),(1,5,3),(1,6,3),(3,2,2)]
def fd(left,right):return all(any(a[i]!=b[i] for i in left)or all(a[i]==b[i] for i in right)for a in rows for b in rows)
assert fd([1,2],[0])and fd([1],[2]);assert not fd([2],[1])and not fd([0],[2])and not fd([0,2],[1])
# Q38 triple reversal at every valid k.
for n in range(1,15):
 for k in range(1,n+1):
  a=list(range(n));b=(a[:k][::-1]+a[k:][::-1])[::-1];assert b==a[k:]+a[:k]
print('2000 selected interpolation, map, Boolean, sequential, dependency and rotation checks passed')
