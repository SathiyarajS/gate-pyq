from pathlib import Path
import html
O=Path(__file__).resolve().parents[1]
def start(title,box):return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img"><title>{title}</title><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="none" stroke="currentColor"/></marker></defs><g fill="none" stroke="currentColor" stroke-width="1.6">']
def text(x,y,t,size=16):return f'<text x="{x}" y="{y}" fill="currentColor" stroke="none" font-size="{size}" font-family="Arial" text-anchor="middle">{html.escape(t)}</text>'
def path(d):return f'<path d="{d}" marker-end="url(#arrow)"/>'
a=start('Five-state DFA with accepting initial state 1','0 -8 360 328')
for d in ['M20 160 L47 144','M80 126 L133 86','M140 98 L88 139','M181 74 L254 55','M255 68 L183 87','M268 34 C165 -10 25 30 56 125','M88 165 L139 208','M133 221 L79 179','M184 224 L254 245','M253 259 L181 238','M268 272 C180 325 85 250 58 177']:a.append(path(d))
for x,y,t in [(102,98,'0'),(125,134,'1'),(214,56,'0'),(221,91,'1'),(125,6,'0'),(99,211,'0'),(119,176,'1'),(220,225,'1'),(213,265,'0'),(130,285,'1')]:a.append(text(x,y,t))
for x,y,n in [(70,150,1),(160,80,2),(280,55,3),(160,225,4),(280,255,5)]:
 a.append(f'<circle cx="{x}" cy="{y}" r="24"/>');a.append(text(x,y+6,str(n)))
a.append('<circle cx="70" cy="150" r="28"/>');a.append('</g></svg>');(O/'CS-2024-S1-Q50-1.svg').write_text(''.join(a))
a=start('Three multiplexers M1, M2 and M3 with labelled inputs, outputs and select lines','0 0 340 390')
for x,y,label in [(80,15,'M1'),(80,220,'M2'),(225,120,'M3')]:
 a.append(f'<rect x="{x}" y="{y}" width="65" height="120"/>');a.append(text(x+33,y+89,label));a.append(text(x+7,y+40,'0',14));a.append(text(x+7,y+88,'1',14))
for d in ['M55 51 L80 51','M55 99 L80 99','M55 256 L80 256','M55 304 L80 304','M145 75 H180 V156 H225','M145 280 H185 V204 H225','M290 180 H322','M113 162 V135','M113 367 V340','M258 267 V240']:a.append(path(d))
for x,y,t in [(42,56,'X1'),(42,104,'X2'),(42,261,'X3'),(42,309,'X4'),(134,73,'Q1'),(134,278,'Q2'),(329,185,'Y'),(113,130,'S1'),(113,335,'S2'),(258,235,'S3'),(113,180,'A'),(113,385,'B'),(258,285,'C')]:a.append(text(x,y,t,14))
a.append('</g></svg>');(O/'CS-2024-S1-Q64-1.svg').write_text(''.join(a))
