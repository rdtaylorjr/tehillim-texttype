"""Writes the per-chapter profiles and the transition list to a directory as CSV."""

import argparse
from pathlib import Path

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import PSALMS, book_clauses
from texttype.export import write_profiles, write_transitions
from texttype.profile import vocabulary
from texttype.transitions import transitions


def main() -> None:
    """Exports one book's text-type analysis as two CSV files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--book", default=PSALMS)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    clauses = book_clauses(load_api(args.version), args.book)
    found = transitions(clauses)
    profiles = args.output / f"{args.book.lower()}_profiles.csv"
    changes = args.output / f"{args.book.lower()}_transitions.csv"
    print(f"{write_profiles(clauses, found, vocabulary(clauses), profiles)} chapters -> {profiles}")
    print(f"{write_transitions(found, changes)} transitions -> {changes}")


if __name__ == "__main__":
    main()
