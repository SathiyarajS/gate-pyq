"""Targeted reproducible author checks; not independent mathematical review."""
import itertools,json,heapq
from pathlib import Path
out=Path(__file__).resolve().parents[1]
V=set('ABCDEF');E={frozenset(e) for e in ['AB','AD','AE','AF','BC','BD','CF','DE','DF','EF']}
def components(es):
 unseen=set(V);parts=[]
 while unseen:
  seen={next(iter(unseen))};front=list(seen)
  while front:
   a=front.pop()
   for e in es:
    if a in e:
     for b in e-seen:seen.add(b);front.append(b)
  parts.append(sorted(seen));unseen-=seen
 return sorted(parts)
assert len(components(E-{frozenset(e) for e in ['AB','EF','BD','AE','AD']}))==1
assert components(E-{frozenset(e) for e in ['BD','CF','AB']})==[['A','D','E','F'],['B','C']]
cuts=[]
for k in range(1,len(E)+1):
 cuts=[s for s in itertools.combinations(E,k) if len(components(E-set(s)))>1]
 if cuts:break
assert k==2
# Enumerate all linear extensions of the 3x3 grid order, i.e. all distinct-key monotone matrices.
matrices=0;outcomes=set()
for perm in itertools.permutations(range(9)):
 if any(perm[r*3+c]>=perm[r*3+c+1] for r in range(3) for c in range(2)):continue
 if any(perm[r*3+c]>=perm[(r+1)*3+c] for r in range(2) for c in range(3)):continue
 b,c,d,e=perm[1],perm[3],perm[2],perm[6]
 if b<=c:ans=[perm[0],b,min(c,d)];leaf=('b', 'd' if d<=c else 'c')
 else:ans=[perm[0],c,min(b,e)];leaf=('c','e' if e<=b else 'b')
 assert ans==[0,1,2];matrices+=1;outcomes.add(leaf)
assert len(outcomes)==4
# Every legal pumping-lemma decomposition for chosen p fails on pumping down.
pumping_checks=0
for p in range(1,9):
 w='0'*p+'1'*p+'c'+'0'*p+'1'*p
 for start in range(len(w)):
  for end in range(start+1,min(start+p,len(w))+1):
   for v_end in range(start,end+1):
    for y_start in range(v_end,end+1):
     if v_end-start+end-y_start==0:continue
     s=w[:start]+w[v_end:y_start]+w[end:]
     assert s.count('c')!=1 or s.split('c')[0]!=s.split('c')[1]
     pumping_checks+=1
for seq in [[7,6,5,4,3,2,1],[7,6,5,4,2,3,1]]:
 h=[]
 for x in seq:heapq.heappush(h,x)
 assert h==[1,4,2,7,5,6,3]
 heapq.heappop(h);assert h==[2,4,3,7,5,6]
# Attribute rules tested against exact rational evaluation.
from fractions import Fraction
attribute_checks=0
for il in range(1,5):
 for fl in range(1,5):
  for bits in itertools.product('01',repeat=il+fl):
   left=''.join(bits[:il]);right=''.join(bits[il:]);v=Fraction(int(left,2))+Fraction(int(right,2),2**fl)
   expected=sum(Fraction(int(b))*Fraction(2)**(il-1-j) for j,b in enumerate(left))+sum(Fraction(int(b),2**(j+1)) for j,b in enumerate(right))
   assert v==expected;attribute_checks+=1
rows=[q for q in json.load(open(out/'data/questions.json')) if q['paper_id']=='CS-1999' and 51<=int(q['source_question_number'])<=70];inv=json.load(open(out/'data/source-provenance/CS-1999-inventory.json'))
for n,r in enumerate(rows,51):
 i=inv['items'][n-1]
 assert r['question_id']==f'CS-1999-Q{n}'
 assert r['marks']==i['marks'] and r['source_parent_marks']==i['source_parent_marks']
 assert r['official_answer'] is None and r['key_url'] is None
 assert r['independent_review']['status']=='reviewed'
report={'status':'passed','scope':'Targeted author computational checks only; independent review pending','graph_min_cut':k,'min_cut_witnesses':[[ ''.join(sorted(e)) for e in s] for s in cuts],'matrix_linear_extensions_checked':matrices,'matrix_decision_tree_leaves':sorted(outcomes),'pumping_decompositions_checked':pumping_checks,'binary_fraction_attribute_cases':attribute_checks,'heap_variants_checked':2,'inventory_and_metadata_rows':len(rows)}
print(json.dumps(report,indent=2))
