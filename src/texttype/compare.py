"""Summarizes one book's text-type composition so books can be set beside each other."""

from collections import Counter
from dataclasses import dataclass

from texttype.corpus import Clause, clauses_by_chapter
from texttype.transitions import chapters_with_transitions, transitions


@dataclass(frozen=True, slots=True)
class BookSummary:
    """One book's clause counts, text-type shares and frequency of text-type change."""

    book: str
    clauses: int
    chapters: int
    chapters_with_transition: int
    transitions: int
    distinct_strings: int
    mean_depth: float
    shares: dict[str, float]

    @property
    def transitions_per_clause(self) -> float:
        """Transitions divided by clauses, which no division of the book into chapters affects."""
        return self.transitions / self.clauses if self.clauses else 0.0

    @property
    def chapters_with_transition_rate(self) -> float:
        """Fraction of chapters carrying a transition, which chapter length confounds."""
        return self.chapters_with_transition / self.chapters if self.chapters else 0.0


def summarize(clauses: list[Clause]) -> BookSummary:
    """Summarizes the clauses of a single book."""
    books = {c.book for c in clauses}
    if len(books) != 1:
        raise ValueError(f"summarize expects one book, received {sorted(books)}")
    chapters = clauses_by_chapter(clauses)
    found = transitions(clauses)
    changing = chapters_with_transitions(found)
    counts = Counter(c.txt for c in clauses)
    total = len(clauses)
    return BookSummary(
        book=books.pop(),
        clauses=total,
        chapters=len(chapters),
        chapters_with_transition=len(changing),
        transitions=len(found),
        distinct_strings=len(counts),
        mean_depth=sum(len(c.txt) for c in clauses) / total,
        shares={txt: n / total for txt, n in counts.items()},
    )


def summarize_books(clauses: list[Clause]) -> list[BookSummary]:
    """One summary per book present, in the order the books first occur."""
    order: list[str] = []
    grouped: dict[str, list[Clause]] = {}
    for clause in clauses:
        if clause.book not in grouped:
            order.append(clause.book)
            grouped[clause.book] = []
        grouped[clause.book].append(clause)
    return [summarize(grouped[book]) for book in order]


def domain_share(summary: BookSummary, domain: str) -> float:
    """Share of a book's clauses whose innermost text type is the given domain."""
    return sum(share for txt, share in summary.shares.items() if txt.endswith(domain))
