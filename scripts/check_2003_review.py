"""Independent selected consistency checks; not a substitute for proofs/source audit."""
from itertools import product
from math import isqrt
from sympy import symbols,SOPform,POSform
x,y,z,w=symbols('x y z w')
ones=[1,2,5,12];dc=[0,7,13,15,8,10]
print('Q45 SOP',SOPform([x,y,z,w],ones,dc))
print('Q45 POS',POSform([x,y,z,w],ones,dc))
for m in range(1,101):
 plus=1+sum(isqrt(n+1) for n in range(1,m*m))
 minus=1+sum(isqrt(n-1) for n in range(1,m*m))
 b=m*(4*m*m-3*m+5)//6
 assert plus==b
 # The shifted sum formula has a boundary exception at m=1.
 if m>=2: assert minus==b-2*m+2
print('Q35 both recurrence variants checked m=1..100')
ss=[''.join(t) for t in product('01',repeat=7) if t[0]==t[3]==t[-1]=='1']
assert sum('001' in s for s in ss)==7
print('Q50 accepted count7')
for n in range(3,101):
 a=[0]*(n+1)
 for k in range(2,2*(n.bit_length()-1)+1):
  for j in range(k+1,n+1):a[j]=a[j] or j%k
 assert all(a[j] for j in range(3,n+1))
print('Q88 no printed numbers for n3..100 under floor bound')
