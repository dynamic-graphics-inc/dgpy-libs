from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

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


def lib_pyproject_toml_2_deps(libname: str, dgpylibs_only: bool = True):
    pyproject_toml_dict = lib_pyproject_toml(libname)
    deps = pyproject_toml_dict["tool"]["poetry"]["dependencies"]
    return {k: v for k, v in deps.items() if k in DGPY_LIBS} if dgpylibs_only else deps


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
def update():
    click.echo("updating")
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
def tree():
    dgpylibs_deptree: dict[str, DgpyLibInfo] = {}
    for lib in DGPY_LIBS:
        click.echo(f"lib: {lib}")
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


def main():
    cli()


if __name__ == "__main__":
    main()
