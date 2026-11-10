#!/usr/bin/env python3
"""Static tests for optional private source-crop presentation; not browser QA."""
import hashlib,json
from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];S=R/'_site-crop-preview'
class Images(HTMLParser):
 def __init__(self,t):super().__init__();self.images=[];self.feed(t)
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
crops=json.loads((R/'data/crops.json').read_text());expected={q:cs for q,cs in crops.items() if cs and all(c['status']=='verified' for c in cs)}
seen={};report=json.loads((S/'build-report.json').read_text())
for subject in report['subject_counts']:
 for q in json.loads((S/subject/'index.json').read_text()):
  images=Images(q['html']).images
  if q['id'] not in expected:assert not images,q['id'];continue
  assert len(images)==len(expected[q['id']]),q['id'];seen[q['id']]=len(images)
  for im in images:
   assert im['src'].startswith('../assets/questions/');name=Path(im['src']).name
   assert (S/'assets/questions'/name).read_bytes()==(R/'site-assets/q'/name).read_bytes()
   assert im['alt'] and int(im['width'])>0 and int(im['height'])>0
assert set(seen)==set(expected);assert report['original_crop_questions']==len(expected);assert report['original_crop_parts']==sum(seen.values())
result={'questions_with_reviewed_crops':len(seen),'image_parts':sum(seen.values()),'only_reviewed_images':True,'copied_image_byte_identity':True,'alt_text_and_dimensions':True,'browser_layout_qa':'not_performed','limitations':'Static completeness and file checks only; alt text is not a complete accessible transcription. No source rights, original completeness or answer certification.'}
(R/'audits/site-crop-display-review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
