from itertools import product
# Cache, exact LRU list per set, oldest first.
c=[[] for _ in range(4)]
for x in [0,255,1,4,3,8,133,159,216,129,63,8,48,32,73,92,155]:
 s=c[x%4]
 if x in s:s.remove(x)
 elif len(s)==4:s.pop(0)
 s.append(x)
print('Q29 final LRU sets',c)
# All permissible left/right splits of a three-key overflowing leaf.
states=[((),0,[])]
for x in [10,3,6,8,4,2,1]:
 new=[]
 for leaves,k,history in states:
  leaves=list(leaves) or [()]
  i=max([i for i,l in enumerate(leaves) if l and l[0]<=x],default=0)
  a=tuple(sorted(leaves[i]+(x,)))
  if len(a)<=2:new.append((tuple(leaves[:i]+[a]+leaves[i+1:]),k,history+[(x,None)]))
  else:
   for cut in [1,2]:new.append((tuple(leaves[:i]+[a[:cut],a[cut:]]+leaves[i+1:]),k+1,history+[(x,cut)]))
 states=new
print('Q44 max',max(x[1] for x in states),'witness',max(states,key=lambda x:x[1]))
# Structural exhaustive NOR circuits with at most two gates.
A,B,C=[sum(((i>>k)&1)<<i for i in range(8)) for k in [2,1,0]];mask=255;target=(A&B)|C
found=False
for x,y in product([A,B,C],repeat=2):
 z=mask^(x|y)
 for u,v in product([A,B,C,z],repeat=2):
  if mask^(u|v)==target:found=True
print('Q6 any <=2 NOR implementation?',found)
