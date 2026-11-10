from pathlib import Path
from html import escape
p=Path(__file__).parent
# Drawing coordinates only, not architectural measurements.
W,H=60,84
vacant={(5,0),(0,2),(1,4),(4,4),(5,3)}
occupied={(1,0),(2,0),(3,0),(4,0),(0,1),(5,1),(0,3),(2,4),(3,4),(5,4)}
choices={'A':{(0,2):'Z',(1,4):'X',(4,4):'Y'},'B':{(5,0):'X',(0,2):'Z',(5,3):'Y'},'C':{(5,0):'Z',(1,4):'X',(5,3):'Y'},'D':{(1,4):'X',(4,4):'Z',(5,3):'Y'}}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="1050" viewBox="0 0 980 1050" role="img" aria-labelledby="title desc">', '<title id="title">GATE 2019 CS, General Aptitude Q10: four hostel allocation plans</title>', '<desc id="desc">Accessible reconstruction of official page 3. All four plans have identical room boundaries and occupancy. North points upper-left, east upper-right, south lower-right, west lower-left. Gray rooms are occupied. Detailed room-by-room description and all option placements are in question.md. Dimensions are drawing coordinates only; the source supplies no architectural dimensions.</desc>', '<rect width="980" height="1050" fill="white"/>','<style>text {font-family:serif;font-size:23px;fill:black} rect.room {stroke:black;stroke-width:2} .occupied{fill:#bfbfbf} .vacant{fill:white}</style>']
for i,(key,labels) in enumerate(choices.items()):
 x=35+(i%2)*490;y=55+(i//2)*490
 s.append(f'<g transform="translate({x},{y})" role="group" aria-label="Option {key}"><text x="0" y="-18">({key})</text>')
 for c,r in sorted(vacant|occupied|{(0,0),(0,4)}, key=lambda cr:(cr[1],cr[0])):
  label='WR' if (c,r) in {(0,0),(0,4)} else labels.get((c,r),'')
  status='washroom' if label=='WR' else 'occupied' if (c,r) in occupied else 'vacant'+(' assigned to '+label if label else ', unlabelled')
  s.append(f'<rect class="room {"occupied" if (c,r) in occupied else "vacant"}" x="{c*W}" y="{r*H}" width="{W}" height="{H}"><title>Row {r+1}, column {c+1}: {escape(status)}</title></rect>')
  if label:s.append(f'<text x="{c*W+W/2}" y="{r*H+H/2+8}" text-anchor="middle">{label}</text>')
 for r in [0,3]:
  s.append(f'<rect class="room vacant" x="360" y="{r*H}" width="60" height="168"/><text transform="translate(397,{r*H+84}) rotate(-90)" text-anchor="middle">Garden</text>')
 s.append('<rect class="room vacant" x="300" y="168" width="120" height="84"/><text x="360" y="218" text-anchor="middle">Entrance</text>')
 s.append('<path d="M 110,135 L 245,270 M 245,135 L 110,270" fill="none" stroke="black" stroke-width="2"/><text x="73" y="127">N</text><text x="251" y="143">E</text><text x="73" y="310">W</text><text x="251" y="310">S</text></g>')
s.extend(['<text x="35" y="1000" style="font-size:18px">Gray = already occupied; WR = washroom. Schematic: no dimensions supplied in source.</text>','<text x="35" y="1028" style="font-size:16px">Source: official GATE 2019 CS paper, General Aptitude Set-6, page 3. Accessible redraw.</text>','</svg>'])
(p/'options.svg').write_text('\n'.join(s))
