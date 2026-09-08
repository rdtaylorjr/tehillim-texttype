import importlib

import pytest

SCRIPT_MODULES = [
    "texttype.scripts.replicate",
    "texttype.scripts.report",
    "texttype.scripts.boundaries",
    "texttype.scripts.compare_books",
    "texttype.scripts.compare_versions",
    "texttype.scripts.export_data",
    "texttype.scripts.genre_separation",
    "texttype.scripts.narrative_entries",
    "texttype.scripts.quotations",
    "texttype.scripts.transition_markers",
    "texttype.scripts.undecided_clauses",
]


@pytest.mark.parametrize("name", SCRIPT_MODULES)
def test_script_module_imports_and_exposes_a_main(name):
    module = importlib.import_module(name)
    assert callable(module.main)


@pytest.mark.parametrize("name", SCRIPT_MODULES)
def test_script_module_documents_itself(name):
    assert importlib.import_module(name).__doc__
