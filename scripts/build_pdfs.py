#!/usr/bin/env python3
"""Generate the two PDFs per subject (with answers; questions only). --release for the public site, --preview for local drafts."""
import argparse, asyncio, html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

TITLES = ['Digital Logic','Computer Organization & Architecture','Programming in C','Data Structures','Algorithms','Theory of Computation','Compiler Design','Operating Systems','Database Management Systems','Computer Networks','General Aptitude','Discrete Mathematics','Engineering Mathematics & Other Topics']

PDF_CSS = """@page{size:A4;margin:16mm 15mm 18mm}
body{font:10.5pt/1.45 'Inter','Helvetica Neue',Arial,sans-serif;color:#111;background:#fff}
h1{font-size:26pt;letter-spacing:-.02em;margin:0 0 6pt}h2.topic{font-size:15pt;margin:0 0 10pt;padding-bottom:4pt;border-bottom:2px solid #006a51;color:#006a51;break-before:page}
h3.qhead{font-size:11pt;margin:0 0 4pt;color:#006a51}
.cover{break-after:page;padding-top:60mm}.cover .sub{font-size:13pt;color:#444}.cover p{max-width:150mm}
.toc{break-after:page}.toc ol{list-style:none;padding:0}.toc li{display:flex;gap:8pt;padding:3pt 0;border-bottom:1px dotted #bbb}.toc li span:first-child{flex:1}
.question{border:none;border-top:1px solid #ccc;border-radius:0;padding:10pt 0 4pt;margin:0;background:none;break-inside:auto}
.question-meta,.question-tools,.practice,.js-only,button,details.provenance,details.text-version,.view-original>summary{display:none!important}
.qtitle{font-weight:650;margin:2pt 0}.eyebrow{font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:#666;margin:0 0 4pt}
.original-source h3,.original-source .h,.original-source .source-note{display:none}.original-source figure{margin:4pt 0;break-inside:avoid}
.original-source img{max-width:100%;max-height:235mm;width:auto;height:auto;border:1px solid #ddd}
figcaption,.source-note{font-size:7.5pt;color:#666}
details{border:none;padding:0;margin:4pt 0}summary{list-style:none;font-weight:700;color:#006a51}summary::-webkit-details-marker{display:none}
.answer{background:#f4f8f5;border-left:3px solid #006a51;padding:6pt 9pt;margin-top:6pt}.answer .h{font-weight:700;margin:6pt 0 2pt}
.discrepancy{background:#fff4d6;border-left:3px solid #b58100;padding:5pt 8pt;margin:6pt 0;font-size:9pt}.discrepancy .h{font-weight:700}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:8.5pt;background:#f6f6f6;padding:6pt}a{color:#204d76;text-decoration:none}
p{margin:3pt 0;orphans:3;widows:3}.answers-index{break-before:page}.answers-index table{border-collapse:collapse;width:100%;font-size:8.5pt}.answers-index td,.answers-index th{border:1px solid #ccc;padding:3pt 5pt;text-align:left;vertical-align:top}
"""

def _strip_headings(body):
    """Keep bookmarks to subject > topic > question: demote headings inside a question."""
    body=re.sub(r'<h2>(.*?)</h2>', r'<div class="qtitle">\1</div>', body, flags=re.S)
    body=re.sub(r'<h3>(.*?)</h3>', r'<div class="h">\1</div>', body, flags=re.S)
    return body

def document(subject, records, questions_only, release=False):
    title=TITLES[int(subject[:2])-1]
    by_id={q['question_id']:q for q in json.loads((ROOT/'data/questions.json').read_text())}
    topics=json.loads((ROOT/'data/topics.json').read_text()).get(subject,{})
    topic_title={t['id']:t['title'] for t in topics.get('topics',[])}
    assign=topics.get('assign',{})
    sections=[];toc=[];index_rows=[];current=None;n=0
    for row in records:
        n+=1;q=by_id[row['id']]
        meta=re.search(r'<div class="question-meta">.*?<span>\((.*?)\)</span>\s*<span>(.*?)</span>',row['html'],re.S)
        label=html.unescape(meta.group(1)) if meta else row['id'];marks=html.unescape(meta.group(2)) if meta else ''
        tid=assign.get(row['id'],'other')
        if tid!=current:
            current=tid;anchor='topic-'+tid
            toc.append([topic_title.get(tid,tid),anchor,n,n])
            sections.append(f'<h2 class="topic" id="{anchor}">{html.escape(topic_title.get(tid,tid))}</h2>')
        toc[-1][3]=n
        body=row['html']
        body=re.sub(r'<a href="(?!https?://)[^"]*"[^>]*>(.*?)</a>',r'\1',body,flags=re.S)
        if questions_only:
            body=re.sub(r'<details\b[^>]*class="[^"]*answer[^"]*"[^>]*>.*?</details>','',body,flags=re.S)
        else:
            body=re.sub(r'<details\b','<details open',body)
        body=re.sub(r'<button\b.*?</button>','',body,flags=re.S)
        body=body.replace(' loading="lazy"','').replace(' · tap to enlarge','')
        body=_strip_headings(body)
        head=f'<h3 class="qhead">Q{n}. ({html.escape(label)}) · {html.escape(marks)}{" · ⚠ discrepancy" if q["discrepancy_ids"] else ""}</h3>'
        sections.append(head+body)
        key=q['official_answer'] if q['official_answer'] is not None else '—'
        ours='' if (q['official_answer'] is not None and str(q['derived_answer'])==str(q['official_answer'])) else str(q['derived_answer'])
        index_rows.append(f'<tr><td>Q{n}</td><td>{html.escape(label)}</td><td>{html.escape(str(key))}</td><td>{html.escape(ours[:160])}</td></tr>')
    if questions_only:
        sections.append('<section class="answers-index"><h2 class="topic" id="answers">Answer index</h2><p>Official key where one exists; otherwise (or where it differs) our independently derived answer. Full solutions are in the with-answers PDF.</p><table><thead><tr><th>#</th><th>Question</th><th>Official key</th><th>Our answer (if different / no key)</th></tr></thead><tbody>'+''.join(index_rows)+'</tbody></table></section>')
    toc_html='<section class="toc"><h2>Contents</h2><ol>'+''.join(f'<li><span><a href="#{a}">{html.escape(t)}</a></span><span>Q{s}–Q{e}</span></li>' for t,a,s,e in toc)+('<li><span><a href="#answers">Answer index</a></span><span></span></li>' if questions_only else '')+'</ol></section>'
    kind='Questions only' if questions_only else 'Questions, answers and detailed solutions'
    from datetime import date
    note=('Each question shows the original from the source paper where available, otherwise a paraphrase with the source page. '
          'Official keys are shown exactly as published; where none was found, the answer is independently derived and marked as such. '
          'Discrepancies between the key and our working are flagged with ⚠ and explained.')
    if not release:note='Private working preview. '+note
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape('GATE CS · '+title)+'</title>'
            '<link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css">'
            '<script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/app.js"></script>'
            '<style>'+PDF_CSS+'</style><body data-base="../">'
            '<section class="cover"><p class="sub">GATE Computer Science · 1991–2026</p><h1>'+html.escape(title)+'</h1><p class="sub">'+kind+'</p>'
            '<p>'+str(len(records))+' questions grouped by topic, newest first within each topic. Year and paper are shown in brackets for every question.</p><p>'+note+'</p>'
            '<p class="source-note">Generated '+date.today().isoformat()+' · https://sathiyarajs.github.io/gate-pyq/</p></section>'
            +toc_html+''.join(sections)+'</body></html>')

