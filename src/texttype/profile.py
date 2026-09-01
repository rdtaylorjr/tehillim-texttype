"""Builds each psalm's text-type composition as a vector over the attested strings."""

from collections import Counter

import numpy as np

from texttype.corpus import Clause, clauses_by_psalm


def vocabulary(clauses: list[Clause]) -> list[str]:
    """The attested text-type strings, in a fixed order."""
    return sorted({c.txt for c in clauses})


def profile_matrix(
    clauses: list[Clause], vocab: list[str], *, normalize: bool = True
) -> tuple[list[int], np.ndarray]:
    """Psalm numbers and their text-type composition, one row per psalm."""
    grouped = clauses_by_psalm(clauses)
    psalms = sorted(grouped)
    index = {txt: i for i, txt in enumerate(vocab)}
    matrix = np.zeros((len(psalms), len(vocab)), dtype=np.float64)
    for row, psalm in enumerate(psalms):
        counts = Counter(c.txt for c in grouped[psalm])
        for txt, n in counts.items():
            if txt in index:
                matrix[row, index[txt]] = n
    if normalize:
        totals = matrix.sum(axis=1, keepdims=True)
        matrix = np.divide(matrix, totals, out=np.zeros_like(matrix), where=totals > 0)
    return psalms, matrix


def uniform_psalms(clauses: list[Clause]) -> dict[int, str]:
    """Psalms whose clauses all carry one text-type string, mapped to that string."""
    result = {}
    for psalm, group in clauses_by_psalm(clauses).items():
        distinct = {c.txt for c in group}
        if len(distinct) == 1:
            result[psalm] = distinct.pop()
    return dict(sorted(result.items()))
