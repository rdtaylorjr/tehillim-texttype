import csv

from texttype.corpus import Clause
from texttype.export import write_profiles, write_transitions
from texttype.transitions import transitions


def clause(node, chapter, verse, txt, book="Psalmi"):
    return Clause(node=node, book=book, chapter=chapter, verse=verse, index_in_verse=0, txt=txt)


def test_write_profiles_writes_one_row_per_chapter(tmp_path):
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN"), clause(3, 2, 1, "Q")]
    path = tmp_path / "profiles.csv"
    assert write_profiles(clauses, transitions(clauses), ["Q", "QN"], path) == 2
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["chapter"] for r in rows] == ["1", "2"]


def test_profile_rows_carry_shares_summing_to_one(tmp_path):
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN")]
    path = tmp_path / "profiles.csv"
    write_profiles(clauses, transitions(clauses), ["Q", "QN"], path)
    with path.open(encoding="utf-8") as handle:
        row = next(iter(csv.DictReader(handle)))
    assert float(row["Q"]) + float(row["QN"]) == 1.0
    assert row["mean_depth"] == "1.5"
    assert row["transitions"] == "1"


def test_a_chapter_without_transitions_records_zero(tmp_path):
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "Q")]
    path = tmp_path / "profiles.csv"
    write_profiles(clauses, transitions(clauses), ["Q"], path)
    with path.open(encoding="utf-8") as handle:
        row = next(iter(csv.DictReader(handle)))
    assert row["transitions"] == "0"


def test_write_transitions_records_the_kind_of_each_change(tmp_path):
    clauses = [clause(1, 1, 1, "Q"), clause(2, 1, 2, "QN"), clause(3, 1, 3, "Q")]
    path = tmp_path / "transitions.csv"
    assert write_transitions(transitions(clauses), path) == 2
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["kind"] for r in rows] == ["entry", "return"]
    assert [r["depth_change"] for r in rows] == ["1", "-1"]


def test_writing_no_transitions_leaves_only_a_header(tmp_path):
    path = tmp_path / "transitions.csv"
    assert write_transitions([], path) == 0
    with path.open(encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 0
