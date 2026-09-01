"""Registers the formal markers present in a clause, without assigning a cause."""

from dataclasses import dataclass
from typing import Any

TRIGGER_FEATURES = "otype book chapter verse txt domain vt lex function"
VERBA_DICENDI = frozenset({">MR[", "DBR[", "QR>["})
MARKER_NAMES = ("wayyiqtol", "yiqtol", "imperative", "verbum_dicendi", "vocative")


@dataclass(frozen=True, slots=True)
class ClauseMarkers:
    """Which formal markers occur in one clause."""

    node: int
    wayyiqtol: bool
    yiqtol: bool
    imperative: bool
    verbum_dicendi: bool
    vocative: bool

    def present(self) -> tuple[str, ...]:
        """The marker names that occur, in a fixed order."""
        flags = (self.wayyiqtol, self.yiqtol, self.imperative, self.verbum_dicendi, self.vocative)
        return tuple(name for name, flag in zip(MARKER_NAMES, flags, strict=True) if flag)


def clause_markers(api: Any, node: int) -> ClauseMarkers:
    """The formal markers occurring in one clause."""
    F, L = api.F, api.L  # noqa: N806
    words = L.d(node, otype="word")
    tenses = {F.vt.v(w) for w in words}
    lexemes = {F.lex.v(w) for w in words}
    functions = {F.function.v(p) for p in L.d(node, otype="phrase")}
    return ClauseMarkers(
        node=int(node),
        wayyiqtol="wayq" in tenses,
        yiqtol="impf" in tenses,
        imperative="impv" in tenses,
        verbum_dicendi=bool(lexemes & VERBA_DICENDI),
        vocative="Voct" in functions,
    )


def markers_for_nodes(api: Any, nodes: list[int]) -> dict[int, ClauseMarkers]:
    """Formal markers for each of the given clause nodes."""
    return {int(n): clause_markers(api, n) for n in nodes}
