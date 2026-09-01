"""Compares the text-type value of the same clause position across two BHSA versions."""

from collections import Counter
from dataclasses import dataclass

from texttype.corpus import Clause, clause_key


@dataclass(frozen=True, slots=True)
class Change:
    """One clause position whose text-type string differs between two versions."""

    psalm: int
    verse: int
    index_in_verse: int
    before: str
    after: str


def changes(before: list[Clause], after: list[Clause]) -> list[Change]:
    """Clause positions present in both versions whose text-type string differs."""
    left = {clause_key(c): c.txt for c in before}
    right = {clause_key(c): c.txt for c in after}
    shared = sorted(set(left) & set(right))
    return [
        Change(psalm=k[0], verse=k[1], index_in_verse=k[2], before=left[k], after=right[k])
        for k in shared
        if left[k] != right[k]
    ]


def comparable_count(before: list[Clause], after: list[Clause]) -> int:
    """How many clause positions occur in both versions."""
    return len({clause_key(c) for c in before} & {clause_key(c) for c in after})


def change_counts(found: list[Change]) -> Counter[tuple[str, str]]:
    """How often each before/after text-type pair occurs."""
    return Counter((c.before, c.after) for c in found)


def affected_psalms(found: list[Change]) -> list[int]:
    """Psalms containing at least one changed clause."""
    return sorted({c.psalm for c in found})
