"""Selected independent finite checks; no official scoring assertion."""
from itertools import combinations
import sympy as s
for sign,det in [(-3,-70),(3,14)]:
 a=s.Matrix([[2,-1,sign],[3,2,5],[-1,4,1]])
 assert a.det()==det
profits=[15,20,30,18,18,10,23,16,25];deadlines=[7,2,5,3,4,5,2,7,3]
feasible=[]
for k in range(10):
 for sub in combinations(range(9),k):
  ds=sorted(deadlines[i] for i in sub)
  if all(j<=d for j,d in enumerate(ds,1)):feasible.append((sum(profits[i] for i in sub),sub))
assert max(x[0] for x in feasible)==147
assert {x[1] for x in feasible if x[0]==147}=={(0,1,2,4,6,7,8)}
assert int(s.Rational(239,1000)*256)==61
assert (77<<8)|61==0x4d3d
assert (74<<8)|((61<<3)&255)==0x4ae8
# Equal-rate, store-and-forward three-link packetization.
assert min(((24//p+2)*(p+3),p+3) for p in range(1,25) if 24%p==0)==(54,9)
print('2005 matrices, scheduling, encoding, packetization checks passed.')
