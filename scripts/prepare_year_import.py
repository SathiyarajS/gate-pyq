#!/usr/bin/env python3
"""Stage a modern GATE CS paper and key inventory for independent review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
MAX_PDF_BYTES = 32 * 1024 * 1024
KEY_ROW = re.compile(
    r"\s*(\d+)\s+(\d+)\s+(MCQ|MSQ|NAT)\s+(GA|CS(?:\s*-?\s*\d+)?)\s+(.+?)\s+(\d+)\s*"
)
QUESTION_START = re.compile(r"^\s*Q\s*\.\s*(\d+)\b\s*(.*)$", re.IGNORECASE)
NUMBER = r"[+\-−]?(?:\d+(?:\.\d*)?|\.\d+)"


def official_url(url):
    if not isinstance(url, str) or re.search(r"\s|\\", url):
        raise ValueError("Use an official HTTPS PDF URL.")
    parts = urlsplit(url)
    host = parts.hostname or ""
    if (
        parts.scheme != "https" or not host.endswith(".ac.in")
        or parts.username is not None or parts.password is not None
        or parts.port not in (None, 443) or parts.fragment
    ):
        raise ValueError("Use an HTTPS URL on an official .ac.in host, without credentials or a page fragment.")
    return url


class OfficialRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, official_url(newurl))


def fetch_pdf(url):
    opener = build_opener(OfficialRedirect)
    with opener.open(Request(official_url(url), headers={"User-Agent": "GATE-PYQ import"}), timeout=45) as response:
        content = response.read(MAX_PDF_BYTES + 1)
    if len(content) > MAX_PDF_BYTES or not content.startswith(b"%PDF-"):
        raise ValueError(f"Expected a PDF under 32 MiB at {url}")
    return content


def key_rows(document, variant):
    rows = {}
    sessions = set()
    for page_no, page in enumerate(document, start=1):
        for line in page.get_text(sort=True).splitlines():
            match = KEY_ROW.fullmatch(line)
            if not match:
                continue
            number, session, kind, section, answer, marks = match.groups()
            ordinal = int(number)
            section = re.sub(r"\s|-", "", section)
            if ordinal in rows or section not in ("GA", "CS", f"CS{variant}"):
                raise ValueError(f"Duplicate question or wrong CS set in key row {ordinal}.")
            answer = " ".join(answer.split())
            if answer != "MTA":
                valid = (
                    re.fullmatch(r"[A-D]", answer) if kind == "MCQ" else
                    re.fullmatch(r"[A-D](?:\s*[,;]\s*[A-D])*", answer) if kind == "MSQ" else
                    re.fullmatch(rf"{NUMBER}(?:\s*(?:to|:)\s*{NUMBER})?", answer)
                )
                if not valid:
                    raise ValueError(f"Unsupported answer format in key row {ordinal}.")
            if int(marks) not in (1, 2):
                raise ValueError(f"Unsupported mark value in key row {ordinal}.")
            rows[ordinal] = {
                "question_type": kind, "marks": int(marks), "key_page": page_no,
                "source_section": "GA" if section == "GA" else "CS", "official_answer": answer,
            }
            sessions.add(int(session))
    if not rows or sorted(rows) != list(range(1, len(rows) + 1)) or len(sessions) != 1:
        raise ValueError("Expected one session with consecutive key rows starting at 1. Check the key format.")
    if len(rows) <= 10 or any(
        row["source_section"] != ("GA" if number <= 10 else "CS") for number, row in rows.items()
    ):
        raise ValueError("Expected ten General Aptitude questions followed by Computer Science.")
    return rows, sessions.pop()


def paper_pages(document, variant):
    heading = document[0].get_text(sort=True) if len(document) else ""
    if not re.search(r"Computer Science", heading, re.IGNORECASE):
        raise ValueError("The first paper page does not have a readable Computer Science heading.")
    label = re.search(r"\(CS\s*-?\s*(\d+)\)", heading, re.IGNORECASE)
    if label and int(label[1]) != variant:
        raise ValueError("The paper heading identifies a different CS set.")
    pages = {}
    for page_no, page in enumerate(document, start=1):
        for line in page.get_text().splitlines():
            match = QUESTION_START.fullmatch(line)
            if match and not match[2].lstrip(". ").startswith(("–", "—", "-")):
                ordinal = int(match[1])
                if ordinal in pages:
                    raise ValueError(f"Duplicate printed question Q{ordinal}. Check the paper numbering.")
                pages[ordinal] = page_no
    return pages


def prepare_session(year, variant, multiple, paper_url, key_url, paper_pdf, key_pdf):
    paper_id = f"CS-{year}" + (f"-S{variant}" if multiple else "")
    with pymupdf.open(stream=paper_pdf, filetype="pdf") as paper:
        pages = paper_pages(paper, variant)
    with pymupdf.open(stream=key_pdf, filetype="pdf") as key:
        rows, session = key_rows(key, variant)
    if set(pages) != set(rows):
        raise ValueError(f"{paper_id}: paper and key question numbers differ "
                         f"(paper only: {sorted(pages.keys() - rows.keys())}, "
                         f"key only: {sorted(rows.keys() - pages.keys())}).")
    inventory = {
        "paper_id": paper_id, "year": year, "paper_variant": variant, "exam_session": session,
        "paper_url": paper_url, "key_url": key_url,
        "paper_sha256": hashlib.sha256(paper_pdf).hexdigest(),
        "key_sha256": hashlib.sha256(key_pdf).hexdigest(),
        "expected_question_count": len(rows),
        "expected_question_numbers": [str(number) for number in sorted(rows)],
        "ga_expected": True, "inventory_verified": False, "final_key_verified": False,
        "source_review_status": "pending",
    }
    questions = []
    for number, row in sorted(rows.items()):
        page = pages[number]
        questions.append({
            "question_id": f"{paper_id}-Q{number}", "paper_id": paper_id,
            "source_question_number": str(number), "source_page": page,
            "source_url": f"{paper_url}#page={page}", "key_url": f"{key_url}#page={row['key_page']}",
            "official_session": session, "printed_question_number": str(number),
            "source_numbering_scheme": "ga_first_continuous",
            "subject": "11-general-aptitude" if row["source_section"] == "GA" else None,
            "question_text": "", "solution": "", "derived_answer": None,
            "verification_status": "pending", "discrepancy_ids": [], **row,
        })
    return inventory, questions


def sessions_from_json(value):
    sessions = json.loads(value)
    if not isinstance(sessions, list) or not sessions:
        raise ValueError("Sessions must be a nonempty JSON array.")
    for entry in sessions:
        if not isinstance(entry, dict) or set(entry) != {"set", "paper_url", "key_url"} or type(entry["set"]) is not int:
            raise ValueError("Each session needs an integer set, paper_url, and key_url.")
        official_url(entry["paper_url"])
        official_url(entry["key_url"])
    sessions.sort(key=lambda entry: entry["set"])
    if [entry["set"] for entry in sessions] != list(range(1, len(sessions) + 1)):
        raise ValueError("Set numbers must be unique and consecutive starting at 1.")
    urls = [entry[field] for entry in sessions for field in ("paper_url", "key_url")]
    if len(set(urls)) != len(urls):
        raise ValueError("Use distinct official paper and key URLs for each set.")
    return sessions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("year", type=int)
    parser.add_argument("--sessions", required=True, help="JSON array of {set, paper_url, key_url} objects")
    args = parser.parse_args()
    try:
        current = json.loads((ROOT / "data/papers.json").read_text())
        latest = max(paper["year"] for paper in current)
        if args.year != latest + 1:
            raise ValueError(f"Expected the next inventory year, {latest + 1}.")
        output = ROOT / "data/imports" / str(args.year)
        if output.exists():
            raise ValueError(f"Import already exists at {output.relative_to(ROOT)}.")
        sessions = sessions_from_json(args.sessions)
        inventory, questions = [], []
        seen_hashes = {
            paper[field] for paper in current for field in ("paper_sha256", "key_sha256")
            if paper.get(field)
        }
        seen_sessions = set()
        for entry in sessions:
            paper_url, key_url = entry["paper_url"], entry["key_url"]
            paper, rows = prepare_session(
                args.year, entry["set"], len(sessions) > 1, paper_url, key_url,
                fetch_pdf(paper_url), fetch_pdf(key_url),
            )
            hashes = {paper["paper_sha256"], paper["key_sha256"]}
            if len(hashes) != 2 or hashes & seen_hashes or paper["exam_session"] in seen_sessions:
                raise ValueError("The supplied PDFs repeat an archived document, a supplied document, or an exam session.")
            seen_hashes.update(hashes)
            seen_sessions.add(paper["exam_session"])
            inventory.append(paper)
            questions.extend(rows)
        output.mkdir(parents=True)
        for name, records in (("papers", inventory), ("questions", questions)):
            (output / f"{name}.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
        for paper in inventory:
            print(f"{paper['paper_id']}: {paper['expected_question_count']} candidate questions")
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Import stopped: {error}\n")


if __name__ == "__main__":
    main()
