from pathlib import Path
from html import escape
out=Path(__file__).resolve().parents[1];out.mkdir(exist_ok=True)
def text(x,y,s,size=16,anchor='start'):return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="currentColor">{escape(s)}</text>'
def line(x,y,X,Y):return f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="currentColor"/>'
def rect(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor"/>'
def save(n,w,h,title,body):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><title>{title}</title>'+body+'</svg>'
 (out/f'CS-2026-S1-{n}.svg').write_text(s)
s=rect(5,5,280,296)
for x in [61,117,173,229]:s+=line(x,55 if x in [117,229] else 5,x,301)
for y in [55,85]+list(range(112,301,27)):s+=line(5,y,285,y)
s+=text(33,28,'Input',14,'middle')+text(117,27,'Current',14,'middle')+text(117,45,'State',14,'middle')+text(229,27,'Next',14,'middle')+text(229,45,'State',14,'middle')
for x,a in zip([33,89,145,201,257],['P','Q₁','Q₀','Q₁⁺','Q₀⁺']):s+=text(x,76,a,16,'middle')
for row,v in enumerate(['00001','00110','01011','01111','10000','10100','11001','11110']):
 for x,a in zip([33,89,145,201,257],v):s+=text(x,105+row*27,a,16,'middle')
save('Q37-1',290,310,'Saturating counter Next State table',s)
s='<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="currentColor"/></marker></defs>'
def arrow(points):return f'<path d="{points}" fill="none" stroke="currentColor" marker-end="url(#arrow)"/>'
s+=text(155,17,'ENTRY',14)+arrow('M150 10 L150 38')
for x,y,w,h,label,lines in [(105,40,90,32,'B1',['a = b + i']),(20,108,110,70,'B2',['a = g * k','f = d − f','a = c * 4']),(190,108,110,50,'B3',['t = g * k','b = c + m']),(110,218,100,48,'B4',['x = g * k','y = b + i']),(110,302,100,32,'B5',['z = c + m'])]:
 s+=rect(x,y,w,h)+text(x+w+4,y+10,label,14)
 for j,t in enumerate(lines):s+=text(x+w/2,y+22+j*20,t,16,'middle')
for path in ['M150 72 L75 108','M150 72 L245 108','M75 178 L160 218','M245 158 L160 218','M160 266 L160 302','M160 334 L160 364']:s+=arrow(path)
s+=text(167,362,'EXIT',14)
save('Q42-1',332,375,'Control flow graph with blocks B1 through B5',s)
for num,title,rows in [(1,'SDD1', [('D → T V',['D.type = T.type','V.type = T.type']),('T → int',['T.type = int']),('T → float',['T.type = float']),('V → V₁ id',['V₁.type = V.type','put(id.entry, V.type)']),('V → id',['put(id.entry, V.type)'])]),(2,'SDD2',[('D → D₁ id',['D.type = D₁.type','put(id.entry, D₁.type)']),('D → T id',['D.type = T.type','put(id.entry, T.type)']),('T → int',['T.type = int']),('T → float',['T.type = float'])])]:
 y=80;s=text(165,22,title,17,'middle')+text(56,44,'Grammar',15,'middle')+text(56,65,f'(G{num})',15,'middle')+text(222,50,'Semantic Rules',15,'middle')+line(5,28,325,28)+line(5,76,325,76)
 for lhs,rhs in rows:
  s+=text(12,y+18,lhs,15)
  for j,r in enumerate(rhs):s+=text(119,y+18+20*j,r,15)
  y+=20*len(rhs)+5;s+=line(5,y,325,y)
 s+=rect(5,3,320,y-3)+line(110,28,110,y)
 save(f'Q53-{num}',330,y+5,f'{title} grammar and semantic rules',s)
