from texttype.corpus import Clause
from texttype.inventory import depth_distribution, inventory


def clause(psalm, txt, node=0):
    return Clause(node=node, psalm=psalm, verse=1, index_in_verse=0, txt=txt)


def test_inventory_counts_clauses_and_distinct_psalms():
    counts = inventory([clause(1, "Q"), clause(2, "Q"), clause(2, "QN")])
    by_txt = {c.txt: c for c in counts}
    assert by_txt["Q"].clauses == 2
    assert by_txt["Q"].psalms == 2
    assert by_txt["QN"].psalms == 1


def test_inventory_reports_share_and_depth():
    counts = inventory([clause(1, "Q"), clause(1, "QNQ")])
    by_txt = {c.txt: c for c in counts}
    assert by_txt["Q"].share_of_clauses == 0.5
    assert by_txt["QNQ"].depth == 3


def test_inventory_orders_by_descending_clause_count():
    counts = inventory([clause(1, "QN"), clause(1, "Q"), clause(1, "Q")])
    assert [c.txt for c in counts] == ["Q", "QN"]


def test_inventory_of_no_clauses_is_empty():
    assert inventory([]) == []


def test_depth_distribution_counts_string_lengths():
    clauses = [clause(1, "Q"), clause(1, "QN"), clause(1, "QNQ")]
    assert depth_distribution(clauses) == {1: 1, 2: 1, 3: 1}
