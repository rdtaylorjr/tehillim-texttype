from texttype.corpus import Clause
from texttype.transitions import (
    ENTRY,
    RETURN,
    SWITCH,
    chapters_with_transitions,
    transition_counts,
    transitions,
)


def clause(node, chapter, verse, txt, book="Psalmi"):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def test_transitions_records_each_change_between_consecutive_clauses():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN"), clause(3, 1, 3, "QN")]
    found = transitions(clauses)
    assert len(found) == 1
    assert (found[0].from_txt, found[0].to_txt) == ("Q", "QN")
    assert found[0].verse == 2


def test_transitions_do_not_cross_a_chapter_boundary():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 2, 1, "N")]
    assert transitions(clauses) == []


def test_depth_change_records_nesting_direction():
    clauses = [clause(1, 1, 1, "QNQ"), clause(2, 1, 2, "Q")]
    assert transitions(clauses)[0].depth_change == -2


def test_transition_counts_aggregates_ordered_pairs():
    clauses = [
        clause(1, 1, 1, "Q"),
        clause(2, 1, 2, "QN"),
        clause(3, 1, 3, "Q"),
        clause(4, 1, 4, "QN"),
    ]
    assert transition_counts(transitions(clauses))[("Q", "QN")] == 2


def test_chapters_with_transitions_lists_only_chapters_that_change():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "N"), clause(3, 2, 1, "Q")]
    assert chapters_with_transitions(transitions(clauses)) == {("Psalmi", 1)}


def test_kind_is_entry_when_a_level_opens():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN")]
    assert transitions(clauses)[0].kind == ENTRY


def test_kind_is_return_when_a_level_closes():
    clauses = [clause(1, 1, 1, "QND"), clause(2, 1, 2, "QN")]
    assert transitions(clauses)[0].kind == RETURN


def test_kind_is_switch_when_neither_string_prefixes_the_other():
    clauses = [clause(1, 1, 1, "QN"), clause(2, 1, 2, "QD")]
    assert transitions(clauses)[0].kind == SWITCH


def test_opens_requires_both_an_entry_and_the_named_domain():
    entry_into_narrative = transitions([clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN")])[0]
    assert entry_into_narrative.opens("N") is True
    assert entry_into_narrative.opens("D") is False
    back_to_narrative = transitions([clause(1, 1, 1, "QND"), clause(2, 1, 2, "QN")])[0]
    assert back_to_narrative.opens("N") is False
