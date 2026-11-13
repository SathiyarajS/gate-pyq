#!/usr/bin/env python3
"""Screenshot each question's side-by-side comparison (source crop vs redrawn draft).

Gives a reviewer who cannot run a browser (e.g. Codex) the rendered evidence that
docs/TRANSCRIPTIONS.md requires for `rendered_comparison_checked`: KaTeX-typeset
maths, options, tables and SVG figures exactly as the production renderer shows them.

For each paper: renders any missing crop images (most are committed), builds audits/compare/<paper>.html with
scripts/compare_transcription.py, then saves per question
  <out>/<paper>/<question_id>-desktop.jpg       1280 px, light theme
  <out>/<paper>/<question_id>-mobile-dark.jpg   390 px, dark theme
plus <out>/<paper>/index.json listing every file and the draft status shown.

Usage: python scripts/screenshot_comparisons.py [--out DIR] PAPER_ID [PAPER_ID ...]
       python scripts/screenshot_comparisons.py --all-drafted
"""
import argparse, asyncio, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def drafted_papers():
    return sorted(p.stem for p in (ROOT / "data/transcriptions").glob("*.json"))


async def shoot(paper, out):
    from playwright.async_api import async_playwright
    page_file = ROOT / "audits/compare" / f"{paper}.html"
    dest = out / paper
    dest.mkdir(parents=True, exist_ok=True)
    index = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for label, width, scheme in (("desktop", 1280, "light"), ("mobile-dark", 390, "dark")):
            page = await browser.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme, device_scale_factor=1)
            await page.goto(page_file.as_uri(), wait_until="networkidle")
            # Crops are lazy-loaded on the page; force them all in before capturing.
            await page.evaluate("""() => Promise.all([...document.images].map(img => {
                img.loading = 'eager';
                return img.complete && img.naturalWidth ? null :
                    new Promise(r => { img.onload = img.onerror = r; img.src = img.src; });
            }))""")
            await page.wait_for_timeout(500)  # KaTeX typesetting
            ids = await page.eval_on_selector_all("h2[id]", "els => els.map(e => e.id)")
            for qid in ids:
                # Heading + its <article> (crop on the left, rendered draft on the right).
                box = await page.evaluate(
                    """id => { const h = document.getElementById(id); const a = h.nextElementSibling;
                        const r1 = h.getBoundingClientRect(), r2 = a.getBoundingClientRect();
                        return {x: 0, y: r1.top + scrollY, width: document.documentElement.clientWidth,
                                height: r2.bottom - r1.top}; }""", qid)
                path = dest / f"{qid}-{label}.jpg"
                await page.screenshot(path=str(path), clip=box, full_page=True, type="jpeg", quality=70)
                if label == "desktop":
                    status = await page.evaluate(
                        "id => document.getElementById(id).nextElementSibling.innerText.match(/Stored status: (\\w+)/)?.[1] || 'none'", qid)
                    index.append({"question_id": qid, "status": status, "files": [f"{qid}-desktop.jpg", f"{qid}-mobile-dark.jpg"]})
            await page.close()
        await browser.close()
    (dest / "index.json").write_text(json.dumps({"paper_id": paper, "questions": index}, indent=1))
    print(f"{paper}: {len(index)} questions -> {dest}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("papers", nargs="*")
    ap.add_argument("--all-drafted", action="store_true", help="every paper that has data/transcriptions/<paper>.json")
    ap.add_argument("--out", default=str(ROOT / "audits/compare-shots"))
    args = ap.parse_args()
    papers = drafted_papers() if args.all_drafted else args.papers
    if not papers:
        ap.error("give paper IDs or --all-drafted")
    questions = json.loads((ROOT / "data/questions.json").read_text())
    for paper in papers:
        qids = [q["question_id"] for q in questions if q["paper_id"] == paper]
        if not qids:
            sys.exit(f"unknown paper {paper}")
        have = json.loads((ROOT / "site-assets/q/manifest.json").read_text())
        missing = [q for q in qids if not all((ROOT / "site-assets/q" / e["file"]).is_file() for e in have.get(q, [])) or q not in have]
        if missing:  # committed images cover existing papers; new ones need the source PDF locally
            subprocess.run([sys.executable, str(ROOT / "scripts/render_crops.py")] + [a for q in missing for a in ("--question", q)], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts/compare_transcription.py"), paper], check=True)
        asyncio.run(shoot(paper, Path(args.out)))


if __name__ == "__main__":
    main()
