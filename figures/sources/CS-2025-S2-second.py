from pathlib import Path
from xml.sax.saxutils import escape
D=Path(__file__).resolve().parents[1]
def save(n,w,h,title,parts):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{title}</title>'+''.join(parts)+'</svg>'
 (D/f'CS-2025-S2-Q{n}-1.svg').write_text(s)
def line(x,y,x2,y2):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="1"/>'
def text(x,y,s,size=16,anchor='middle',extra=''):return f'<text x="{x}" y="{y}" font-family="serif" font-size="{size}" text-anchor="{anchor}" fill="currentColor" {extra}>{escape(s)}</text>'
p=[line(30,10,60,40),text(68,18,'yz',16,extra=''),text(38,48,'wx',16,extra='')]
for i in range(5):p+=[line(60+i*40,40,60+i*40,184),line(60,40+i*36,220,40+i*36)]
for r,row in enumerate(['1001','0110','0110','1001']):
 for c,v in enumerate(row):p.append(text(80+40*c,64+36*r,v))
save(43,250,200,'Karnaugh Map for F(w,x,y,z)',p)
# Merged header table: same cell order and asterisks as source.
p=[];w=780;xs=[10,114]+[114+50*i for i in range(1,14)];ys=[10,40,70,100,130,160]
for y in ys:p.append(line(10,y,764,y))
p.extend([line(10,10,10,160),line(114,10,114,160),line(764,10,764,160)])
for x in xs[2:-1]:p.append(line(x,40,x,160))
p.extend([text(62,31,'initially',28,extra='font-style="italic"'),text(439,31,'after',28,extra='font-style="italic"')])
rows=[['-','1*','2*','3*','4*','5*','4','1','6*','4','5','1*','3*','2*'],['-','1','1','1','1','1','1','1','6','6','6','6','6','2'],['-','-','2','2','4','4','4','4','4','4','4','1','1','1'],['-','-','-','3','3','5','5','5','5','5','5','5','3','3']]
for r,row in enumerate(rows):
 for c,v in enumerate(row):p.append(text(62 if c==0 else 114+(c-.5)*50,62+r*30,v,28))
save(47,780,175,'Frame contents initially and after each page reference',p)
p=[]
for x,y,width,height in [(15,10,190,260),(300,38,190,180)]:
 p.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="none" stroke="currentColor"/>')
for x,y,rows in [(29,38,['Transaction T1','R1(X)','W1(Y)','R1(X)','W1(X)','COMMIT(T1)']),(314,66,['Transaction T2','W2(X)','W2(Y)','COMMIT(T2)'])]:
 for i,s in enumerate(rows):p.append(text(x,y+40*i,s,20,'start','font-weight="bold"' if i==0 else ''))
save(53,510,285,'Transactions T1 and T2',p)
# Unlabelled tree, pinned positions copied from the actual source.
points=[(75,230),(100,153),(115,62),(177,119),(209,18),(241,86),(337,77),(262,163),(180,238),(315,213),(366,135),(415,62),(460,148),(563,150)]
edges=[(0,1),(1,3),(2,3),(3,5),(4,5),(5,6),(3,7),(7,8),(7,9),(7,10),(10,11),(10,12),(12,13)]
p=[line(*points[a],*points[b]) for a,b in edges]
p +=[f'<circle cx="{x}" cy="{y}" r="4" fill="currentColor"/>' for x,y in points]
save(59,600,260,'Unlabelled tree T',p)
