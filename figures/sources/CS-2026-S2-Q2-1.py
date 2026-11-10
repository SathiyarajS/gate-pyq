from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent
class SVG:
 def __init__(self,title,w,h):self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title, quote=True)}"><title id="title">{escape(title)}</title><g stroke="currentColor" fill="none" stroke-width="1">']
 def line(self,x1,y1,x2,y2,dash=False):self.a.append(f'<path d="M{x1},{y1} L{x2},{y2}"'+(' stroke-dasharray="3 3"' if dash else '')+'/>')
 def text(self,x,y,t):self.a.append(f'<text x="{x}" y="{y}" fill="currentColor" stroke="none" font-family="serif" font-size="16" text-anchor="middle">{escape(t)}</text>')
 def cell(self,x,y,s,fill):self.a.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="'+('currentColor' if fill else 'none')+'"/>')
 def mask(self,x,y,rows,s):
  edges=set()
  for r,row in enumerate(rows):
   for c,v in enumerate(row):
    if v!='1':continue
    points=[(c,r),(c+1,r),(c+1,r+1),(c,r+1)]
    for a,b in zip(points,points[1:]+points[:1]):
     if (b,a) in edges:edges.remove((b,a))
     else:edges.add((a,b))
  paths=[]
  while edges:
   start,end=min(edges);edges.remove((start,end));points=[start,end]
   while end!=start:
    edge=next(e for e in edges if e[0]==end);edges.remove(edge);end=edge[1];points.append(end)
   paths.append('M'+' L'.join(f'{x+c*s},{y+r*s}' for c,r in points)+'Z')
  self.a.append('<path stroke="none" fill="currentColor" d="'+' '.join(paths)+'"/>')
 def tile(self,x,y,bits,s=55):
  self.cell(x,y,s,False)
  for i,b in enumerate(bits):self.a.append(f'<circle cx="{x+12+(i%3)*15}" cy="{y+12+(i//3)*15}" r="3.6" fill="'+('currentColor' if b=='1' else 'none')+'"/>')
 def save(self,n): (OUT/f'CS-2026-S2-Q{n}-1.svg').write_text(''.join(self.a)+'</g></svg>\n')
s=SVG('Panel I: cut square PQRS. Panel II: four candidate missing pieces (i)–(iv).',560,350)
s.text(105,25,'Panel I');s.text(400,25,'Panel II');s.line(235,35,235,335);s.line(400,45,400,325,True);s.line(260,190,550,190,True)
s.mask(25,130,['111111','101100','100001','111011','100011','111111'],25)
for x,y,t in [(25,125,'S'),(175,125,'R'),(25,298,'P'),(175,298,'Q')]:s.text(x,y,t)
for x,y,rows,label in [(270,60,['10011','11110','00100','11110'],'(i)'),(425,60,['10011','11110','00100','01110'],'(ii)'),(270,215,['10011','11110','00100','11100'],'(iii)'),(425,215,['10011','11110','00110','01100'],'(iv)')]:s.mask(x,y,rows,22);s.text(x+55,y+115,label)
s.save(2)
