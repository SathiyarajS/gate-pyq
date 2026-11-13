#!/usr/bin/env python3
"""Update only docs/COVERAGE.md Redrawn counts using the production eligibility gate."""
import json
from pathlib import Path
from transcription import load_paper, resolve
ROOT = Path(__file__).resolve().parents[1]

def main():
    questions = json.loads((ROOT / 'data/questions.json').read_text())
    papers = {q['paper_id']: load_paper(ROOT, q['paper_id']) for q in questions}
    counts = {p: sum(bool(resolve(ROOT, q, papers[p])) for q in questions if q['paper_id'] == p) for p in papers}
    path = ROOT / 'docs/COVERAGE.md'
    lines = path.read_text().splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith('| Paper |'))
    cells = [x.strip() for x in lines[header].split('|')[1:-1]]
    if 'Redrawn' in cells:
        column = cells.index('Redrawn')
    else:
        column = len(cells)
        lines[header] += ' Redrawn |'
        lines[header + 1] += ' ---: |'
    for i in range(header + 2, len(lines)):
        if not lines[i].startswith('| CS-'): break
        row = [x.strip() for x in lines[i].split('|')[1:-1]]
        if row[0] not in counts: raise SystemExit('Unknown coverage paper: ' + row[0])
        if len(row) == column: row.append(str(counts[row[0]]))
        else: row[column] = str(counts[row[0]])
        lines[i] = '| ' + ' | '.join(row) + ' |'
    path.write_text('\n'.join(lines) + '\n')

if __name__ == '__main__': main()
