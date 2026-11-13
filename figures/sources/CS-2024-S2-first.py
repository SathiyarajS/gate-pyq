# CS-2024-S2 first-half figure generator.
# Q22 is rendered from its pinned Graphviz DOT source. Q8-1, Q8-2 and Q10-1 are
# hand-authored SVGs in figures/ and are their own editable source.
from pathlib import Path
import subprocess, re, xml.etree.ElementTree as E

root = Path(__file__).resolve().parent
E.register_namespace('', 'http://www.w3.org/2000/svg')

def render(name, title, desc):
    svg = subprocess.check_output(['neato', '-n2', '-Tsvg', str(root / (name + '.dot'))], text=True)
    svg = re.sub(r'<\?xml.*?\?>', '', svg, flags=re.S)
    svg = re.sub(r'<!DOCTYPE.*?>', '', svg, flags=re.S)
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'<svg width="[^"]+" height="[^"]+"', f'<svg role="img" aria-label="{title}"', svg)
    svg = svg.replace('stroke="black"', 'stroke="currentColor"').replace('fill="black"', 'fill="currentColor"')
    svg = svg.replace('<g id="graph0"', f'<title>{title}</title><desc>{desc}</desc><g fill="currentColor" id="graph0"')
    svg = re.sub(r' class="[^"]*"', '', svg)
    svg = re.sub(r'font-size="([0-9.]+)"', lambda m: f'font-size="{max(12, float(m[1])):g}"', svg)
    tree = E.fromstring(svg)
    for node in tree.iter():
        node.attrib.pop('id', None)
        node.attrib.pop('version', None)
    # Drop the transparent background polygon Graphviz emits first in the graph group.
    g = tree.find('{http://www.w3.org/2000/svg}g')
    # Graphviz adds a <title> per node/edge ("left", "left->right"); those names are not
    # source labels and would surface as tooltips, so keep only the root title.
    for parent in g.iter():
        for child in list(parent):
            if child.tag.endswith('title'):
                parent.remove(child)
    for child in list(g):
        if child.tag.endswith('polygon') and child.get('fill') in ('transparent', 'none') and child.get('stroke') in ('transparent', None):
            g.remove(child)
    (root.parent / (name + '.svg')).write_text(E.tostring(tree, encoding='unicode'))

render('CS-2024-S2-Q22-1', 'DFA with two unlabelled states',
       'The left state is the start state and has a self-loop on 0. On 1 it goes to the right state, '
       'which is accepting and has a self-loop on 0. On 1 the right state returns to the left state.')
