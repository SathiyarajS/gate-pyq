from itertools import product
sets=[set() for _ in range(4)]
for w,x,y,z in product([0,1],repeat=4):
 P=(not x and not y and not z) or (not w and x and not y) or (w and not y and z) or (x and z)
 Q=(not w and not y and z) or (w and not x and not y) or (x and z)
 R=(not w and not y and not z) or (w and not x and not y) or (x and y and z) or (x and not y and z)
 S=(not x and not y and not z) or (w and not x and not y) or (not w and y)
 for a,b in zip(sets,[P,Q,R,S]):
  if b:a.add(8*w+4*x+2*y+z)
print('Q32 P,Q,R,S minterms:',sets)
# Validate the claimed regular intersection for B=ww^R x, nonempty w,x.
for k in range(1,20,2):
 for j in range(1,20,2):
  a='0'+'1'*k+'00'+'1'*j+'01'
  accepted=any(a[:i]==a[i:2*i][::-1] for i in range(1,(len(a)-1)//2+1))
  assert accepted==(k==j)
print('Q31 intersection witness family checked for odd block sizes1..19')
