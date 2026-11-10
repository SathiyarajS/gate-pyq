"""Selected finite checks supplement, not replace, the written proofs."""
from collections import deque
from itertools import permutations

def queue_steps(vals):
 q=deque(vals);s=[];steps=0
 while q:
  if not s or s[-1]<=q[0]:s.append(q.popleft())
  else:q.append(s.pop())
  steps+=1
 return steps
for n in range(1,8):
 assert max(queue_steps(p) for p in permutations(range(n)))==n*n
assert queue_steps(range(16,0,-1))==256
seq=list(range(20))*2

def faults(opt):
 resident=[];total=0
 for i,v in enumerate(seq):
  if v in resident:continue
  total+=1
  if len(resident)==10:
   if opt:
    future=seq[i+1:]
    victim=max(resident,key=lambda x:future.index(x) if x in future else float('inf'))
    resident.remove(victim)
   else:resident.pop()
  resident.append(v)
 return total
assert faults(False)==31 and faults(True)==30
assert (191-63)+(191-10)+(47-10)==346
assert (20+7+1+5)/4==8.25
assert (1-.6)+10*.6>6 and (1-.4)+10*.4<6
print('2016 queue exhaustive n<=7, LIFO/OPT, disk, scheduler and cache checks passed.')
