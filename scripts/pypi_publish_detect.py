#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detect which dgpy-libs packages have a version not yet published on PyPI.

Reads each publishable lib's ``pyproject.toml`` version and compares it against
the versions already available on PyPI. A package is selected for publishing
when its current version string is not present on PyPI (this also covers a
package's very first release, where PyPI returns 404).

Outputs:
- a human-readable table to stderr
- the GitHub Actions matrix (JSON array of ``{"package", "version"}``) to stdout
- ``matrix=`` / ``any=`` rows appended to ``$GITHUB_OUTPUT`` when running in CI

Stdlib only (``tomllib`` requires Python >= 3.11); no third-party deps.
"""

from __future__ import annotations

import json
import os
import sys
import tomllib
import urllib.error
import urllib.request

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBS_DIR = REPO_ROOT / "libs"

# Publishable packages. Excludes the private root (`dgpydev`) and `dgpytest`
# (classifier "Private :: Do Not Upload"). `dgpylibs` is the publishable
# meta-package.
PACKAGES = [
    "aiopen",
    "asyncify",
    "fmts",
    "funkify",
    "h5",
    "jsonbourne",
    "lager",
    "listless",
    "requires",
    "shellfish",
    "xtyping",
]


def local_version(pkg: str) -> str:
    """Return the version declared in ``libs/<pkg>/pyproject.toml``."""
    pyproject = LIBS_DIR / pkg / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def pypi_versions(pkg: str) -> set[str]:
    """Return the set of versions already released on PyPI for ``pkg``."""
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return set()  # never published -> first release
        raise
    return set(data.get("releases", {}).keys())


def main() -> None:
    to_publish: list[dict[str, str]] = []
    print(f"{'package':<12} {'version':<10} status", file=sys.stderr)  # noqa: T201
    print(f"{'-' * 12} {'-' * 10} {'-' * 7}", file=sys.stderr)  # noqa: T201
    for pkg in PACKAGES:
        version = local_version(pkg)
        ahead = version not in pypi_versions(pkg)
        status = "PUBLISH" if ahead else "ok"
        print(f"{pkg:<12} {version:<10} {status}", file=sys.stderr)  # noqa: T201
        if ahead:
            to_publish.append({"package": pkg, "version": version})

    matrix = json.dumps(to_publish)
    print(matrix)  # machine-readable matrix on stdout  # noqa: T201

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={matrix}\n")
            fh.write(f"any={'true' if to_publish else 'false'}\n")


if __name__ == "__main__":
    main()
