"""Independent bounded checks; general proofs are in the solutions."""
from itertools import combinations
best_any=best_adj=seen=0
for zeros in combinations(range(12),4):
 z=set(zeros)
 for ones in combinations([i for i in range(12) if i not in z],5):
  a=[2]*12
  for i in z:a[i]=0
  for i in ones:a[i]=1
  m=[[0]*3 for _ in range(3)]
  for i,v in enumerate(a):m[0 if i<4 else 1 if i<9 else 2][v]+=1
  d=0
  for i,j in [(0,1),(0,2),(1,2)]:
   t=min(m[i][j],m[j][i]);d+=t;m[i][j]-=t;m[j][i]-=t
  remain=sum(m[i][j] for i in range(3) for j in range(3) if i!=j)
  assert remain%3==0
  best_any=max(best_any,d+2*(remain//3))
  best_adj=max(best_adj,sum(a[i]>a[j] for i in range(12) for j in range(i+1,12)));seen+=1
assert (seen,best_any,best_adj)==(27720,7,47)
a=[1,1,1,1,0,0,2,2,2,0,0,1]
for i,j in [(1,5),(2,6),(7,12),(3,10),(8,10),(4,11),(9,11)]:a[i-1],a[j-1]=a[j-1],a[i-1]
assert a==[0]*4+[1]*5+[2]*3
s=[]
for t in '5 2 * 3 4 + 5 2 * * +'.split():
 if t.isdigit():s.append(int(t))
 else:
  y=s.pop();x=s.pop();s.append(x+y if t=='+' else x*y)
assert s==[80]
assert (4-(2-4))*2==12
print('PASS:27720 arrays, swap maxima7/47, constructive7 swaps, postfix80, grammar arithmetic12')
