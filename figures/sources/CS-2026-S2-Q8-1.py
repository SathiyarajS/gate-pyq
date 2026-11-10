from pathlib import Path
import subprocess,re
p=Path(__file__).parent
lines=['graph G {','graph [layout=neato, overlap=true, splines=line, outputorder=edgesfirst, bgcolor="transparent", margin=0];','node [shape=point, width=0.09, label=""];','edge [penwidth=1.1];']
for r in range(4):
 for c in range(4):
  lines.append(f'n{r}{c} [pos="{c*55},{165-r*55}!"];')
  if r:lines.append(f'n{r-1}{c} -- n{r}{c};')
  if c:lines.append(f'n{r}{c-1} -- n{r}{c};')
for name,x,y in [('a',260,170),('b',405,169),('c',338,136),('d',318,26),('e',238,68)]:lines.append(f'{name} [pos="{x},{y}!"];')
lines+=['a -- b;','b -- d;','d -- c;','c -- a;','a -- e;','e -- d;','label1 [shape=plaintext, pos="12,190!", label="(i)", fontsize=16];','label2 [shape=plaintext, pos="228,190!", label="(ii)", fontsize=16];','}']
dot=p/'CS-2026-S2-Q8-1.dot';dot.write_text('\n'.join(lines)+'\n')
s=subprocess.check_output(['neato','-n2','-Tsvg',str(dot)]).decode()
import xml.etree.ElementTree as ET
root=ET.fromstring(s[s.index('<svg'):])
# Drop Graphviz per-node/edge <title> tooltips; the figure keeps one accessible title.
for g in root.iter():
 for t in [c for c in g if c.tag.endswith('}title') or c.tag=='title']:g.remove(t)
for k in ('width','height'):root.attrib.pop(k,None)
for node in root.iter():
 node.tag=node.tag.removeprefix('{http://www.w3.org/2000/svg}')
 node.attrib.pop('class',None)
 for key in ('stroke','fill'):
  if node.get(key)=='black':node.set(key,'currentColor')
  if node.get(key)=='transparent':node.set(key,'none')
 if node.tag=='text':node.set('fill','currentColor')
title='Intercity highways: (i) four-by-four grid and (ii) five-city network.'
root.set('xmlns','http://www.w3.org/2000/svg');root.set('role','img');root.set('aria-label',title)
label=ET.Element('title',{'id':'title'});label.text=title;root.insert(0,label)
(p.parent/'CS-2026-S2-Q8-1.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')
