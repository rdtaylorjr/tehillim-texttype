"""Prints one book's text-type inventory, transitions and chapter composition."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import PSALMS, book_clauses
from texttype.inventory import depth_distribution, inventory
from texttype.profile import uniform_chapters
from texttype.transitions import chapters_with_transitions, transition_counts, transitions


def main() -> None:
    """Reports the text-type composition of one book for one BHSA version."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", default=PSALMS)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    clauses = book_clauses(load_api(args.version), args.book)
    counts = inventory(clauses)
    print(f"BHSA {args.version}, {args.book}: {len(clauses)} clauses")
    print(f"\nattested text-type strings: {len(counts)}")
    print(f"{'txt':<8}{'clauses':>9}{'share':>8}{'chapters':>10}")
    for count in counts[: args.top]:
        print(f"{count.txt:<8}{count.clauses:>9}{count.share_of_clauses:>7.1%}{count.chapters:>10}")

    print(f"\nembedding depth: {depth_distribution(clauses)}")

    found = transitions(clauses)
    changing = chapters_with_transitions(found)
    uniform = uniform_chapters(clauses)
    print(f"\n{len(found)} transitions in {len(changing)} chapters")
    print(f"uniform chapters: {len(uniform)}")
    print("\nmost frequent transitions:")
    for (before, after), n in transition_counts(found).most_common(args.top):
        print(f"   {before:<7} -> {after:<7} {n:>5}")


if __name__ == "__main__":
    main()
