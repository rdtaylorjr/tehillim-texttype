from texttype.corpus import Clause
from texttype.published import (
    TABLES,
    PublishedVerse,
    check_table,
    check_verse,
    mismatches,
)


def clause(book, chapter, verse, txt, node=1):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def test_every_published_table_names_its_book_and_verses():
    for table in TABLES.values():
        for verse in table:
            assert verse.book
            assert verse.text_types
            assert verse.printed_rows > 0


def test_check_verse_collects_only_the_clauses_of_that_verse():
    clauses = [
        clause("Psalmi", 105, 10, "QN"),
        clause("Psalmi", 105, 11, "QNQ"),
        clause("Genesis", 105, 10, "N"),
    ]
    published = PublishedVerse("Psalmi", 105, 10, ("QN",), 1)
    assert check_verse(published, clauses).observed == ("QN",)


def test_values_match_ignores_how_many_rows_the_article_printed():
    clauses = [clause("Psalmi", 105, 1, "Q", 1), clause("Psalmi", 105, 1, "Q", 2)]
    result = check_verse(PublishedVerse("Psalmi", 105, 1, ("Q",), 1), clauses)
    assert result.values_match is True
    assert result.rows_match is False
    assert result.clauses == 2


def test_a_different_text_type_is_a_value_mismatch():
    clauses = [clause("Psalmi", 64, 8, "N")]
    result = check_verse(PublishedVerse("Psalmi", 64, 8, ("QN",), 1), clauses)
    assert result.values_match is False


def test_rows_match_when_the_clause_count_equals_the_printed_count():
    clauses = [clause("Judices", 9, 54, "N", 1), clause("Judices", 9, 54, "NQ", 2)]
    result = check_verse(PublishedVerse("Judices", 9, 54, ("N", "NQ"), 2), clauses)
    assert result.rows_match is True


def test_a_verse_absent_from_the_build_observes_nothing():
    result = check_verse(PublishedVerse("Psalmi", 105, 1, ("Q",), 1), [])
    assert result.observed == ()
    assert result.values_match is False


def test_check_table_returns_one_result_per_published_verse():
    clauses = [clause("Psalmi", 64, 2, "Q")]
    assert len(check_table(TABLES["Psalm 64"], clauses)) == len(TABLES["Psalm 64"])


def test_mismatches_selects_only_the_disagreeing_verses():
    clauses = [clause("Psalmi", 105, 10, "QN"), clause("Psalmi", 105, 11, "N")]
    checks = check_table(TABLES["Psalm 105"], clauses)
    bad = mismatches(checks)
    assert all(not c.values_match for c in bad)
    assert any(c.verse.verse == 11 for c in bad)
