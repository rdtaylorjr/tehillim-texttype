import numpy as np

from texttype.corpus import Clause
from texttype.profile import profile_matrix, uniform_psalms, vocabulary


def clause(psalm, txt, node=0):
    return Clause(node=node, psalm=psalm, verse=1, index_in_verse=0, txt=txt)


def test_vocabulary_is_sorted_and_unique():
    assert vocabulary([clause(1, "QN"), clause(1, "Q"), clause(2, "Q")]) == ["Q", "QN"]


def test_profile_matrix_normalizes_each_psalm_to_proportions():
    clauses = [clause(1, "Q"), clause(1, "QN"), clause(2, "Q")]
    psalms, matrix = profile_matrix(clauses, ["Q", "QN"])
    assert psalms == [1, 2]
    np.testing.assert_allclose(matrix, [[0.5, 0.5], [1.0, 0.0]])


def test_profile_matrix_can_return_raw_counts():
    _, matrix = profile_matrix([clause(1, "Q"), clause(1, "Q")], ["Q"], normalize=False)
    np.testing.assert_allclose(matrix, [[2.0]])


def test_profile_matrix_ignores_strings_outside_the_vocabulary():
    _, matrix = profile_matrix([clause(1, "Q"), clause(1, "ND")], ["Q"], normalize=False)
    np.testing.assert_allclose(matrix, [[1.0]])


def test_uniform_psalms_reports_only_psalms_with_one_text_type():
    clauses = [clause(1, "Q"), clause(1, "Q"), clause(2, "Q"), clause(2, "QN")]
    assert uniform_psalms(clauses) == {1: "Q"}
