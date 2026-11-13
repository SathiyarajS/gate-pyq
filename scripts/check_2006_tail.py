"""Independent checks for selected 2006 conditional derivations, not official scoring."""
r=[2,4,8];t=0;ends={}
while any(r):
 i=max(range(3),key=lambda i:(r[i],-i));r[i]-=1;t+=1
 if not r[i]:ends[i]=t
assert ends=={0:12,1:13,2:14}
fds=[('AB','CD'),('AF','D'),('DE','F'),('C','G'),('F','E'),('G','A')]
for a,answer in [('CF','ACDEFG'),('BG','ABCDG'),('AF','ADEF'),('AB','ABCDG')]:
 s=set(a)
 while True:
  old=s.copy()
  for x,y in fds:
   if set(x)<=s:s|=set(y)
  if old==s:break
 assert ''.join(sorted(s))==answer
for n in range(6,9):
 adj={x:{y for y in range(2**n) if x!=y and (x&y).bit_count()==2} for x in range(2**n)}
 assert sum(not v for v in adj.values())==n+1
 assert max(map(len,adj.values()))==3*2**(n-3)
 unseen=set(adj);cc=0
 while unseen:
  todo=[unseen.pop()];cc+=1
  while todo:
   for v in adj[todo.pop()]&unseen:unseen.remove(v);todo.append(v)
 assert cc==n+2
heap=[9,5,6,8,3,1]
for x in [7,2,10,4]:
 heap.append(x);i=len(heap)-1
 while i and heap[(i-1)//3]<heap[i]:
  j=(i-1)//3;heap[j],heap[i]=heap[i],heap[j];i=j
assert heap==[10,7,9,8,3,1,5,2,6,4]
print('2006 scheduling, closures, subset graph, ternary heap checks passed.')
