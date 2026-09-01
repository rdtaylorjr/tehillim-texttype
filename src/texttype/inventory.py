"""Counts the text-type strings attested in the Psalter."""

from collections import Counter
from dataclasses import dataclass

from texttype.corpus import Clause


@dataclass(frozen=True, slots=True)
class TextTypeCount:
    """One text-type string with its clause and psalm frequency."""

    txt: str
    clauses: int
    psalms: int
    share_of_clauses: float
    depth: int


def inventory(clauses: list[Clause]) -> list[TextTypeCount]:
    """Every attested text-type string, most frequent first."""
    total = len(clauses)
    if total == 0:
        return []
    clause_counts = Counter(c.txt for c in clauses)
    psalms_seen: dict[str, set[int]] = {}
    for clause in clauses:
        psalms_seen.setdefault(clause.txt, set()).add(clause.psalm)
    counts = [
        TextTypeCount(
            txt=txt,
            clauses=n,
            psalms=len(psalms_seen[txt]),
            share_of_clauses=n / total,
            depth=len(txt),
        )
        for txt, n in clause_counts.items()
    ]
    return sorted(counts, key=lambda c: (-c.clauses, c.txt))


def depth_distribution(clauses: list[Clause]) -> dict[int, int]:
    """Clause count at each embedding depth, where depth is the text-type string length."""
    return dict(sorted(Counter(len(c.txt) for c in clauses).items()))
