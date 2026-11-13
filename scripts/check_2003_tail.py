import itertools,math,json
# Q68: independent Kruskal implementation.
edges=[('a','b',6),('a','c',1),('a','d',2),('a','e',8),('b','d',3),('b','g',2),('c','d',2),('d','h',15),('e','h',8),('e','f',11),('e','i',2),('f','h',4),('f','i',9),('g','h',8),('g','i',14),('g','j',19),('h','i',4),('i','j',5)]
p={v:v for v in 'abcdefghij'}
def find(x):
 while p[x]!=x:x=p[x]
 return x
total=0;selected=[]
for a,b,w in sorted(edges,key=lambda e:e[2]):
 if find(a)!=find(b):p[find(a)]=find(b);total+=w;selected.append((a,b,w))
assert total==31 and len(selected)==9
print('Q68 MST',total,selected)
# Q69 complete alternate sequence.
events='as bs cs ae ds ce es fs be de gs ee fe hs ge he'.split()
active=set();counts=[]
for e in events:
 if e[-1]=='s':active.add(e[0])
 else:active.remove(e[0])
 counts.append(len(active))
assert max(counts)==4 and not active
print('Q69 maximum overlap',max(counts),counts)
# Q70: exhaustive loop-free digraphs through four vertices.
for n in range(1,5):
 es=[(u,v) for u in range(n) for v in range(n) if u!=v]
 for bits in range(1<<len(es)):
  E={e for b,e in enumerate(es) if bits>>b&1}
  A=[[int((u,v) in E) for v in range(n)] for u in range(n)]
  for i in range(n):
   for j in range(n):
    for k in range(n):A[j][k]=max(A[j][k],A[j][i]+A[i][k])
  for L in range(2,n+1):
   for path in itertools.permutations(range(n),L):
    if all((path[i],path[i+1]) in E for i in range(L-1)):
     assert A[path[0]][path[-1]]>=L-1
print('Q70 simple-path upper bound checked on all loop-free digraphs n<=4')
# Q82.
mask=(255,255,31,0)
pairs=[('172.57.88.62','172.56.87.233'),('10.35.28.2','10.35.29.4'),('191.203.31.87','191.234.31.88'),('128.8.129.13','128.8.161.55')]
def masked(s):return tuple(a&m for a,m in zip(map(int,s.split('.')),mask))
assert [masked(a)==masked(b) for a,b in pairs]==[False,False,False,True]
assert math.isclose(5*1000*8/(450e-6),88888888.88888889)
print('Q82 D; Q84 throughput',5*1000*8/(450e-6),'bits/s')
# Q85 keys under explicit projected dependencies.
U=set('RNDA');fds=[(set('R'),set('N')),(set('N'),set('R')),(set('D'),set('A'))]
def closure(s):
 s=set(s)
 while True:
  t=s.copy()
  for lhs,rhs in fds:
   if lhs<=s:s|=rhs
  if s==t:return s
keys=[]
for size in range(1,5):
 for combo in itertools.combinations(sorted(U),size):
  c=set(combo)
  if closure(c)==U and not any(k<=c for k in keys):keys.append(c)
assert set(map(frozenset,keys))=={frozenset('RD'),frozenset('ND')}
print('Q85 keys',keys)
# Q88 directly simulate representative n for both floor and ceiling.
for n in range(3,1001):
 for L in [2*(n.bit_length()-1),2*((n-1).bit_length())]:
  A=[0]*(n+1)
  for k in range(2,L+1):
   for j in range(k+1,n+1):A[j]=int(bool(A[j] or j%k))
  assert all(A[j] for j in range(3,n+1))
print('Q88 floor/ceiling loops output empty for all n=3..1000')
# Required artifact integrity.
p='/workspace/shared/gate-pyq-contributions/cs-2003-q66-90.json'
rows=json.load(open(p))
assert len(rows)==25 and [int(d['source_question_number']) for d in rows]==list(range(66,91))
assert all(d['official_answer'] is None and d['key_url'] is None and d['verification_status']=='independently_solved' and d['independent_review']['status']=='pending' for d in rows)
assert [d['source_question_number'] for d in rows if d['derived_answer'] is None]==['69','72','78','84']
assert [d['source_question_number'] for d in rows if d['subject']=='excluded']==['75']
print('25 artifact rows valid; four conditional/unmatched answers; Q75 excluded')
