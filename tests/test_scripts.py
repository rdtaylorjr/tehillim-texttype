import importlib

import pytest

SCRIPT_MODULES = [
    "texttype.scripts.report",
    "texttype.scripts.compare_versions",
    "texttype.scripts.transition_markers",
]


@pytest.mark.parametrize("name", SCRIPT_MODULES)
def test_script_module_imports_and_exposes_a_main(name):
    module = importlib.import_module(name)
    assert callable(module.main)


@pytest.mark.parametrize("name", SCRIPT_MODULES)
def test_script_module_documents_itself(name):
    assert importlib.import_module(name).__doc__
