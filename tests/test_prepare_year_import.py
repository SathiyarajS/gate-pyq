import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_year_import import official_url, prepare_session, sessions_from_json


SOURCES = ROOT / "sources/web/gate2026.iitg.ac.in/doc/download/2026"
PAPER_URL = "https://gate2026.iitg.ac.in/official-paper.pdf"
KEY_URL = "https://gate2026.iitg.ac.in/official-key.pdf"


@pytest.mark.parametrize("variant", [1, 2])
def test_modern_paper_and_key_match_recorded_inventory(variant):
    paper, questions = prepare_session(
        2026, variant, True, PAPER_URL, KEY_URL,
        (SOURCES / f"QPs/CS{variant}.pdf").read_bytes(),
        (SOURCES / f"Keys/CS{variant}_Keys.pdf").read_bytes(),
    )
    assert paper["expected_question_count"] == len(questions) == 65
    assert sum(question["marks"] for question in questions) == 100
    assert not paper["final_key_verified"]
    current = {q["question_id"]: q for q in json.loads((ROOT / "data/questions.json").read_text())}
    for question in questions:
        existing = current[question["question_id"]]
        for field in ("source_page", "question_type", "marks", "official_answer"):
            assert question[field] == existing[field]
        assert question["verification_status"] == "pending"
        assert question["solution"] == ""


def test_other_set_key_is_rejected():
    with pytest.raises(ValueError, match="wrong CS set"):
        prepare_session(
            2026, 1, True, PAPER_URL, KEY_URL,
            (SOURCES / "QPs/CS1.pdf").read_bytes(),
            (SOURCES / "Keys/CS2_Keys.pdf").read_bytes(),
        )


@pytest.mark.parametrize("url", [
    "http://example.ac.in/file.pdf",
    "https://example.ac.in.evil.example/file.pdf",
    "https://user@example.ac.in/file.pdf",
    "https://example.ac.in:8080/file.pdf",
    "https://example.ac.in/file.pdf#page=1",
])
def test_only_official_https_sources_are_accepted(url):
    with pytest.raises(ValueError):
        official_url(url)


def test_duplicate_session_sources_are_rejected():
    with pytest.raises(ValueError, match="distinct"):
        sessions_from_json(json.dumps([{"set": 1, "paper_url": PAPER_URL, "key_url": PAPER_URL}]))


def test_site_uses_published_inventory_for_years_and_counts(tmp_path, monkeypatch):
    import shutil

    import build_site

    paper = {"paper_id": "CS-2027", "year": 2027}
    original = next(
        q for q in json.loads((ROOT / "data/questions.json").read_text())
        if q["question_id"] == "CS-2026-S2-Q1"
    )
    question = dict(original, paper_id=paper["paper_id"], question_id="CS-2027-Q1")
    data = tmp_path / "data"
    data.mkdir()
    for path in ("templates", "site-static"):
        shutil.copytree(ROOT / path, tmp_path / path)
    shutil.copy2(ROOT / "DISCREPANCIES.md", tmp_path / "DISCREPANCIES.md")
    (data / "papers.json").write_text(json.dumps([paper]))
    (data / "questions.json").write_text(json.dumps([question]))
    staged = data / "imports/2028"
    staged.mkdir(parents=True)
    (staged / "papers.json").write_text(json.dumps([{"paper_id": "CS-2028", "year": 2028}]))
    monkeypatch.setattr(build_site, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["build_site.py", "--preview"])
    build_site.main()

    site = tmp_path / "_site"
    home = (site / "index.html").read_text()
    assert "2027—2027" in home
    assert "<option>2027</option>" in home and "<option>2028</option>" not in home
    assert "<strong>1</strong><span>papers</span>" in home
    subject = (site / question["subject"] / "index.html").read_text()
    assert 'max="2027" value="2027"' in subject
    assert "<th>2027</th>" in subject
    manifest = json.loads((site / "manifest.webmanifest").read_text())
    assert "2027–2027" in manifest["description"]
    assert (site / "papers/CS-2027/index.html").is_file()
    assert not (site / "papers/CS-2028/index.html").exists()
