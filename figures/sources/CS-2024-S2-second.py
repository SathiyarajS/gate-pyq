from pathlib import Path
import subprocess,xml.etree.ElementTree as E,html
D=Path(__file__).resolve().parent; F=D.parent
def graph(n,dot,title):
 p=F/f'CS-2024-S2-Q{n}-1';d=D/f'CS-2024-S2-Q{n}-1.dot';d.write_text(dot)
 raw=subprocess.check_output(['neato','-n2','-Tsvg',str(d)]).decode(); root=E.fromstring(raw)
 for node in root.iter():
  node.tag=node.tag.split('}')[-1]
  for a in list(node.attrib):
   if a in ('class','version'):del node.attrib[a]
   if a in ('fill','stroke') and node.attrib[a]!='none':node.attrib[a]='currentColor'
 root.attrib.pop('width',None);root.attrib.pop('height',None)
 # remove generated background polygon, preserve graph edges and vertices
 g=root.find('g')
 for node in list(g):
  if node.tag=='polygon':g.remove(node)
 # Graphviz numerical node identifiers may start with digits; strip unused ids.
 for node in root.iter():node.attrib.pop('id',None)
 # Drop Graphviz per-node/edge <title>s (internal names would surface as tooltips); keep one root title.
 for parent in list(root.iter()):
  for child in list(parent):
   if child.tag=='title':parent.remove(child)
 root.insert(0,E.Element('title'));root[0].text=title
 root.set('xmlns','http://www.w3.org/2000/svg');p.with_suffix('.svg').write_text(E.tostring(root,encoding='unicode'))
import math
def seg(P,u,v,arrow=False,r=17.28):
 # Straight edge spline between two pinned circles; neato -n2 honours lp only for edges with pos.
 (x1,y1),(x2,y2)=P[u],P[v]; L=math.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/L,(y2-y1)/L
 s=(x1+ux*r,y1+uy*r); e=(x2-ux*r,y2-uy*r); tip=''
 if arrow: tip='e,%.2f,%.2f '%e; e=(e[0]-ux*10,e[1]-uy*10)
 pts=[s,(s[0]+(e[0]-s[0])/3,s[1]+(e[1]-s[1])/3),(s[0]+2*(e[0]-s[0])/3,s[1]+2*(e[1]-s[1])/3),e]
 return 'pos="'+tip+' '.join('%.2f,%.2f'%q for q in pts)+'"'
base='graph [splines=true, overlap=true]; node [fontname="serif", fontsize=20, fixedsize=true, width=0.48, height=0.48]; edge [fontname="serif", fontsize=18];'
P41={'1':(0,70),'2':(65,125),'3':(170,125),'4':(65,0),'5':(170,0)}
graph(41,'''digraph M {'''+base+'''
start [label="", shape=none, width=0, height=0, pos="-40,45!"];
1 [pos="0,70!", shape=circle]; 2 [pos="65,125!",shape=doublecircle]; 3 [pos="170,125!",shape=circle];4 [pos="65,0!",shape=circle];5 [pos="170,0!",shape=doublecircle];
start -> 1; 1 -> 2 [label="ϵ", lp="20,108", '''+seg(P41,'1','2',True)+'''];  1 -> 4 [label="ϵ", lp="20,28", '''+seg(P41,'1','4',True)+'''];
2 -> 3 [label="0"];3 -> 2 [label="0"];3 -> 5 [label="ϵ", lp="184,62", '''+seg(P41,'3','5',True)+'''];4 -> 5 [label="1"];5 -> 4 [label="1"];
}''','Five-state NFA')
P59={'a':(0,70),'b':(110,140),'c':(330,140),'d':(440,70),'e':(330,0),'f':(110,0),'g':(220,70)}
graph(59,'''graph G {'''+base+'''
node [shape=circle];
a [pos="0,70!"]; b [pos="110,140!"];c [pos="330,140!"];d [pos="440,70!"];e [pos="330,0!"];f [pos="110,0!"];g [pos="220,70!"];
a -- b [label="1", lp="44,116", '''+seg(P59,'a','b')+'''];a -- f [label="1", lp="44,22", '''+seg(P59,'a','f')+'''];b -- c [label="3", lp="220,152", '''+seg(P59,'b','c')+'''];c -- d [label="1", lp="396,116", '''+seg(P59,'c','d')+'''];d -- e [label="1", lp="396,22", '''+seg(P59,'d','e')+'''];e -- f [label="3", lp="220,-14", '''+seg(P59,'e','f')+'''];
a -- g [label="2", lp="110,80", '''+seg(P59,'a','g')+'''];b -- g [label="2", lp="177,117", '''+seg(P59,'b','g')+'''];c -- g [label="2", lp="263,117", '''+seg(P59,'c','g')+'''];d -- g [label="2", lp="330,80", '''+seg(P59,'d','g')+'''];e -- g [label="2", lp="287,46", '''+seg(P59,'e','g')+'''];f -- g [label="2", lp="153,46", '''+seg(P59,'f','g')+'''];
}''','Weighted undirected graph')
graph(60,'''graph G {graph [splines=line, overlap=true];node [shape=circle, label="", width=0.13, height=0.13, fixedsize=true,style=filled];
a [pos="90,220!"];b [pos="210,220!"];c [pos="0,155!"];d [pos="300,155!"];e [pos="0,60!"];f [pos="300,60!"];g [pos="90,0!"];h [pos="210,0!"];
a--b;b--d;d--f;f--h;h--g;g--e;e--c;c--a;
a--g;b--h;c--d;e--f;a--f;b--e;c--h;d--g;
}''','Unlabelled graph with eight marked vertices')
def svg(n,w,h,title,content):
 (F/f'CS-2024-S2-Q{n}-1.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke="currentColor" stroke-width="1.4"><title>{title}</title>{content}</svg>')
