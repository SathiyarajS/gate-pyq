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
s=subprocess.check_output(['neato','-n2','-Tsvg',str(dot)]).decode();s=s[s.index('<svg'):];s=re.sub(r'width="[^"]*" height="[^"]*"','',s,count=1);s=s.replace('stroke="black"','stroke="currentColor"').replace('fill="black"','fill="currentColor"');s=s.replace('<svg ', '<svg role="img" aria-labelledby="title" ',1);s=s.replace('<!-- Generated','<title id="title">Intercity highways: (i) four by four grid; (ii) five-city graph.</title>\n<!-- Generated',1)
# Graphviz plain text defaults lack fill attribute; set explicitly.
s=s.replace('<text ','<text fill="currentColor" ')
if '<title id="title">' not in s:s=s.replace('<!-- Title:', '<title id="title">Intercity highways: (i) four by four grid; (ii) five-city graph.</title>\n<!-- Title:',1)
(p.parent/'CS-2026-S2-Q8-1.svg').write_text(s)
