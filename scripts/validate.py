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
if set(x['year'] for x in papers)!=set(range(1991,2027)):errors.append('Year coverage differs from 1991–2026')
qids=[];pairs=[]
for q in qs:
 for f in ['question_id','paper_id','source_question_number','subject','question_text','source_page','solution','derived_answer','official_answer','verification_status','discrepancy_ids']:
  if f not in q:errors.append(f'Missing {f}: {q.get("question_id")}')
 if re.search(r'\d\. +(?!0x)\d',q.get('solution','')):errors.append('Possible damaged decimal/IP notation: '+str(q.get('question_id')))
 if q.get('source_url') and not q['source_url'].endswith('#page='+str(q.get('source_page'))):errors.append('Source-page link mismatch: '+str(q.get('question_id')))
 qids.append(q.get('question_id'));pairs.append((q.get('paper_id'),q.get('source_question_number')))
 if q.get('paper_id') not in ids:errors.append('Unknown paper reference')
 if q.get('subject') not in subjects|{'excluded'}:errors.append('Unknown subject')
 if q.get('subject')=='excluded' and not q.get('exclusion_reason'):errors.append('Unexplained exclusion')
 if args.require_complete and q.get('subject')!='excluded' and (q.get('verification_status')!='reviewed' or q.get('source_transcription_verified') is not True):errors.append(f'Not release-verified (including transcription): {q.get("question_id")}')
if len(qids)!=len(set(qids)) or len(pairs)!=len(set(pairs)):errors.append('Duplicate question identifiers')
counts=Counter(q.get('paper_id') for q in qs)
if args.require_complete:
 for x in papers:
  actual={q['source_question_number'] for q in qs if q['paper_id']==x['paper_id']}
  if not x.get('expected_question_numbers') or actual!=set(x['expected_question_numbers']):errors.append('Unreconciled question numbers: '+x['paper_id'])
  if not x.get('final_key_verified') or not x['inventory_verified'] or x['source_review_status']!='reviewed' or not x['paper_url'] or not x['key_url'] or x['expected_question_count'] is None or counts[x['paper_id']]!=x['expected_question_count']:errors.append('Incomplete paper: '+x['paper_id'])
print(f'{len(papers)} candidate papers; {len(qs)} recorded questions. Structural checks '+('FAILED' if errors else 'passed')+'.')
for e in errors:print(e)
raise SystemExit(bool(errors))
