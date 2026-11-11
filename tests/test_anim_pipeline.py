import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from animations.pipeline import pipeline_animation


@pytest.fixture(scope="module")
def questions():
    return json.loads((ROOT / "data/animations/pipeline.json").read_text())["questions"]


@pytest.mark.parametrize(
    ("qid", "cycles", "stage"),
    [
        ("CS-1999-Q71", 15, "W"),
        ("CS-2007-Q37", 8, "WB"),
        ("CS-2010-Q43", 15, "WO"),
        ("CS-2015-S2-Q53", 13, "WB"),
    ],
)
def test_timing_ends_with_last_writeback(questions, qid, cycles, stage):
    animation = pipeline_animation(qid, questions[qid])
    final = animation["schedules"][0]["steps"][-1]
    assert animation["cycles"] == cycles
    assert final["rows"][-1][-1] == [cycles, stage, "work"]
    assert final["final"]


def test_same_cycle_write_then_read_is_not_a_hazard(questions):
    qid = "CS-2001-Q74"
    steps = pipeline_animation(qid, questions[qid])["schedules"][0]["steps"]
    assert "the same cycle" in steps[-2]["note"]
    assert "I2→I4 on r4" in steps[-1]["note"]
    assert "I1→I4 on r2" not in steps[-1]["note"]


def test_wrong_expected_completion_stops_the_build(questions):
    qid = "CS-2007-Q37"
    spec = copy.deepcopy(questions[qid])
    spec["expect"]["cycles"] = 7
    with pytest.raises(SystemExit, match="not the expected 7"):
        pipeline_animation(qid, spec)
