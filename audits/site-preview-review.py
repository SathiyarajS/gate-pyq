#!/usr/bin/env python3
"""Independent, read-only generated-preview coverage and metadata checks."""
import collections,html,json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'_site'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.articles=[];self.links=[];self.ids=set();self.answers=0;self.openanswers=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='article' and 'data-id' in a:self.articles.append(a['data-id'])
  if tag in ('a','script','link','img'):
   u=a.get('href',a.get('src'))
   if u:self.links.append(u)
  if tag=='details' and a.get('class')=='answer':
   self.answers+=1;self.openanswers+=('open' in a)
qs=json.loads((ROOT/'data/questions.json').read_text()); qm={q['question_id']:q for q in qs}
errors=[];subjects=collections.Counter();papers=collections.Counter();paths={};pages={}
for p in SITE.rglob('*.html'):
 parsed=Page(p.read_text());pages[p.resolve()]=parsed
 rel=p.relative_to(SITE).parts
 if re.match(r'^\d\d-',rel[0]) and 'topic' not in rel:
  subjects.update(parsed.articles)
  for qid in parsed.articles:paths[qid]=str(p.relative_to(SITE))
 if rel[0]=='papers':papers.update(parsed.articles)
 if rel[0]!='pdf' and (parsed.answers!=len(parsed.articles) or parsed.openanswers):errors.append(f'Answer collapse/count: {p}')
expected=collections.Counter(iter(qm))
for label,c in [('subjects',subjects),('papers',papers)]:
 if c!=expected:errors.append(f'{label} coverage mismatch: {len(c)} unique, {sum(c.values())} total')
for p,parsed in pages.items():
 for link in parsed.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target/= 'index.html'
  if not target.exists():errors.append(f'Broken link: {p.relative_to(SITE)} → {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'Broken anchor: {p.relative_to(SITE)} → {link}')
for subject in sorted({q['subject'] if q['subject']!='excluded' else '13-other-topics' for q in qs}):
 records=json.loads((SITE/subject/'index.json').read_text())
 for record in records:
  q=qm[record['id']];raw=html.unescape(re.sub('<[^>]*>',' ',record['html']));raw=' '.join(raw.split())
  for field in ['question_text','official_answer','derived_answer','solution','source_access_note','key_revision_status','source_numbering_note','source_provenance','shared_context','source_group_marks','source_subpart']:
   value=q.get(field)
   if value is not None and field not in ['question_text','solution']:
    if field=='derived_answer' and value==q['official_answer']:continue
    if ' '.join(str(value).split()) not in raw:errors.append(f'Missing {field}: {q["question_id"]}')
  if q['official_answer'] is None and 'none located' not in raw:errors.append('Missing no-key label '+q['question_id'])
  if q['discrepancy_ids'] and '⚠ Discrepancy' not in raw:errors.append('Missing discrepancy badge '+q['question_id'])
  label=f'(GATE {q["paper_id"].split("-")[1]}'
  if label not in raw:errors.append('Missing year label '+q['question_id'])
  number=str(q.get('printed_question_number') or q['source_question_number'])
  if ', Q'+number+')' not in raw:errors.append('Missing printed number '+q['question_id'])
report={'html_pages':len(pages),'subject_records':sum(subjects.values()),'paper_records':sum(papers.values()),'unique_subject_records':len(subjects),'unique_paper_records':len(papers),'errors':errors,'sample_paths':{k:paths[k] for k in ['CS-1991-Q1','CS-2019-Q22','CS-2019-Q52','CS-2020-Q17','CS-2023-Q30']}}
(ROOT/'audits/site-preview-review.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2)[:10000]);raise SystemExit(bool(errors))
