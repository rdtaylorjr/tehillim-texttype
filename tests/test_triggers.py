from conftest import FakeApi, FakeF, FakeFeature, FakeL, FakeT

from texttype.triggers import clause_markers, markers_for_nodes


def api_with(words, phrases, *, vt=None, lex=None, function=None):
    f = FakeF(
        {
            "vt": FakeFeature(vt or {}),
            "lex": FakeFeature(lex or {}),
            "function": FakeFeature(function or {}),
        }
    )
    down = {(1, "word"): words, (1, "phrase"): phrases}
    return FakeApi(F=f, L=FakeL(down), T=FakeT({}))


def test_wayyiqtol_is_registered_from_the_verbal_tense():
    api = api_with([10], [], vt={10: "wayq"})
    assert clause_markers(api, 1).wayyiqtol is True


def test_imperative_and_yiqtol_are_registered_separately():
    api = api_with([10, 11], [], vt={10: "impv", 11: "impf"})
    markers = clause_markers(api, 1)
    assert markers.imperative is True
    assert markers.yiqtol is True
    assert markers.wayyiqtol is False


def test_verbum_dicendi_is_registered_from_the_lexeme():
    api = api_with([10], [], lex={10: ">MR["})
    assert clause_markers(api, 1).verbum_dicendi is True


def test_vocative_is_registered_from_a_phrase_function():
    api = api_with([], [20], function={20: "Voct"})
    assert clause_markers(api, 1).vocative is True


def test_a_clause_with_no_markers_registers_none():
    assert clause_markers(api_with([10], [20]), 1).present() == ()


def test_present_lists_marker_names_in_a_fixed_order():
    api = api_with([10, 11], [20], vt={10: "wayq"}, lex={11: "DBR["}, function={20: "Voct"})
    assert clause_markers(api, 1).present() == ("wayyiqtol", "verbum_dicendi", "vocative")


def test_markers_for_nodes_keys_by_clause_node():
    api = api_with([10], [], vt={10: "wayq"})
    assert set(markers_for_nodes(api, [1])) == {1}
