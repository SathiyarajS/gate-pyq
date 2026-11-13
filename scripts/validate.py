#!/usr/bin/env python3
"""Structural validation and explicit completeness gate, not mathematical proof."""
import argparse,json,re
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--require-complete',action='store_true');args=a.parse_args()
papers=json.loads((p/'data/papers.json').read_text());qs=json.loads((p/'data/questions.json').read_text());errors=[]
ids=[x['paper_id'] for x in papers]; subjects={x.name for x in (p/'subjects').iterdir()}
if len(ids)!=len(set(ids)):errors.append('Duplicate paper IDs')
years={paper.get('year') for paper in papers}
if not years or any(type(year) is not int or not 1991 <= year <= 9999 for year in years):
 errors.append('Invalid year in paper inventory')
elif years!=set(range(1991,max(years)+1)):
 errors.append('Paper inventory must cover consecutive years starting in 1991')
legacy_items={}
for inventory in (p/'data/source-provenance').glob('*-inventory.json'):
 data=json.loads(inventory.read_text())
 for row in data.get('items',[]):legacy_items[(f"CS-{data['year']}",row['normalized_ordinal'])]=row
qids=[];pairs=[]
for q in qs:
 for f in ['question_id','paper_id','source_question_number','subject','question_text','source_page','solution','derived_answer','official_answer','verification_status','discrepancy_ids']:
  if f not in q:errors.append(f'Missing {f}: {q.get("question_id")}')
 if re.search(r'\d\. +(?!0x)\d',q.get('solution','')):errors.append('Possible damaged decimal/IP notation: '+str(q.get('question_id')))
 if q.get('source_url') and not q.get('source_archive_member') and not q['source_url'].endswith('#page='+str(q.get('source_page'))):errors.append('Source-page link mismatch: '+str(q.get('question_id')))
 if q.get('source_section'):
  ordinal=int(q['source_question_number']); scheme=q.get('source_numbering_scheme'); raw_printed=str(q.get('printed_question_number',''))
  if scheme in {'legacy_sections_subparts','secondary_reproduction_label_original_unverified'}:
   row=legacy_items.get((q['paper_id'],ordinal))
   if not row or any([q['source_section']!=row['section'],raw_printed!=row['printed_id'],str(q.get('source_group_number'))!=str(row['printed_question']),q.get('source_subpart')!=row['printed_subpart'],q.get('marks')!=row['marks'],q.get('source_group_marks')!=row['source_group_marks']]):errors.append('Legacy source ledger mismatch: '+str(q.get('question_id')))
   printed=ordinal
  elif scheme=='cs_grouped_subparts':
   expected_printed=str(q.get('source_group_number',''))+str(q.get('source_subpart',''))
   if raw_printed!=expected_printed or q['source_section']!='CS':errors.append('Grouped source numbering mismatch: '+str(q.get('question_id')))
   if q.get('paper_id')=='CS-2005':
    mapped=str(ordinal) if ordinal<=80 else str(81+(ordinal-81)//2)+('a' if ordinal%2 else 'b')
    if not 1<=ordinal<=90 or raw_printed!=mapped:errors.append('2005 grouped item mapping mismatch: '+str(q.get('question_id')))
    if q.get('marks')!=(1 if ordinal<=30 else 2):errors.append('2005 item marks mismatch: '+str(q.get('question_id')))
   printed=ordinal
  else:printed=int(raw_printed or -1)
  ga_printed=ordinal+55 if q.get('source_numbering_scheme')=='cs_first_continuous' else ordinal
  cs_printed=ordinal if q.get('source_numbering_scheme')=='ga_first_continuous' else ordinal-10
  expected=(q['source_section'],ordinal) if scheme in {'legacy_sections_subparts','secondary_reproduction_label_original_unverified'} else ('CS',ordinal) if scheme in {'cs_only_continuous','cs_grouped_subparts'} else (('GA',ga_printed) if ordinal<=10 else ('CS',cs_printed))
  if (q['source_section'],printed)!=expected:
   errors.append('Printed/normalized numbering mismatch: '+str(q.get('question_id')))
 if q.get('official_answer') is None and (q.get('key_url') is not None or q.get('key_page') is not None or q.get('verification_status')=='official_key_matched'):
  errors.append('Unsupported official-key claim: '+str(q.get('question_id')))
 if q.get('explanatory_depth_status')=='reviewed_expanded' and q.get('independent_depth_review',{}).get('status')!='reviewed':errors.append('Expanded explanation lacks independent depth review: '+str(q.get('question_id')))
 if q.get('explanatory_depth_status')=='reviewed_expanded' and q.get('question_text','').strip() in {'','See linked original.'}:errors.append('Reviewed expansion lacks essential problem context: '+str(q.get('question_id')))
 if args.require_complete and q.get('subject')!='excluded' and (q.get('explanatory_depth_status')!='reviewed_expanded' or q.get('independent_depth_review',{}).get('status')!='reviewed'):errors.append('Explanation-depth review incomplete: '+str(q.get('question_id')))
 qids.append(q.get('question_id'));pairs.append((q.get('paper_id'),q.get('source_question_number')))
 if q.get('paper_id') not in ids:errors.append('Unknown paper reference')
 if q.get('subject') not in subjects|{'excluded'}:errors.append('Unknown subject')
 if q.get('subject')=='excluded' and not q.get('exclusion_reason'):errors.append('Unexplained exclusion')
 if args.require_complete and q.get('subject')!='excluded' and (q.get('verification_status')!='reviewed' or q.get('source_transcription_verified') is not True):errors.append(f'Not release-verified (including transcription): {q.get("question_id")}')
if len(qids)!=len(set(qids)) or len(pairs)!=len(set(pairs)):errors.append('Duplicate question identifiers')
# Scanned source keys retain a separate, visually verified transcription.
lookup={(q['paper_id'],int(q['source_question_number'])):q for q in qs}
for keyfile in (p/'data/key-transcriptions').glob('*.json'):
 for row in json.loads(keyfile.read_text()):
  q=lookup.get((row['paper_id'],row['ordinal']))
  if not q or any(q.get(f)!=row.get(f) for f in ['official_answer','question_type','marks','source_section','printed_question_number','official_session']):
   errors.append('Scanned-key transcription mismatch: '+row['paper_id']+' Q'+str(row['ordinal']))
# Source PDFs are not stored, so every reviewed crop needs its rendered image committed
# in site-assets/q, matching the current crop record (render_crops.py writes crop_sha256).
import hashlib
crop_records=json.loads((p/'data/crops.json').read_text()) if (p/'data/crops.json').is_file() else {}
image_manifest=json.loads((p/'site-assets/q/manifest.json').read_text()) if (p/'site-assets/q/manifest.json').is_file() else {}
missing_images=[]
for qid,entries in crop_records.items():
 if not entries or not all(c.get('status')=='verified' for c in entries):continue
 imgs=sorted(image_manifest.get(qid,[]),key=lambda e:e.get('index',0))
 fps=[hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest() for c in entries]
 if len(imgs)!=len(entries) or any(not (p/'site-assets/q'/e['file']).is_file() or e.get('crop_sha256')!=f for e,f in zip(imgs,fps)):missing_images.append(qid)
if missing_images:errors.append(f'{len(missing_images)} reviewed questions have no committed image (or a stale one) in site-assets/q, e.g. '+', '.join(missing_images[:5])+'. Restore the PDFs (python scripts/fetch_sources.py), run python scripts/render_crops.py --question <id> ..., and commit site-assets/q.')
counts=Counter(q.get('paper_id') for q in qs)
if args.require_complete:
 for x in papers:
  actual={q['source_question_number'] for q in qs if q['paper_id']==x['paper_id']}
  if not x.get('expected_question_numbers') or actual!=set(x['expected_question_numbers']):errors.append('Unreconciled question numbers: '+x['paper_id'])
  if not x.get('final_key_verified') or not x['inventory_verified'] or x['source_review_status']!='reviewed' or not x['paper_url'] or not x['key_url'] or x['expected_question_count'] is None or counts[x['paper_id']]!=x['expected_question_count']:errors.append('Incomplete paper: '+x['paper_id'])
print(f'{len(papers)} candidate papers; {len(qs)} recorded entries. Structural checks '+('FAILED' if errors else 'passed')+'.')
for e in errors:print(e)
raise SystemExit(bool(errors))
