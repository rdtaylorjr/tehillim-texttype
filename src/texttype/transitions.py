"""Registers where the text type changes between consecutive clauses of a chapter."""

from collections import Counter
from dataclasses import dataclass
from itertools import pairwise

from texttype.corpus import Clause, clauses_by_chapter

ENTRY = "entry"
RETURN = "return"
SWITCH = "switch"


@dataclass(frozen=True, slots=True)
class Transition:
    """A change of text-type string between two consecutive clauses."""

    book: str
    chapter: int
    from_txt: str
    to_txt: str
    from_node: int
    to_node: int
    verse: int
    depth_change: int

    @property
    def kind(self) -> str:
        """Whether an embedding level opened, closed, or was replaced at the same position."""
        if self.to_txt.startswith(self.from_txt) and self.depth_change > 0:
            return ENTRY
        if self.from_txt.startswith(self.to_txt) and self.depth_change < 0:
            return RETURN
        return SWITCH

    def opens(self, domain: str) -> bool:
        """Whether this transition opens a new level of the given text-type domain."""
        return self.kind == ENTRY and self.to_txt.endswith(domain)


def transitions(clauses: list[Clause]) -> list[Transition]:
    """Every text-type change between consecutive clauses, within chapters."""
    found: list[Transition] = []
    for (book, chapter), group in sorted(clauses_by_chapter(clauses).items()):
        for before, after in pairwise(group):
            if before.txt == after.txt:
                continue
            found.append(
                Transition(
                    book=book,
                    chapter=chapter,
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


def chapters_with_transitions(found: list[Transition]) -> set[tuple[str, int]]:
    """Chapters in which the text type changes at least once."""
    return {(t.book, t.chapter) for t in found}
