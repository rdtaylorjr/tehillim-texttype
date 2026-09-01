"""Registers where the text type changes between consecutive clauses of a psalm."""

from collections import Counter
from dataclasses import dataclass
from itertools import pairwise

from texttype.corpus import Clause, clauses_by_psalm


@dataclass(frozen=True, slots=True)
class Transition:
    """A change of text-type string between two consecutive clauses."""

    psalm: int
    from_txt: str
    to_txt: str
    from_node: int
    to_node: int
    verse: int
    depth_change: int


def transitions(clauses: list[Clause]) -> list[Transition]:
    """Every text-type change between consecutive clauses, within psalms."""
    found: list[Transition] = []
    for psalm, group in sorted(clauses_by_psalm(clauses).items()):
        for before, after in pairwise(group):
            if before.txt == after.txt:
                continue
            found.append(
                Transition(
                    psalm=psalm,
                    from_txt=before.txt,
                    to_txt=after.txt,
                    from_node=before.node,
                    to_node=after.node,
                    verse=after.verse,
                    depth_change=len(after.txt) - len(before.txt),
                )
            )
    return found


def transition_counts(found: list[Transition]) -> Counter[tuple[str, str]]:
    """How often each ordered text-type change occurs."""
    return Counter((t.from_txt, t.to_txt) for t in found)


def psalms_with_transitions(found: list[Transition]) -> set[int]:
    """Psalms in which the text type changes at least once."""
    return {t.psalm for t in found}