def pdf_images(out):
    """Smaller grayscale copies of the question images, used only inside PDFs.

    Site images are 216 DPI WebP; Chromium re-encodes them losslessly, which makes
    each subject PDF ~60 MB. 150 DPI, 16 grey levels, PNG keeps text sharp at a
    fraction of the size.
    """
    from PIL import Image
    src=out/'assets/questions';dst=ROOT/'.pdf-images';dst.mkdir(exist_ok=True)
    for f in src.glob('*.webp'):
        target=dst/(f.stem+'.png')
        if target.exists() and target.stat().st_mtime>=f.stat().st_mtime:continue
        im=Image.open(f).convert('L');w,h=im.size;scale=150/216
        im=im.resize((max(1,round(w*scale)),max(1,round(h*scale))),Image.LANCZOS)
        im.quantize(16).save(target,optimize=True)
    return dst

async def run(args):
    out=ROOT/args.site
    report=json.loads((out/'build-report.json').read_text())
    if not args.preview and not args.release:raise SystemExit('Use --release (public build) or --preview (local draft).')
    pdfdir=out/'pdf';pdfdir.mkdir(exist_ok=True)
    if args.html_only:
        count=0
        for subject in report['subject_counts']:
            if args.subject and subject!=args.subject:continue
            records=json.loads((out/subject/'index.json').read_text())
            for qo in (False,True):
                name=subject+('-questions' if qo else '')
                (pdfdir/(name+'.html')).write_text(document(subject,records,qo,args.release));count+=1
        print(f'Prepared {count} local print HTML drafts; no PDF rendering claimed.');return
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=args.chromium if args.chromium and Path(args.chromium).is_file() else None,headless=True,args=['--no-sandbox'])
        page=await browser.new_page();imgdir=pdf_images(out)
        results=[]
        for subject in report['subject_counts']:
            if args.subject and subject!=args.subject:continue
            records=json.loads((out/subject/'index.json').read_text())
            for qo in (False,True):
                name=subject+('-questions' if qo else '')
                doc=document(subject,records,qo,args.release)
                doc=re.sub(r'src="\.\./assets/questions/([^"]+)\.webp"',lambda m:'src="'+(imgdir/(m.group(1)+'.png')).as_uri()+'"',doc)
                htmlpath=pdfdir/(name+'.html')
                htmlpath.write_text(doc)
                await page.goto(htmlpath.as_uri(),wait_until='networkidle')
                await page.evaluate('document.fonts.ready')
                path=pdfdir/(name+'.pdf')
                await page.pdf(path=str(path),format='A4',print_background=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#666">'+('' if args.release else 'Private working preview · ')+'GATE CS · '+html.escape(TITLES[int(subject[:2])-1])+(' · questions only' if qo else '')+' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',outline=True,tagged=True)
                results.append({'subject':subject,'questions_only':qo,'entries':len(records),'path':str(path.relative_to(out)),'bytes':path.stat().st_size,'status':'release' if args.release else 'draft_rendered; visual_review_pending'})
        await browser.close()
    (out/'pdf-build-report.json').write_text(json.dumps(results,indent=2))
    print(f'Rendered {len(results)} PDFs: '+', '.join(f"{r['path']} {r['bytes']//1048576} MB" for r in results))
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--preview',action='store_true');a.add_argument('--release',action='store_true');a.add_argument('--site',default='_site');a.add_argument('--subject');a.add_argument('--html-only',action='store_true');a.add_argument('--chromium',default=None,help="Chromium binary; defaults to Playwright's bundled browser");asyncio.run(run(a.parse_args()))
