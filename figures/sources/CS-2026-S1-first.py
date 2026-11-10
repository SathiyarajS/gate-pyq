from pathlib import Path
from html import escape
O=Path(__file__).resolve().parents[1]
def svg(w,h,title,body):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="currentColor" font-family="serif" font-size="24"><title>{title}</title>{body}</svg>\n'
def text(x,y,s,size=24):return f'<text x="{x}" y="{y}" font-size="{size}">{escape(s)}</text>'
def path(d,fill='none',opacity=1):return f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}" stroke="currentColor" stroke-width="1.3"/>'
def grid(x,y,r,c):return ''.join(f'<rect x="{x+j*20}" y="{y+i*20}" width="18" height="18" fill="currentColor"/>' for i in range(r) for j in range(c))
b=grid(120,50,2,2)+grid(240,10,4,1)
for lab,y,r,c in [('A',120,2,4),('B',190,3,4),('C',280,3,5),('D',370,4,5)]:b+=text(15,y+24,f'({lab})')+grid(85,y,r,c)
(O/'CS-2026-S1-Q2-1.svg').write_text(svg(320,460,'Two permitted four-tile patterns: a 2-by-2 square and a vertical column of four square tiles. Options A–D are rectangular tile grids described below.',b))
b=''
for n in range(0,13,2):
 y=220-n*15;b+=f'<line x1="60" y1="{y}" x2="330" y2="{y}" stroke="currentColor" stroke-opacity="0.35"/>'+text(25,y+6,str(n),18)
for n in [0,10,20,30]:
 x=60+n*9;b+=f'<line x1="{x}" y1="40" x2="{x}" y2="220" stroke="currentColor" stroke-opacity="0.35"/>'+text(x-8,246,str(n),18)
b+=path('M60 220 H150 L240 70 H330')+text(190,277,'S',20)+'<text x="17" y="150" font-size="20" transform="rotate(-90 17 150)">N(S)</text>'
(O/'CS-2026-S1-Q8-1.svg').write_text(svg(360,290,'Plot of N(S) versus S',b))
# Orthographic paths and each visible perspective face are traced from the source crop.
# Coordinates below are local 2D face vertices, not an inferred 3D model.
b=text(20,30,'Panel I',25)+text(300,30,'Panel II',25)
b+=path('M165 40 V450')+''.join(path(f'M{x} 245 h2') for x in range(185,615,5))+''.join(path(f'M400 {y} v2') for y in range(55,450,5))
b+=path('M25 95 H50 V120 H100 V170 H25 Z','currentColor',.3)+path('M25 120 H50 V145 H100 M75 145 V170')
b+=text(35,195,'Front',24)+text(35,220,'View',24)
b+=path('M25 255 H100 V305 H75 V330 H25 Z','currentColor',.3)+path('M50 255 V330 M25 305 H50 M50 280 H100')
b+=text(35,357,'Top',24)+text(35,382,'View',24)
# source coordinates for visible surfaces, in units based on source crop pixel geometry
faces={
'i':[
('M0 80 H40 V120 H120 V160 H0 Z',.4),('M14 27 H54 V67 H14 Z',.4),('M67 53 H147 V93 H67 Z',.4),
('M0 80 L14 67 H54 L40 80 Z',.2),('M14 27 L40 0 H80 L54 27 Z',.2),('M67 53 L80 40 H160 L147 53 Z',.2),('M40 120 L67 93 H147 L120 120 Z',.2),
('M54 27 L80 0 V40 L67 53 V93 L40 120 V80 L54 67 Z',.6),('M120 120 L147 93 V53 L160 40 V120 L120 160 Z',.6)],
'ii':[
('M0 80 H40 V120 H80 V160 H0 Z',.4),('M14 27 H54 V67 H14 Z',.4),('M54 67 H94 V107 H54 Z',.4),('M107 53 H147 V93 H107 Z',.4),('M94 107 H134 V147 H94 Z',.4),
('M14 27 L40 0 H80 L54 27 Z',.2),('M0 80 L14 67 H54 L40 80 Z',.2),('M54 67 L80 40 H160 L147 53 H107 L94 67 Z',.2),('M40 120 L54 107 H94 L80 120 Z',.2),('M94 107 L107 93 H147 L134 107 Z',.2),
('M54 27 L80 0 V40 L54 67 Z',.6),('M40 80 L54 67 V107 L40 120 Z',.6),('M94 67 L107 53 V93 L94 107 Z',.6),('M134 107 L147 93 V53 L160 40 V120 L134 147 Z',.6),('M80 120 L94 107 V147 L80 160 Z',.6)],
'iii':[
('M0 80 H40 V120 H80 V160 H0 Z',.4),('M14 27 H54 V67 H14 Z',.4),('M67 14 H107 V54 H147 V94 H67 Z',.4),('M94 107 H134 V147 H94 Z',.4),
('M14 27 L40 0 H120 L107 14 H67 L54 27 Z',.2),('M0 80 L14 67 H54 L40 80 Z',.2),('M107 54 L120 40 H160 L147 54 Z',.2),('M40 120 L67 94 H147 L134 107 H94 L80 120 Z',.2),
('M54 27 L67 14 V94 L40 120 V80 L54 67 Z',.6),('M107 14 L120 0 V40 L107 54 Z',.6),('M134 107 L147 94 V54 L160 40 V120 L134 147 Z',.6),('M80 120 L94 107 V147 L80 160 Z',.6)],
'iv':[
('M0 80 H40 V120 H80 V160 H0 Z',.4),('M14 27 H54 V67 H14 Z',.4),('M67 53 H147 V93 H67 Z',.4),('M94 107 H134 V147 H94 Z',.4),
('M14 27 L40 0 H80 L54 27 Z',.2),('M0 80 L14 67 H54 L40 80 Z',.2),('M67 53 L80 40 H160 L147 53 Z',.2),('M40 120 L67 93 H147 L134 107 H94 L80 120 Z',.2),
('M54 27 L80 0 V40 L67 53 V93 L40 120 V80 L54 67 Z',.6),('M134 107 L147 93 V53 L160 40 V120 L134 147 Z',.6),('M80 120 L94 107 V147 L80 160 Z',.6)]}
for name,x,y in [('i',240,85),('ii',455,85),('iii',240,315),('iv',455,315)]:
 b+=text(x+15,y-34,'Top',24)+text(x+5,y-10,'View',24)
 b+=path(f'M{x+79} {y-37} V{y-5} M{x+75} {y-11} L{x+79} {y-5} L{x+83} {y-11}')
 b+=f'<g transform="translate({x} {y}) scale(0.6)">'+''.join(path(d,'currentColor',o) for d,o in faces[name])+'</g>'
 b+=text(x-45,y+124,'Front',24)+text(x-45,y+148,'View',24)+path(f'M{x-2} {y+123} L{x+24} {y+102} M{x+17} {y+104} L{x+24} {y+102} L{x+22} {y+109}')+text(x+50,y+140,f'({name})',24)
# Preserve dotted Panel II separators as in original.
b=b.replace('d="M185 225 H615"','stroke-dasharray="2 3" d="M185 225 H615"').replace('d="M400 55 V425"','stroke-dasharray="2 3" d="M400 55 V425"')
(O/'CS-2026-S1-Q7-1.svg').write_text(svg(635,475,'Panel I front and top views; Panel II structures (i)–(iv)',b))
