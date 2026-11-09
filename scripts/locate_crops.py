#!/usr/bin/env python3
"""Prepare conservative, unverified crop proposals. Never certifies source fidelity.

Local PDFs are matched by SHA-256, not filename. Nothing is downloaded or copied
into the publication. --ocr enables Tesseract on pages lacking embedded text.
"""
import argparse, collections, hashlib, json, re, subprocess, tempfile, zipfile
from pathlib import Path
import fitz
ROOT = Path(__file__).resolve().parents[1]
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--search-root',action='append',default=['/tmp','/workspace/shared'])
    ap.add_argument('--archive',default='/tmp/gate-official-CS.zip')
    ap.add_argument('--cache',default='/tmp/gate-crop-source-cache')
    ap.add_argument('--ocr',action='store_true')
    args=ap.parse_args()
    existing=ROOT/'data/crops.json'
    if existing.exists() and any((e.get('status')=='verified' or e.get('method','').startswith('manual') or e.get('review_status')) for es in json.loads(existing.read_text()).values() for e in es):
        raise SystemExit('Refusing to overwrite reviewed crops; merge new proposals separately.')
    qs=json.loads((ROOT/'data/questions.json').read_text()); manifest=json.loads((ROOT/'sources/manifest.json').read_text())
    wanted={q.get('source_file_sha256') for q in qs} | {v.get('sha256') for v in manifest['files'].values()}; index={}; errors=[]; archive_hashes={}
    for root in args.search_root:
        for path in Path(root).rglob('*.pdf'):
            try:
                sha=digest(path)
                if sha in wanted:index.setdefault(sha,str(path.resolve()))
            except OSError:pass
    cache=Path(args.cache); cache.mkdir(parents=True,exist_ok=True)
    members=sorted({q['source_archive_member'] for q in qs if q.get('source_archive_member')})
    if Path(args.archive).is_file():
        with zipfile.ZipFile(args.archive) as archive:
            for member in members:
                try:
                    content=archive.read(member); sha=hashlib.sha256(content).hexdigest()
                    path=cache/(sha+'.pdf'); path.write_bytes(content)
                    archive_hashes[member]=sha; index.setdefault(sha,str(path))
                except KeyError:errors.append({'member':member,'error':'Missing archive member'})
    docs={}; sources={}; crops={}; textcache={}; counts=collections.Counter(); bypaper=collections.defaultdict(collections.Counter)
    for q in qs:
        member=q.get('source_archive_member'); url=q['source_url'].split('#')[0]
        expected=q.get('source_file_sha256') or manifest.get('files',{}).get(url,{}).get('sha256')
        sha=expected or archive_hashes.get(member)
        logical=('sources/archive/'+member) if member else manifest.get('files',{}).get(url,{}).get('path','sources/by-sha256/'+str(sha)+'.pdf')
        if logical not in sources:
            item={'url':url,'archive_member':member,'sha256':sha,'local_path':index.get(sha),'status':'missing','source_provenance':q.get('source_provenance'),'original_source_verified':False,'hash_basis':'record_or_manifest' if expected else 'local_archive_member_only'}
            if sha in index:
                try:
                    fitz.TOOLS.mupdf_warnings(reset=True)
                    doc=fitz.open(index[sha]); docs[sha]=doc
                    if not doc.is_pdf or doc.is_encrypted or not len(doc):raise ValueError('Unreadable/encrypted/empty PDF')
                    item.update(status='hash_verified_parseable',pages=len(doc),text_pages=sum(bool(p.get_text().strip()) for p in doc))
                    warnings=fitz.TOOLS.mupdf_warnings(reset=True)
                    if warnings:item['parse_warnings']=warnings
                except Exception as exc:item.update(status='parse_failed',error=str(exc))
            sources[logical]=item
        doc=docs.get(sha); entries=[]
        pages=q.get('source_pages') or [q.get('source_page')]
        for page_no in sorted(set(pages)):
            if doc is None or not isinstance(page_no,int) or not 1<=page_no<=len(doc):
                counts['unresolved_page_entries']+=1;continue
            page=doc[page_no-1]; key=(sha,page_no); method='page_fallback'
            if key not in textcache:
                lines=[]
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        lines.append((''.join(s['text'] for s in line['spans']),line['bbox']))
                if not lines and args.ocr:
                    with tempfile.TemporaryDirectory() as td:
                        png=Path(td)/'page.png';page.get_pixmap(matrix=fitz.Matrix(2,2)).save(png)
                        out=subprocess.run(['tesseract',str(png),'stdout','tsv'],capture_output=True,text=True,check=True).stdout
                        import csv,io
                        grouped=collections.defaultdict(list)
                        for row in csv.DictReader(io.StringIO(out),delimiter='\t'):
                            if row.get('text','').strip():grouped[(row['block_num'],row['par_num'],row['line_num'])].append(row)
                        for rows in grouped.values():
                            x=min(int(r['left']) for r in rows)/2;y=min(int(r['top']) for r in rows)/2
                            xx=max(int(r['left'])+int(r['width']) for r in rows)/2;yy=max(int(r['top'])+int(r['height']) for r in rows)/2
                            lines.append((' '.join(r['text'] for r in rows),(x,y,xx,yy)))
                textcache[key]=lines
            lines=textcache[key]; number=str(q.get('printed_question_number') or q['source_question_number'])
            pattern=re.compile(r'^\s*(?:Q\s*\.?\s*)?'+re.escape(number)+r'(?:\s|[.):])',re.I)
            found=[box for text,box in lines if pattern.search(text) and not re.search(r'Q\.?\s*\d+\s*[–—-]\s*Q\.?\s*\d+|carry.*marks?',text,re.I)]
            bbox=list(page.rect); flags=['visual_review_required','header_footer_unreviewed','figure_completeness_unreviewed']
            if found and page_no==min(pages) and not q.get('shared_context'):
                start=min(b[1] for b in found)
                following=[b[1] for t,b in lines if b[1]>start+4 and re.match(r'^\s*(?:Q\s*\.?\s*)?\d+(?:\.\d+)?[.)]?\s',t)]
                # This is a proposal only: list numbers/code may resemble markers.
                bbox=[0,max(0,start-4),page.rect.width,min(following)-2 if following else page.rect.height]
                method='text_marker_candidate' if page.get_text().strip() else 'ocr_marker_candidate'
            else:flags.append('full_page_fallback')
            if sources[logical].get('parse_warnings'):flags.append('source_parse_warning_check_missing_figures')
            if q.get('shared_context'):flags.append('shared_context_preserved_full_page')
            if len(pages)>1:flags.append('multipart_boundary_review_required')
            entries.append({'file':logical,'page':page_no,'bbox':[round(v,2) for v in bbox],'status':'draft','method':method,'number_detected':bool(found),'flags':flags})
            counts[method]+=1
        crops[q['question_id']]=entries
        state='candidate' if len(entries)==len(set(pages)) else 'unresolved'
        counts[state+'_questions']+=1;bypaper[q['paper_id']][state]+=1
    # Overlap is not silently clipped: shared stems and multipart items legitimately overlap.
    groups=collections.defaultdict(list)
    for qid,entries in crops.items():
        for entry in entries:groups[(entry['file'],entry['page'])].append((qid,entry))
    overlap_pairs=0
    for entries in groups.values():
        for i,(qa,a) in enumerate(entries):
            for qb,b in entries[i+1:]:
                if qa!=qb and not (fitz.Rect(a['bbox']) & fitz.Rect(b['bbox'])).is_empty:
                    overlap_pairs+=1
                    for e in (a,b):
                        if 'overlap_review_required' not in e['flags']:e['flags'].append('overlap_review_required')
    counts['overlap_pairs']=overlap_pairs;counts['verified_questions']=0;counts['pending_visual_review_questions']=len(qs)
    dump(ROOT/'data/crops.json',crops)
    local_paths={name:info.pop('local_path',None) for name,info in sources.items()}
    dump(ROOT/'.local-source-cache/source-paths.json',local_paths)
    dump(ROOT/'audits/crop-source-map.json',{'schema_version':1,'sources':sources,'errors':errors})
    dump(ROOT/'audits/crop-summary.json',{'counts':dict(counts),'papers':bypaper,'source_count':len(sources),'resolved_sources':sum(s['status']=='hash_verified_parseable' for s in sources.values())})
    print(json.dumps(dict(counts),indent=2))
if __name__=='__main__':main()
