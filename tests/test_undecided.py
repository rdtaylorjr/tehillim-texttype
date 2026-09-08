from conftest import FakeApi, FakeF, FakeFeature, FakeL, FakeT

from texttype.corpus import Clause
from texttype.undecided import describe, undecided, verb_profile


def clause(txt, node=1):
    return Clause(node=node, book="Psalmi", chapter=1, verse=1, index_in_verse=0, txt=txt)


def api_with(words, vt=None, sp=None):
    f = FakeF({"vt": FakeFeature(vt or {}), "sp": FakeFeature(sp or {})})
    return FakeApi(F=f, L=FakeL({(1, "word"): words}), T=FakeT({}))


def test_undecided_selects_every_string_carrying_an_unknown_level():
    clauses = [clause("Q"), clause("?"), clause("?Q"), clause("QN"), clause("??ND")]
    assert [c.txt for c in undecided(clauses)] == ["?", "?Q", "??ND"]


def test_describe_collects_the_distinct_verb_tenses():
    api = api_with([10, 11], vt={10: "perf", 11: "perf"})
    assert describe(api, clause("?")).tenses == ("perf",)


def test_describe_ignores_the_not_applicable_tense():
    api = api_with([10, 11], vt={10: "NA", 11: "ptca"})
    assert describe(api, clause("?")).tenses == ("ptca",)


def test_a_participle_is_a_verb_but_not_a_finite_one():
    api = api_with([10], vt={10: "ptca"}, sp={10: "verb"})
    described = describe(api, clause("?"))
    assert described.has_verb is True
    assert described.has_finite_verb is False


def test_a_qatal_is_a_finite_verb():
    api = api_with([10], vt={10: "perf"}, sp={10: "verb"})
    assert describe(api, clause("?")).has_finite_verb is True


def test_a_clause_without_a_verb_records_neither():
    api = api_with([10], sp={10: "subs"})
    described = describe(api, clause("?"))
    assert described.has_verb is False
    assert described.has_finite_verb is False


def test_verb_profile_sorts_clauses_into_three_groups():
    finite = describe(api_with([10], vt={10: "perf"}, sp={10: "verb"}), clause("?"))
    participle = describe(api_with([10], vt={10: "ptca"}, sp={10: "verb"}), clause("?"))
    verbless = describe(api_with([10], sp={10: "subs"}), clause("?"))
    profile = verb_profile([finite, participle, verbless])
    assert profile["finite verb"] == 1
    assert profile["non-finite verb only"] == 1
    assert profile["no verb"] == 1


def test_opening_split_separates_the_first_verse_from_the_rest():
    from texttype.undecided import opening_split

    clauses = [
        Clause(node=1, book="Psalmi", chapter=3, verse=1, index_in_verse=0, txt="?"),
        Clause(node=2, book="Psalmi", chapter=3, verse=1, index_in_verse=1, txt="Q"),
        Clause(node=3, book="Psalmi", chapter=3, verse=2, index_in_verse=0, txt="Q"),
        Clause(node=4, book="Psalmi", chapter=3, verse=3, index_in_verse=0, txt="Q"),
    ]
    split = opening_split(clauses)
    assert split.first_verse_rate == 0.5
    assert split.later_rate == 0.0


def test_opening_split_rates_are_zero_without_clauses():
    from texttype.undecided import opening_split

    split = opening_split([])
    assert split.first_verse_rate == 0.0
    assert split.later_rate == 0.0
