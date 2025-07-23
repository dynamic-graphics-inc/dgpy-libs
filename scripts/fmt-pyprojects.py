# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyproject-fmt",
#     "ry",
# ]
# ///
from __future__ import annotations

from subprocess import run
from typing import TYPE_CHECKING

from ry import glob

if TYPE_CHECKING:
    from pathlib import Path

echo = print


def fmt_pyproject(p: list[Path]) -> bool:
    """Format pyproject.toml files."""
    done = run(
        ["uvx", "pyproject-fmt", *(str(p) for p in p)],
        check=False,
    )
    return done.returncode == 0


def main() -> None:
    files = glob("**/pyproject.toml").collect()
    fmt_pyproject(files)


if __name__ == "__main__":
    main()
