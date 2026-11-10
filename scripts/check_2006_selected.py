from itertools import product
# Q36: group carry generation, independent of incoming carry.
for a,b in product(range(8), repeat=2):
 a2,a1,a0=[a>>i&1 for i in (2,1,0)];b2,b1,b0=[b>>i&1 for i in (2,1,0)]
 G=(a2 and b2) or ((a2 or b2) and a1 and b1) or ((a2 or b2) and (a1 or b1) and a0 and b0)
 assert bool(G)==(a+b>=8)
# Q38: independently verified proposed cover, not a claim about blurry option D.
ON={5,7,11,12,13,15}
cubes=[{i for i in range(16) if i&5==5},{i for i in range(16) if i&11==11},{i for i in range(16) if i&14==12}]
assert set.union(*cubes)==ON
pairs=[(i,j) for i in sorted(ON) for j in sorted(ON) if i<j and (i^j).bit_count()==1]
assert all(any(i in c and j in c for c in cubes) for i,j in pairs)
print('Q38 adjacent ON pairs:',pairs)
q=(0,0,0)
for b in '100110000':q=(q[1],q[0]^q[2],int(b))
assert q==(0,1,0)
sets={i:[] for i in range(4)}
for n in range(16):
 h=n^(n>>1);m=(n+1)%16;g=m^(m>>1)
 for i in range(4):
  if g>>i&1:sets[i].append(h)
assert sorted(sets[2])==[2,4,5,6,7,12,13,15]
print('Q40 output ON sets:',{i:sorted(s) for i,s in sets.items()})
for n in range(1,1000):
 i=n;j=0
 while i>0:i//=2;j+=i
 assert j==n-n.bit_count()
print('Q15, Q36, Q37, Q38, Q40 checks passed.')
