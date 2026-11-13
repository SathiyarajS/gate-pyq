from itertools import product
from fractions import Fraction
# Q12: visually read axes columns wx, rows yz, Gray order.
gray=[(0,0),(0,1),(1,1),(1,0)]
a=[[0,1,1,0],[None,0,0,1],[None,0,0,1],[0,1,1,None]]
for i,(y,z) in enumerate(gray):
 for j,(w,x) in enumerate(gray):
  if a[i][j] is not None: assert (x^z)==a[i][j]
# Q26 and Q27 truth tables; active-high enable forces zero when disabled.
for x,y,z in product(range(2),repeat=3):
 m=4*x+2*y+z
 f1=m in {0,1,3,5};f2=m in {6,7};f3=m in {1,4,5}
 assert (not((not(f1 and f2))and(not f3)))==f3
 data=[x,x,y,1-y];result=data[2*(1-y)+z] if not z else 0
 assert result==x*y*(1-z)
# Q28 composition, Q29 flags, Q48 fanout.
for x,y,z in product(range(2),repeat=3):
 f=lambda a,b:int(not a or b)
 assert f(f(x or y,y),z)==int((x and not y)or z)
assert 0x5d+0x6b==0xc8 and 0xd+0xb>15
assert 43*4+42*8<=512<44*4+43*8
assert Fraction(1,8)/(1-Fraction(1,2))==Fraction(1,4)
print('2002 selected independent arithmetic/truth-table checks passed')
