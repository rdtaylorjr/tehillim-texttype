"""Reports how often a quotation opening follows a verb of speaking, book by book."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import COMPARISON_BOOKS, PSALMS, book_clauses
from texttype.quotation import introduction_rate, openings
from texttype.transitions import transitions
from texttype.triggers import TRIGGER_FEATURES


def main() -> None:
    """Registers the introduction of quoted speech without assigning a cause."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--books", nargs="*", default=list(COMPARISON_BOOKS))
    parser.add_argument("--deepest", type=int, default=0)
    args = parser.parse_args()

    api = load_api(args.version, TRIGGER_FEATURES)
    print(f"BHSA {args.version}")
    print(f"{'book':<12}{'openings':>10}{'introduced':>12}{'share':>8}{'unintroduced':>14}")
    for book in (PSALMS, *args.books):
        clauses = book_clauses(api, book)
        found = openings(api, clauses, transitions(clauses))
        if not found:
            continue
        rate = introduction_rate(found)
        print(
            f"{book:<12}{rate.openings:>10}{rate.introduced:>12}"
            f"{rate.share:>7.0%}{rate.openings - rate.introduced:>14}"
        )

    if args.deepest:
        clauses = book_clauses(api, PSALMS)
        found = openings(api, clauses, transitions(clauses))
        print(f"\ndeepest quotation nestings in {PSALMS}:")
        for opening in sorted(found, key=lambda o: -len(o.to_txt))[: args.deepest]:
            print(f"   {opening.chapter}:{opening.verse}  {opening.from_txt} -> {opening.to_txt}")


if __name__ == "__main__":
    main()
