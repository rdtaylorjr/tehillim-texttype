"""Compares the Psalter's text-type values between two BHSA versions."""

import argparse

from library.bhsa import load_api
from texttype.corpus import PSALMS, book_clauses
from texttype.drift import affected_chapters, change_counts, changes, comparable_count


def main() -> None:
    """Reports every clause position whose text-type string differs between two versions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()

    before = book_clauses(load_api(args.before), PSALMS)
    after = book_clauses(load_api(args.after), PSALMS)
    shared = comparable_count(before, after)
    found = changes(before, after)

    print(f"BHSA {args.before}: {len(before)} clauses")
    print(f"BHSA {args.after}: {len(after)} clauses")
    print(f"comparable positions: {shared}")
    print(f"changed: {len(found)} ({len(found) / shared:.1%})")
    print(f"chapters affected: {affected_chapters(found)}")
    print("\nchanges:")
    for (b, a), n in change_counts(found).most_common():
        print(f"   {b:<8} -> {a:<8} {n:>5}")


if __name__ == "__main__":
    main()
