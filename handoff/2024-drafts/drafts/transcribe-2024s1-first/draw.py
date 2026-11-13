from pathlib import Path
import math,html
O=Path(__file__).parent
s=[]
def line(x,y,X,Y,dash=False):s.append(f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="currentColor"'+(' stroke-dasharray="5 3"' if dash else '')+'/>')
def text(x,y,t,size=14):s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="currentColor" text-anchor="middle">{html.escape(t)}</text>')
def rect(x,y,w,h):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor"/>')
def save(n,w,h,title):
 p=O/f'figures/CS-2024-S1-Q{n}-1.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><title>{title}</title>'+''.join(s)+'</svg>')
s=[];rect(1,1,518,338);text(260,25,'Macronutrient energy contribution',17)
cx,cy,r=260,185,135;start=-90
for frac in [35,20,20,20,5]:
 end=start+frac*3.6;x=cx+r*math.cos(math.radians(start));y=cy+r*math.sin(math.radians(start));X=cx+r*math.cos(math.radians(end));Y=cy+r*math.sin(math.radians(end));s.append(f'<path d="M{cx} {cy} L{x} {y} A{r} {r} 0 0 1 {X} {Y} Z" fill="none" stroke="currentColor"/>');start=end
for x,y,rows in [(325,158,['Carbohydrates','35%']),(287,264,['Proteins','20%']),(191,238,['Unsaturated fat','20%']),(187,132,['Saturated fat','20%']),(245,77,['Trans','fat','5%'])]:
 for k,t in enumerate(rows):text(x,y+16*k,t,13)
save(8,520,340,'Macronutrient energy contribution pie chart')
s=[]
for x in range(20,330,9):line(x,60,min(x+6,330),60)
text(40,49,'A',18);text(300,49,'B',18)
for col,row in [(1,-1),(0,0),(1,1),(3,0),(4,0),(4,1)]:rect(100+col*27,60+row*27,27,27)
save(10,350,135,'Six squares and horizontal symmetry line AB')
s=[];line(20,50,280,50);line(65,50,65,108);line(65,108,120,108);s.append('<path d="M120 78 L120 138 L182 108 Z" fill="none" stroke="currentColor"/><circle cx="192" cy="108" r="10" fill="none" stroke="currentColor"/>');text(144,113,'NOT',16);line(202,108,245,108);line(245,108,245,88);line(245,88,280,88);s.append('<path d="M280 36 L322 36 A34 34 0 0 1 322 104 L280 104 Z" fill="none" stroke="currentColor"/>');text(316,77,'AND',23);line(356,70,372,70);text(27,43,'X',19);text(366,64,'Y',22)
for x,y in [(280,50),(280,88)]:s.append(f'<path d="M{x-12} {y-5} L{x} {y} L{x-12} {y+5} L{x-8} {y} Z" fill="currentColor"/>')
save(28,390,155,'X and its NOT feed an AND gate producing Y')
# ER panels preserve each entity/relationship and connection, including erroneous alternatives.
s=[]
def box(x,y,t,w=70):rect(x-w/2,y-15,w,30);text(x,y+4,t,12)
def diamond(x,y,t,w=80):s.append(f'<path d="M{x-w/2} {y} L{x} {y-29} L{x+w/2} {y} L{x} {y+29} Z" fill="none" stroke="currentColor"/>');text(x,y+4,t,12)
for idx,(ox,oy) in enumerate([(10,10),(370,10),(10,300),(370,300)]):
 # coordinates in each panel
 def L(a,b,c,d):line(ox+a,oy+b,ox+c,oy+d)
 def B(x,y,t,w=70):box(ox+x,oy+y,t,w)
 def D(x,y,t,w=80):diamond(ox+x,oy+y,t,w)
 L(70,55,85,55);L(155,55,175,55);L(210,70,210,111);L(35,70,35,225);L(35,225,85,225)
 if idx!=2:L(170,140,150,140)
 L(245,55,310,55);L(310,55,310,111);L(310,169,310,225);L(155,225,175,225)
 B(35,55,'Instructor');D(120,55,'Teaches',70);B(210,55,'Course');B(115,140,'Classroom');D(210,140,'Allocation')
 if idx==0:
  L(210,40,210,15);L(210,15,245,15);B(280,15,'Registration');D(310,140,'Student',70);D(120,225,'Guides',70);L(155,225,310,225)
 else:
  D(310,140,'Registration');D(120,225,'Guides',70);B(210,225,'Projects' if idx==1 else 'Student');L(245,225,310,225)
 if idx==2:L(190,70,130,125)
 text(ox+53,oy+274,['(i)','(ii)','(iii)','(iv)'][idx],17)
save(20,725,590,'Four ER diagram alternatives (i), (ii), (iii), and (iv)')
