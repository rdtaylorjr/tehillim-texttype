import pytest

from texttype.compare import domain_share, summarize, summarize_books
from texttype.corpus import Clause


def clause(book, chapter, txt, node=0, verse=1):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def test_summarize_counts_clauses_chapters_and_distinct_strings():
    summary = summarize(
        [clause("Psalmi", 1, "Q"), clause("Psalmi", 1, "QN", verse=2), clause("Psalmi", 2, "Q")]
    )
    assert summary.book == "Psalmi"
    assert summary.clauses == 3
    assert summary.chapters == 2
    assert summary.distinct_strings == 2


def test_chapters_with_transition_rate_counts_chapters_that_change():
    summary = summarize(
        [clause("Psalmi", 1, "Q"), clause("Psalmi", 1, "QN", verse=2), clause("Psalmi", 2, "Q")]
    )
    assert summary.chapters_with_transition == 1
    assert summary.chapters_with_transition_rate == 0.5


def test_transitions_per_clause_is_independent_of_the_chapter_division():
    one_chapter = [
        clause("Psalmi", 1, "Q"),
        clause("Psalmi", 1, "QN", verse=2),
        clause("Psalmi", 1, "Q", verse=3),
    ]
    assert summarize(one_chapter).transitions_per_clause == pytest.approx(2 / 3)


def test_rates_of_an_empty_book_are_zero():
    summary = summarize([clause("Psalmi", 1, "Q")])
    object.__setattr__(summary, "chapters", 0)
    object.__setattr__(summary, "clauses", 0)
    assert summary.chapters_with_transition_rate == 0.0
    assert summary.transitions_per_clause == 0.0


def test_mean_depth_averages_the_string_lengths():
    assert summarize([clause("Psalmi", 1, "Q"), clause("Psalmi", 1, "QNQ")]).mean_depth == 2.0


def test_shares_sum_to_one():
    summary = summarize([clause("Psalmi", 1, "Q"), clause("Psalmi", 1, "QN")])
    assert sum(summary.shares.values()) == pytest.approx(1.0)


def test_summarize_rejects_clauses_from_more_than_one_book():
    with pytest.raises(ValueError, match="one book"):
        summarize([clause("Psalmi", 1, "Q"), clause("Genesis", 1, "N")])


def test_summarize_books_returns_one_summary_per_book_in_first_occurrence_order():
    summaries = summarize_books(
        [clause("Psalmi", 1, "Q"), clause("Genesis", 1, "N"), clause("Psalmi", 2, "Q")]
    )
    assert [s.book for s in summaries] == ["Psalmi", "Genesis"]
    assert summaries[0].clauses == 2


def test_domain_share_sums_every_string_ending_in_that_domain():
    summary = summarize(
        [
            clause("Psalmi", 1, "Q"),
            clause("Psalmi", 1, "QN"),
            clause("Psalmi", 1, "QNQ"),
            clause("Psalmi", 1, "D"),
        ]
    )
    assert domain_share(summary, "Q") == pytest.approx(0.5)
    assert domain_share(summary, "N") == pytest.approx(0.25)
