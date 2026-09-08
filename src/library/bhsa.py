"""Loads a BHSA version from the local clone and exposes the Psalms clause objects."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from tf.fabric import Fabric as _RealFabric

BHSA_CLONE_ROOT = Path.home() / "Developer" / "hebrew" / "bhsa" / "tf"
DEFAULT_VERSION = "2021"
REQUIRED_FEATURES = "otype book chapter verse txt domain"


def version_location(version: str, clone_root: Path = BHSA_CLONE_ROOT) -> Path:
    """Resolves a BHSA version name to its Text-Fabric data directory."""
    location = clone_root / version
    if not (location / "otype.tf").exists():
        raise FileNotFoundError(f"No BHSA Text-Fabric data at {location}")
    return location


def available_versions(clone_root: Path = BHSA_CLONE_ROOT) -> list[str]:
    """Every BHSA version present in the local clone, in sorted order."""
    if not clone_root.exists():
        return []
    return sorted(p.name for p in clone_root.iterdir() if (p / "otype.tf").exists())


def load_api(
    version: str = DEFAULT_VERSION,
    features: str = REQUIRED_FEATURES,
    clone_root: Path = BHSA_CLONE_ROOT,
    fabric_class: Callable[..., Any] = _RealFabric,
) -> Any:
    """Loads one BHSA version with the named features."""
    location = version_location(version, clone_root)
    api = fabric_class(locations=[str(location)], silent="deep").load(features, silent="deep")
    if api is None:
        raise RuntimeError(f"Text-Fabric failed to load {features} from {location}")
    return api
