#!/usr/bin/env python3
"""Fail if any internal link or image in the built site points at a missing file."""
import re, sys
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
ATTR = re.compile(r'(?:href|src)="([^"#?]+)')
broken = {}
pages = list(site.rglob("*.html"))
for page in pages:
    rel = page.relative_to(site).as_posix()
    for link in ATTR.findall(page.read_text(errors="ignore")):
        if urlparse(link).scheme or link.startswith(("mailto:", "data:", "//")):
            continue
        target = urlparse(urljoin("http://x/" + rel, link)).path
        path = site / unquote(target.lstrip("/"))
        if target.endswith("/"):
            path = path / "index.html"
        if not path.exists():
            broken.setdefault(target, rel)
print(f"Checked {len(pages)} pages; {len(broken)} broken internal targets")
for target, page in list(broken.items())[:20]:
    print(f"  {target}  (first seen on {page})")
sys.exit(1 if broken else 0)
