"""Tests whether a psalm's text-type profile recovers a received genre classification."""

import argparse
from pathlib import Path

import numpy as np

from library.bhsa import DEFAULT_VERSION, load_api
from texttype.corpus import PSALMS, book_clauses, clauses_by_chapter
from texttype.genre import read_labels, separation
from texttype.profile import profile_matrix, vocabulary
from texttype.transitions import transitions

FEATURE_SETS = ("full profile", "Q share only", "depth and change only")


def _reduced(matrix: np.ndarray, vocab: list[str], name: str, extra: np.ndarray) -> np.ndarray:
    """Selects one feature set from the full text-type profile."""
    if name == "Q share only":
        return matrix[:, [i for i, v in enumerate(vocab) if v == "Q"]]
    if name == "depth and change only":
        return extra
    return matrix


def main() -> None:
    """Scores each feature set against a psalm-label permutation null."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", type=Path, help="CSV with Psalm and Genre columns")
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--permutations", type=int, default=2000)
    args = parser.parse_args()

    clauses = book_clauses(load_api(args.version), PSALMS)
    vocab = vocabulary(clauses)
    keys, matrix = profile_matrix(clauses, vocab)

    grouped = clauses_by_chapter(clauses)
    found = transitions(clauses)
    changes = dict.fromkeys(grouped, 0)
    for transition in found:
        changes[(transition.book, transition.chapter)] += 1
    extra = np.array(
        [
            [
                sum(len(c.txt) for c in grouped[k]) / len(grouped[k]),
                changes[k] / len(grouped[k]),
            ]
            for k in keys
        ]
    )

    labels_by_psalm = read_labels(args.labels)
    labels = [labels_by_psalm[chapter] for _, chapter in keys]
    print(f"BHSA {args.version}: {len(keys)} psalms, {len(set(labels))} genres")
    print(f"{'feature set':<24}{'dims':>6}{'AUC':>8}{'p':>9}")
    for name in FEATURE_SETS:
        features = _reduced(matrix, vocab, name, extra)
        result = separation(features, labels, permutations=args.permutations)
        print(f"{name:<24}{features.shape[1]:>6}{result.auc:>8.3f}{result.p_value:>9.4f}")
    print(f"\nsame-genre pairs {result.n_same}, different-genre pairs {result.n_different}")


if __name__ == "__main__":
    main()
