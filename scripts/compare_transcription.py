#!/usr/bin/env python3
"""Render a private side-by-side review aid, never a verification certificate.

Uses the production safe transcription renderer, including drafts. No content is
promoted by this command. Render crops separately before reviewing every symbol.
"""
import argparse
import html
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from transcription import load_paper, render_entry, resolve

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paper_id')
    args = ap.parse_args()
    questions = [q for q in json.loads((ROOT / 'data/questions.json').read_text()) if q['paper_id'] == args.paper_id]
    if not questions: ap.error('Unknown paper ID')
    trans = load_paper(ROOT, args.paper_id)
    assetfile = ROOT / 'site-assets/q/manifest.json'
    assets = json.loads(assetfile.read_text()) if assetfile.exists() else {}
    out = ROOT / 'audits/compare' / f'{args.paper_id}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    esc = lambda s: html.escape(str(s), quote=True)
    local = lambda path: esc(os.path.relpath(path, out.parent))
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Private transcription comparison</title><link rel="stylesheet" href="' + local(ROOT / 'site-static/style.css') + '"><style>body{display:block;margin:1rem}article{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1rem;border-top:1px solid;padding:1rem 0}article>div{min-width:0}img{max-width:100%;height:auto;background:white}pre{white-space:pre-wrap;overflow-wrap:anywhere}@media(max-width:700px){article{display:block}}</style>']
    katex = ROOT / 'node_modules/katex/dist'
    if (katex / 'katex.min.js').is_file():
        parts.append('<link rel="stylesheet" href="' + local(katex / 'katex.min.css') + '"><script defer src="' + local(katex / 'katex.min.js') + '"></script><script defer src="' + local(ROOT / 'site-static/app.js') + '"></script>')
    parts.append('</head><body data-base="../../"><h1>' + esc(args.paper_id) + '</h1><p>Private review aid, not a verification certificate. Drafts are rendered here but are never promoted to verified by this command. Compare every number, symbol, option, label and edge, check full source pages for crop omissions, and confirm that the existing solution still matches.</p>')
    if not (katex / 'katex.min.js').is_file(): parts.append('<p>Local KaTeX unavailable: original LaTeX remains visible. Typeset math review is pending.</p>')
    for q in questions:
        qid = q['question_id']; entry = trans.get(qid); imgs = []
        for a in assets.get(qid, []):
            name = a.get('file', '')
            if not name or Path(name).name != name: continue
            path = ROOT / 'site-assets/q' / name
            if path.is_file(): imgs.append('<p>Crop status: ' + esc(a.get('status', 'unknown')) + ' · source page ' + esc(a.get('page', '?')) + '</p><a href="' + local(path) + '"><img loading="lazy" alt="' + esc(qid) + ' source crop" src="' + local(path) + '"></a>')
        right = '<p>No transcription yet.</p>'
        if entry:
            try:
                right = '<p>Stored status: ' + esc(entry.get('status', 'draft')) + ' · accepted for site display: ' + ('yes' if resolve(ROOT, q, trans) else 'no') + '</p><section class="transcription">' + str(render_entry(ROOT, entry, trans.get('_contexts', {}))) + '</section><p>Review notes: ' + esc(entry.get('notes', '')) + '</p><details><summary>Stored transcription and review metadata</summary><pre>' + esc(json.dumps(entry, ensure_ascii=False, indent=2)) + '</pre></details>'
            except (ValueError, TypeError, KeyError, OSError, ET.ParseError) as error:
                right = '<p>Cannot safely render this entry: ' + esc(error) + '</p>'
        parts.append('<h2 id="' + esc(qid) + '">' + esc(qid) + '</h2><article><div><h3>Source crop(s)</h3>' + (''.join(imgs) or '<p>No rendered crop available. Source comparison remains blocked.</p>') + '</div><div><h3>Rendered transcription</h3>' + right + '</div></article>')
    out.write_text(''.join(parts) + '</body></html>')
    print(out)


if __name__ == '__main__': main()
