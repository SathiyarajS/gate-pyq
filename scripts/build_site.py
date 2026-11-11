#!/usr/bin/env python3
"""Build locally: python scripts/build_site.py --preview. Default is fail-closed release."""
import argparse, collections, html, json, math, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import quote, urlparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from transcription import load_paper, resolve
import site_features
import question_groups
TITLES = ['Digital Logic','Computer Organization & Architecture','Programming in C','Data Structures','Algorithms','Theory of Computation','Compiler Design','Operating Systems','Database Management Systems','Computer Networks','General Aptitude','Discrete Mathematics','Engineering Mathematics & Other Topics']

def load(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default

def safe_url(value):
    return str(value) if value and urlparse(str(value)).scheme in ('https','http') else ''

def inline_math(text):
    """Only explicit LaTeX delimiters; preserve legacy dollar end-markers verbatim."""
    pattern = r'(\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$)'
    parts = re.split(pattern, text, flags=re.S)
    result=[]
    for part in parts:
        explicit = ((part.startswith(r'\(') and part.endswith(r'\)')) or
                    (part.startswith(r'\[') and part.endswith(r'\]')) or
                    (part.startswith('$$') and part.endswith('$$')))
        if explicit:
            display=part.startswith((r'\[','$$'))
            result.append('<span class="math-source" data-math="'+html.escape(part[2:-2],quote=True)+'" data-display="'+str(display).lower()+'">'+html.escape(part)+'</span>')
        else:result.append(html.escape(part))
    return ''.join(result)

def rich(value):
    # Escape first. Preserve text/code/paragraphs without allowing source HTML execution.
    chunks = re.split(r'(```[^\n]*\n.*?```)', str(value or ''), flags=re.S)
    result=[]
    for chunk in chunks:
        if chunk.startswith('```'):
            result.append('<pre><code>'+html.escape(chunk.split('\n',1)[-1].removesuffix('```'))+'</code></pre>')
        else:
            result.extend('<p>'+inline_math(p).replace('\n','<br>')+'</p>' for p in chunk.split('\n\n') if p.strip())
    return Markup(''.join(result))

def solution(value):
    """Solution text: like rich(), plus numbered steps and '- ' notes laid out as steps and lists."""
    chunks = re.split(r'(```[^\n]*\n.*?```)', str(value or ''), flags=re.S)
    result = []
    for chunk in chunks:
        if chunk.startswith('```'):
            result.append('<pre><code>'+html.escape(chunk.split('\n',1)[-1].removesuffix('```'))+'</code></pre>')
            continue
        for para in chunk.split('\n\n'):
            if not para.strip(): continue
            lines, buf, items = para.strip('\n').split('\n'), [], []
            def flush_text():
                if not buf: return
                body = inline_math('\n'.join(buf)).replace('\n','<br>'); buf.clear()
                step = re.match(r'(\d{1,2})[.)]\s+(.*)', body, flags=re.S)
                result.append('<p class="step"><span class="n">'+step[1]+'.</span> '+step[2]+'</p>' if step else '<p>'+body+'</p>')
            def flush_items():
                if items: result.append('<ul>'+''.join('<li>'+inline_math(i)+'</li>' for i in items)+'</ul>'); items.clear()
            for line in lines:
                m = re.match(r'-\s+(\S.*)', line)
                if m: flush_text(); items.append(m[1])
                else: flush_items(); buf.append(line)
            flush_items(); flush_text()
    return Markup(''.join(result))

def discrepancies():
    rows={}
    for line in (ROOT/'DISCREPANCIES.md').read_text().splitlines():
        if line.startswith('| CS-'):
            cols=[x.strip().replace('\\|','|') for x in re.split(r'(?<!\\)\|',line)[1:-1]]
            if len(cols)==9: rows[cols[0]]=dict(zip(['id','subject','year','number','type','summary','official','derived','status'],cols))
    return rows

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--preview',action='store_true');ap.add_argument('--release',action='store_true',help='Public build: no preview banner; original-question crops for every question whose source PDF is present.');ap.add_argument('--output',default='_site');ap.add_argument('--with-reviewed-crops',action='store_true',help='Private local preview only: regenerate and include reviewed source crops. Does not grant redistribution rights.');args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if out == ROOT or ROOT not in out.parents: raise SystemExit('Output must be a subdirectory of repository')
    questions=load(ROOT/'data/questions.json'); papers=load(ROOT/'data/papers.json'); topics=load(ROOT/'data/topics.json',{}); ds=discrepancies()
    transcriptions={p['paper_id']:load_paper(ROOT,p['paper_id']) for p in papers}
    pmap={p['paper_id']:p for p in papers}; groups=collections.defaultdict(list); issues=[]
    off_syllabus,syllabus=site_features.load_syllabus(ROOT,topics)
    seen=set()
    for q in questions:
        if q['question_id'] in seen: raise SystemExit('Duplicate question ID')
        q.setdefault('question_title', q['question_id'])
        if not re.fullmatch(r'[A-Za-z0-9_-]+',q['question_id']) or not re.fullmatch(r'[A-Za-z0-9_-]+',q['paper_id']):raise SystemExit('Unsafe identifier')
        seen.add(q['question_id']); subject=q['subject'] if q['subject']!='excluded' else '13-other-topics'
        q['subject_dir']=subject;q['year']=pmap[q['paper_id']]['year'];q['display_type']=q['question_type'].upper() if q['question_type'].upper() in ('MCQ','MSQ','NAT') else ('Descriptive' if q['question_type'].lower() in ('descriptive','short-answer') else 'Other')
        q['number']=q.get('printed_question_number') or q['source_question_number'];set_match=re.search(r'-S(\d+)$',q['paper_id']);q['session']='Set '+set_match.group(1) if set_match else ''
        q['source_link']=safe_url(q.get('source_page_url') or q.get('source_url'));q['key_link']=safe_url(q.get('key_url'))
        if q['key_link'] and q.get('key_page') and '#' not in q['key_link']:q['key_link']+='#page='+str(q['key_page'])
        q['topic']=topics.get(subject,{}).get('assign',{}).get(q['question_id'],'unreviewed')
        q['off_syllabus']={'label':'Not in '+syllabus['syllabus']+' syllabus','note':off_syllabus[(subject,q['topic'])]} if (subject,q['topic']) in off_syllabus else None
        q['discrepancies']=[]
        for did in q['discrepancy_ids']:
            if did not in ds: raise SystemExit('Missing discrepancy row: '+did)
            q['discrepancies'].append(ds[did])
        q['transcription']=resolve(ROOT,q,transcriptions[q['paper_id']])
        q['options_data']=q.get('options') or q.get('question_options') or None
        # Options are never invented. A paraphrase often omits the original option set.
        q['practice_key']=str(q['official_answer']) if q['official_answer'] is not None else ''
        q['key_source']='official' if q['practice_key'] else ''
        if not q['practice_key'] and q.get('verification_status')=='independently_solved' and re.fullmatch(r'[A-Z](;[A-Z])*|-?\d+(\.\d+)?( to -?\d+(\.\d+)?)?',str(q.get('derived_answer') or '')):
            # No official key: practise against our own derived answer, labelled as such. Never for open discrepancies or conditional answers.
            q['practice_key']=str(q['derived_answer']);q['key_source']='derived'
        key_letters=re.findall(r'[A-Z]',q['practice_key']) if re.fullmatch(r'[A-Z](;[A-Z])*',q['practice_key']) else []
        last=max(['D']+key_letters);q['choices']=[chr(c) for c in range(ord('A'),ord(last)+1)]
        q['permalink']='q/'+q['question_id']+'/'
        q['report']='https://github.com/SathiyarajS/gate-pyq/issues/new?'+ 'title='+quote('['+q['question_id']+'] ')+'&body='+quote('Question: https://sathiyarajs.github.io/gate-pyq/'+q['permalink']+'\n\nDescribe the issue and cite the source page:\n')
        groups[subject].append(q)
    # Previously recorded repeats: links on every question and a separate folded study view.
    repeats=site_features.load_repeats(ROOT,questions);byid={q['question_id']:q for q in questions}
    for q in questions:
        info=repeats.get(q['question_id'])
        q['also']=[dict(url='q/'+o+'/',kind=kind,label='GATE '+str(byid[o]['year'])+(' '+byid[o]['session'] if byid[o]['session'] else '')+', Q'+str(byid[o]['number'])) for o,kind in info['others']] if info else []
    patterns=question_groups.load_patterns(ROOT,questions)
    repeat_studies=question_groups.repeat_groups(repeats)
    pattern_studies=question_groups.with_uncovered_repeats(patterns,repeat_studies,questions)
    missing_topics=[q['question_id'] for q in questions if q['topic']=='unreviewed']
    if missing_topics:issues.append(f'{len(missing_topics)} questions have no topic assignment; draft grouping is displayed.')
    topic_review_counts=collections.Counter()
    nonreviewed_topics=[]
    for q in questions:
        status=topics.get(q['subject_dir'],{}).get('review',{}).get(q['question_id'],'missing')
        topic_review_counts[status]+=1
        q['topic_review_status']=status
        if status!='reviewed':nonreviewed_topics.append(q['question_id'])
    if nonreviewed_topics:
        issues.append(f"Topic grouping: {topic_review_counts['reviewed']} reviewed, {topic_review_counts['candidate']} candidate, {len(nonreviewed_topics)-topic_review_counts['candidate']} other or missing; {len(nonreviewed_topics)} assignments require review.")
    redrawn=sum(bool(q['transcription']) for q in questions)
    redrawn_by_paper={p['paper_id']:sum(bool(q['transcription']) for q in questions if q['paper_id']==p['paper_id']) for p in papers}
    issues.append(f'{redrawn}/{len(questions)} questions are redrawn as verified text and figures; the rest show the original question image where its source PDF is available, otherwise a paraphrase with a link to the source page.')
    katex_dir=ROOT/'node_modules/katex/dist'
    has_math=(katex_dir/'katex.min.js').is_file() and (katex_dir/'katex.min.css').is_file()
    if not has_math:issues.append('Mathematical typesetting assets are unavailable; explicit LaTeX is preserved as text. Run npm ci to provision pinned local assets.')
    if not args.release:issues.append('PDF verification and Pagefind indexing must be run and checked separately after this build.')
    if args.release:args.with_reviewed_crops=True
    if not args.preview and not args.release:raise SystemExit('Release blocked:\n- '+'\n- '.join(issues))
    out.mkdir(parents=True,exist_ok=True)
    crop_assets={}
    if args.with_reviewed_crops:
        manifest=load(ROOT/'data/crops.json',{})
        approved=[qid for qid,entries in manifest.items() if entries and all(c.get('status')=='verified' for c in entries)]
        if args.release:
            missing_src=[qid for qid in approved if not all((ROOT/c['file']).is_file() for c in manifest[qid])]
            approved=[qid for qid in approved if qid not in missing_src]
            if missing_src:issues.append(f'{len(missing_src)} questions show a paraphrase instead of the original image because their source PDF is not in the repository yet (papers: '+', '.join(sorted({q.rsplit("-Q",1)[0] for q in missing_src}))+').')
        if not approved:raise SystemExit('No independently reviewed crop records available')
        # Regenerate from hash-checked original PDFs, rather than trust stale local images.
        subprocess.run([sys.executable,str(ROOT/'scripts/render_crops.py')]+[v for qid in approved for v in ('--question',qid)],check=True)
        assets=load(ROOT/'site-assets/q/manifest.json',{})
        dest=out/'assets/questions';dest.mkdir(parents=True,exist_ok=True)
        for qid in approved:
            if qid not in seen:raise SystemExit('Crop record has unknown question ID')
            entries=assets.get(qid,[])
            if len(entries)!=len(manifest[qid]):raise SystemExit('Crop image count mismatch: '+qid)
            for entry in entries:
                name=entry['file']
                if Path(name).name!=name or entry.get('status')!='verified':raise SystemExit('Unsafe or unreviewed crop asset')
                shutil.copy2(ROOT/'site-assets/q'/name,dest/name)
            crop_assets[qid]=entries
        for q in questions:q['original_crops']=crop_assets.get(q['question_id'],[])
        issues.append(f'{len(crop_assets)} questions show the original question image cropped from its source paper.' if args.release else f'{len(crop_assets)} questions include reviewed original-source crops in this private local preview. Remaining questions retain source-linked paraphrases. No redistribution rights are asserted.')
    if has_math:
        shutil.copytree(katex_dir,out/'assets/vendor/katex',dirs_exist_ok=True)
        shutil.copy2(ROOT/'node_modules/katex/LICENSE',out/'assets/vendor/katex/LICENSE')
    shutil.copytree(ROOT/'site-static',out/'assets',dirs_exist_ok=True)
    env=Environment(loader=FileSystemLoader(ROOT/'templates/site'),autoescape=select_autoescape(['html']));env.filters['rich']=rich;env.filters['solution']=solution
    counts={s:len(qs) for s,qs in groups.items()};titles={s:TITLES[int(s[:2])-1] for s in groups}
    cards=[dict(slug=s,title=titles[s],count=counts[s],topics=len(topics.get(s,{}).get('topics',[]))) for s in sorted(groups)]
    def render(path,**ctx):
        target=out/path/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
        prefix='../'*len(Path(path).parts) if path else './'
        target.write_text(env.get_template('page.html').render(prefix=prefix,cards=cards,issues=issues,syllabus=syllabus,w=weights,preview=not args.release,has_math=has_math,redrawn=redrawn,redrawn_percent=round(100*redrawn/len(questions),2),**ctx))
    topic_titles={(s,t['id']):t['title'] for s in groups for t in topics.get(s,{}).get('topics',[])}
    weights=site_features.weightage(questions,titles,topic_titles,off_syllabus)
    packs=[]  # what each subject or paper needs to work offline
    def sortkey(q):return (-q['year'],q['paper_id'],tuple(int(n) for n in re.findall(r'\d+',q['source_question_number'])))
    search=[];canonical={};subject_seen=[];paper_seen=[]
    for subject,qs in sorted(groups.items()):
        topic_list=topics.get(subject,{}).get('topics',[]) or [{'id':'unreviewed','title':'Draft grouping: topic review pending'}]
        allowed={t['id'] for t in topic_list};off_topics={t for (s,t) in off_syllabus if s==subject};urls=[subject+'/index.json','search.json']
        if any(not re.fullmatch(r'[a-zA-Z0-9_-]+',tid) for tid in allowed):raise SystemExit('Unsafe topic identifier')
        invalid=[q['question_id'] for q in qs if q['topic'] not in allowed]
        if invalid and allowed!={'unreviewed'}:raise SystemExit('Invalid topic IDs: '+str(invalid[:5]))
        qs.sort(key=sortkey)  # newest first, everywhere except paper pages
        for i,q in enumerate(qs,1):q['ordinal']=i;q['similar']=None;q['alt']=False;q['topic_title']=next((t['title'] for t in topic_list if t['id']==q['topic']),'Unreviewed')+('' if args.release and q['topic_review_status']=='reviewed' else ' · '+('reviewed grouping' if q['topic_review_status']=='reviewed' else 'candidate grouping'))
        heat=[{'title':t['title'],'cells':[sum(q['topic']==t['id'] and q['year']==y for q in qs) for y in range(1991,2027)]} for t in topic_list]
        def years(items):
            first={}
            for q in items:first.setdefault(q['year'],q['question_id'])
            return list(first.items())
        # Similar questions: each reviewed pattern (or repeat outside any pattern) gets its own page, newest first.
        # Every member links to it; all but the newest are marked so "One per method" can hide them.
        similar_pages=[]
        for u in question_groups.study_units(qs,pattern_studies,sortkey):
            if not u['alternatives']:continue
            members=sorted([u['representative']]+u['alternatives'],key=sortkey);gid=u['group']['id']
            for n,q in enumerate(members):q['similar']=dict(url=f'{subject}/similar/{gid}/#'+q['question_id'],others=len(members)-1);q['alt']=n>0
            similar_pages.append((gid,u['group'],members))
        render(subject,title=titles[subject],kind='subject',questions=qs,subject=subject,topics=topic_list,total=len(qs),heat=heat,off_topics=off_topics,topic_weights=weights['subject_topics'][subject] if weights else None,years=years(qs),pageable=True);urls.append(subject+'/')
        for q in qs:canonical[q['question_id']]=subject+'/#'+q['question_id'];subject_seen.append(q['question_id'])
        for t in topic_list:
            tqs=[q for q in qs if q['topic']==t['id']];base=f'{subject}/topic/{t["id"]}'
            render(base,title=titles[subject]+' · '+t['title'],kind='topic',questions=tqs,subject=subject,topics=topic_list,total=len(tqs),off_topics=off_topics,topic_off=off_syllabus.get((subject,t['id'])),years=years(tqs),pageable=True);urls.append(base+'/')
            for n in range(2,math.ceil(len(tqs)/10)+1):render(f'{base}/page/{n}',title=t['title'],kind='redirect',target=base+'/')
        for gid,group,members in similar_pages:
            repeat_only=gid.startswith('repeat-')
            render(f'{subject}/similar/{gid}',title=group['title'],kind='similar',questions=members,subject=subject,subject_title=titles[subject],total=len(members),group_note='GATE asked this question again.' if repeat_only else '',method_note='' if repeat_only else question_groups.reader_note(group));urls.append(f'{subject}/similar/{gid}/')
        # Older paginated and study-view addresses move to the single subject page.
        for n in range(2,math.ceil(len(qs)/10)+1):render(f'{subject}/page/{n}',title=titles[subject],kind='redirect',target=subject+'/')
        for view in ('unique','patterns'):
            render(f'{subject}/{view}',title=titles[subject],kind='redirect',target=subject+'/')
            for n in range(2,math.ceil(len(qs)/10)+1):render(f'{subject}/{view}/page/{n}',title=titles[subject],kind='redirect',target=subject+'/')
        # HTML fragments generated by the same safe autoescaped template as static pages.
        records=[]
        for q in qs:
            fragment=env.get_template('question.html').render(q=q,prefix='../',paper_view=False,preview=not args.release)
            records.append(dict(id=q['question_id'],year=q['year'],marks=q.get('marks'),type=q['display_type'],discrepancy=bool(q['discrepancy_ids']),off=bool(q['off_syllabus']),html=fragment))
            urls.append(q['permalink']);urls.extend('assets/questions/'+c['file'] for c in q.get('original_crops',[]))
            search.append(dict(id=q['question_id'],title=q['question_title'],text=q['question_text']+('\n'+q['transcription']['search'] if q['transcription'] else ''),year=q['year'],subject=titles[subject],type=q['display_type'],url=q['permalink']))
        (out/subject/'index.json').write_text(json.dumps(records,ensure_ascii=False))
        packs.append(dict(id=subject,title=titles[subject],group='subject',note=f'{len(qs)} questions',urls=urls))
    for paper in papers:
        qs=[q for q in questions if q['paper_id']==paper['paper_id']];qs.sort(key=lambda q:tuple(int(n) for n in re.findall(r'\d+',q['source_question_number'])))
        paper_seen.extend(q['question_id'] for q in qs)
        render('papers/'+paper['paper_id'],title=paper['paper_id'],kind='paper',questions=qs,paper_view=True,total=len(qs))
        packs.append(dict(id=paper['paper_id'],title=paper['paper_id'],group='paper',note=f'{len(qs)} questions',urls=['papers/'+paper['paper_id']+'/']+['assets/questions/'+c['file'] for q in qs for c in q.get('original_crops',[])]))
    for qid,target in canonical.items():render('q/'+qid,title=qid,kind='redirect',target=target)
    render('',title='Practice with provenance.',kind='home',total=len(questions))
    render('papers',title='All papers',kind='papers',papers=sorted(papers,key=lambda p:p['paper_id'],reverse=True))
    render('about',title='Know what you are studying.',kind='about')
    if weights:render('weightage',title='Where the marks are.',kind='weightage',total=len(questions))
    render('discrepancies',title='Discrepancies & interpretations',kind='discrepancies',discrepancy_groups=[(titles[s],[q for q in qs if q['discrepancy_ids']]) for s,qs in sorted(groups.items())])
    (out/'search.json').write_text(json.dumps(search,ensure_ascii=False))
    for item in search:
        render('search-docs/'+item['id'],title=item['title'],kind='searchdoc',item=item)
    # Offline: per-subject and per-paper packs, the always-cached core, the web app manifest and the service worker.
    (out/'manifest.webmanifest').write_text(json.dumps({'name':'GATE CS Archive','short_name':'GATE CS','description':'GATE Computer Science previous-year questions, 1991–2026, with sources, answers and solutions.','start_url':'./','scope':'./','display':'standalone','background_color':'#f7f7f1','theme_color':'#006a51','icons':[{'src':'assets/icons/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'assets/icons/icon-512.png','sizes':'512x512','type':'image/png'},{'src':'assets/icons/maskable-512.png','sizes':'512x512','type':'image/png','purpose':'maskable'}]},indent=1))
    core=['','papers/','about/']+(['weightage/'] if weights else [])+['manifest.webmanifest','assets/style.css','assets/app.js','assets/offline.js','assets/icons/icon-192.png']
    if has_math:core+=['assets/vendor/katex/katex.min.css','assets/vendor/katex/katex.min.js']+['assets/vendor/katex/fonts/'+f.name for f in sorted((katex_dir/'fonts').glob('*.woff2'))]
    pack_index,core_files,offline_total=site_features.write_offline(out,packs,core)
    render('offline',title='Study without a connection.',kind='offline',packs=pack_index,offline_total=offline_total)
    site_features.finish_offline(out,core_files,(ROOT/'templates/site/sw.js').read_text())
    assert collections.Counter(subject_seen)==collections.Counter(seen)==collections.Counter(paper_seen)
    (out/'build-report.json').write_text(json.dumps({'mode':'release' if args.release else 'private-preview','redrawn_questions':redrawn,'redrawn_by_paper':redrawn_by_paper,'questions':len(questions),'papers':len(papers),'subject_counts':counts,'limitations':issues,'original_crop_questions':len(crop_assets),'original_crop_parts':sum(map(len,crop_assets.values())),'topic_review_counts':dict(topic_review_counts),'topic_nonreviewed_ids':nonreviewed_topics},indent=2))
    print(f'Built {"RELEASE" if args.release else "PRIVATE PREVIEW"}: {len(questions)} questions, {len(papers)} papers, {len(groups)} subjects in {out}')
    print('\n'.join(issues))
if __name__=='__main__':main()
