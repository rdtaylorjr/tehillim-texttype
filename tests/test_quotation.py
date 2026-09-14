from conftest import FakeApi, FakeF, FakeFeature, FakeL, FakeT

from texttype.corpus import Clause
from texttype.quotation import (
    IntroductionRate,
    introduction_rate,
    openings,
    quotation_entries,
)
from texttype.transitions import transitions


def clause(node, verse, txt, book="Psalmi", chapter=1):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def api_with(lex):
    f = FakeF({"vt": FakeFeature({}), "lex": FakeFeature(lex), "function": FakeFeature({})})
    down = {(n, "word"): [n * 10] for n in (1, 2, 3)} | {(n, "phrase"): [] for n in (1, 2, 3)}
    return FakeApi(F=f, L=FakeL(down), T=FakeT({}))


def test_quotation_entries_keeps_only_openings_of_a_quotation_level():
    clauses = [clause(1, 1, "Q"), clause(2, 2, "QN"), clause(3, 3, "QNQ")]
    entries = quotation_entries(transitions(clauses))
    assert [t.to_txt for t in entries] == ["QNQ"]


def test_a_return_to_a_quotation_level_is_not_an_opening():
    clauses = [clause(1, 1, "QQ"), clause(2, 2, "Q")]
    assert quotation_entries(transitions(clauses)) == []


def test_an_opening_after_a_verb_of_speaking_is_introduced():
    clauses = [clause(1, 1, "Q"), clause(2, 2, "QQ")]
    api = api_with({10: ">MR["})
    assert openings(api, clauses, transitions(clauses))[0].introduced is True


def test_an_opening_without_a_preceding_verb_of_speaking_is_not_introduced():
    clauses = [clause(1, 1, "Q"), clause(2, 2, "QQ")]
    api = api_with({10: "MLK/"})
    assert openings(api, clauses, transitions(clauses))[0].introduced is False


def test_an_opening_in_the_first_clause_has_nothing_before_it():
    clauses = [clause(1, 1, "Q"), clause(2, 2, "QQ")]
    api = api_with({})
    found = openings(api, clauses, transitions(clauses))
    assert found[0].introduced is False


def test_openings_record_their_position_and_strings():
    clauses = [clause(1, 1, "Q"), clause(2, 5, "QQ")]
    opening = openings(api_with({10: ">MR["}), clauses, transitions(clauses))[0]
    assert (opening.book, opening.chapter, opening.verse) == ("Psalmi", 1, 5)
    assert (opening.from_txt, opening.to_txt) == ("Q", "QQ")


def test_introduction_rate_counts_and_divides():
    clauses = [clause(1, 1, "Q"), clause(2, 2, "QQ")]
    rate = introduction_rate(openings(api_with({10: ">MR["}), clauses, transitions(clauses)))
    assert rate == IntroductionRate(openings=1, introduced=1)
    assert rate.share == 1.0


def test_introduction_rate_of_no_openings_is_zero():
    assert introduction_rate([]).share == 0.0
