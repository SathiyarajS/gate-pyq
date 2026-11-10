#!/usr/bin/env python3
"""Render reviewed crops at 216 DPI. Draft rendering requires explicit opt-in.
Output metadata includes dimensions and status. Local source paths are resolved
through the audit map; SHA-256 is rechecked before any rendering.
"""
import argparse, hashlib, json, math
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def crop_geometry(page, crop):
    """Return bounds and source-to-output matrix in PDF points.

    Legacy bbox coordinates are unchanged. With transform present, bbox is in
    the rotated page's axis-aligned bounding rectangle, translated to (0, 0).
    Positive rotation_degrees is clockwise in PDF's downward-y coordinates.
    Only rigid full-page rotation is supported: no masking or content changes.
    """
    transform = crop.get('transform')
    matrix = fitz.Matrix(1, 1)
    bounds = page.rect
    if transform is not None:
        if not isinstance(transform, dict) or set(transform) != {'rotation_degrees', 'coordinate_space'}:
            raise ValueError('invalid crop transform fields')
        if transform['coordinate_space'] != 'rotated_page':
            raise ValueError('invalid crop coordinate space')
        angle = transform['rotation_degrees']
        if isinstance(angle, bool) or not isinstance(angle, (int, float)) or not math.isfinite(angle) or not -10 <= angle <= 10:
            raise ValueError('rotation must be finite and within +/-10 degrees')
        matrix = fitz.Matrix(angle)
        rotated = page.rect * matrix
        matrix = matrix * fitz.Matrix(1, 0, 0, 1, -rotated.x0, -rotated.y0)
        bounds = fitz.Rect(0, 0, rotated.width, rotated.height)
    values = crop['bbox']
    if len(values) != 4 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError('invalid bounds')
    box = fitz.Rect(values)
    tolerance = fitz.Rect(bounds.x0-.02, bounds.y0-.02, bounds.x1+.02, bounds.y1+.02)
    if box.is_empty or box.is_infinite or not tolerance.contains(box):
        raise ValueError('invalid bounds')
    return box & bounds, matrix


def crop_source_polygon(page, crop):
    """Map TL, TR, BR, BL crop corners back to original source-page points.

    For overlap audits across different transforms, compare these polygons,
    not their axis-aligned enclosing rectangles (which can overlap spuriously).
    """
    box, matrix = crop_geometry(page, crop)
    inverse = ~matrix
    return [tuple(point * inverse) for point in (box.tl, box.tr, box.br, box.bl)]


def render_crop(page, crop, scale=3):
    """Render directly from source; transformed crops cut a full-page raster.

    Pixel edges round outward using MuPDF IRect, as in legacy clip rendering.
    The source is rotated once by MuPDF, not cropped then rotated. No pixels
    inside the resulting rectangle are erased, redrawn, or post-processed.
    """
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('scale must be positive and finite')
    box, matrix = crop_geometry(page, crop)
    if crop.get('transform') is None:
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=box, alpha=False)
        return Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    pix = page.get_pixmap(matrix=matrix * fitz.Matrix(scale, scale), alpha=False)
    image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    pixels = (box * fitz.Matrix(scale, scale)).irect
    return image.crop((pixels.x0-pix.x, pixels.y0-pix.y,
                       pixels.x1-pix.x, pixels.y1-pix.y))


def trim_blank_tail(img, qid, min_tail=150, pad=24):
    """Remove the empty answer-box area left below questions in 2022+ papers.

    Those papers print each question in a table that runs to the page end, so a
    reviewed crop can carry a tall blank block. Only rows with no ink other than
    the table's vertical rules (and full-width horizontal rules) are removed, and
    only from the bottom; question content is never touched.
    """
    import re
    year = re.match(r'CS-(\d{4})', qid)
    if not year or int(year.group(1)) < 2022:
        return img
    gray = img.convert('L'); w, h = gray.size; px = gray.load()
    def row_is_empty(y):
        dark = sum(1 for x in range(0, w, 2) if px[x, y] < 150) * 2
        return dark <= max(6, int(0.02 * w)) or dark > 0.9 * w
    tail = 0
    for y in range(h - 1, -1, -1):
        if not row_is_empty(y):
            break
        tail += 1
    if tail < min_tail or h - tail < 60:
        return img
    return img.crop((0, 0, w, h - tail + pad))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--crops', default=str(ROOT/'data/crops.json'))
    ap.add_argument('--allow-draft',action='store_true');ap.add_argument('--question',action='append')
    ap.add_argument('--source-cache',default=str(ROOT/'.local-source-cache/source-paths.json'))
    ap.add_argument('--output',default=str(ROOT/'site-assets/q'));ap.add_argument('--scale',type=float,default=3)
    args=ap.parse_args()
    if not math.isfinite(args.scale) or args.scale<=0:ap.error('--scale must be positive')
    crops=json.loads(Path(args.crops).read_text()); sources=json.loads((ROOT/'audits/crop-source-map.json').read_text())['sources']
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
            page=doc[crop['page']-1]
            try: crop_geometry(page, crop)
            except (ValueError, TypeError, KeyError) as error: raise SystemExit(f'{qid}: {error}')
            jobs.append((qid,n,crop,page))
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    previous=output/'manifest.json'
    assets=json.loads(previous.read_text()) if args.question and previous.exists() else {}
    for qid in selected:assets.pop(qid,None)
    for qid,n,crop,page in jobs:
        img=trim_blank_tail(render_crop(page,crop,args.scale),qid);name=f'{qid}-{n}.webp'
        try:img.save(output/name,'WEBP',quality=80)
        except (KeyError,OSError):name=f'{qid}-{n}.png';img.save(output/name,'PNG')
        assets.setdefault(qid,[]).append({'file':name,'width':img.width,'height':img.height,'status':crop['status'],'page':crop['page']})
    (output/'manifest.json').write_text(json.dumps(assets,indent=2)+'\n');print(f'Rendered {len(jobs)} images for {len(assets)} questions')
if __name__=='__main__':main()
