from texttype.corpus import Clause
from texttype.drift import affected_psalms, change_counts, changes, comparable_count


def clause(psalm, verse, index, txt, node=0):
    return Clause(node=node, psalm=psalm, verse=verse, index_in_verse=index, txt=txt)


def test_changes_finds_positions_whose_text_type_differs():
    before = [clause(64, 8, 0, "QN")]
    after = [clause(64, 8, 0, "N")]
    found = changes(before, after)
    assert len(found) == 1
    assert (found[0].before, found[0].after) == ("QN", "N")


def test_changes_ignores_positions_that_agree():
    assert changes([clause(1, 1, 0, "Q")], [clause(1, 1, 0, "Q")]) == []


def test_changes_ignores_positions_absent_from_either_version():
    assert changes([clause(1, 1, 0, "Q")], [clause(2, 1, 0, "N")]) == []


def test_changes_match_on_position_not_node_number():
    before = [clause(1, 1, 0, "Q", node=5)]
    after = [clause(1, 1, 0, "N", node=9999)]
    assert len(changes(before, after)) == 1


def test_comparable_count_is_the_shared_position_count():
    before = [clause(1, 1, 0, "Q"), clause(1, 2, 0, "Q")]
    after = [clause(1, 1, 0, "Q")]
    assert comparable_count(before, after) == 1


def test_change_counts_and_affected_psalms_summarize_the_differences():
    found = changes(
        [clause(1, 1, 0, "Q"), clause(2, 1, 0, "Q")],
        [clause(1, 1, 0, "N"), clause(2, 1, 0, "N")],
    )
    assert change_counts(found)[("Q", "N")] == 2
    assert affected_psalms(found) == [1, 2]
