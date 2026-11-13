import json,itertools,math,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
b=[r for r in json.loads((P/'data/questions.json').read_text()) if r['paper_id']=='CS-2019']
assert len(b)==65 and len({r['question_id'] for r in b})==65
for n,new in enumerate(b,1):
 assert new['question_id']==f'CS-2019-Q{n}'
 assert re.search(r'(?m)^1\.',new['solution']),n
 assert new['question_text']!='See linked original.'
 assert new['explanatory_depth_status']=='reviewed_expanded'
 assert new['independent_depth_review']['status']=='reviewed'
 assert new['source_url'].endswith('#page='+str(new['source_page']))
 assert new['solution_word_count']==len(new['solution'].split())
assert 20/(60-50)==2
assert 6000/8-6000/10==150
assert 50/160*100==31.25
assert (60+80+30+(40-2)+(12-2)+(7-2)+2)/0.25==900
assert 32-math.log2(16)==28
assert hex((0b11001)<<11)=='0xc800' and hex((0b11001<<11)+2**11-1)=='0xcfff'
assert format(2**16-28,'016b')=='1111111111100100'
for n in range(1,15):assert sum(k*math.comb(n,k) for k in range(1,n+1))==n*2**(n-1)
x,y,z=1,1,0; assert ((x|y)^z)!=(x^(y|z))
# Check the stated pumping choices in a bounded range, supplemental to the written general proof.
def lang_a(m):return m>=2 and (m-2)%3==0
def lang_b(m):return m>=10 and (m-10)%12==0
for m in range(24,1000):
 if lang_a(m):assert all(lang_a(m+(i-1)*3) for i in range(20))
 if lang_b(m):assert all(lang_b(m+(i-1)*12) for i in range(20))
for p in [3,5,9]:assert all(not lang_b(10+r) for r in range(1,p+1))
assert sum(2**i for i in range(5))==31
assert 2*(2*5+2)+2==26
assert 2/25==0.08 and pow(3,51,5)==2
assert round((7**2+6**2)/13**2,3)==0.503
# All legal interleavings of each process's read before its write.
vals=[]
for order in itertools.permutations([(p,k) for p in range(3) for k in 'rw']):
 if any(order.index((p,'r'))>order.index((p,'w')) for p in range(3)):continue
 d=100;local={}
 for p,k in order:
  if k=='r':local[p]=d
  else:d=local[p]+[20,-50,10][p]
 vals.append(d)
assert len(vals)==90 and min(vals)==50 and max(vals)==130
arr=[1,2,3,4,5,6,7,8,9,0,1,2,5];assert arr[4+1]==6
A=[-5,-10,6,3,-1,-2,13,4,-9,-1,4,12,-3,0]
assert max(sum(A[i:j+1]) for i in range(14) for j in range(i,14))==29
assert (2&252,5&252,6&252)==(0,4,4)
assert ({0,2,5,8,14}&{2,3,6,8,14,15})^{2,7,11,14}=={7,8,11}
assert 128*8192//4==262144
assert (12+1024+1024**2)*4096==4299210752
assert round(((12+1024+1024**2)*4096)/2**30,1)==4.0
assert math.prod(y-x for x,y in itertools.combinations([2,3,4,5],2))==12
assert 32*60000000/(1+3+8)==160000000
assert (0+2+2*4+4*6)/8==4.25
assert (6-2)/(6-1)==0.8
assert math.factorial(5)==120
assert 6*2+2<15<=6*3+2
# Exhaustive truth-table realization check for Q60 with complemented input literals.
assign=list(itertools.product([0,1],repeat=4));mask=(1<<16)-1
lit=[sum(bits[k]<<i for i,bits in enumerate(assign)) for k in range(4)]
lit+= [mask^x for x in lit]
target=sum((bits[1]==bits[3])<<i for i,bits in enumerate(assign))
nor=lambda x,y:mask^(x|y)
one={nor(x,y) for x in lit for y in lit}
assert target not in one
assert all(nor(x,y)!=target for g in one for x in lit+[g] for y in lit+[g])
bvar=lit[1];dvar=lit[3];nb=mask^bvar;nd=mask^dvar
assert nor(nor(bvar,nd),nor(nb,dvar))==target
assert sum([86,95,90,89,92])==452
j=1;count=0
while 2/j>0.0625:j*=2;count+=1
assert count==5
assert sum((10-i)-[2,4,6,8,10][4-i] for i in range(5))==10
assert 97*31==3007 and 96*30==2880
print('PASS: 65 complete records; numbered expansions and independent depth-review metadata; source links; selected algebra, Boolean, code traces, all 90 concurrency interleavings, and numerical results.')
