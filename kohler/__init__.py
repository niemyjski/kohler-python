"""Kohler DTV+ device control library."""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .kohler import Kohler, KohlerError


def _resolve_version() -> str:
    try:
        return version("kohler")
    except PackageNotFoundError:
        pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
        try:
            with pyproject_path.open("rb") as pyproject_file:
                project = tomllib.load(pyproject_file)["project"]
        except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError):
            return "0+unknown"
        return str(project.get("version", "0+unknown"))


__version__ = _resolve_version()

__all__ = ["Kohler", "KohlerError", "__version__"]