def text(x,y,t,size=18,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="serif" font-size="{size}" text-anchor="{anchor}" fill="currentColor" stroke="none">{html.escape(t)}</text>'
def line(x1,y1,x2,y2):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
s=''
for y in range(10,111,25):s+=line(10,y,130,y)
s+=line(10,10,10,110)+line(130,10,130,110)
for y,t in zip([29,54,79,104],['400 (Top)','300','200','100']):s+=text(20,y,t)
s+=text(20,134,'Stack S1')
for y in [20,45,70]:s+=line(210,y,330,y)
s+=line(210,20,210,70)+line(330,20,330,70)+text(220,94,'Stack S2')
svg(48,350,145,'Initial stacks S1 and S2',s)
# Hand-authored editable gate geometry. Arrowheads present on input wires as in source.
s='<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 L3 5 Z" fill="currentColor" stroke="none"/></marker></defs>'
def arrow(points):return f'<polyline points="{points}" fill="none" marker-end="url(#arrow)"/>'
s+='<path d="M90 15 L130 15 A35 35 0 0 1 130 85 L90 85 Z"/>'
s+=text(124,56,'AND',18,'middle')
s+='<path d="M90 160 Q137 160 165 195 Q137 230 90 230 Q112 195 90 160 Z"/>'
s+=text(123,201,'OR',18,'middle')
s+='<path d="M305 90 Q352 90 380 125 Q352 160 305 160 Q327 125 305 90 Z"/><path d="M297 90 Q319 125 297 160"/>'
s+=text(342,131,'XOR',18,'middle')
for y,t in [(32,'f1'),(65,'f2'),(179,'f3'),(211,'f4')]:s+=text(16,y-5,t)+arrow(f'15,{y} 97,{y}' if y>100 else f'15,{y} 90,{y}')
s+=arrow('165,50 245,50 245,108 307,108')+arrow('165,195 245,195 245,142 307,142')
s+=line(380,125,398,125)+text(382,117,'Y')
svg(50,415,245,'AND and OR outputs feeding XOR',s)
# Format labels remain actual text. Widths mirror source approximately.
s=text(8,23,'R-type Instruction Format:')
xs=[8,98,188,328,468,608]
for a,b,t in zip(xs,xs[1:],['OPCODE','UNUSED','DST Register','SRC Register1','SRC Register 2']):
 s+=f'<rect x="{a}" y="37" width="{b-a}" height="40"/>'+text(a+8,63,t,16)
s+=text(8,108,'I-type Instruction Format:')
xs=[8,98,218,338,608]
for a,b,t in zip(xs,xs[1:],['OPCODE','DST Register','SRC Register','# Immediate value/address']):
 s+=f'<rect x="{a}" y="122" width="{b-a}" height="40"/>'+text(a+8,148,t,16)
svg(61,620,175,'R-type and I-type instruction formats',s)
