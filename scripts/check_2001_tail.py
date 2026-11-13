import itertools,json
from collections import deque

def explore(order1,order2):
 programs=[]
 for order in [order1,order2]:
  a,b=order
  programs.append([('check',a),('set',a),('check',b),('set',b),('enter',0),('exit',0),('free',a),('free',b)])
 start=(0,0,0,0,0,0);todo=[start];seen={start};violate=False;dead=False
 while todo:
  st=todo.pop();p=list(st[:2]);flags=list(st[2:4]);inside=list(st[4:]);moves=0
  if all(inside):violate=True
  for k in (0,1):
   if p[k]==8:continue
   op,r=programs[k][p[k]]
   if op=='check' and flags[r]:continue
   moves+=1;q=p.copy();f=flags.copy();u=inside.copy();q[k]+=1
   if op=='set':f[r]=1
   if op=='free':f[r]=0
   if op=='enter':u[k]=1
   if op=='exit':u[k]=0
   ns=tuple(q+f+u)
   if ns not in seen:seen.add(ns);todo.append(ns)
  if moves==0 and p!=[8,8]:dead=True
 return dict(states=len(seen),overlap_reachable=violate,deadlock_reachable=dead)
print('GFG opposite',explore((0,1),(1,0)))
print('Swapped same',explore((0,1),(0,1)))
# Literal Forum release sequence is R2,R1, unlike acquire sequence R1,R1.
# State exploration above is only for the two GFG versions.
edges=[(1,2,2),(1,3,8),(1,6,3),(2,4,4),(2,5,12),(3,4,7),(4,5,9),(4,6,4)]
trees=[]
for es in itertools.combinations(edges,5):
 c={1};changed=True
 while changed:
  old=len(c)
  for a,b,w in es:
   if a in c or b in c:c.update([a,b])
  changed=len(c)!=old
 if len(c)==6:trees.append((sum(e[2] for e in es),es))
m=min(t[0] for t in trees)
print('MST weight,count',m,sum(t[0]==m for t in trees))
assert m==25 and sum(t[0]==m for t in trees)==2
assert explore((0,1),(1,0))['overlap_reachable']==False
assert explore((0,1),(0,1))['overlap_reachable']==True
