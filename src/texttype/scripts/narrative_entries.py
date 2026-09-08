"""Reports every clause where a narrative level opens, and the marker it carries."""

import argparse
from collections import Counter

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import PSALMS, book_clauses
from texttype.transitions import ENTRY, RETURN, transitions
from texttype.triggers import TRIGGER_FEATURES, clause_markers


def main() -> None:
    """Separates entry into a narrative level from return to one already open."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", default=PSALMS)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    args = parser.parse_args()

    api = load_api(args.version, TRIGGER_FEATURES)
    found = transitions(book_clauses(api, args.book))
    entries = [t for t in found if t.opens("N")]
    returns = [t for t in found if t.kind == RETURN and t.to_txt.endswith("N")]

    print(f"BHSA {args.version}, {args.book}: {len(found)} transitions")
    print(f"entries into a narrative level: {len(entries)}")
    print(f"returns to a narrative level already open: {len(returns)}")

    for label, group in ((ENTRY, entries), (RETURN, returns)):
        marked = Counter(
            "wayyiqtol" if clause_markers(api, t.to_node).wayyiqtol else "no wayyiqtol"
            for t in group
        )
        print(f"\n{label}: {dict(marked)}")

    unmarked = [t for t in entries if not clause_markers(api, t.to_node).wayyiqtol]
    print(f"\nentries lacking a wayyiqtol: {len(unmarked)}")
    for t in unmarked:
        print(f"   {t.book} {t.chapter}:{t.verse}  {t.from_txt} -> {t.to_txt}")


if __name__ == "__main__":
    main()
