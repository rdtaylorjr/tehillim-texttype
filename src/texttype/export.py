"""Writes the per-chapter profiles and the transition list as CSV."""

import csv
from pathlib import Path

from texttype.corpus import Clause, clauses_by_chapter
from texttype.transitions import Transition

PROFILE_FIELDS = ("book", "chapter", "clauses", "mean_depth", "transitions")
TRANSITION_FIELDS = ("book", "chapter", "verse", "from_txt", "to_txt", "kind", "depth_change")


def write_profiles(
    clauses: list[Clause], found: list[Transition], vocab: list[str], path: Path
) -> int:
    """Writes one row per chapter, holding its size, mean depth and text-type shares."""
    grouped = clauses_by_chapter(clauses)
    counted: dict[tuple[str, int], int] = dict.fromkeys(grouped, 0)
    for transition in found:
        counted[(transition.book, transition.chapter)] += 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([*PROFILE_FIELDS, *vocab])
        for key in sorted(grouped):
            group = grouped[key]
            shares = [sum(1 for c in group if c.txt == txt) / len(group) for txt in vocab]
            writer.writerow(
                [
                    key[0],
                    key[1],
                    len(group),
                    sum(len(c.txt) for c in group) / len(group),
                    counted[key],
                    *[f"{s:.6f}" for s in shares],
                ]
            )
    return len(grouped)


def write_transitions(found: list[Transition], path: Path) -> int:
    """Writes one row per text-type change, with the kind of change it is."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(TRANSITION_FIELDS)
        for t in found:
            writer.writerow(
                [t.book, t.chapter, t.verse, t.from_txt, t.to_txt, t.kind, t.depth_change]
            )
    return len(found)
