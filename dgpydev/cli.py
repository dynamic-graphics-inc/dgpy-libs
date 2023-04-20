from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import click
import tomli

from rich.console import Console
from rich.rule import Rule

from dgpydev.const import DGPY_LIBS

console = Console()


@lru_cache(maxsize=1)
def repo_root() -> Path:
    return Path(__file__).parent.parent


@lru_cache(maxsize=1)
def libs_dirpath() -> Path:
    return repo_root() / "libs"


@lru_cache(maxsize=32)
def lib_dirpath(libname: str) -> Path:
    return libs_dirpath() / libname


@lru_cache(maxsize=32)
def lib_pyproject_toml(libname: str):
    pyproject_toml_filepath = lib_dirpath(libname) / "pyproject.toml"
    with open(pyproject_toml_filepath) as f:
        return tomli.loads(f.read())


def lib_version(libname: str) -> str:
    return lib_pyproject_toml(libname)["tool"]["poetry"]["version"]


def lib_pyproject_toml_2_deps(libname: str, dgpylibs_only: bool = True):
    pyproject_toml_dict = lib_pyproject_toml(libname)
    deps = pyproject_toml_dict["tool"]["poetry"]["dependencies"]
    return {k: v for k, v in deps.items() if k in DGPY_LIBS} if dgpylibs_only else deps


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug:
        click.echo("dgpydev-debug: ON")


@cli.command()
def update():
    raise NotImplementedError("TODO")


@dataclass
class DgpyLibInfo:
    name: str
    version: str
    dependencies: set[str]
    dependents: set[str]

    def __json__(self) -> Any:
        return {
            "name": self.name,
            "version": self.version,
            "dependencies": sorted(self.dependencies),
            "dependents": sorted(self.dependents),
        }


def topo_sort(dgpylibs_deptree: dict[str, DgpyLibInfo]) -> list[str]:
    import graphlib

    ts = graphlib.TopologicalSorter(
        {v.name: v.dependencies for v in dgpylibs_deptree.values()}
    )
    return list(ts.static_order())


@cli.command()
def ls():
    from rich.table import Table

    t = Table(
        "lib",
        "version",
    )
    for lib in DGPY_LIBS:
        t.add_row(lib, lib_version(lib))
    console.print(
        t,
    )


@cli.command()
def tree():
    dgpylibs_deptree: dict[str, DgpyLibInfo] = {}
    for lib in DGPY_LIBS:
        console.print(f"lib: {lib}")
        pyproject_toml_dict = lib_pyproject_toml(lib)
        dgpylibs_deps = lib_pyproject_toml_2_deps(lib)
        lib_info = DgpyLibInfo(
            name=lib,
            version=pyproject_toml_dict["tool"]["poetry"]["version"],
            dependencies=dgpylibs_deps,
            dependents=set(),
        )
        dgpylibs_deptree[lib] = lib_info
        pyproject_toml = lib_pyproject_toml(lib)
        console.print(Rule(f"lib: {lib}"))
        console.print(pyproject_toml)

    for lib, lib_info in dgpylibs_deptree.items():
        for dep in lib_info.dependencies:
            dgpylibs_deptree[dep].dependents.add(lib)

    console.print(Rule("topo_sorted"))
    console.print(topo_sort(dgpylibs_deptree))
    console.print(Rule("deptree"))
    console.print(
        {lib: lib_info.__json__() for lib, lib_info in dgpylibs_deptree.items()}
    )


@cli.command()
@click.argument(
    "version",
    type=click.Choice(
        ["patch", "minor", "major", "prepatch", "preminor", "premajor", "prerelease"],
        case_sensitive=False,
    ),
    default=None,
    nargs=1,
    required=False,
)
@click.option(
    "--dry-run",
    "-n",
    default=False,
    is_flag=True,
    help="dry run - don't actually do anything",
)
def version(
    version: Optional[str] = None,
    dry_run: bool = False,
):
    console.print(f"version: {version}")
    console.print(f"dry_run: {dry_run}")

    raise NotImplementedError("TODO")


def main():
    cli()


if __name__ == "__main__":
    main()
