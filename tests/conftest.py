"""Fakes standing in for a Text-Fabric api, so tests never load BHSA."""

from dataclasses import dataclass, field

import pytest


class FakeFeature:
    """One Text-Fabric feature: a node-to-value mapping."""

    def __init__(self, values):
        self._values = values

    def v(self, node):
        return self._values.get(node)

    def s(self, value):
        return [n for n, v in self._values.items() if v == value]


@dataclass
class FakeF:
    """The api.F namespace, holding one FakeFeature per feature name."""

    features: dict = field(default_factory=dict)

    def __getattr__(self, name):
        try:
            return self.features[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


class FakeL:
    """The api.L namespace, resolving containment by an explicit map."""

    def __init__(self, down):
        self._down = down

    def d(self, node, otype):
        return self._down.get((node, otype), [])


class FakeT:
    """The api.T namespace, resolving a node to its (book, chapter, verse) section."""

    def __init__(self, sections):
        self._sections = sections

    def sectionFromNode(self, node):  # noqa: N802 -- Text-Fabric's method name
        return self._sections[node]


@dataclass
class FakeApi:
    """A Text-Fabric api with the three namespaces the code uses."""

    F: FakeF
    L: FakeL
    T: FakeT


@pytest.fixture
def two_psalm_api():
    """Two psalms: psalm 1 with one Q clause, psalm 2 with a Q clause then a QN clause."""
    otype = {
        100: "book",
        110: "chapter",
        120: "chapter",
        111: "verse",
        121: "verse",
        1: "clause",
        2: "clause",
        3: "clause",
    }
    book = {100: "Psalmi"}
    txt = {1: "Q", 2: "Q", 3: "QN"}
    down = {
        (100, "chapter"): [110, 120],
        (110, "verse"): [111],
        (120, "verse"): [121],
        (111, "clause"): [1],
        (121, "clause"): [2, 3],
    }
    sections = {
        110: ("Psalmi", 1),
        120: ("Psalmi", 2),
        111: ("Psalmi", 1, 1),
        121: ("Psalmi", 2, 1),
    }
    f = FakeF({"otype": FakeFeature(otype), "book": FakeFeature(book), "txt": FakeFeature(txt)})
    return FakeApi(F=f, L=FakeL(down), T=FakeT(sections))
