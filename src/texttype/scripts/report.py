"""Prints the Psalter's text-type inventory, transitions and per-psalm composition."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import psalter_clauses
from texttype.inventory import depth_distribution, inventory
from texttype.profile import uniform_psalms
from texttype.transitions import psalms_with_transitions, transition_counts, transitions


def main() -> None:
    """Reports the text-type composition of all 150 psalms for one BHSA version."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    clauses = psalter_clauses(load_api(args.version))
    print(f"BHSA {args.version}: {len(clauses)} clauses in 150 psalms")

    counts = inventory(clauses)
    print(f"\nattested text-type strings: {len(counts)}")
    print(f"{'txt':<8}{'clauses':>9}{'share':>8}{'psalms':>8}")
    for count in counts[: args.top]:
        print(f"{count.txt:<8}{count.clauses:>9}{count.share_of_clauses:>7.1%}{count.psalms:>8}")

    print(f"\nembedding depth: {depth_distribution(clauses)}")

    found = transitions(clauses)
    changing = psalms_with_transitions(found)
    print(f"\n{len(found)} transitions in {len(changing)} of 150 psalms")
    print(f"uniform psalms: {uniform_psalms(clauses)}")
    print("\nmost frequent transitions:")
    for (before, after), n in transition_counts(found).most_common(args.top):
        print(f"   {before:<7} -> {after:<7} {n:>5}")


if __name__ == "__main__":
    main()
