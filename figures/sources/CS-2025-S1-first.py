from pathlib import Path
from html import escape
O=Path(__file__).resolve().parents[1]
def txt(x,y,t,size=16,extra=''):return f'<text x="{x}" y="{y}" font-size="{size}" fill="currentColor" stroke="none" {extra}>{escape(t)}</text>'
def path(d,extra=''):return f'<path d="{d}" fill="none" stroke="currentColor" {extra}/>'
def rect(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor"/>'
def poly(points,fill='none'):return f'<path d="M {points.replace(chr(32),chr(32)+"L " )} Z" fill="{fill}" stroke="currentColor"/>'
def save(n,w,h,b,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{title}</title><g stroke-width="1.3" font-family="serif">{b}</g></svg>'
 (O/f'CS-2025-S1-Q{n}-1.svg').write_text(s)
# Map, exactly the source labels and relative positions.
b=path('M 180 10 V 170 H 20 M 210 10 V 170 H 370 M 20 195 H 180 V 350 M 370 195 H 210 V 350')
for x,y,w,h,label in [(55,55,105,44,'Library'),(225,55,100,44,'Canteen'),(55,108,105,44,'Physics Lab'),(225,108,100,44,'Hospital'),(55,215,105,44,'Hostels'),(55,265,105,44,'Classrooms')]:b+=rect(x,y,w,h)+txt(x+w/2,y+25,label,16,'text-anchor="middle"')
b+=rect(225,210,100,54)+txt(275,230,'Chemistry',16,'text-anchor="middle"')+txt(275,250,'Lab',16,'text-anchor="middle"')+txt(110,188,'5th Cross Road',16,'text-anchor="middle"')+txt(202,150,'1st Main Road',16,'transform="rotate(-90 202 150)"')
b+='<g transform="translate(25 25)">'+path('M 330 275 V 335 M 300 305 H 360')+poly('330,275 327,282 333,282','currentColor')+poly('330,335 327,328 333,328','currentColor')+poly('300,305 307,302 307,308','currentColor')+poly('360,305 353,302 353,308','currentColor')
for x,y,t in [(330,268,'N'),(330,352,'S'),(288,311,'W'),(371,311,'E')]:b+=txt(x,y,t,16,'text-anchor="middle"')
b+='</g>'
save(5,425,395,b,'Campus map with compass directions')
b=poly('45,205 180,25 235,205')+path('M 112.5 115 H 207.5')
for x,y,t in [(180,20,'P'),(28,222,'Q'),(239,222,'R'),(95,118,'S'),(216,119,'T')]:b+=txt(x,y,t)
save(7,280,240,b,'Triangle PQR with S on PQ and T on PR, and ST parallel to QR')
# B+ tree keeps the unsorted 1,4,3 source leaf.
def node(x,y,vals):
 b=rect(x,y,126,28)
 for z in [6,40,46,80,86,120]:b+=path(f'M {x+z} {y} V {y+28}')
 for i,v in enumerate(vals):b+=txt(x+23+40*i,y+20,str(v),18,'text-anchor="middle"')
 return b
b=node(230,15,[6,12,19]);
for x,vals,rootx in [(10,[1,4,3],233),(155,[7,9,10],273),(300,[13,15,17],313),(445,[20,21,22],353)]:b+=path(f'M {rootx} 43 L {x+3} 115')+node(x,115,vals)
b+=txt(10,169,'[sic: first leaf is printed 1, 4, 3]',14)
save(21,585,180,b,'B+ tree with root 6, 12, 19 and four leaves; source unsorted first leaf retained')
# Folding diagrams and all four option patterns.
b=''
for x,label in [(10,'(I)'),(125,'(II)')]:b+=rect(x,10,90,90)+txt(x+45,122,label,18,'text-anchor="middle"')
b+=''.join(path(f'M {125+i} {10+i} L {125+i+2} {10+i+2}') for i in range(0,90,5))
b+=poly('240,10 330,10 330,100')+txt(285,122,'(III)',18,'text-anchor="middle"')+''.join(path(f'M {330-i} {10+i} L {328-i} {12+i}') for i in range(0,45,5))
b+=poly('355,10 445,10 400,55')+txt(400,122,'(IV)',18,'text-anchor="middle"')
b+=path('M 165 63 C 150 43 174 40 175 48')+poly('175,48 169,43 177,42','currentColor')
b+=path('M 295 37 C 302 24 318 34 307 46')+poly('307,46 308,38 314,43','currentColor')
b+=poly('396,18 404,18 400,10','currentColor')+poly('371,27 382,27 382,38','currentColor')+poly('410,27 421,27 421,32 410,32','currentColor')
def square(x,y):return f'<rect x="{x}" y="{y}" width="9" height="9" fill="currentColor" stroke="none"/>'
def diamond(x,y):return poly(f'{x+4.5},{y-2} {x+11},{y+4.5} {x+4.5},{y+11} {x-2},{y+4.5}','currentColor')
for i,k in enumerate('ABCD'):
 x=55+i*110;y=155;b+=txt(x+45,285,f'({k})',18,'text-anchor="middle"')+rect(x,y,100,100)
 # triangles at outer edges: A/B/D point outward, C reverses vertical orientation.
 top=f'{x+46},{y+8} {x+54},{y+8} {x+50},{y}' if k!='C' else f'{x+46},{y} {x+54},{y} {x+50},{y+8}'
 bot=f'{x+46},{y+92} {x+54},{y+92} {x+50},{y+100}' if k!='C' else f'{x+46},{y+100} {x+54},{y+100} {x+50},{y+92}'
 b+=poly(top,'currentColor')+poly(bot,'currentColor')+poly(f'{x},{y+50} {x+8},{y+46} {x+8},{y+54}','currentColor')+poly(f'{x+100},{y+50} {x+92},{y+46} {x+92},{y+54}','currentColor')
 b+=poly(f'{x+78},{y+11} {x+88},{y+11} {x+88},{y+22} {x+84},{y+22} {x+84},{y+15} {x+78},{y+15}','currentColor')
 b+=poly(f'{x+12},{y+78} {x+16},{y+78} {x+16},{y+85} {x+23},{y+85} {x+23},{y+89} {x+12},{y+89}','currentColor')
 if k=='D':b+=square(x+44,y+46)
 else:
  f=diamond if k=='B' else square;b+=f(x+12,y+11)+f(x+79,y+80)
save(9,505,300,b,'Paper folding stages I to IV and answer patterns A to D')
# Partial datapath; real labels and independent immediate mux inputs.
def arrow(d,x,y,orient='down'):
 b=path(d)
 if orient=='down':b+=poly(f'{x},{y} {x-3},{y-6} {x+3},{y-6}','currentColor')
 if orient=='right':b+=poly(f'{x},{y} {x-6},{y-3} {x-6},{y+3}','currentColor')
 if orient=='left':b+=poly(f'{x},{y} {x+6},{y-3} {x+6},{y+3}','currentColor')
 return b
b=rect(175,10,80,44)+txt(215,37,'RA (32 bit)',14,'text-anchor="middle"')+rect(310,10,80,44)+txt(350,37,'RB (32 bit)',14,'text-anchor="middle"')
b+=poly('155,105 265,105 245,140 175,140')+poly('310,105 420,105 400,140 330,140')+txt(210,128,'Mux_A',16,'text-anchor="middle"')+txt(365,128,'Mux_B',16,'text-anchor="middle"')
b+=arrow('M 212 54 V 105',212,105)+arrow('M 350 54 V 105',350,105)
b+=txt(88,60,'immediate value',14,'text-anchor="middle"')+txt(88,78,'32 bit',14,'text-anchor="middle"')+arrow('M 65 84 H 175 V 105',175,105)
b+=txt(470,60,'immediate value',14,'text-anchor="middle"')+txt(470,78,'32 bit',14,'text-anchor="middle"')+arrow('M 495 84 H 390 V 105',390,105)
b+=arrow('M 85 123 H 165',165,123,'right')+txt(20,145,'Select RA/immediate',14)+arrow('M 495 123 H 410',410,123,'left')+txt(405,145,'Select RB/immediate',14)
b+=arrow('M 210 140 V 205',210,205)+arrow('M 365 140 V 205',365,205)
b+=poly('165,205 270,205 281,222 291,205 390,205 345,255 210,255')+txt(284,249,'ALU',16,'text-anchor="middle"')
b+=arrow('M 280 255 V 288',280,288)+rect(240,288,80,44)+txt(280,315,'RZ (32 bit)',14,'text-anchor="middle"')
b+=arrow('M 117 226 H 184',184,226,'right')+arrow('M 117 240 H 197',197,240,'right')+txt(108,237,'⋮',18)+path('M 108 216 C 100 216 100 218 100 225 V 228 Q 100 233 95 233 Q 100 233 100 239 V 244 C 100 251 100 251 108 251')+txt(9,238,'ALU control',14)
for x,y in [(212,75),(350,75),(120,84),(420,84),(210,175),(365,175),(280,273)]:b+=path(f'M {x-9} {y+5} L {x+9} {y-5}')
save(27,560,345,b,'Processor datapath with independent register or immediate selection at Mux_A and Mux_B')
