from pathlib import Path
import fitz
p=Path(__file__).resolve().parents[1];p.mkdir(exist_ok=True)
def save(n,w,h,body,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{title}</title><g stroke="currentColor" fill="none" stroke-width="1.5">{body}</g></svg>'
 (p/f'CS-2025-S2-Q{n}-1.svg').write_text(s)
 doc=fitz.open(stream=s.encode(),filetype='svg'); pdf=fitz.open(stream=doc.convert_to_pdf(),filetype='pdf'); pdf[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(p/f'CS-2025-S2-Q{n}-1.png'))
def text(x,y,s):return f'<text x="{x}" y="{y}" font-size="18" font-family="serif" fill="currentColor" stroke="none">{s}</text>'
def path(d):return f'<path d="{d}"/>'
def circ(x,y,r,fill='none'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
# net and option cubes, geometry follows source page 4.
s=''
for x,y in [(110,10),(60,60),(110,60),(160,60),(210,60),(110,110)]:s+=f'<rect x="{x}" y="{y}" width="50" height="50"/>'
s+=circ(135,35,5,'currentColor')+circ(135,135,5)+path('M131 89 L135 81 L139 89 Z')+'<path d="M231 89 L235 81 L239 89 Z" fill="currentColor"/>'
for j,label in enumerate('ABCD'):
 x=35+j*85;y=215
 s+=text(x,y+85,f'({label})')+path(f'M{x} {y} h50 v50 h-50 Z M{x} {y} l24 -16 h50 l-24 16 M{x+50} {y} l24 -16 v50 l-24 16')+path(f'M{x+21} {y+29} l4 -8 l4 8 Z')
 if label=='A':s+=f'<ellipse cx="{x+36}" cy="{y-8}" rx="7" ry="3" fill="currentColor"/>'
 if label=='B':s+=f'<path d="M{x+59} {y+26} l5 -12 l2 8 Z" fill="currentColor"/>'
 if label=='D':s+=f'<path d="M{x+28} {y-5} l8 -6 l5 6 Z" fill="currentColor"/><ellipse cx="{x+63}" cy="{y+20}" rx="2.5" ry="5" fill="currentColor"/>'
save(4,380,315,s,'Cube net and options (A), (B), (C), (D)')
s=path('M50 60 H150 V160 H50 Z M50 60 L130 20 L180 120 L100 160 Z')
for x,y,t in [(37,62,'P'),(35,173,'Q'),(155,172,'R'),(155,61,'S'),(101,178,'L'),(185,126,'M'),(133,19,'N')]:s+=text(x,y,t)
save(9,220,195,s,'Square PQRS and rectangle PLMN')
s='<rect x="10" y="10" width="360" height="220" stroke-width="0.5"/>'
s+='<g stroke-width="9"><path d="M10 130 C55 122 85 130 130 100 C175 100 186 97 205 112 C225 124 245 119 285 120 C321 106 342 72 370 62 M130 100 C145 72 128 65 163 42 L211 10 M224 121 C195 136 185 159 166 180 L125 230 M285 120 C315 139 347 165 370 174"/></g>'
for x,y,t in [(47,115,'P'),(168,123,'Q'),(176,61,'R'),(178,190,'S'),(252,108,'T'),(322,184,'U'),(332,62,'V'),(88,168,'Z1'),(60,52,'Z2'),(252,48,'Z3'),(343,122,'Z4'),(249,185,'Z5')]:s+=text(x,y,t)
save(10,380,240,s,'River segments P through V separate zones Z1 through Z5')
# Gates: NAND, inverter, AND into three-input OR; branches are source exact.
s=path('M20 40 H205 M20 65 H205 M60 40 V215 H100 M165 65 V190 H205 M165 125 H205 M261 52 H292 V112 H335 M258 125 H337 M255 203 H292 V138 H336 M153 215 H205 M383 125 H405')
s+=path('M205 28 H230 C263 28 263 77 230 77 H205 Z')+circ(258,52,3)
s+=path('M205 100 L252 125 L205 150 Z')+circ(255,125,3)
s+=path('M100 192 L147 215 L100 238 Z')+circ(150,215,3)
s+=path('M205 178 H230 C263 178 263 228 230 228 H205 Z')
s+=path('M330 100 Q345 125 330 150 H350 Q373 150 388 125 Q373 100 350 100 Z')
for x,y in [(60,40),(165,65),(165,125)]:s+=circ(x,y,3,'currentColor')
s+=text(34,33,'Y')+text(34,85,'X')+text(393,112,'F')
save(31,430,255,s,'Logic circuit with inputs Y and X and output F')
