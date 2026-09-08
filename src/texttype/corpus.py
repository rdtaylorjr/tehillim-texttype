"""Extracts a book's clauses with their BHSA text-type values."""

from dataclasses import dataclass
from typing import Any

UNKNOWN_TEXT_TYPE = "?"
PSALMS = "Psalmi"
# A psalm is a composition, a chapter of Genesis is a medieval division, so per-chapter rates
# across these books compare incommensurable units. Prefer the per-clause measures.
COMPARISON_BOOKS = (
    "Genesis",
    "Exodus",
    "Josua",
    "Judices",
    "Samuel_I",
    "Samuel_II",
    "Reges_I",
    "Reges_II",
    "Jesaia",
    "Jeremia",
    "Ezechiel",
    "Iob",
    "Proverbia",
    "Threni",
    "Canticum",
)


@dataclass(frozen=True, slots=True)
class Clause:
    """One BHSA clause, with its position and text-type string."""

    node: int
    book: str
    chapter: int
    verse: int
    index_in_verse: int
    txt: str


def clause_key(clause: Clause) -> tuple[str, int, int, int]:
    """Position identifier that is stable across BHSA versions."""
    return (clause.book, clause.chapter, clause.verse, clause.index_in_verse)


def book_node(api: Any, book: str) -> int:
    """The book node for one book name."""
    for node in api.F.otype.s("book"):
        if api.F.book.v(node) == book:
            return int(node)
    raise RuntimeError(f"Book {book} not found in this BHSA version")


def book_clauses(api: Any, book: str) -> list[Clause]:
    """Every clause of one book, in canonical order."""
    F, L, T = api.F, api.L, api.T  # noqa: N806
    clauses: list[Clause] = []
    for chapter_node in L.d(book_node(api, book), otype="chapter"):
        chapter = T.sectionFromNode(chapter_node)[1]
        for verse_node in L.d(chapter_node, otype="verse"):
            verse = T.sectionFromNode(verse_node)[2]
            for index, node in enumerate(L.d(verse_node, otype="clause")):
                clauses.append(
                    Clause(
                        node=int(node),
                        book=book,
                        chapter=chapter,
                        verse=verse,
                        index_in_verse=index,
                        txt=F.txt.v(node) or UNKNOWN_TEXT_TYPE,
                    )
                )
    return clauses


def books_clauses(api: Any, books: tuple[str, ...]) -> list[Clause]:
    """Every clause of several books, in the order the books are given."""
    return [c for book in books for c in book_clauses(api, book)]


def clauses_by_chapter(clauses: list[Clause]) -> dict[tuple[str, int], list[Clause]]:
    """The clauses of each chapter, keyed by book name and chapter number."""
    grouped: dict[tuple[str, int], list[Clause]] = {}
    for clause in clauses:
        grouped.setdefault((clause.book, clause.chapter), []).append(clause)
    return grouped
