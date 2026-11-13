"""Repeatable independent author checks; no external answer key is consulted."""
import collections,itertools,json,math
from pathlib import Path
root=Path(__file__).parent
rows=json.loads((root/'cs-2002-q51-72.json').read_text())
ledger={d['normalized_ordinal']:d for d in json.load(open('/workspace/shared/gate2002-audit/inventory.json'))['items']}
assert len(rows)==22
for n,d in zip(range(51,73),rows):
 assert d['question_id']==f'CS-2002-Q{n}'
 assert d['printed_question_number']==ledger[n]['printed_id']
 assert d['source_subpart']==ledger[n]['printed_subpart']
 assert d['marks'] is None and d['source_group_marks']==5
 assert d['official_answer'] is None and d['key_url'] is None
 assert d['verification_status']=='independently_solved'
 assert d['independent_review']['status']=='pending'
 assert d['source_page'] in d['source_pages']
 assert d['explanatory_depth_status']=='expanded'
 assert d['explanatory_depth_review']['status']=='pending'
 assert d['solution'].startswith('1.') and d['solution'].count('```')%2==0
 assert d['shared_context'] and d['shared_context_reference']['source_url']==d['source_url']
 assert all('#page=' in u for u in d['source_figure_urls'])
 assert d['source_visual_reviewed'] and not d['source_transcription_verified']
for x,y,z in itertools.product([0,1],repeat=3):
 assert ((x and not y) or (y and not z))==((x or y) and not(y and z))
NAND=lambda x,y:not(x and y)
for a,b,c,d,e,f in itertools.product([0,1],repeat=6):
 n1,n2,n3=NAND(a,b),NAND(c,d),NAND(e,f)
 n4=NAND(n1,n2);n5=NAND(n4,n4);n6=NAND(n5,n3)
 assert n6==((a and b) or (c and d) or (e and f))
F=0x780000;E=65
word=(1<<31)|(F<<7)|E
assert word==0xbc000041 and -(F/2**24)*16**(E-64)==-7.5
assert round(math.log10((1-2**-24)*16.**63))==76
r0=(0,)*6;r1=(0,)*6;r2=(0,)*5;out=[]
for a,b in zip([6,3,7,5,0,0,0,0],[5,5,3,6,0,0,0,0]):
 b2,a2,b1,a1,b0,a0=r0;s=a0+b0
 new1=(b2,a2,b1,a1,s>>1,s&1)
 b2,a2,b1,a1,c1,s0=r1;s=a1+b1+c1
 new2=(b2,a2,s>>1,s&1,s0)
 r0=((b>>2)&1,(a>>2)&1,(b>>1)&1,(a>>1)&1,b&1,a&1)
 r1=new1;r2=new2
 b2,a2,c2,s1,s0=r2;out.append(((a2+b2+c2)<<2)|(s1<<1)|s0)
assert out==[0,0,11,8,10,11,0,0]
cache=[None]*512;miss=0
for i in range(2047,-1,-1):
 block=i//4;line=block%512
 if cache[line]!=block:miss+=1;cache[line]=block
assert miss==512
assert {i//4 for i in range(2048) if (i//4)%512==0}=={0}
n=3
for mask in range(1<<(n*n)):
 G=[[bool(mask&(1<<(i*n+j))) for j in range(n)] for i in range(n)]
 P=[[0 if i==j else (1 if G[i][j] else float('inf')) for j in range(n)] for i in range(n)]
 for i in range(n):
  for j in range(n):
   for k in range(n):P[j][k]=min(P[j][k],P[j][i]+P[i][k])
 for src in range(n):
  d=[float('inf')]*n;d[src]=0;q=collections.deque([src])
  while q:
   u=q.popleft()
   for v in range(n):
    if G[u][v] and d[v]==float('inf'):d[v]=d[u]+1;q.append(v)
  assert P[src]==d

def hanoi(n,a,b,c):
 return [] if n==0 else hanoi(n-1,a,c,b)+[(n,a,c)]+hanoi(n-1,b,a,c)
for n in range(1,9):
 poles={'A':list(range(n,0,-1)),'B':[],'C':[]};m=hanoi(n,'A','B','C')
 for disk,a,c in m:
  assert poles[a].pop()==disk
  assert not poles[c] or poles[c][-1]>disk
  poles[c].append(disk)
 assert poles=={'A':[],'B':[],'C':list(range(n,0,-1))}
 assert len(m)==2**n-1
print('PASS: 22 ledger/metadata/depth-structure checks; 8 one-NOT and 64 NAND truth cases; float encoding/range; synchronous pipeline; cache scan; 512 directed-graph Floyd/BFS comparisons; Hanoi n=1..8.')
