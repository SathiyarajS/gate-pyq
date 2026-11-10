from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent
class SVG:
 def __init__(self,title,w,h):self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title, quote=True)}"><title id="title">{escape(title)}</title><g stroke="currentColor" fill="none" stroke-width="1">']
 def line(self,x1,y1,x2,y2,dash=False):self.a.append(f'<path d="M{x1},{y1} L{x2},{y2}"'+(' stroke-dasharray="3 3"' if dash else '')+'/>')
 def text(self,x,y,t):self.a.append(f'<text x="{x}" y="{y}" fill="currentColor" stroke="none" font-family="serif" font-size="16" text-anchor="middle">{escape(t)}</text>')
 def cell(self,x,y,s,fill):self.a.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill-opacity="0.4" fill="'+('currentColor' if fill else 'none')+'"/>')
 def mask(self,x,y,rows,s):
  # Unit-cell paths merge visually without exposing artificial grid edges.
  for r,row in enumerate(rows):
   for c,v in enumerate(row):
    if v=='1':self.a.append(f'<path stroke="none" fill="currentColor" d="M{x+c*s},{y+r*s}h{s}v{s}h-{s}Z"/>')
 def tile(self,x,y,bits,s=55):
  self.cell(x,y,s,False)
  for i,b in enumerate(bits):self.a.append(f'<circle cx="{x+12+(i%3)*15}" cy="{y+12+(i//3)*15}" r="3.6" fill="'+('currentColor' if b=='1' else 'none')+'"/>')
 def save(self,n): (OUT/f'CS-2026-S2-Q{n}-1.svg').write_text(''.join(self.a)+'</g></svg>\n')
s=SVG('Panel I: empty four by four grid, column totals 2,2,2,2 and row totals 3,1,2,2. Panel II: candidate shaded grids (i)–(iv).',570,390)
s.text(100,25,'Panel I');s.text(400,25,'Panel II');s.line(215,30,215,380);s.line(400,40,400,370,True);s.line(225,210,565,210,True)
for c in range(4):s.text(45+35*c,140,'2')
for r,label in enumerate('3122'):s.text(17,166+35*r,label)
def grid(x,y,rows):
 for r,row in enumerate(rows):
  for c,b in enumerate(row):s.cell(x+c*35,y+r*35,35,b=='1')
grid(27.5,148,['0000']*4)
for x,y,rows,label in [(235,40,['1011','0101','0010','1100'],'(i)'),(420,40,['1011','0100','0011','1100'],'(ii)'),(235,225,['1011','0110','0010','1100'],'(iii)'),(420,225,['1011','0100','0010','1101'],'(iv)')]:grid(x,y,rows);s.text(x+70,y+160,label)
s.save(9)

