#!/usr/bin/env python3
"""Generate local, explicitly labelled private-preview PDFs. No deployment."""
import argparse, asyncio, html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def document(subject, records, questions_only):
    title=subject.replace('-', ' ').title()
    blocks=[]
    by_id={q['question_id']:q for q in json.loads((ROOT/'data/questions.json').read_text())}
    answer_index=[]
    for row in records:
        body=row['html']
        q=by_id[row['id']]
        answer=q['official_answer'] if q['official_answer'] is not None else 'Independent / conditional: '+str(q['derived_answer'])
        answer_index.append('<li>'+html.escape(row['id'])+': '+html.escape(str(answer))+'</li>')
        body=re.sub(r'<a href="(?!https?://)[^"]*"[^>]*>(.*?)</a>',r'\1',body,flags=re.S)
        if questions_only:
            body=re.sub(r'<details\b[^>]*class="[^"]*answer[^\"]*"[^>]*>.*?</details>', '', body, flags=re.S)
        else:
            body=re.sub(r'<details\b', '<details open', body)
        body=re.sub(r'<button\b.*?</button>', '', body, flags=re.S)
        blocks.append(body)
    if questions_only:
        blocks.append('<section class="question"><h2>Answer index for self-checking</h2><p>Preserve all conditional interpretations and source qualifications; this is not an official key where none was located.</p><ol>'+''.join(answer_index)+'</ol></section>')
    note='Private working preview: per-question transcription status is shown. Original source links and discrepancy qualifications remain authoritative context. Accepted independently reviewed transcriptions are shown where available; other entries retain reviewed crops where enabled or paraphrases. This draft is not a visual verification certificate.'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape(title)+'</title><style>@page{size:A4;margin:18mm}body{font:11pt/1.45 sans-serif;color:#111}h1{font-size:24pt}h2{font-size:16pt}.cover{page-break-after:always}.question{break-before:page}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#204d76;overflow-wrap:anywhere}button,input,.practice{display:none}summary{font-weight:bold}img,svg{max-width:100%}p{orphans:3;widows:3}</style><link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/app.js"></script><body data-base="../"><section class="cover"><h1>'+html.escape(title)+'</h1><h2>'+('Questions only' if questions_only else 'Questions and solutions')+'</h2><p>'+note+'</p><p>'+str(len(records))+' entries. Unknown marks and unresolved answers are intentionally retained.</p></section>'+''.join(blocks)+'</body></html>'

async def run(args):
    out=ROOT/args.site
    report=json.loads((out/'build-report.json').read_text())
    if not args.preview:raise SystemExit('Final original-question PDF export is blocked until transcription/crop and rights gates are satisfied. Use --preview for local paraphrase drafts.')
    pdfdir=out/'pdf';pdfdir.mkdir(exist_ok=True)
    if args.html_only:
        count=0
        for subject in report['subject_counts']:
            if args.subject and subject!=args.subject:continue
            records=json.loads((out/subject/'index.json').read_text())
            for qo in (False,True):
                name=subject+('-questions' if qo else '')
                (pdfdir/(name+'.html')).write_text(document(subject,records,qo));count+=1
        print(f'Prepared {count} local print HTML drafts; no PDF rendering claimed.');return
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=args.chromium,headless=True,args=['--no-sandbox'])
        page=await browser.new_page()
        results=[]
        for subject in report['subject_counts']:
            if args.subject and subject!=args.subject:continue
            records=json.loads((out/subject/'index.json').read_text())
            for qo in (False,True):
                name=subject+('-questions' if qo else '')
                doc=document(subject,records,qo)
                htmlpath=pdfdir/(name+'.html')
                htmlpath.write_text(doc)
                await page.goto(htmlpath.as_uri(),wait_until='load')
                await page.evaluate('document.fonts.ready')
                path=pdfdir/(name+'.pdf')
                await page.pdf(path=str(path),format='A4',print_background=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;text-align:center">Private working preview · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',outline=True,tagged=True)
                results.append({'subject':subject,'questions_only':qo,'entries':len(records),'path':str(path.relative_to(out)),'bytes':path.stat().st_size,'status':'draft_rendered; visual_review_pending'})
        await browser.close()
    (out/'pdf-build-report.json').write_text(json.dumps(results,indent=2))
    print(f'Rendered {len(results)} draft PDFs; visual review remains required.')
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--preview',action='store_true');a.add_argument('--site',default='_site');a.add_argument('--subject');a.add_argument('--html-only',action='store_true');a.add_argument('--chromium',default='/usr/bin/chromium');asyncio.run(run(a.parse_args()))
