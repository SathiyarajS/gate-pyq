import json
from pathlib import Path

import pytest

from scripts.animations.ctrace import ctrace_animation


ROOT = Path(__file__).resolve().parents[1]
SPECS = json.loads((ROOT / "data/animations/ctrace.json").read_text())["questions"]


def steps_for(qid):
    return ctrace_animation(qid, SPECS[qid])["schedules"][0]["steps"]


def test_retained_specs_have_readable_completed_traces():
    for qid, spec in SPECS.items():
        result = json.loads(json.dumps(ctrace_animation(qid, spec)))
        assert result["kind"] == "c-trace"
        assert result["count"] == sum(len(schedule["steps"]) for schedule in result["schedules"])
        for schedule in result["schedules"]:
            assert schedule["steps"][-1]["final"] is True
            for step in schedule["steps"]:
                assert step["note"].strip()
                if "line" in step:
                    assert 0 <= step["line"] < len(result["code"])


def test_pointer_trace_marks_the_exact_array_cell_it_writes():
    steps = steps_for("CS-2025-S2-Q62")
    increment = next(step for step in steps if "arr[1] becomes 51" in step["note"])
    variables = {row["n"]: row for group in increment["vars"] for row in group["rows"]}
    assert variables["ptr"]["v"] == "→ arr[1]"
    assert variables["arr"]["rows"][0]["c"][1] == [1, "51", "w"]
    assert steps[-1]["out"] == "111"


def test_multidimensional_array_keeps_source_dimension_order():
    steps = steps_for("CS-2020-Q32")
    printed = next(step for step in steps if step.get("new"))
    array = printed["vars"][0]["rows"][0]
    assert array["t"] == "int[4][5]"
    assert array["rows"][3]["c"][3] == [3, "19", "r"]


def test_inner_block_shadows_only_the_parameter_inside_that_block():
    steps = steps_for("CS-2026-S1-Q34")
    inner = next(step for step in steps if "inner i is 0" in step["note"])
    shadowed = next(group for group in inner["vars"] if group["title"] == "func")
    assert [(row["v"], bool(row.get("h"))) for row in shadowed["rows"] if row["n"] == "i"] == [
        ("9", True),
        ("0", False),
    ]
    printed = next(step for step in steps if step.get("new"))
    active = next(group for group in printed["vars"] if group["title"] == "func")
    assert [row["v"] for row in active["rows"] if row["n"] == "i"] == ["9"]
    assert printed["out"] == "9"


def test_expected_output_must_match_the_executed_program():
    spec = {**SPECS["CS-2017-S2-Q24"], "expect": {"output": "0,1"}}
    with pytest.raises(SystemExit, match="prints '1,0', not '0,1'"):
        ctrace_animation("CS-2017-S2-Q24", spec)


def test_void_call_returns_to_the_caller_with_the_updated_array():
    qid = "CS-2025-S2-Q19"
    result = ctrace_animation(qid, SPECS[qid])
    returned = next(step for step in result["schedules"][0]["steps"] if "stringcopy(a, a + 2) returns." in step["note"])
    assert result["code"][returned["line"]].strip() == "stringcopy(a, a + 2);"
    assert returned["vars"][0]["rows"][0]["s"] == '"Hello World!d!"'


def test_for_initializer_and_condition_highlight_the_caller_loop():
    qid = "CS-2019-Q37"
    result = ctrace_animation(qid, SPECS[qid])
    steps = result["schedules"][0]["steps"]
    initializer = next(step for step in steps if step["note"] == "r(): r() returns 7.")
    conditions = [step for step in steps if step["note"].startswith("Test r()")]
    assert len(conditions) == 3
    for step in [initializer, *conditions]:
        assert result["code"][step["line"]].strip() == "for (r(); r(); r())"
        assert step["fn"] == "main"
    assert any(step["note"] == "Before returning, num becomes 6. r returns 7." for step in steps)


def test_loop_update_and_if_side_effects_have_their_own_steps():
    qid = "CS-2019-Q63"
    result = ctrace_animation(qid, SPECS[qid])
    steps = result["schedules"][0]["steps"]
    update = next(step for step in steps if step["note"] == "i++: i becomes 1.")
    assert result["code"][update["line"]].strip().startswith("for (")
    assert any("a holds {2, 4, 6, 8, 10}" in step["note"] for step in steps)
    body = next(step for step in steps if step["note"].endswith("sum becomes 1."))
    assert "i becomes" not in body["note"]

    qid = "CS-2021-S1-Q47"
    result = ctrace_animation(qid, SPECS[qid])
    steps = result["schedules"][0]["steps"]
    condition = next(step for step in steps if "i becomes 2" in step["note"])
    assert result["code"][condition["line"]].strip().startswith("if (")
    body = next(step for step in steps if step["note"].endswith("count becomes 1."))
    assert "i becomes" not in body["note"]
