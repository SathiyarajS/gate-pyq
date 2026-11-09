import json,sqlite3,itertools,pathlib
out=pathlib.Path(__file__).resolve().parents[1]; results={}
a=[q for q in json.load(open(out/'data/questions.json')) if q['paper_id']=='CS-1999' and 71<=int(q['source_question_number'])<=88]; inv=json.load(open(out/'data/source-provenance/CS-1999-inventory.json'))
assert [int(x['source_question_number']) for x in a]==list(range(71,89))
for x,i in zip(a,inv['items'][70:]):assert x['marks']==i['marks'] and x['printed_question_number']==i['printed_id'] and x['official_answer'] is None
results['schema_inventory']='18 distinct leaves; ordinals, printed labels and marks agree; official answers null.'
dur=[[1,2,1,1],[1,2,2,1],[2,1,3,2],[1,3,2,1],[1,2,1,2]]; c=[[0]*5 for _ in range(6)]
for i in range(1,6):
 for j in range(1,5):c[i][j]=max(c[i-1][j],c[i][j-1])+dur[i-1][j-1]
assert c[5][4]==15
schedule=[[(1,1),(2,3),(4,4),(5,5)],[(2,2),(4,5),(6,7),(8,8)],[(4,5),(6,6),(8,10),(11,12)],[(6,6),(8,10),(11,12),(13,13)],[(8,8),(11,12),(13,13),(14,15)]]
for i in range(5):
 for j in range(4):
  s,e=schedule[i][j];assert e-s+1==dur[i][j]
  if j<3:assert e<schedule[i][j+1][0]
  if i<4:
   # stage is held until transfer to next stage; downstream availability permits simultaneous transfer.
   released=schedule[i][j+1][0] if j<3 else e+1
   assert schedule[i+1][j][0]>=released
results['pipeline']='15-cycle lower bound and no-buffer blocking schedule validated.'
vals=[]
for p,q in itertools.product([False,True],repeat=2):
 v=not((not p) or q) or ((not q)or p);vals.append(v);assert v==(p or not q)
assert vals==[True,False,True,True];results['logic']=vals
for n in range(65536):
 r=n;count=0
 while r:
  old=r;r=(r>>1)<<1;count+=old!=r;r>>=1
 assert count==n.bit_count()
results['assembly']='All 65,536 unsigned 16-bit inputs agree with population count.'
sel=[]
for address in range(65536):
 S=((address>>11)==2)
 if S:sel.append(address)
assert sel==list(range(0x1000,0x1800));assert sum(1 for x in sel if not(x&1024))==1024
results['memory_decode']='Exhaustive 16-bit address decode selects exactly 1000h–17FFh; each bank has 1024 bytes.'
assert min(2**p for p in range(14) if 2*(8192//2**p)<=2**p)==128
assert 16-9-4==3 and 16-(16-9)-5==4
results['paging']={'minimum_page_bytes':128,'tlb_tag_bits':3,'aging_bits':4}
db=sqlite3.connect(':memory:');db.executescript('CREATE TABLE EMP("Employee-no" INTEGER,"Dept-no" INTEGER,"Employee-name" TEXT,Salary INTEGER); CREATE TABLE DEPT("Dept-no" INTEGER PRIMARY KEY,"Dept-name" TEXT,Location TEXT);')
db.executemany('INSERT INTO DEPT VALUES(?,?,?)',[(1,'A','Calcutta'),(2,'B','Delhi'),(3,'C','Calcutta')]);db.executemany('INSERT INTO EMP VALUES(?,?,?,?)',[(1,1,'One',50000),(2,1,'Two',100000),(3,1,'Three',100001),(4,2,'Four',120000),(5,2,'Five',None)])
r=db.execute('SELECT e."Employee-name" FROM EMP e JOIN DEPT d ON d."Dept-no"=e."Dept-no" WHERE d.Location=\'Calcutta\' AND e.Salary>50000').fetchall();assert r==[('Two',),('Three',)]
r2=db.execute('SELECT d."Dept-no",COUNT(e."Dept-no") FROM DEPT d LEFT JOIN EMP e ON e."Dept-no"=d."Dept-no" AND e.Salary>100000 GROUP BY d."Dept-no"').fetchall();assert r2==[(1,1),(2,1),(3,0)]
results['sql']={'names':r,'counts_including_empty_department':r2,'edge_cases':'Exact thresholds excluded, NULL salary excluded, empty department preserved.'}
results['scope']='Author computational checks only, not independent review or an official-key comparison. Source/model qualifications remain in solutions.'
print(json.dumps(results,indent=2))
