import itertools,math,json
# Exhaustive valid-input circuit check.
for d in range(10):
 i1,i2,i3,i4=[(d>>k)&1 for k in range(4)]
 r=i1+2*((i2 and not i3) or i4)+4*(i3 and not i2)
 assert r==d%6
# Multisets via multiplicity vectors.
for n in range(1,7):
 count=sum(sum(v)==4 and 2 in v for v in itertools.product(range(5),repeat=n))
 assert count==n*(n-1)**2//2
# PDA exhaustive bounded strings; consume transition epsilon only from p to q.
def accept(w):
 todo=[('p',0,0)];seen=set()
 while todo:
  st,pos,k=todo.pop()
  if (st,pos,k) in seen:continue
  seen.add((st,pos,k))
  if pos==len(w) and k==0:return True
  if st=='p':
   todo.append(('q',pos,k))
   if pos<len(w) and w[pos]=='0':todo.append(('p',pos+1,k+1))
  elif pos<len(w) and w[pos]=='1' and k:
   if st=='q':todo.extend([('q',pos+1,k-1),('r',pos+1,k)])
   else:todo.append(('q',pos+1,k-1))
 return False
for l in range(10):
 for t in itertools.product('01',repeat=l):
  w=''.join(t);n=w.count('0');m=w.count('1')
  assert accept(w)==(w=='0'*n+'1'*m and n<=m<=2*n)
# Standard DAA correction uses low digit/AC and high digit/CY.
def enc(d):return 16*(d//10)+d%10
def daa(a,cy,ac):
 correction=(6 if (a&15)>9 or ac else 0)+(0x60 if a>0x99 or cy else 0)
 return (a+correction)&255, bool(cy or a>0x99 or a+correction>255)
for b in range(100):
 for c in range(100):
  a=0x99-enc(c);v=a+enc(b);ac=((a&15)+(enc(b)&15)>15)
  a,cy=daa(v&255,v>255,ac)
  if cy:
   ac=(a&15)==15;a=(a+1)&255;a,cy=daa(a,cy,ac);d=0;e=a
  else:e=0x99-a;d=0 if e==0 else 255
  expect=enc(c-b) if b<=c else (enc(b-c)+0x60)&255
  assert (d,e)==(255 if b<c else 0,expect),(b,c,d,e,expect)
from pathlib import Path
rows=[q for q in json.load(open(Path(__file__).resolve().parents[1]/'data/questions.json')) if q['paper_id']=='CS-2000' and 50<=int(q['source_question_number'])<=70]
assert len(rows)==21 and [r['question_id'] for r in rows]==[f'CS-2000-Q{n}' for n in range(50,71)]
assert all(r['marks'] is None and r['source_group_marks']==5 and r['official_answer'] is None for r in rows)
print('PASS: 10 circuit rows; multiset counts n=1..6; 1023 PDA strings; 10000 BCD register pairs; 21-leaf schema/numbering.')
