from texttype.corpus import PSALMS, Clause, book_clauses, clause_key, clauses_by_chapter


def test_psalter_clauses_reads_every_clause_in_canonical_order(two_psalm_api):
    clauses = book_clauses(two_psalm_api, PSALMS)
    assert [c.node for c in clauses] == [1, 2, 3]
    assert [c.chapter for c in clauses] == [1, 2, 2]
    assert [c.txt for c in clauses] == ["Q", "Q", "QN"]


def test_psalter_clauses_indexes_position_within_the_verse(two_psalm_api):
    clauses = book_clauses(two_psalm_api, PSALMS)
    assert [c.index_in_verse for c in clauses] == [0, 0, 1]


def test_missing_txt_value_becomes_the_unknown_marker(two_psalm_api):
    two_psalm_api.F.features["txt"]._values[1] = None
    assert book_clauses(two_psalm_api, PSALMS)[0].txt == "?"


def test_clause_key_ignores_the_node_number():
    a = Clause(node=1, book="Psalmi", chapter=3, verse=4, index_in_verse=2, txt="Q")
    b = Clause(node=999, book="Psalmi", chapter=3, verse=4, index_in_verse=2, txt="N")
    assert clause_key(a) == clause_key(b)


def test_clause_key_separates_the_same_position_in_different_books():
    a = Clause(node=1, book="Psalmi", chapter=1, verse=1, index_in_verse=0, txt="Q")
    b = Clause(node=2, book="Genesis", chapter=1, verse=1, index_in_verse=0, txt="N")
    assert clause_key(a) != clause_key(b)


def test_clauses_by_chapter_groups_and_preserves_order():
    clauses = [
        Clause(node=1, book="Psalmi", chapter=1, verse=1, index_in_verse=0, txt="Q"),
        Clause(node=2, book="Psalmi", chapter=2, verse=1, index_in_verse=0, txt="Q"),
        Clause(node=3, book="Psalmi", chapter=1, verse=2, index_in_verse=0, txt="N"),
    ]
    grouped = clauses_by_chapter(clauses)
    assert [c.node for c in grouped[("Psalmi", 1)]] == [1, 3]
    assert [c.node for c in grouped[("Psalmi", 2)]] == [2]


def test_book_clauses_rejects_an_absent_book(two_psalm_api):
    import pytest

    with pytest.raises(RuntimeError):
        book_clauses(two_psalm_api, "Genesis")
