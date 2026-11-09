#!/usr/bin/env python3
"""Download every source PDF referenced by data/questions.json into sources/.

Runs inside GitHub Actions (the build servers have open internet access).
Writes sources/manifest.json mapping each source URL (and zip member) to a
local path and its sha256, so the cropping and site scripts never need the web.
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sources"
DRIVE_ID = "1popAHO-cX69oQEx_tD0wZXL1tTrBljeO"
UA = "Mozilla/5.0 (gate-pyq source fetcher)"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def local_name(url):
    u = re.sub(r"^https?://(web\.archive\.org/web/\d+id_/)?", "", url)
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"[?&=]", "_", u)
    return u


def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                f.write(r.read())
            return True
        except Exception as e:  # noqa: BLE001
            print(f"  attempt {attempt + 1} failed: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return False


def main():
    recs = json.load(open(ROOT / "data/questions.json"))
    urls = set()
    for r in recs:
        for k in ("source_url", "key_url", "recovered_diagram_url"):
            u = r.get(k)
            if u and "drive.google.com" not in u:
                urls.add(u.split("#")[0])
    manifest = {"files": {}, "zip_members": {}, "failed": []}

    for url in sorted(urls):
        dest = OUT / "web" / local_name(url)
        if not dest.name.lower().endswith(".pdf") and "blob" not in url:
            dest = dest.with_suffix(dest.suffix + ".pdf")
        print("GET", url)
        if fetch(url, dest):
            manifest["files"][url] = {"path": str(dest.relative_to(ROOT)), "sha256": sha256(dest)}
        else:
            manifest["failed"].append(url)

    # Official GATE 2026 archive (CS.zip) on Google Drive.
    zpath = OUT / "CS.zip"
    subprocess.run([sys.executable, "-m", "gdown", "--fuzzy", "-O", str(zpath),
                    f"https://drive.google.com/file/d/{DRIVE_ID}/view"], check=False)
    if zpath.exists() and zipfile.is_zipfile(zpath):
        with zipfile.ZipFile(zpath) as z:
            for m in z.namelist():
                if m.endswith("/"):
                    continue
                dest = OUT / "drive-cs-zip" / m
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(z.read(m))
                manifest["zip_members"][m] = {"path": str(dest.relative_to(ROOT)), "sha256": sha256(dest)}
        manifest["zip_sha256"] = sha256(zpath)
        zpath.unlink()
    else:
        manifest["failed"].append("drive:CS.zip")

    # Cross-check hashes recorded by the earlier audit.
    mismatches = []
    for r in recs:
        want = r.get("source_file_sha256")
        if not want:
            continue
        m = r.get("source_archive_member")
        got = (manifest["zip_members"].get(m) if m else manifest["files"].get((r.get("source_url") or "").split("#")[0]))
        if got and got["sha256"] != want:
            mismatches.append([r["question_id"], want, got["sha256"]])
    manifest["sha_mismatches"] = mismatches[:50]
    manifest["sha_mismatch_count"] = len(mismatches)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True))
    print(f"files={len(manifest['files'])} zip_members={len(manifest['zip_members'])} "
          f"failed={manifest['failed']} sha_mismatches={len(mismatches)}")


if __name__ == "__main__":
    main()
