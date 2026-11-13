#!/usr/bin/env python3
"""Build source navigation without reproducing original paper content."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
qs=json.loads((P/'data/questions.json').read_text());routes=json.loads((P/'data/source-access-routes.json').read_text());by={r['paper_id']:r for r in routes};counts={};updated=0
for q in qs:
 r=by.get(q['paper_id'])
 if not r:continue
 page=q['source_page'];printed=q.get('printed_question_number',q['source_question_number']);section=q.get('source_section','CS');member=q.get('source_archive_member')
 if r['route']=='indirect_official_linked_zip':
  member=member or r['archive_members'][0]
  instruction=f"Open CS.zip from the official-linked archive, extract {member}, then open physical PDF page {page}. Locate printed {section} question {printed} in variant {q['paper_id']}. The ZIP link does not open the question directly."
  link=r['paper_url'];panel=f"[Open official-linked CS.zip]({link}). Extract **{member}**, open physical PDF page **{page}**, and locate printed **{section} {printed}** in **{q['paper_id']}**. This is ZIP/member navigation, not a direct question-page link."
 else:
  link=r['paper_url'].split('#')[0]+'#page='+str(page)
  label='archived official PDF' if r['route']=='archived_official_pdf' else 'official PDF'
  instruction=f"Open the {label} at physical page {page}; locate printed {section} question {printed} in variant {q['paper_id']}. Continue to following pages if the question spans pages. PDF viewers may ignore page anchors."
  panel=f"[Open actual source question in the {label}]({link}), physical page **{page}**, printed **{section} {printed}**, variant **{q['paper_id']}**. Continue to following pages for any continuation; some viewers ignore page anchors."
 access={'route':r['route'],'url':link,'physical_page':page,'printed_question':str(printed),'section':section,'variant':q['paper_id'],'instructions':instruction,'full_original_in_repository':'not_certified','reuse_permission':'not_established'}
 if member:access['archive_member']=member
 q['original_source_access']=access
 if q.get('accessible_artwork_status')=='pending_separate_work':
  q['artwork_access_audit']={'local_accessible_artwork':'pending','original_source_figure':'consult_linked_source; not_classified_as_missing','scope':'Essential textual relationships are provided; separate artwork reconstruction remains pending.'}
  panel+=' **Local accessible artwork is pending**; consult the original figure at the source. This does not mean the original PDF lacks the figure.'
 year=q['paper_id'].split('-')[1];f=P/'subjects'/q['subject']/f'{year}.md' if q['subject']!='excluded' else next((P/'supplemental').glob(year+'-*.md'));s=f.read_text()
 pat=re.compile(r'(?m)^# GATE '+year+r'[^\n]*?: Q'+str(q['source_question_number'])+r'(?=\D|$)[^\n]*\n');ms=list(pat.finditer(s))
 if '-S' in q['paper_id']:ms=[m for m in ms if 'CS'+q['paper_id'].split('-S')[1] in m.group(0)]
 assert len(ms)==1,q['question_id'];m=ms[0];n=re.search(r'(?m)^# GATE ',s[m.end():]);end=m.end()+n.start() if n else len(s);chunk=s[m.start():end]
 block='<!-- original-source-access:start -->\n**Actual source access:** '+panel+'\n<!-- original-source-access:end -->\n\n'
 chunk=re.sub(r'<!-- original-source-access:start -->.*?<!-- original-source-access:end -->\n\n','',chunk,flags=re.S)
 first=chunk.index('\n')+1;chunk=chunk[:first]+'\n'+block+chunk[first:].lstrip('\n');f.write_text(s[:m.start()]+chunk+s[end:]);counts[r['route']]=counts.get(r['route'],0)+1;updated+=1
(P/'data/questions.json').write_text(json.dumps(qs,indent=2,ensure_ascii=False)+'\n')
lines=['# Access the actual question sources','','Essential question paraphrases and independent solutions are in this repository. The links below open the source papers; they do not certify complete original wording or grant copying permission. No whole papers are reproduced by this navigation update.','', '## Direct and archived PDFs','', 'Physical page means the PDF viewer’s page index, which may differ from the printed page label. Master-paper numbering may differ from a candidate console. Follow the printed section/question and variant identifiers alongside each solution.']
for r in routes:
 if r['route']!='indirect_official_linked_zip':lines.append(f"- **{r['paper_id']}**: [source PDF]({r['paper_url']}); question pages {r['source_page_range'][0]}–{r['source_page_range'][1]}. {'Archived official-origin copy, not a live official host.' if r['route']=='archived_official_pdf' else 'Official-host route.'}")
lines+=['','Fresh audit fetches succeeded for 2019, 2020, 2022, both 2024 and 2025 variants, and both 2026 variants. The 2021 combined PDF exceeded the reader size limit; 2023 timed out. Those are tool limitations, not established broken links. Archived routes are retained from provenance and were not freshly fetched in this pass.','','## ZIP routes: 15 variants, 1,010 entries','','1. Open the [official download index](https://gate2026.iitg.ac.in/download.html) and its [bulk folder](https://drive.google.com/drive/folders/1sV6FgtOUDl_PGjc36Zdc0eJwK1zZ_2OF), or the verified [CS.zip file](https://drive.google.com/file/d/1popAHO-cX69oQEx_tD0wZXL1tTrBljeO/view).','2. Download/extract CS.zip and open the exact member below.','3. Use the physical PDF page and printed question/section shown beside each solution. Combined files contain multiple variants; do not restart page numbering at a divider.','4. A ZIP URL is not a deep link to a question. No invented page anchor is attached to ZIP links.','']
for r in routes:
 if r['route']=='indirect_official_linked_zip':lines.append(f"- **{r['paper_id']}**: member **{r['archive_members'][0]}**, physical question pages **{r['source_page_range'][0]}–{r['source_page_range'][1]}**.")
lines+=['','## Explicitly pending artwork','','These 19 entries have separate accessible artwork pending. Their essential context is present and original figures remain at the linked PDFs. This is not a count of all figures required, nor a claim that other figures are absent.']
for q in qs:
 if q.get('accessible_artwork_status')=='pending_separate_work':lines.append(f"- {q['question_id']}: [original source page {q['source_page']}]({q['original_source_access']['url']}).")
lines+=['','Nine records contain embedded figures, and two have dedicated question-access artifacts. Artwork metadata is incomplete elsewhere; unknown is not missing. The [2019 hostel-plan reconstruction](question-access/CS-2019-Q10/question.md) provides complete independently reviewed topology/choice descriptions without invented dimensions. The [2025 CS1 Q9 source artwork](question-access/CS-2025-S1-Q9/question.md) provides a source-page image; raster access alone is not full screen-reader accessibility.','','## Legacy and rights limits','','1991–2006 use audited third-party reproductions. Their page links remain beside each solution, but original official completeness is unverified. Known source conflicts and recovered community figures remain qualified.','','Official indexes display All Rights Reserved. No bulk-republication license has been established. Public download access is not permission to republish entire original papers. This update supplies navigation and metadata only.']
(P/'docs/SOURCE_ACCESS.md').write_text('\n'.join(lines)+'\n');print(updated,counts)
