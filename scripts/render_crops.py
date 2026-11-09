#!/usr/bin/env python3
"""Render reviewed crops at 216 DPI. Draft rendering requires explicit opt-in.
Output metadata includes dimensions and status. Local source paths are resolved
through the audit map; SHA-256 is rechecked before any rendering.
"""
import argparse, hashlib, json
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--allow-draft',action='store_true');ap.add_argument('--question',action='append')
    ap.add_argument('--source-cache',default=str(ROOT/'.local-source-cache/source-paths.json'))
    ap.add_argument('--output',default=str(ROOT/'site-assets/q'));ap.add_argument('--scale',type=float,default=3)
    args=ap.parse_args()
    if args.scale<=0:ap.error('--scale must be positive')
    crops=json.loads((ROOT/'data/crops.json').read_text()); sources=json.loads((ROOT/'audits/crop-source-map.json').read_text())['sources']
    cache=Path(args.source_cache);local_paths=json.loads(cache.read_text()) if cache.is_file() else {}
    selected=args.question or list(crops);docs={}; jobs=[]
    # Preflight all jobs before emitting any image.
    for qid in selected:
        if qid not in crops or not crops[qid]:raise SystemExit(f'{qid}: missing crops')
        for n,crop in enumerate(crops[qid],1):
            if crop.get('status')!='verified' and not args.allow_draft:raise SystemExit(f'{qid}: draft crop; visual QA required (local preview: --allow-draft)')
            info=sources[crop['file']]; path=ROOT/crop['file']
            if not path.is_file():path=Path(local_paths.get(crop['file']) or '/missing-source')
            if crop['file'] not in docs:
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=info['sha256']:raise SystemExit(f'{qid}: missing or changed source')
                docs[crop['file']]=fitz.open(path)
            doc=docs[crop['file']]
            if not 1<=crop['page']<=len(doc):raise SystemExit(f'{qid}: invalid page')
            page=doc[crop['page']-1];box=fitz.Rect(crop['bbox'])
            tolerance=fitz.Rect(page.rect.x0-.02,page.rect.y0-.02,page.rect.x1+.02,page.rect.y1+.02)
            if box.is_empty or box.is_infinite or not tolerance.contains(box):raise SystemExit(f'{qid}: invalid bounds')
            box=box & page.rect
            jobs.append((qid,n,crop,page,box))
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    previous=output/'manifest.json'
    assets=json.loads(previous.read_text()) if args.question and previous.exists() else {}
    for qid in selected:assets.pop(qid,None)
    for qid,n,crop,page,box in jobs:
        pix=page.get_pixmap(matrix=fitz.Matrix(args.scale,args.scale),clip=box,alpha=False)
        img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);name=f'{qid}-{n}.webp'
        try:img.save(output/name,'WEBP',quality=80)
        except (KeyError,OSError):name=f'{qid}-{n}.png';img.save(output/name,'PNG')
        assets.setdefault(qid,[]).append({'file':name,'width':pix.width,'height':pix.height,'status':crop['status'],'page':crop['page']})
    (output/'manifest.json').write_text(json.dumps(assets,indent=2)+'\n');print(f'Rendered {len(jobs)} images for {len(assets)} questions')
if __name__=='__main__':main()
