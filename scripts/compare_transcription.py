#!/usr/bin/env python3
"""Create a local, escaped comparison aid, never a verification certificate.

Shows exact stored transcription text (including markup) so no untrusted HTML
executes. Figures are linked only when their paths stay inside the repository.
Run render_crops.py first, --allow-draft for private draft review only.
"""
import argparse, html, json, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('paper_id');args=ap.parse_args()
    questions=[q for q in json.loads((ROOT/'data/questions.json').read_text()) if q['paper_id']==args.paper_id]
    if not questions:ap.error('Unknown paper ID')
    source=ROOT/'data/transcriptions'/f'{args.paper_id}.json'
    trans=json.loads(source.read_text()) if source.exists() else {}
    assetfile=ROOT/'site-assets/q/manifest.json';assets=json.loads(assetfile.read_text()) if assetfile.exists() else {}
    out=ROOT/'audits/compare'/f'{args.paper_id}.html';out.parent.mkdir(parents=True,exist_ok=True)
    esc=lambda s:html.escape(str(s),quote=True)
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Draft transcription comparison</title><style>body{font:16px system-ui;margin:2rem}article{display:grid;grid-template-columns:1fr 1fr;gap:1rem;border-top:1px solid;padding:1rem 0}img{max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere}@media(max-width:700px){article{display:block}}</style><h1>'+esc(args.paper_id)+'</h1><p>Private review aid. No item is verified by generating this page. Check every symbol, option and figure against the full source; crops may be incomplete. Transcription markup below is shown literally.</p>']
    for q in questions:
        qid=q['question_id'];t=trans.get(qid);imgs=[]
        for a in assets.get(qid,[]):
            path=ROOT/'site-assets/q'/a['file']
            if path.is_file():imgs.append('<p>Crop status: '+esc(a.get('status','unknown'))+'</p><img alt="'+esc(qid)+' source crop" src="'+esc(os.path.relpath(path,out.parent))+'">')
        right='<p>No transcription yet.</p>' if not t else '<p>Status: '+esc(t.get('status','draft'))+'</p><pre>'+esc(t.get('stem',''))+'\n\n'+esc(json.dumps(t.get('options',{}),ensure_ascii=False,indent=2))+'</pre><p>'+esc(t.get('notes',''))+'</p>'
        for figure in (t or {}).get('figures',[]):
            path=(ROOT/figure).resolve()
            if path.is_relative_to(ROOT) and path.is_file():right+='<p><a href="'+esc(os.path.relpath(path,out.parent))+'">Inspect figure source/render: '+esc(figure)+'</a></p>'
        parts.append('<h2>'+esc(qid)+'</h2><article><div>'+(''.join(imgs) or '<p>No rendered crop available.</p>')+'</div><div>'+right+'</div></article>')
    out.write_text(''.join(parts)+'</html>');print(out)
if __name__=='__main__':main()
