"""Sets the Psalter's text-type composition beside other books as a base rate."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.compare import domain_share, summarize_books
from texttype.corpus import COMPARISON_BOOKS, PSALMS, books_clauses


def main() -> None:
    """Reports per-book text-type shares and within-chapter transition rates."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--books", nargs="*", default=list(COMPARISON_BOOKS))
    args = parser.parse_args()

    books = (PSALMS, *args.books)
    summaries = summarize_books(books_clauses(load_api(args.version), books))

    header = f"{'book':<12}{'clauses':>8}{'chaps':>7}{'cl/chap':>8}{'trans/cl':>10}{'depth':>7}"
    header += f"{'strings':>8}{'Q':>7}{'N':>7}{'D':>7}{'?':>7}"
    print(f"BHSA {args.version}")
    print(header)
    for s in summaries:
        row = f"{s.book:<12}{s.clauses:>8}{s.chapters:>7}{s.clauses / s.chapters:>8.0f}"
        row += f"{s.transitions_per_clause:>10.3f}{s.mean_depth:>7.2f}{s.distinct_strings:>8}"
        for domain in ("Q", "N", "D", "?"):
            row += f"{domain_share(s, domain):>7.1%}"
        print(row)


if __name__ == "__main__":
    main()
