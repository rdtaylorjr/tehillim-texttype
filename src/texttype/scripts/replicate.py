"""Checks a BHSA version against the text-type tables van Peursen published."""

import argparse

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import book_clauses
from texttype.published import TABLES, check_table, mismatches


def main() -> None:
    """Reports, per published table, whether the build reproduces its text-type values."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    args = parser.parse_args()

    api = load_api(args.version)
    books = {v.book for table in TABLES.values() for v in table}
    clauses = [c for book in sorted(books) for c in book_clauses(api, book)]

    print(f"BHSA {args.version}")
    total_bad = 0
    for name, table in TABLES.items():
        checks = check_table(table, clauses)
        bad = mismatches(checks)
        total_bad += len(bad)
        status = "reproduces" if not bad else f"{len(bad)} verse(s) differ"
        print(f"\n{name}: {status}")
        for check in checks:
            flag = " " if check.values_match else "*"
            rows = (
                ""
                if check.rows_match
                else f"  [{check.clauses} clauses, {check.verse.printed_rows} rows printed]"
            )
            print(
                f" {flag} {check.verse.chapter}:{check.verse.verse:<3} "
                f"published {'/'.join(check.verse.text_types):<10} "
                f"observed {'/'.join(check.observed)}{rows}"
            )
    print(f"\ntotal verses differing: {total_bad}")


if __name__ == "__main__":
    main()
