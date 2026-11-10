from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent
class SVG:
 def __init__(self,title,w,h):self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title, quote=True)}"><title id="title">{escape(title)}</title><g stroke="currentColor" fill="none" stroke-width="1">']
 def line(self,x1,y1,x2,y2,dash=False):self.a.append(f'<path d="M{x1},{y1} L{x2},{y2}"'+(' stroke-dasharray="3 3"' if dash else '')+'/>')
 def text(self,x,y,t):self.a.append(f'<text x="{x}" y="{y}" fill="currentColor" stroke="none" font-family="serif" font-size="16" text-anchor="middle">{escape(t)}</text>')
 def cell(self,x,y,s,fill):self.a.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="'+('currentColor' if fill else 'none')+'"/>')
 def mask(self,x,y,rows,s):
  # Unit-cell paths merge visually without exposing artificial grid edges.
  for r,row in enumerate(rows):
   for c,v in enumerate(row):
    if v=='1':self.a.append(f'<path stroke="none" fill="currentColor" d="M{x+c*s},{y+r*s}h{s}v{s}h-{s}Z"/>')
 def tile(self,x,y,bits,s=55):
  self.cell(x,y,s,False)
  for i,b in enumerate(bits):self.a.append(f'<circle cx="{x+12+(i%3)*15}" cy="{y+12+(i//3)*15}" r="3.6" fill="'+('currentColor' if b=='1' else 'none')+'"/>')
 def save(self,n): (OUT/f'CS-2026-S2-Q{n}-1.svg').write_text(''.join(self.a)+'</g></svg>\n')
s=SVG('Panel I: three by three dot tiles with two missing. Panel II: candidate tile pairs (i)–(iv).',540,390)
s.text(100,25,'Panel I');s.text(395,25,'Panel II');s.line(230,10,230,380);s.line(390,45,390,370,True);s.line(245,210,530,210,True)
for r,row in enumerate([['011111111','000000001','011011011'],['001001001','001011011',None],['001001011','111111111',None]]):
 for c,bits in enumerate(row):
  if bits:s.tile(20+c*55,140+r*55,bits)
s.a.append('<rect x="130" y="195" width="55" height="110" stroke-dasharray="4 3"/>');s.text(157.5,255,'?')
for x,y,top,bot,label in [(275,65,'011011111','000001001','(i)'),(435,65,'011011011','000001001','(ii)'),(275,240,'011011111','001001001','(iii)'),(435,240,'011011011','001001011','(iv)')]:
 s.tile(x,y,top);s.tile(x,y+55,bot);s.text(x+27.5,y+135,label)
s.save(7)
