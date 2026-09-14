"""Confronts text-type transitions with the received verse division, against its base rate."""

from dataclasses import dataclass
from typing import Any

import numpy as np

from texttype.corpus import Clause
from texttype.transitions import Transition

DEFAULT_RESAMPLES = 2000
DEFAULT_SEED = 20260831


@dataclass(frozen=True, slots=True)
class Alignment:
    """How often transitions begin a container, against how often any clause does."""

    container: str
    clauses: int
    clauses_at_start: int
    transitions: int
    transitions_at_start: int

    @property
    def base_rate(self) -> float:
        """Share of all clauses that begin the container."""
        return self.clauses_at_start / self.clauses if self.clauses else 0.0

    @property
    def transition_rate(self) -> float:
        """Share of transitions whose landing clause begins the container."""
        return self.transitions_at_start / self.transitions if self.transitions else 0.0

    @property
    def lift(self) -> float:
        """Transition rate minus base rate, which is zero when the two are unrelated."""
        return self.transition_rate - self.base_rate


def begins_container(api: Any, node: int, container: str) -> bool:
    """Whether this clause's first word is also the container's first word."""
    words = api.L.d(node, otype="word")
    if not words:
        return False
    holding = api.L.u(words[0], otype=container)
    return bool(holding) and api.L.d(holding[0], otype="word")[0] == words[0]


def align(api: Any, clauses: list[Clause], found: list[Transition], container: str) -> Alignment:
    """Counts clauses and transitions that begin the container."""
    return Alignment(
        container=container,
        clauses=len(clauses),
        clauses_at_start=sum(1 for c in clauses if begins_container(api, c.node, container)),
        transitions=len(found),
        transitions_at_start=sum(1 for t in found if begins_container(api, t.to_node, container)),
    )


def bootstrap_lift(
    api: Any,
    clauses: list[Clause],
    found: list[Transition],
    container: str,
    resamples: int = DEFAULT_RESAMPLES,
    seed: int = DEFAULT_SEED,
) -> tuple[float, float]:
    """Percentile interval on the lift, resampling chapters since clauses within one correlate."""
    at_start = {c.node: begins_container(api, c.node, container) for c in clauses}
    by_chapter: dict[tuple[str, int], tuple[list[bool], list[bool]]] = {}
    for clause in clauses:
        by_chapter.setdefault((clause.book, clause.chapter), ([], []))[0].append(
            at_start[clause.node]
        )
    for transition in found:
        key = (transition.book, transition.chapter)
        by_chapter.setdefault(key, ([], []))[1].append(
            begins_container(api, transition.to_node, container)
        )

    keys = list(by_chapter)
    rng = np.random.default_rng(seed)
    lifts = np.empty(resamples, dtype=np.float64)
    for i in range(resamples):
        drawn = rng.integers(0, len(keys), size=len(keys))
        clause_flags = [f for j in drawn for f in by_chapter[keys[j]][0]]
        transition_flags = [f for j in drawn for f in by_chapter[keys[j]][1]]
        base = sum(clause_flags) / len(clause_flags) if clause_flags else 0.0
        rate = sum(transition_flags) / len(transition_flags) if transition_flags else base
        lifts[i] = rate - base
    return (float(np.percentile(lifts, 2.5)), float(np.percentile(lifts, 97.5)))
