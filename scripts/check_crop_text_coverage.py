#!/usr/bin/env python3
"""Find PDF text outside proposed crops. Diagnostic only, never visual approval.
Scanned pages, drawings and image-only formulas require independent visual review.
"""
import argparse,json,re
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--paper',required=True);a.add_argument('--manifest',default=str(ROOT/'data/crops.json'));a.add_argument('--source',required=True);a.add_argument('--output');args=a.parse_args()
 crops=json.loads(Path(args.manifest).read_text());groups={}
 for q,entries in crops.items():
  if q.startswith(args.paper+'-Q'):
   for e in entries:groups.setdefault(e['page'],[]).append((q,fitz.Rect(e['bbox'])))
 doc=fitz.open(args.source);uncovered=[];text_spans=0;ignored=0
 for i,p in enumerate(doc,1):
  for b in p.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    for span in line['spans']:
     t=span['text'].strip();box=fitz.Rect(span['bbox'])
     if not t:continue
     # Header/footer bands and explicit paper/rubric labels only; retain all other text.
     if box.y1<90 or box.y0>p.rect.height-65 or re.search(r'Carry (?:ONE|TWO)|General Aptitude|Computer Science.*Information Technology|Organ[izs]ing Institute|Page \d+ of \d+',t):ignored+=1;continue
     text_spans+=1
     covered=any(fitz.Rect(r.x0-2,r.y0-2,r.x1+2,r.y1+2).contains(box) for _,r in groups.get(i,[]))
     if not covered:uncovered.append({'page':i,'text':t,'bbox':list(box)})
 result={'paper_id':args.paper,'pages':len(doc),'text_spans_checked':text_spans,'header_or_rubric_spans_ignored':ignored,'uncovered_spans':uncovered,'limitation':'Text-only heuristic. Does not verify figures, scanned text, original completeness, rights or answers. Inspect each finding against the full original page; do not silently enlarge or certify crops.'}
 data=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
 if args.output:Path(args.output).write_text(data)
 print(json.dumps({'paper_id':args.paper,'text_spans_checked':text_spans,'uncovered_spans':len(uncovered)}))
if __name__=='__main__':main()
