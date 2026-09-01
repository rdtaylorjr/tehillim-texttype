import pytest
from conftest import FakeApi, FakeF, FakeFeature, FakeL, FakeT

from library.bhsa import (
    available_versions,
    load_api,
    psalm_chapter_nodes,
    psalms_book_node,
    version_location,
)


def make_clone(tmp_path, versions):
    for version in versions:
        directory = tmp_path / version
        directory.mkdir(parents=True)
        (directory / "otype.tf").write_text("")
    return tmp_path


def test_version_location_resolves_a_present_version(tmp_path):
    root = make_clone(tmp_path, ["2021"])
    assert version_location("2021", root) == root / "2021"


def test_version_location_rejects_a_missing_version(tmp_path):
    with pytest.raises(FileNotFoundError):
        version_location("1999", make_clone(tmp_path, ["2021"]))


def test_available_versions_lists_only_directories_holding_data(tmp_path):
    root = make_clone(tmp_path, ["2017", "2021"])
    (root / "empty").mkdir()
    assert available_versions(root) == ["2017", "2021"]


def test_available_versions_of_a_missing_root_is_empty(tmp_path):
    assert available_versions(tmp_path / "absent") == []


def test_load_api_passes_the_resolved_location_to_text_fabric(tmp_path):
    root = make_clone(tmp_path, ["2021"])
    seen = {}

    class Fabric:
        def __init__(self, locations, silent):
            seen["locations"] = locations

        def load(self, features, silent):
            seen["features"] = features
            return "api"

    assert load_api("2021", "otype txt", root, Fabric) == "api"
    assert seen["locations"] == [str(root / "2021")]
    assert seen["features"] == "otype txt"


def test_load_api_raises_when_text_fabric_returns_nothing(tmp_path):
    root = make_clone(tmp_path, ["2021"])

    class Fabric:
        def __init__(self, locations, silent):
            pass

        def load(self, features, silent):
            return None

    with pytest.raises(RuntimeError):
        load_api("2021", "otype", root, Fabric)


def test_psalms_book_node_accepts_either_book_name(two_psalm_api):
    assert psalms_book_node(two_psalm_api) == 100


def test_psalms_book_node_raises_when_absent():
    f = FakeF({"otype": FakeFeature({1: "book"}), "book": FakeFeature({1: "Genesis"})})
    with pytest.raises(RuntimeError):
        psalms_book_node(FakeApi(F=f, L=FakeL({}), T=FakeT({})))


def test_psalm_chapter_nodes_maps_psalm_number_to_node(two_psalm_api):
    assert psalm_chapter_nodes(two_psalm_api) == {1: 110, 2: 120}
