#!/usr/bin/env python3
"""Build locally: python scripts/build_site.py --preview. Default is fail-closed release."""
import argparse, collections, html, json, math, re, shutil
from pathlib import Path
from urllib.parse import quote, urlparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
ROOT = Path(__file__).resolve().parents[1]
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

def discrepancies():
    rows={}
    for line in (ROOT/'DISCREPANCIES.md').read_text().splitlines():
        if line.startswith('| CS-'):
            cols=[x.strip().replace('\\|','|') for x in re.split(r'(?<!\\)\|',line)[1:-1]]
            if len(cols)==9: rows[cols[0]]=dict(zip(['id','subject','year','number','type','summary','official','derived','status'],cols))
    return rows

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--preview',action='store_true');ap.add_argument('--output',default='_site');args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if out == ROOT or ROOT not in out.parents: raise SystemExit('Output must be a subdirectory of repository')
    questions=load(ROOT/'data/questions.json'); papers=load(ROOT/'data/papers.json'); topics=load(ROOT/'data/topics.json',{}); ds=discrepancies()
    pmap={p['paper_id']:p for p in papers}; groups=collections.defaultdict(list); issues=[]
    seen=set()
    for q in questions:
        if q['question_id'] in seen: raise SystemExit('Duplicate question ID')
        q.setdefault('question_title', q['question_id'])
        if not re.fullmatch(r'[A-Za-z0-9_-]+',q['question_id']) or not re.fullmatch(r'[A-Za-z0-9_-]+',q['paper_id']):raise SystemExit('Unsafe identifier')
        seen.add(q['question_id']); subject=q['subject'] if q['subject']!='excluded' else '13-other-topics'
        q['subject_dir']=subject;q['year']=pmap[q['paper_id']]['year'];q['display_type']=q['question_type'].upper() if q['question_type'].upper() in ('MCQ','MSQ','NAT') else ('Descriptive' if q['question_type'].lower() in ('descriptive','short-answer') else 'Other')
        q['number']=q.get('printed_question_number') or q['source_question_number'];q['session']=q.get('official_session') or pmap[q['paper_id']].get('exam_session') or ''
        if not q['session'] and re.search(r'-S\d+$',q['paper_id']): q['session']='CS'+q['paper_id'][-1]
        q['source_link']=safe_url(q.get('source_page_url') or q.get('source_url'));q['key_link']=safe_url(q.get('key_url'))
        if q['key_link'] and q.get('key_page') and '#' not in q['key_link']:q['key_link']+='#page='+str(q['key_page'])
        q['topic']=topics.get(subject,{}).get('assign',{}).get(q['question_id'],'unreviewed')
        q['discrepancies']=[]
        for did in q['discrepancy_ids']:
            if did not in ds: raise SystemExit('Missing discrepancy row: '+did)
            q['discrepancies'].append(ds[did])
        q['options_data']=q.get('options') or q.get('question_options') or None
        # Options are never invented. A paraphrase often omits the original option set.
        q['practice_key']=str(q['official_answer']) if q['official_answer'] is not None else ''
        q['permalink']='q/'+q['question_id']+'/'
        q['report']='https://github.com/SathiyarajS/gate-pyq/issues/new?'+ 'title='+quote('['+q['question_id']+'] ')+'&body='+quote('Question: https://sathiyarajs.github.io/gate-pyq/'+q['permalink']+'\n\nDescribe the issue and cite the source page:\n')
        groups[subject].append(q)
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
    # Preview intentionally does not publish unverified crops or transcriptions.
    issues.append('Original question crops and redraw verification are not yet complete; all displayed question text is a paraphrase preview.')
    katex_dir=ROOT/'node_modules/katex/dist'
    has_math=(katex_dir/'katex.min.js').is_file() and (katex_dir/'katex.min.css').is_file()
    if not has_math:issues.append('Mathematical typesetting assets are unavailable; explicit LaTeX is preserved as text. Run npm ci to provision pinned local assets.')
    issues.append('PDF verification and Pagefind indexing must be run and checked separately after this build.')
    if not args.preview:raise SystemExit('Release blocked:\n- '+'\n- '.join(issues))
    out.mkdir(parents=True,exist_ok=True)
    if has_math:
        shutil.copytree(katex_dir,out/'assets/vendor/katex',dirs_exist_ok=True)
        shutil.copy2(ROOT/'node_modules/katex/LICENSE',out/'assets/vendor/katex/LICENSE')
    shutil.copytree(ROOT/'site-static',out/'assets',dirs_exist_ok=True)
    env=Environment(loader=FileSystemLoader(ROOT/'templates/site'),autoescape=select_autoescape(['html']));env.filters['rich']=rich
    counts={s:len(qs) for s,qs in groups.items()};titles={s:TITLES[int(s[:2])-1] for s in groups}
    cards=[dict(slug=s,title=titles[s],count=counts[s],topics=len(topics.get(s,{}).get('topics',[]))) for s in sorted(groups)]
    def render(path,**ctx):
        target=out/path/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
        prefix='../'*len(Path(path).parts) if path else './'
        target.write_text(env.get_template('page.html').render(prefix=prefix,cards=cards,issues=issues,preview=True,has_math=has_math,**ctx))
    def sortkey(q):return (-q['year'],q['paper_id'],tuple(int(n) for n in re.findall(r'\d+',q['source_question_number'])))
    search=[];canonical={};subject_seen=[];paper_seen=[]
    for subject,qs in sorted(groups.items()):
        topic_list=topics.get(subject,{}).get('topics',[]) or [{'id':'unreviewed','title':'Draft grouping: topic review pending'}]
        allowed={t['id'] for t in topic_list}
        if any(not re.fullmatch(r'[a-zA-Z0-9_-]+',tid) for tid in allowed):raise SystemExit('Unsafe topic identifier')
        invalid=[q['question_id'] for q in qs if q['topic'] not in allowed]
        if invalid and allowed!={'unreviewed'}:raise SystemExit('Invalid topic IDs: '+str(invalid[:5]))
        order={t['id']:i for i,t in enumerate(topic_list)};qs.sort(key=lambda q:(order.get(q['topic'],999),sortkey(q)))
        for i,q in enumerate(qs,1):q['ordinal']=i;q['topic_title']=next((t['title'] for t in topic_list if t['id']==q['topic']),'Unreviewed')+' · '+('reviewed grouping' if q['topic_review_status']=='reviewed' else 'candidate grouping')
        heat=[{'title':t['title'],'cells':[sum(q['topic']==t['id'] and q['year']==y for q in qs) for y in range(1991,2027)]} for t in topic_list]
        for i in range(math.ceil(len(qs)/10)):
            path=subject if i==0 else f'{subject}/page/{i+1}'
            pageqs=qs[i*10:(i+1)*10]
            nav=[(n+1,subject+'/' if n==0 else f'{subject}/page/{n+1}/') for n in range(math.ceil(len(qs)/10))]
            render(path,title=titles[subject],kind='subject',questions=pageqs,subject=subject,topics=topic_list,nav=nav,current=i+1,total=len(qs),heat=heat)
            for q in pageqs:canonical[q['question_id']]=path+'/#'+q['question_id'];subject_seen.append(q['question_id'])
        for t in topic_list:
            tqs=[q for q in qs if q['topic']==t['id']]
            for i in range(max(1,math.ceil(len(tqs)/10))):
                base=f'{subject}/topic/{t["id"]}';path=base if i==0 else base+f'/page/{i+1}'
                nav=[(n+1,base+'/' if n==0 else base+f'/page/{n+1}/') for n in range(max(1,math.ceil(len(tqs)/10)))]
                render(path,title=titles[subject]+' · '+t['title'],kind='topic',questions=tqs[i*10:(i+1)*10],subject=subject,topics=topic_list,nav=nav,current=i+1,total=len(tqs))
        # HTML fragments generated by the same safe autoescaped template as static pages.
        records=[]
        for q in qs:
            fragment=env.get_template('question.html').render(q=q,prefix='../',paper_view=False)
            records.append(dict(id=q['question_id'],year=q['year'],marks=q.get('marks'),type=q['display_type'],discrepancy=bool(q['discrepancy_ids']),html=fragment))
            search.append(dict(id=q['question_id'],title=q['question_title'],text=q['question_text'],year=q['year'],subject=titles[subject],type=q['display_type'],url=q['permalink']))
        (out/subject/'index.json').write_text(json.dumps(records,ensure_ascii=False))
    for paper in papers:
        qs=[q for q in questions if q['paper_id']==paper['paper_id']];qs.sort(key=lambda q:tuple(int(n) for n in re.findall(r'\d+',q['source_question_number'])))
        paper_seen.extend(q['question_id'] for q in qs)
        render('papers/'+paper['paper_id'],title=paper['paper_id'],kind='paper',questions=qs,paper_view=True,total=len(qs))
    for qid,target in canonical.items():render('q/'+qid,title=qid,kind='redirect',target=target)
    render('',title='Practice with provenance.',kind='home',total=len(questions))
    render('papers',title='All papers',kind='papers',papers=sorted(papers,key=lambda p:p['paper_id'],reverse=True))
    render('about',title='Know what you are studying.',kind='about')
    render('discrepancies',title='Discrepancies & interpretations',kind='discrepancies',discrepancy_groups=[(titles[s],[q for q in qs if q['discrepancy_ids']]) for s,qs in sorted(groups.items())])
    (out/'search.json').write_text(json.dumps(search,ensure_ascii=False))
    for item in search:
        render('search-docs/'+item['id'],title=item['title'],kind='searchdoc',item=item)
    assert collections.Counter(subject_seen)==collections.Counter(seen)==collections.Counter(paper_seen)
    (out/'build-report.json').write_text(json.dumps({'mode':'private-preview','questions':len(questions),'papers':len(papers),'subject_counts':counts,'limitations':issues,'topic_review_counts':dict(topic_review_counts),'topic_nonreviewed_ids':nonreviewed_topics},indent=2))
    print(f'Built PRIVATE PREVIEW: {len(questions)} questions, {len(papers)} papers, {len(groups)} subjects in {out}')
    print('\n'.join(issues))
if __name__=='__main__':main()
