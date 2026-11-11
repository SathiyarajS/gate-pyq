from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from animations.schedule import cycle, edges, parse, recovery, rollback, topo_orders, txns


def test_conflicting_writes_and_reads_create_cycle():
    ops = parse("CS-2007-Q64", ["r1(X)", "r1(Y)", "r2(X)", "r2(Y)", "w2(Y)", "w1(X)"])
    graph = edges(ops)
    assert set(graph) == {("T1", "T2"), ("T2", "T1")}
    assert cycle(txns(ops), graph) == ["T1", "T2", "T1"]
    assert topo_orders(txns(ops), graph) == []


def test_only_t3_before_t2_constrains_serial_order():
    ops = parse("CS-2024-S1-Q46", ["r1(z)", "w1(z)", "r2(x)", "r3(y)", "w3(y)", "r2(y)", "w2(x)", "w2(y)"])
    assert topo_orders(txns(ops), edges(ops)) == [
        ["T1", "T3", "T2"],
        ["T3", "T1", "T2"],
        ["T3", "T2", "T1"],
    ]


def test_committing_before_writer_is_not_recoverable():
    ops = parse("CS-2021-S2-Q42", ["r1(Y)", "r1(X)", "r2(Z)", "r1(Y)", "w1(X)", "r2(Z)", "w2(Y)", "r3(X)", "w3(Z)", "c3"])
    reads, recoverable, cascadeless, strict = recovery(ops)
    assert reads[7] == 4
    assert (recoverable, cascadeless, strict) == (False, False, False)


def test_dirty_write_can_be_cascadeless_but_not_strict():
    ops = parse("CS-2016-S2-Q61", ["r2(X)", "r1(X)", "r2(Y)", "w1(X)", "r1(Y)", "w2(X)", "a1", "a2"])
    assert recovery(ops)[1:] == (True, True, False)


def test_aborted_writer_rolls_back_both_dirty_readers():
    ops = parse("CS-2025-S1-Q15", ["r1(X)", "w1(Y)", "r2(X)", "r2(Y)", "r3(Y)", "a1"])
    assert rollback(ops) == ["T2", "T3"]
