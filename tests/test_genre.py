import numpy as np
import pytest

from texttype.genre import (
    pairwise_distances,
    read_labels,
    same_genre_mask,
    separation,
)


def test_read_labels_maps_psalm_number_to_genre(tmp_path):
    path = tmp_path / "labels.csv"
    path.write_text("Psalm,Genre\nPs 1,Wisdom\nPs 23,Trust\n", encoding="utf-8")
    assert read_labels(path) == {1: "Wisdom", 23: "Trust"}


def test_read_labels_ignores_other_columns(tmp_path):
    path = tmp_path / "labels.csv"
    path.write_text("Psalm,Attribution,Genre\nPs 8,David,Praise\n", encoding="utf-8")
    assert read_labels(path) == {8: "Praise"}


def test_pairwise_distances_are_symmetric_with_a_zero_diagonal():
    matrix = np.array([[0.0, 0.0], [3.0, 4.0]])
    distances = pairwise_distances(matrix)
    np.testing.assert_allclose(distances, [[0.0, 5.0], [5.0, 0.0]], atol=1e-9)


def test_pairwise_distances_never_go_negative_through_rounding():
    matrix = np.ones((3, 4))
    assert pairwise_distances(matrix).min() >= 0.0


def test_same_genre_mask_covers_every_unordered_pair_once():
    mask = same_genre_mask(["a", "a", "b"])
    assert mask.tolist() == [True, False, False]


def test_separation_is_one_when_same_genre_psalms_coincide():
    matrix = np.array([[0.0], [0.0], [10.0], [10.0]])
    result = separation(matrix, ["a", "a", "b", "b"], permutations=50)
    assert result.auc == 1.0
    assert result.n_same == 2
    assert result.n_different == 4


def test_separation_is_near_half_when_the_labels_carry_no_information():
    rng = np.random.default_rng(1)
    matrix = rng.normal(size=(20, 3))
    result = separation(matrix, ["a", "b"] * 10, permutations=100)
    assert 0.2 < result.auc < 0.8
    assert result.p_value > 0.05


def test_a_perfect_separation_reaches_the_smallest_reportable_p_value():
    matrix = np.array([[0.0]] * 8 + [[9.0]] * 8)
    result = separation(matrix, ["a"] * 8 + ["b"] * 8, permutations=99)
    assert result.p_value == pytest.approx(1 / 100)


def test_a_small_label_set_cannot_reach_the_p_value_floor():
    matrix = np.array([[0.0], [0.0], [0.0], [9.0], [9.0], [9.0]])
    result = separation(matrix, ["a", "a", "a", "b", "b", "b"], permutations=999)
    assert result.auc == 1.0
    assert result.p_value > 1 / 1000


def test_separation_is_repeatable_for_one_seed():
    rng = np.random.default_rng(2)
    matrix = rng.normal(size=(12, 2))
    labels = ["a", "b", "c"] * 4
    first = separation(matrix, labels, permutations=50, seed=5)
    assert first == separation(matrix, labels, permutations=50, seed=5)
