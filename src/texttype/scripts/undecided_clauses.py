"""Reports what the clauses carrying an undecided text-type level contain."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import COMPARISON_BOOKS, PSALMS, book_clauses
from texttype.undecided import (
    UNDECIDED_FEATURES,
    describe,
    opening_split,
    undecided,
    verb_profile,
)


def main() -> None:
    """Reports the verb evidence available in undecided clauses, book by book."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--books", nargs="*", default=list(COMPARISON_BOOKS))
    args = parser.parse_args()

    api = load_api(args.version, UNDECIDED_FEATURES)
    print(f"BHSA {args.version}")
    print(f"{'book':<12}{'clauses':>9}{'undecided':>11}{'share':>8}", end="")
    print(f"{'finite':>9}{'non-finite':>12}{'no verb':>9}{'verse 1':>9}{'later':>8}")
    for book in (PSALMS, *args.books):
        clauses = book_clauses(api, book)
        marked = undecided(clauses)
        described = [describe(api, c) for c in marked]
        profile = verb_profile(described)
        total = len(marked) or 1
        print(
            f"{book:<12}{len(clauses):>9}{len(marked):>11}{len(marked) / len(clauses):>7.1%}",
            end="",
        )
        split = opening_split(clauses)
        print(
            f"{profile['finite verb'] / total:>8.0%}"
            f"{profile['non-finite verb only'] / total:>12.0%}"
            f"{profile['no verb'] / total:>9.0%}"
            f"{split.first_verse_rate:>9.0%}{split.later_rate:>8.1%}"
        )


if __name__ == "__main__":
    main()
