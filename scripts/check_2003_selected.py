from math import isqrt
from itertools import product
for m in range(1,100):
 F=m*(4*m*m-3*m+5)//6
 assert sum(isqrt(j) for j in range(1,m*m+1))==F
 assert 1+sum(isqrt(j) for j in range(max(0,m*m-1)))==F-2*m+2
plus=['bac','abc','acb'];mul=['abc','baa','ccb'];sol=[]
for x,y in product(range(3),repeat=2):
 t=lambda a,b:'abc'.index(mul[a][b]);s=lambda a,b:plus[a][b]
 if s(t(0,x),t(0,y))=='c' and s(t(1,x),t(2,y))=='c':sol.append(('abc'[x],'abc'[y]))
assert sol==[('c','b')]
# Formula D: universal modus ponens on a two-element domain.
for a,b in product(product((False,True),repeat=2),repeat=2):
 prem=all(not x or y for x,y in zip(a,b))
 assert not prem or not all(a) or all(b)
print('Recurrence variants checked m1–99; table solution(c,b); universal modus ponens passed.')
