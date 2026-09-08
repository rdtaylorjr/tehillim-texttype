"""Tests whether a psalm's text-type profile recovers a received genre classification."""

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DEFAULT_PERMUTATIONS = 2000
DEFAULT_SEED = 20260831


@dataclass(frozen=True, slots=True)
class Separation:
    """How far same-genre psalm pairs sit from different-genre pairs, and how likely by chance."""

    auc: float
    n_same: int
    n_different: int
    permutations: int
    p_value: float


def read_labels(path: Path) -> dict[int, str]:
    """Reads a psalm-number to genre mapping from a CSV with Psalm and Genre columns."""
    labels: dict[int, str] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            number = row["Psalm"].split()[-1]
            labels[int(number)] = row["Genre"]
    return labels


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    """Euclidean distance between every pair of rows, as a square matrix."""
    squared = np.sum(matrix**2, axis=1)
    gram = matrix @ matrix.T
    distances = np.maximum(squared[:, None] + squared[None, :] - 2 * gram, 0.0)
    return np.asarray(np.sqrt(distances))


def _upper_triangle(values: np.ndarray) -> np.ndarray:
    """The values above the diagonal, which hold each unordered pair once."""
    rows, cols = np.triu_indices(values.shape[0], k=1)
    return np.asarray(values[rows, cols])


def _auc(same: np.ndarray, different: np.ndarray) -> float:
    """Probability a same-genre pair is closer than a different-genre pair, ties counted half."""
    if same.size == 0 or different.size == 0:
        return 0.5
    combined = np.concatenate([same, different])
    order = np.argsort(np.argsort(combined))
    ranks = order.astype(np.float64) + 1.0
    unique, inverse, counts = np.unique(combined, return_inverse=True, return_counts=True)
    mean_ranks = np.zeros(unique.size)
    np.add.at(mean_ranks, inverse, ranks)
    mean_ranks /= counts
    tie_corrected = mean_ranks[inverse]
    statistic = tie_corrected[: same.size].sum() - same.size * (same.size + 1) / 2
    return 1.0 - statistic / (same.size * different.size)


def same_genre_mask(labels: Sequence[str] | np.ndarray) -> np.ndarray:
    """Boolean vector over unordered psalm pairs, true where both psalms share a genre."""
    array = np.asarray(labels, dtype=object)
    return _upper_triangle(array[:, None] == array[None, :])


def separation(
    matrix: np.ndarray,
    labels: Sequence[str],
    permutations: int = DEFAULT_PERMUTATIONS,
    seed: int = DEFAULT_SEED,
) -> Separation:
    """Scores whether same-genre psalms sit closer together, against a psalm-label permutation."""
    distances = _upper_triangle(pairwise_distances(matrix))
    mask = same_genre_mask(labels)
    observed = _auc(distances[mask], distances[~mask])

    rng = np.random.default_rng(seed)
    shuffled = np.asarray(labels, dtype=object)
    at_least = 1
    for _ in range(permutations):
        drawn = rng.permutation(shuffled)
        drawn_mask = same_genre_mask(drawn)
        if _auc(distances[drawn_mask], distances[~drawn_mask]) >= observed:
            at_least += 1
    return Separation(
        auc=observed,
        n_same=int(mask.sum()),
        n_different=int((~mask).sum()),
        permutations=permutations,
        p_value=at_least / (permutations + 1),
    )
