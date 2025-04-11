# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyproject-fmt",
#     "ry",
# ]
# ///
from __future__ import annotations

from pathlib import Path
from subprocess import run

from ry import glob

echo = print


def fmt_pyproject(p: list[Path]) -> bool:
    """Format pyproject.toml files."""
    done = run(
        ["uvx", "pyproject-fmt", *(str(p) for p in p)],
        check=False,
    )
    return done.returncode == 0


def main():
    files = glob("**/pyproject.toml").collect()
    fmt_pyproject(files)


if __name__ == "__main__":
    main()
