from pathlib import Path
import subprocess,re,xml.etree.ElementTree as E
root=Path(__file__).parent
for n,title,desc in [
 (45,'Control flow graph','ENTRY leads to B1: a = b + c. B1 branches to B2: d = a + e, and B3: e = a + f. B3 loops back to B1. B2 leads to B4: g = d + e; B4 leads to EXIT.'),
 (47,'Finite automata D1 and D2','Both automata have unlabeled states; only the start state is accepting. For accessible reference, call the D1 states s (start), u (upper middle), w (upper right), z (top right), v (lower middle), t (bottom left). Transitions: s to u on 0; s to v on 1; u to w on 0; u to z on 1; w to s on 0 and 1; z to s on 0; v to t on 0; t to s on 1. For D2, call the states s (start), u (upper middle), w (upper right), v (lower middle), t (bottom left). Transitions: s to u on 0; s to v on 1; u to w on 1; w to s on 1; v to w on 1; v to t on 0 and 1; t to s on 0. These reference names are not labels in the original drawing.')]:
 name=f'CS-2026-S2-Q{n}-1'
 svg=subprocess.check_output(['neato','-n2','-Tsvg',str(root/(name+'.dot'))],text=True)
 svg=re.sub(r'<\?xml.*?\?>','',svg,flags=re.S);svg=re.sub(r'<!DOCTYPE.*?>','',svg,flags=re.S)
 svg=re.sub(r'<svg width="[^"]+" height="[^"]+"', '<svg role="img" aria-labelledby="title desc"',svg)
 svg=svg.replace('stroke="black"','stroke="currentColor"').replace('fill="black"','fill="currentColor"')
 svg=svg.replace('<g id="graph0"',f'<title id="title">{title}</title><desc id="desc">{desc}</desc><g fill="currentColor" id="graph0"')
 # Keep all SVG text at least 12px; graph labels are 16 or 18px.
 svg=re.sub(r'font-size="([0-9.]+)"',lambda m:f'font-size="{max(12,float(m[1])):g}"',svg)
 svg=re.sub(r'<!--.*?-->','',svg,flags=re.S)
 svg=re.sub(r' class="[^"]*"','',svg)
 svg=svg.replace('aria-labelledby="title desc"',f'aria-label="{title}"')
 # Explicit coordinate shift is more portable than baseline-shift on SVG text.
 tree=E.fromstring(svg)
 for node in tree.iter():
  if node.attrib.pop('baseline-shift',None)=='sub':
   node.set('y',str(float(node.get('y'))+5));node.set('font-size','12')
 E.register_namespace('','http://www.w3.org/2000/svg')
 svg=E.tostring(tree,encoding='unicode')
 (root.parent/(name+'.svg')).write_text(svg)
