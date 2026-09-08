"""Reports which formal markers occur in the clause each text-type transition lands on."""

import argparse
from collections import Counter

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import PSALMS, book_clauses
from texttype.profile import profile_matrix, vocabulary
from texttype.transitions import transitions
from texttype.triggers import TRIGGER_FEATURES, markers_for_nodes


def main() -> None:
    """Registers the markers present where the text type changes, without assigning a cause."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--to", default="", help="only transitions into this text-type string")
    args = parser.parse_args()

    api = load_api(args.version, TRIGGER_FEATURES)
    clauses = book_clauses(api, PSALMS)
    found = [t for t in transitions(clauses) if not args.to or t.to_txt == args.to]
    markers = markers_for_nodes(api, [t.to_node for t in found])

    print(
        f"BHSA {args.version}: {len(found)} transitions" + (f" into {args.to}" if args.to else "")
    )
    combinations = Counter(markers[t.to_node].present() for t in found)
    print(f"\n{'markers present in the landing clause':<52}{'count':>7}")
    for combination, n in combinations.most_common():
        label = ", ".join(combination) if combination else "(none)"
        print(f"{label:<52}{n:>7}")

    vocab = vocabulary(clauses)
    keys, matrix = profile_matrix(clauses, vocab)
    print(f"\nper-chapter profile: {len(keys)} chapters over {len(vocab)} strings")
    print(f"mean share of the most common string: {matrix[:, vocab.index('Q')].mean():.3f}")


if __name__ == "__main__":
    main()
