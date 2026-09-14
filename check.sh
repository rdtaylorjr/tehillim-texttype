#!/usr/bin/env bash
# Every gate CI runs, in CI's order, so a local pass cannot diverge from a CI pass.
set -euo pipefail
PY=.venv/bin/python
# Fakes mirror Text-Fabric's signatures, so their unused parameters are the contract, not dead code.
UNUSED_BY_DESIGN="pytestmark,pytest_*,silent"
$PY -m ruff check .
$PY -m ruff format --check .
$PY -m mypy --strict src
$PY -m deptry src
$PY -m vulture src tests .vulture-whitelist.py --min-confidence 60 \
  --ignore-decorators "@pytest.fixture" --ignore-names "$UNUSED_BY_DESIGN"
$PY -m pytest -q
