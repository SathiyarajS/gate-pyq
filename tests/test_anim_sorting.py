import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from animations.sorting import sorting_animation


@pytest.fixture(scope="module")
def questions():
    return json.loads((ROOT / "data/animations/sorting.json").read_text())["questions"]


@pytest.mark.parametrize(
    ("qid", "array"),
    [
        ("CS-1999-Q14", [8, 15, 20, 47, 4, 9, 30, 40, 12, 17]),
        ("CS-2017-S2-Q53", [6, 5, 4, 3, 2, 1]),
        ("CS-2026-S2-Q32", [7, 8, 10, 19, 25, 31, 35, 41]),
    ],
)
def test_trace_final_array(questions, qid, array):
    final = sorting_animation(qid, questions[qid])["schedules"][0]["steps"][-1]
    assert final["final"]
    assert final["arr"] == array
    if qid == "CS-2026-S2-Q32":
        assert "Void merges: 3 of 7" in final["note"]


def test_insertion_uses_fewest_comparisons_on_sorted_input(questions):
    qid = "CS-2021-S1-Q19"
    tabs = sorting_animation(qid, questions[qid])["schedules"]
    comparisons = {tab["short"]: tab["steps"][-1]["comps"] for tab in tabs}
    assert comparisons["Insertion sort"] == 7
    assert all(value > 7 for name, value in comparisons.items() if name != "Insertion sort")


def test_first_element_pivot_compares_more_on_sorted_input(questions):
    qid = "CS-2014-S1-Q24"
    sorted_run, mixed_run = sorting_animation(qid, questions[qid])["schedules"]
    assert sorted_run["steps"][-1]["comps"] == 10
    assert mixed_run["steps"][-1]["comps"] < 10
