"""Builds each chapter's text-type composition as a vector over the attested strings."""

from collections import Counter

import numpy as np

from texttype.corpus import Clause, clauses_by_chapter


def vocabulary(clauses: list[Clause]) -> list[str]:
    """The attested text-type strings, in a fixed order."""
    return sorted({c.txt for c in clauses})


def profile_matrix(
    clauses: list[Clause], vocab: list[str], *, normalize: bool = True
) -> tuple[list[tuple[str, int]], np.ndarray]:
    """Chapter keys and their text-type composition, one row per chapter."""
    grouped = clauses_by_chapter(clauses)
    keys = sorted(grouped)
    index = {txt: i for i, txt in enumerate(vocab)}
    matrix = np.zeros((len(keys), len(vocab)), dtype=np.float64)
    for row, key in enumerate(keys):
        counts = Counter(c.txt for c in grouped[key])
        for txt, n in counts.items():
            if txt in index:
                matrix[row, index[txt]] = n
    if normalize:
        totals = matrix.sum(axis=1, keepdims=True)
        matrix = np.divide(matrix, totals, out=np.zeros_like(matrix), where=totals > 0)
    return keys, matrix


def uniform_chapters(clauses: list[Clause]) -> dict[tuple[str, int], str]:
    """Chapters whose clauses all carry one text-type string, mapped to that string."""
    result = {}
    for key, group in clauses_by_chapter(clauses).items():
        distinct = {c.txt for c in group}
        if len(distinct) == 1:
            result[key] = distinct.pop()
    return dict(sorted(result.items()))
