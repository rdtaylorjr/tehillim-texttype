from texttype.corpus import Clause
from texttype.transitions import (
    psalms_with_transitions,
    transition_counts,
    transitions,
)


def clause(node, psalm, verse, txt):
    return Clause(node=node, psalm=psalm, verse=verse, index_in_verse=0, txt=txt)


def test_transitions_records_each_change_between_consecutive_clauses():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN"), clause(3, 1, 3, "QN")]
    found = transitions(clauses)
    assert len(found) == 1
    assert (found[0].from_txt, found[0].to_txt) == ("Q", "QN")
    assert found[0].verse == 2


def test_transitions_do_not_cross_a_psalm_boundary():
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


def test_psalms_with_transitions_lists_only_psalms_that_change():
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "N"), clause(3, 2, 1, "Q")]
    assert psalms_with_transitions(transitions(clauses)) == {1}
