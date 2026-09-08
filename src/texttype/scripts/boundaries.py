"""Reports how often text-type transitions fall on a received division, against its base rate."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import COMPARISON_BOOKS, PSALMS, book_clauses
from texttype.delimitation import align, bootstrap_lift
from texttype.transitions import transitions

CONTAINERS = ("verse", "half_verse")


def main() -> None:
    """Confronts the ETCBC text-type analysis with the Masoretic division of the text."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--books", nargs="*", default=list(COMPARISON_BOOKS))
    parser.add_argument("--resamples", type=int, default=2000)
    args = parser.parse_args()

    api = load_api(args.version)
    print(f"BHSA {args.version}")
    print(f"{'book':<12}{'container':<12}{'base':>7}{'at transition':>15}{'lift':>8}{'95% CI':>18}")
    for book in (PSALMS, *args.books):
        clauses = book_clauses(api, book)
        found = transitions(clauses)
        for container in CONTAINERS:
            result = align(api, clauses, found, container)
            low, high = bootstrap_lift(api, clauses, found, container, resamples=args.resamples)
            print(
                f"{book:<12}{container:<12}{result.base_rate:>6.1%}"
                f"{result.transition_rate:>14.1%}{result.lift:>+8.1%}"
                f"{f'[{low:+.1%}, {high:+.1%}]':>18}"
            )


if __name__ == "__main__":
    main()
