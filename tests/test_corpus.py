from texttype.corpus import Clause, clause_key, clauses_by_psalm, psalter_clauses


def test_psalter_clauses_reads_every_clause_in_canonical_order(two_psalm_api):
    clauses = psalter_clauses(two_psalm_api)
    assert [c.node for c in clauses] == [1, 2, 3]
    assert [c.psalm for c in clauses] == [1, 2, 2]
    assert [c.txt for c in clauses] == ["Q", "Q", "QN"]


def test_psalter_clauses_indexes_position_within_the_verse(two_psalm_api):
    clauses = psalter_clauses(two_psalm_api)
    assert [c.index_in_verse for c in clauses] == [0, 0, 1]


def test_missing_txt_value_becomes_the_unknown_marker(two_psalm_api):
    two_psalm_api.F.features["txt"]._values[1] = None
    assert psalter_clauses(two_psalm_api)[0].txt == "?"


def test_clause_key_ignores_the_node_number():
    a = Clause(node=1, psalm=3, verse=4, index_in_verse=2, txt="Q")
    b = Clause(node=999, psalm=3, verse=4, index_in_verse=2, txt="N")
    assert clause_key(a) == clause_key(b)


def test_clauses_by_psalm_groups_and_preserves_order():
    clauses = [
        Clause(node=1, psalm=1, verse=1, index_in_verse=0, txt="Q"),
        Clause(node=2, psalm=2, verse=1, index_in_verse=0, txt="Q"),
        Clause(node=3, psalm=1, verse=2, index_in_verse=0, txt="N"),
    ]
    grouped = clauses_by_psalm(clauses)
    assert [c.node for c in grouped[1]] == [1, 3]
    assert [c.node for c in grouped[2]] == [2]
