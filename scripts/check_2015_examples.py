#!/usr/bin/env python3
"""Independent small-case checks for selected 2015 derivations; not full-paper certification."""
from fractions import Fraction
from itertools import product, combinations
import struct
# Session1 Q9: official product contradicts the marginal-sum constraint.
mean=Fraction(1,4)+2*Fraction(2,5)+3*Fraction(1,10)
assert mean==Fraction(27,20) and (mean/3)**3 < Fraction(1,10)
# Session2 Q24.
f=[0,1]
for n in range(2,6):f.append(1+sum(f[k]*f[n-k] for k in range(1,n)))
assert f[5]==51
# Session2 Q55 outer-complement circuit.
on=[]
for a,b,c,d in product([0,1],repeat=4):
 inner=(not d) or (a and not b) or (not a and c) or (a and not c and d) or (not a and not c and d)
 if not inner:on.append((a,b,c,d))
assert on==[(1,1,1,1)]
# Session2 Q58 onto functions.
assert sum(len(set(v))==3 for v in product(range(3),repeat=4))==36
# Session3 Q62 maximal cubes.
ones={0,2,4,5,6,10}
cubes={}
for c in product('01-',repeat=4):
 cover={v for v in range(16) if all(x=='-' or int(x)==(v>>(3-i)&1) for i,x in enumerate(c))}
 if cover<=ones:cubes[''.join(c)]=cover
primes={c for c,v in cubes.items() if not any(v<w for w in cubes.values())}
assert primes=={'0--0','010-','-010'}
# Session3 Q53 switch fall-through count.
j=int(2*3//4+2.0/5+8//5);j-=1;k=-j
counts={1:3,2:3,3:2}
assert sum(counts.get(i+k,1) for i in range(5))==10
# Session3 Q63 repeated squaring.
z=1
for b in [1,0,1,1]:
 z=z*z%8
 if b:z=z*2%8
assert z==0
print('Selected 2015 checks passed: probability contradiction, recursion, Boolean minterm, surjections, prime cubes, switch count, modular exponentiation.')
# Session3 Q30: no valid max-heap within two arbitrary swaps.
a=(89,19,50,17,12,15,2,5,7,11,6,9,100)
def heap(a):return all(a[(i-1)//2]>=a[i] for i in range(1,len(a)))
def swapped(a):
 for i,j in combinations(range(len(a)),2):
  b=list(a);b[i],b[j]=b[j],b[i];yield tuple(b)
level={a};seen=set(level)
for depth in range(3):
 assert not any(map(heap,level))
 if depth<2:
  level={b for v in level for b in swapped(v)}-seen;seen|=level
b=list(a)
for i,j in [(12,5),(5,2),(2,0)]:b[i],b[j]=b[j],b[i]
assert heap(b)
print('2015 CS3 heap minimum3 also exhaustively verified through two arbitrary swaps.')
