from pathlib import Path
from html import escape
D=Path(__file__).resolve().parents[1];D.mkdir(exist_ok=True)
def text(x,y,s,size=16):return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="currentColor" stroke="none">{escape(s)}</text>'
def path(d,arrow=False):return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.5"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def rect(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor"/>'
def circle(x,y,r):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
def save(n,w,h,body,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><title>{escape(title)}</title><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="currentColor"/></marker></defs>'+body+'</svg>'
 (D/f'CS-2025-S1-Q{n}-1.svg').write_text(s+'\n')
# Unnamed DFA states, initial arrow, double accepting circle. Curves match source directions.
b=''
for x in [65,190,315,440]:b+=circle(x,100,17)
b+=circle(440,100,12)+path('M15 100 H48',True)
for x,label in [(65,'b'),(190,'a'),(315,'b')]:b+=path(f'M{x+17} 100 H{x+108}',True)+text(x+62,91,label,20)
for x,label in [(65,'a'),(190,'b')]:b+=path(f'M{x-11} 87 C{x-10} 22 {x+10} 22 {x+11} 87',True)+text(x,30,label,20)
b+=path('M440 83 C435 37 350 37 315 82',True)+text(380,31,'a',20)
b+=path('M315 117 C280 157 100 157 65 117',True)+text(190,166,'a',20)
b+=path('M440 117 C400 159 227 153 198 116',True)+text(337,166,'b',20)
save(50,480,185,b,'DFA over a and b')
# Memory hierarchy: all access times include the source qualifiers.
b=rect(160,10,100,50)+text(210,40,'Processor')+path('M210 60 V90',True)
b+=rect(100,90,220,80)+text(210,113,'L1 cache')+text(210,137,'Hit rate=95%,')+text(210,160,'Access time = 10 ns')+path('M210 170 V200',True)
b+=rect(10,200,400,100)+text(210,222,'L2 cache')+text(210,245,'Hit rate=85%,')+text(210,269,'Access time (including L1 cache miss penalty)')+text(210,291,'= 20 ns')+path('M210 300 V330',True)
b+=rect(10,330,400,110)+text(210,357,'Main Memory')+text(210,383,'Access time (including L1 and L2 cache miss')+text(210,407,'penalty) = 200 ns')
save(53,420,450,b,'Two-level cache and main memory access times')
# Router path.
b=rect(10,10,100,80)+text(60,55,'Source')+rect(550,10,110,80)+text(605,55,'Destination')
b+=rect(150,145,175,80)+text(237.5,178,'Router-1')+text(237.5,204,'(MTU=5000 bytes)')
b+=rect(365,145,175,80)+text(452.5,178,'Router-2')+text(452.5,204,'(MTU=3000 bytes)')
b+=path('M60 90 V185 H150',True)+path('M325 185 H365',True)+path('M540 185 H605 V90',True)
save(57,675,245,b,'IPv4 route through two routers')
# Merged state table.
b=rect(10,10,400,330)
for y in range(76,341,33):b+=path(f'M10 {y} H410')
b+=path('M10 43 H410')
for x in [130,270]:b+=path(f'M{x} 10 V340')
for x in [200,340]:b+=path(f'M{x} 43 V340')
b+=text(70,33,'Present state')+text(200,33,'Next state')+text(340,33,'Output f')
for x,s in zip([165,235,305,375],['X = 0','X = 1','X = 0','X = 1']):b+=text(x,66,s)
rows=[['A','F','B','0','0'],['B','D','C','0','0'],['C','F','E','0','0'],['D','G','A','1','0'],['E','D','C','0','0'],['F','F','B','1','1'],['G','G','H','0','1'],['H','G','A','1','0']]
for i,row in enumerate(rows):
 for x,s in zip([70,165,235,305,375],row):b+=text(x,99+33*i,s)
save(59,420,350,b,'FSM state transition and output table')
# 4 D flip flops with common rising-edge clock and complemented feedback.
b=''
for i,x in enumerate([50,185,320,455]):
 b+=rect(x,90,80,160)+text(x+25,165,f'D{i}',14)+text(x+67,125,f'Q{chr(8320+i)}',14)+text(x+67,211,f'Q{chr(8320+i)}',14)
 b+=path(f'M{x+57} 198 H{x+77}')
 b+=path(f'M{x+17} 250 L{x+40} 207 L{x+63} 250')+path(f'M{x+40} 250 V320')
 b+=path(f'M{x+80} 125 H{x+135 if i<3 else x+115}')
 if i<3:b+=path(f'M{x+80} 207 H{x+115}')
b+=path('M535 207 H615 V15 H15 V125 H50')+path('M40 320 H495')+text(43,298,'CLK',14)
save(60,635,340,b,'Four D-flip-flops with complemented Q3 feedback')
# Linked lists; preserve every value, head pointer, data/pointer divider and NULL mark.
b=''
for row,(label,values) in enumerate([('L1',[1,7,12,3,9,5,11,15,8]),('L2',[1,11,6,9,15,12,4])]):
 y=30+row*80;b+=text(16,y-8,label,14)+circle(16,y,2)+path(f'M18 {y} H46',True)
 for i,v in enumerate(values):
  x=46+70*i;b+=rect(x,y-17,48,34)+path(f'M{x+35} {y-17} V{y+17}')+text(x+17,y+6,str(v),16)+circle(x+41,y,2)
  if i<len(values)-1:b+=path(f'M{x+43} {y} H{x+70}',True)
  else:
   z=x+64;b+=path(f'M{x+43} {y} H{z} V{y+35}')+path(f'M{z-10} {y+35} H{z+10} M{z-7} {y+41} H{z+7} M{z-4} {y+47} H{z+4}')
save(62,690,170,b,'Linked lists L1 and L2 before code execution')
# Weighted graph, crossing diagonals have no vertex at intersection.
b=path('M65 45 H215 V185 H65 Z M65 45 L215 185 M65 185 L215 45')
for x,y,label in [(65,45,'A'),(215,45,'B'),(65,185,'D'),(215,185,'C')]:
 # Edge endpoints are shortened below so circle interiors stay transparent safely.
 pass
b=''
for d in ['M87 45 H193','M215 67 V163','M87 185 H193','M65 67 V163','M81 60 L199 170','M81 170 L199 60']:b+=path(d)
for x,y,label in [(65,45,'A'),(215,45,'B'),(65,185,'D'),(215,185,'C')]:b+=circle(x,y,22)+text(x,y+7,label,20)
for x,y,label in [(140,35,'7'),(233,121,'x'),(140,216,'8'),(48,125,'6'),(152,98,'1'),(162,163,'3')]:b+=text(x,y,label,20)
save(64,275,235,b,'Weighted undirected graph on A B C D')
