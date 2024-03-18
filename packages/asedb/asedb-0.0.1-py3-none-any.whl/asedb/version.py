from __future__ import annotations

from pathlib import Path

from packaging.version import Version, parse

__all__ = ["__version__", "get_version"]


def get_version() -> Version:
    """Get the packaging Version object for the package."""
    with Path(__file__).with_name("_version.txt").open("r") as fd:
        return parse(fd.readline().strip())


__version__ = str(get_version())
