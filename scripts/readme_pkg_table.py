from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PackagesTableRow:
    name: str
    relative_path: str
    install: str
    pypi_version_badge: str
    python_version_badge: str

    def md_table_row(self) -> str:
        return f"| [{self.name}]({self.relative_path}) | {self.install} | {self.pypi_version_badge} | {self.python_version_badge} |"

    @classmethod
    def from_pkg_name(cls, pkgname: str) -> PackagesTableRow:
        pypi_pkg_version_badge = f"[![PyPI](https://img.shields.io/pypi/v/{pkgname}?style=flat-square&cacheSeconds=600)](https://pypi.org/project/{pkgname}/)"
        python_version_badge = f"[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{pkgname}?style=flat-square&cacheSeconds=600)](https://pypi.org/project/{pkgname}/)"
        return PackagesTableRow(
            name=pkgname,
            relative_path=f"./libs/{pkgname}",
            install=f"`pip install {pkgname}`",
            pypi_version_badge=pypi_pkg_version_badge,
            python_version_badge=python_version_badge,
        )


def main():
    packages = [
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
    packages = [PackagesTableRow.from_pkg_name(pkg) for pkg in packages]
    table_lines = [
        "| Package | Install | Version | Python Versions |",
        "|--------|---------|---------|-----------------|",
        *(pkg.md_table_row() for pkg in packages),
    ]
    print("\n".join(table_lines) + "\n")  # noqa: T201


if __name__ == "__main__":
    main()
