"""Extracts the Psalter's clauses with their BHSA text-type values."""

from dataclasses import dataclass
from typing import Any

from library.bhsa import psalm_chapter_nodes

UNKNOWN_TEXT_TYPE = "?"


@dataclass(frozen=True, slots=True)
class Clause:
    """One BHSA clause in the Psalter, with its position and text-type string."""

    node: int
    psalm: int
    verse: int
    index_in_verse: int
    txt: str


def clause_key(clause: Clause) -> tuple[int, int, int]:
    """Position identifier that is stable across BHSA versions."""
    return (clause.psalm, clause.verse, clause.index_in_verse)


def psalter_clauses(api: Any) -> list[Clause]:
    """Every clause of the 150 psalms, in canonical order."""
    F, L, T = api.F, api.L, api.T  # noqa: N806
    clauses: list[Clause] = []
    for psalm, chapter in sorted(psalm_chapter_nodes(api).items()):
        for verse_node in L.d(chapter, otype="verse"):
            verse = T.sectionFromNode(verse_node)[2]
            for index, node in enumerate(L.d(verse_node, otype="clause")):
                clauses.append(
                    Clause(
                        node=int(node),
                        psalm=psalm,
                        verse=verse,
                        index_in_verse=index,
                        txt=F.txt.v(node) or UNKNOWN_TEXT_TYPE,
                    )
                )
    return clauses


def clauses_by_psalm(clauses: list[Clause]) -> dict[int, list[Clause]]:
    """The clauses of each psalm, keyed by psalm number."""
    grouped: dict[int, list[Clause]] = {}
    for clause in clauses:
        grouped.setdefault(clause.psalm, []).append(clause)
    return grouped
