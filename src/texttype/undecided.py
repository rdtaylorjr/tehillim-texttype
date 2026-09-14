"""Describes the clauses whose text type the syntax does not decide."""

from collections import Counter
from dataclasses import dataclass
from typing import Any

from texttype.corpus import Clause

UNDECIDED_FEATURES = "otype book chapter verse txt domain vt sp"
FINITE_TENSES = frozenset({"perf", "impf", "wayq", "impv"})


@dataclass(frozen=True, slots=True)
class UndecidedClause:
    """One clause carrying an undecided level, with the verb evidence it offers."""

    node: int
    book: str
    chapter: int
    verse: int
    txt: str
    tenses: tuple[str, ...]
    has_finite_verb: bool
    has_verb: bool


def undecided(clauses: list[Clause]) -> list[Clause]:
    """Clauses whose text-type string carries an undecided level."""
    return [c for c in clauses if "?" in c.txt]


def describe(api: Any, clause: Clause) -> UndecidedClause:
    """Records which verb forms one clause contains."""
    words = api.L.d(clause.node, otype="word")
    tenses = tuple(sorted({api.F.vt.v(w) for w in words if api.F.vt.v(w) not in (None, "NA")}))
    return UndecidedClause(
        node=clause.node,
        book=clause.book,
        chapter=clause.chapter,
        verse=clause.verse,
        txt=clause.txt,
        tenses=tenses,
        has_finite_verb=bool(set(tenses) & FINITE_TENSES),
        has_verb=any(api.F.sp.v(w) == "verb" for w in words),
    )


def verb_profile(described: list[UndecidedClause]) -> Counter[str]:
    """How many undecided clauses have a finite verb, a non-finite verb, or none."""
    profile: Counter[str] = Counter()
    for clause in described:
        if clause.has_finite_verb:
            profile["finite verb"] += 1
        elif clause.has_verb:
            profile["non-finite verb only"] += 1
        else:
            profile["no verb"] += 1
    return profile


@dataclass(frozen=True, slots=True)
class OpeningSplit:
    """Undecided rate in the first verse of a chapter against the rate everywhere else."""

    first_verse_clauses: int
    first_verse_undecided: int
    later_clauses: int
    later_undecided: int

    @property
    def first_verse_rate(self) -> float:
        """Share of first-verse clauses carrying an undecided level."""
        return (
            self.first_verse_undecided / self.first_verse_clauses
            if self.first_verse_clauses
            else 0.0
        )

    @property
    def later_rate(self) -> float:
        """Share of clauses outside the first verse carrying an undecided level."""
        if not self.later_clauses:
            return 0.0
        return self.later_undecided / self.later_clauses


def opening_split(clauses: list[Clause]) -> OpeningSplit:
    """Splits undecided clauses by whether they stand in a chapter's first verse."""
    first = [c for c in clauses if c.verse == 1]
    later = [c for c in clauses if c.verse != 1]
    return OpeningSplit(
        first_verse_clauses=len(first),
        first_verse_undecided=sum(1 for c in first if "?" in c.txt),
        later_clauses=len(later),
        later_undecided=sum(1 for c in later if "?" in c.txt),
    )
