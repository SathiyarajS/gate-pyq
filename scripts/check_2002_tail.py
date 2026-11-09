import itertools, math, json, sqlite3
from pathlib import Path
O=Path('/workspace/shared/gate-pyq-contributions')
R=set('LMNOP'); fds=[(set('M'),set('O')),(set('NO'),set('P')),(set('P'),set('L')),(set('L'),set('MN'))]
def close(X,F):
 X=set(X)
 while True:
  old=X.copy()
  for a,b in F:
   if a<=X:X|=b
  if X==old:return X
def subsets(X):
 return [set(c) for n in range(len(X)+1) for c in itertools.combinations(sorted(X),n)]
projected=[]
for attrs in [set('LMNP'),set('MO')]:
 pf=[(x,close(x,fds)&attrs-x) for x in subsets(attrs)]
 pf=[(x,y) for x,y in pf if y]
 projected+=pf
 keys=[x for x in subsets(attrs) if attrs<=close(x,fds) and not any(attrs<=close(z,fds) for z in subsets(x) if z!=x)]
 assert all(attrs<=close(x,pf) for x,y in pf)
 print('BCNF relation', ''.join(sorted(attrs)), 'keys', [''.join(sorted(x)) for x in keys])
assert close(set('NO'),projected)==set('NO')
assert set('MO')<=close(set('M'),fds)
print('Lossless criterion true; projected NO closure:', ''.join(sorted(close(set('NO'),projected))))
r={(1,2),(2,3),(2,4),(4,5),(6,7),(6,8),(9,10)}
def view(r):return {(a,d) for a,b in r for c,d in r if b==c}
v=view(r);new=view(r|{(2,11),(11,6)})-v
assert v=={(1,3),(1,4),(2,5)}
assert new=={(1,11),(2,6),(11,7),(11,8)}
print('Self-join baseline',sorted(v),'additions', sorted(new))
dfa={0:{'a':1,'b':0},1:{'a':1,'b':2},2:{'a':1,'b':3},3:{'a':1,'b':0}}
nfa={(0,'a'):{0,1},(0,'b'):{0},(1,'b'):{2},(2,'b'):{3}}
for n in range(13):
 for seq in itertools.product('ab',repeat=n):
  s=''.join(seq);d=0;ns={0}
  for c in s:
   d=dfa[d][c]
   ns=set().union(*(nfa.get((q,c),set()) for q in ns))
  assert (d==3)==(3 in ns)==s.endswith('abb')
print('NFA/DFA correct for all 8191 binary-alphabet strings of lengths 0–12.')
for n in range(2,10):
 for k in range(1,n+1):
  # Simple dynamic program for the number of ordered positive k-part compositions.
  dp=[[0]*(n+1) for _ in range(k+1)];dp[0][0]=1
  for j in range(1,k+1):
   for total in range(1,n+1):dp[j][total]=sum(dp[j-1][total-v] for v in range(1,total+1))
  assert dp[k][n]==math.comb(n-1,k-1)
print('Composition formula checked for 2≤n≤9 and 1≤k≤n.')
c=sqlite3.connect(':memory:')
c.executescript('CREATE TABLE STUDENT(srollno INTEGER PRIMARY KEY,sname TEXT,sdegree TEXT); CREATE TABLE OFFER(cname TEXT,srollno INTEGER,osalary REAL,PRIMARY KEY(cname,srollno));')
c.executemany('INSERT INTO STUDENT VALUES(?,?,?)',[(i,f'S{i}','X' if i<=6 else 'Y') for i in range(1,12)])
c.executemany('INSERT INTO OFFER VALUES(?,?,?)',[('C1',i,100+i) for i in range(1,12)]+[('C2',7,200)])
ans=c.execute('SELECT S.sdegree, AVG(O.osalary) FROM STUDENT S JOIN OFFER O ON O.srollno=S.srollno GROUP BY S.sdegree HAVING COUNT(DISTINCT S.srollno)>5').fetchall()
assert ans==[('X',103.5)]
print('SQL test: six students qualify; five students with six offers do not.')
rows=json.load(open(O/'cs-2002-q73-101.json'))
assert len(rows)==29 and {x['question_id'] for x in rows}=={f'CS-2002-Q{q}' for q in range(73,102)}
assert all(x['source_section']=='B' and x['source_numbering_scheme']=='legacy_sections_subparts' and x['question_type']=='descriptive' and x['official_answer'] is None and x['marks'] is None and x['source_group_marks']==5 for x in rows)
assert rows[1]['source_issue_note'].startswith('Source variance:')
print('29 unique leaves, correct IDs/marks/provenance statuses.')
