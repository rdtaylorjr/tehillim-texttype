from conftest import FakeApi, FakeF, FakeL, FakeT

from texttype.corpus import Clause
from texttype.delimitation import Alignment, align, begins_container, bootstrap_lift
from texttype.transitions import transitions


def clause(node, chapter, verse, txt, book="Psalmi"):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def api_with(down):
    return FakeApi(F=FakeF({}), L=FakeL(down), T=FakeT({}))


class UpFakeL(FakeL):
    """FakeL that also resolves containment upward."""

    def __init__(self, down, up):
        super().__init__(down)
        self._up = up

    def u(self, node, otype):
        return self._up.get((node, otype), [])


def two_clause_api():
    """Clause 1 opens verse 10, clause 2 does not."""
    down = {(1, "word"): [100], (2, "word"): [101], (10, "word"): [100, 101]}
    up = {(100, "verse"): [10], (101, "verse"): [10]}
    return FakeApi(F=FakeF({}), L=UpFakeL(down, up), T=FakeT({}))


def test_begins_container_is_true_only_for_the_first_word():
    api = two_clause_api()
    assert begins_container(api, 1, "verse") is True
    assert begins_container(api, 2, "verse") is False


def test_begins_container_is_false_for_a_clause_with_no_words():
    api = FakeApi(F=FakeF({}), L=UpFakeL({(1, "word"): []}, {}), T=FakeT({}))
    assert begins_container(api, 1, "verse") is False


def test_begins_container_is_false_when_no_container_holds_the_word():
    api = FakeApi(F=FakeF({}), L=UpFakeL({(1, "word"): [100]}, {}), T=FakeT({}))
    assert begins_container(api, 1, "verse") is False


def test_align_counts_clauses_and_transitions_separately():
    api = two_clause_api()
    clauses = [clause(1, 1, 10, "Q"), clause(2, 1, 10, "QN")]
    result = align(api, clauses, transitions(clauses), "verse")
    assert result.clauses == 2
    assert result.clauses_at_start == 1
    assert result.transitions == 1
    assert result.transitions_at_start == 0


def test_lift_is_the_difference_between_the_two_rates():
    result = Alignment(
        container="verse",
        clauses=100,
        clauses_at_start=25,
        transitions=50,
        transitions_at_start=20,
    )
    assert result.base_rate == 0.25
    assert result.transition_rate == 0.4
    assert result.lift == 0.15000000000000002


def test_rates_of_an_empty_alignment_are_zero():
    result = Alignment(
        container="verse", clauses=0, clauses_at_start=0, transitions=0, transitions_at_start=0
    )
    assert result.base_rate == 0.0
    assert result.transition_rate == 0.0


def test_bootstrap_lift_returns_an_ordered_interval():
    api = two_clause_api()
    clauses = [clause(1, 1, 10, "Q"), clause(2, 1, 10, "QN")]
    low, high = bootstrap_lift(api, clauses, transitions(clauses), "verse", resamples=50)
    assert low <= high


def test_bootstrap_lift_is_repeatable_for_one_seed():
    api = two_clause_api()
    clauses = [clause(1, 1, 10, "Q"), clause(2, 1, 10, "QN")]
    found = transitions(clauses)
    first = bootstrap_lift(api, clauses, found, "verse", resamples=50, seed=7)
    assert first == bootstrap_lift(api, clauses, found, "verse", resamples=50, seed=7)
