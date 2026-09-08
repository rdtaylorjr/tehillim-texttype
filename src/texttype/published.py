"""The text-type tables van Peursen published, held as data for checking a build."""

from dataclasses import dataclass

from texttype.corpus import Clause

PSALMS = "Psalmi"


@dataclass(frozen=True, slots=True)
class PublishedVerse:
    """One verse of a published table, with the text-type values printed for it."""

    book: str
    chapter: int
    verse: int
    text_types: tuple[str, ...]
    printed_rows: int


@dataclass(frozen=True, slots=True)
class Check:
    """One verse compared against its published values."""

    verse: PublishedVerse
    observed: tuple[str, ...]
    clauses: int

    @property
    def values_match(self) -> bool:
        """Whether the distinct text-type values agree, ignoring how many rows were printed."""
        return set(self.observed) == set(self.verse.text_types)

    @property
    def rows_match(self) -> bool:
        """Whether the clause count agrees with the number of rows the article prints."""
        return self.clauses == self.verse.printed_rows


#: Tracing Text Types in Biblical Hebrew, Vetus Testamentum 70 (2020), section 5.2.
PSALM_105 = (
    PublishedVerse(PSALMS, 105, 1, ("Q",), 2),
    PublishedVerse(PSALMS, 105, 8, ("Q",), 1),
    PublishedVerse(PSALMS, 105, 9, ("Q",), 2),
    PublishedVerse(PSALMS, 105, 10, ("QN",), 2),
    PublishedVerse(PSALMS, 105, 11, ("QN", "QNQ"), 2),
)

#: Same article, section 5.2. Verse 8 is printed QN and reads N in BHSA from version c onward.
PSALM_64 = (
    PublishedVerse(PSALMS, 64, 2, ("Q",), 3),
    PublishedVerse(PSALMS, 64, 6, ("Q", "QQ"), 5),
    PublishedVerse(PSALMS, 64, 7, ("Q", "QQ"), 3),
    PublishedVerse(PSALMS, 64, 8, ("QN",), 2),
)

#: Same article, section 5.1.
JUDGES_9 = (PublishedVerse("Judices", 9, 54, ("N", "NQ", "NQQ"), 8),)

#: Same article, section 5.3. The article splits one discontinuous clause across three rows.
GENESIS_43 = (PublishedVerse("Genesis", 43, 32, ("N", "ND"), 8),)

TABLES = {
    "Psalm 105": PSALM_105,
    "Psalm 64": PSALM_64,
    "Judges 9:54": JUDGES_9,
    "Genesis 43:32": GENESIS_43,
}


def check_verse(published: PublishedVerse, clauses: list[Clause]) -> Check:
    """Compares one published verse against the clauses a build produced for it."""
    matching = [
        c
        for c in clauses
        if c.book == published.book
        and c.chapter == published.chapter
        and c.verse == published.verse
    ]
    return Check(verse=published, observed=tuple(c.txt for c in matching), clauses=len(matching))


def check_table(table: tuple[PublishedVerse, ...], clauses: list[Clause]) -> list[Check]:
    """Compares every verse of one published table."""
    return [check_verse(v, clauses) for v in table]


def mismatches(checks: list[Check]) -> list[Check]:
    """The verses whose distinct text-type values disagree with the published table."""
    return [c for c in checks if not c.values_match]
