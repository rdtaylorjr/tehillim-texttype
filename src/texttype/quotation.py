"""Records whether a clause opening a quotation follows a verb of speaking."""

from dataclasses import dataclass
from typing import Any

from texttype.corpus import Clause
from texttype.transitions import ENTRY, Transition
from texttype.triggers import clause_markers


@dataclass(frozen=True, slots=True)
class Opening:
    """One clause that opens a quotation level, and whether a verb of speaking precedes it."""

    book: str
    chapter: int
    verse: int
    from_txt: str
    to_txt: str
    node: int
    introduced: bool


@dataclass(frozen=True, slots=True)
class IntroductionRate:
    """How many quotation openings a verb of speaking introduces."""

    openings: int
    introduced: int

    @property
    def share(self) -> float:
        """Share of quotation openings preceded by a verb of speaking."""
        return self.introduced / self.openings if self.openings else 0.0


def quotation_entries(found: list[Transition]) -> list[Transition]:
    """Transitions that open a quotation level rather than closing or replacing one."""
    return [t for t in found if t.kind == ENTRY and t.to_txt.endswith("Q")]


def openings(api: Any, clauses: list[Clause], found: list[Transition]) -> list[Opening]:
    """Each quotation opening, with whether the clause before it carries a verb of speaking."""
    position = {clause.node: index for index, clause in enumerate(clauses)}
    result = []
    for transition in quotation_entries(found):
        index = position[transition.to_node]
        before = clauses[index - 1] if index else None
        result.append(
            Opening(
                book=transition.book,
                chapter=transition.chapter,
                verse=transition.verse,
                from_txt=transition.from_txt,
                to_txt=transition.to_txt,
                node=transition.to_node,
                introduced=(before is not None and clause_markers(api, before.node).verbum_dicendi),
            )
        )
    return result


def introduction_rate(found: list[Opening]) -> IntroductionRate:
    """Counts how many of the quotation openings a verb of speaking introduces."""
    return IntroductionRate(openings=len(found), introduced=sum(1 for o in found if o.introduced))
