#!/usr/bin/env python3
"""Restore the source PDFs on this machine (they are not stored in the repository).

The site needs only the committed question images in site-assets/q. The PDFs are
needed only to re-render an image or to transcribe a question, so they are kept as
local, git-ignored working files at the paths recorded in audits/crop-source-map.json
(sources/web/..., sources/archive/...).

For every source in that map that is missing locally, this downloads it from its
recorded URL (or extracts it from the official CS.zip archive; staged new years in
data/imports/<year>/papers.json are included), checks its sha256
against the recorded value, and saves it at its recorded path. A file whose hash
differs is rejected, never used. If a link has gone, the committed images remain the
record; transcribe from them instead.

Usage: python scripts/fetch_sources.py [PATH_OR_PAPER_FILTER ...]
       e.g.  python scripts/fetch_sources.py            (everything missing)
             python scripts/fetch_sources.py 2019 GATE1995
"""
import hashlib, json, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRIVE_ID = "1popAHO-cX69oQEx_tD0wZXL1tTrBljeO"
CACHE = ROOT / ".local-source-cache"
UA = "Mozilla/5.0 (gate-pyq source restore)"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def download(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - report and retry any network error
            print(f"  attempt {attempt + 1} failed: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    return None


def archive():
    """The official GATE 2026 CS.zip (2007-2018 papers), downloaded once into the cache."""
    zpath = CACHE / "CS.zip"
    CACHE.mkdir(exist_ok=True)
    if not (zpath.exists() and zipfile.is_zipfile(zpath)):
        subprocess.run([sys.executable, "-m", "gdown", DRIVE_ID, "-O", str(zpath)], check=False)
    if not (zpath.exists() and zipfile.is_zipfile(zpath)):
        data = download(f"https://drive.usercontent.google.com/download?id={DRIVE_ID}&export=download&confirm=t")
        if data:
            zpath.write_bytes(data)
    return zipfile.ZipFile(zpath) if zpath.exists() and zipfile.is_zipfile(zpath) else None


def main(filters):
    sources = json.loads((ROOT / "audits/crop-source-map.json").read_text())["sources"]
    # Answer keys and other fetched files (not cropped, so not in the map) are in sources/manifest.json.
    manifest = ROOT / "sources/manifest.json"
    if manifest.is_file():
        for url, info in json.loads(manifest.read_text()).get("files", {}).items():
            sources.setdefault(info["path"], {"url": url, "sha256": info["sha256"], "archive_member": None})
    # A new year staged by scripts/prepare_year_import.py (or its GitHub workflow) is
    # listed in data/imports/<year>/papers.json before it reaches the source map.
    for staged in sorted((ROOT / "data/imports").glob("*/papers.json")):
        for paper in json.loads(staged.read_text()):
            for kind in ("paper", "key"):
                sources.setdefault(paper[f"{kind}_path"], {"url": paper[f"{kind}_url"], "sha256": paper[f"{kind}_sha256"], "archive_member": None})
    wanted = {p: v for p, v in sources.items() if not filters or any(f in p for f in filters)}
    ok = present = 0
    failed = []
    zf = None
    for path, info in sorted(wanted.items()):
        dest = ROOT / path
        if dest.is_file() and sha256_bytes(dest.read_bytes()) == info["sha256"]:
            present += 1
            continue
        if info.get("archive_member"):
            zf = zf or archive()
            data = zf.read(info["archive_member"]) if zf and info["archive_member"] in zf.namelist() else None
        else:
            print("GET", info["url"])
            data = download(info["url"])
        if data is None:
            failed.append(f"{path}: could not download")
            continue
        if sha256_bytes(data) != info["sha256"]:
            failed.append(f"{path}: sha256 differs from the recorded value; not used")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        ok += 1
    print(f"Source PDFs: {present} already present, {ok} restored, {len(failed)} unavailable")
    for line in failed:
        print("  " + line, file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith("--")]))
