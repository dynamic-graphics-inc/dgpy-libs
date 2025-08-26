from __future__ import annotations

import datetime
import itertools as it

from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

import click
import tomli

from pydantic.dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt
from rich.rule import Rule
from rich.tree import Tree

from dgpydev.const import DGPY_LIBS
from jsonbourne.pydantic import JsonBaseModel
from shellfish import sh

if TYPE_CHECKING:
    from shellfish._types import FsPath

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


def lib_pyproject_toml(libname: str) -> dict[str, Any]:
    pyproject_toml_filepath = lib_dirpath(libname) / "pyproject.toml"
    with open(pyproject_toml_filepath) as f:
        return tomli.loads(f.read())


def lib_version(libname: str) -> str:
    return lib_pyproject_toml(libname)["project"]["version"]


def lib_pyproject_toml_2_deps(
    libname: str, *, dgpylibs_only: bool = True
) -> dict[str, str]:
    pyproject_toml_dict = lib_pyproject_toml(libname)
    deps = pyproject_toml_dict["project"]["dependencies"]
    return {k: v for k, v in deps.items() if k in DGPY_LIBS} if dgpylibs_only else deps


def pyproject_tomls() -> dict[str, dict[str, Any]]:
    return {libname: lib_pyproject_toml(libname) for libname in DGPY_LIBS}


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option("--debug/--no-debug", default=False, help="print/log more stuff")
def cli(*, debug: bool = False) -> None:
    if debug:
        console.log("dgpydev-debug: ON")


def update_abouts() -> None:
    for libname, pyproject_toml_dict in pyproject_tomls().items():
        project_metadata = pyproject_toml_dict["project"]
        lib_about_filepath = lib_dirpath(libname) / "src" / libname / "__about__.py"
        metadata_file_lines = [
            "# -*- coding: utf-8 -*-",
            '"""Package metadata/info"""\n',
            "from __future__ import annotations\n",
            '__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")',
            '__title__ = "{}"'.format(project_metadata["name"]),
            '__description__ = "{}"'.format(project_metadata["description"]),
            '__pkgroot__ = __file__.replace("__about__.py", "").rstrip("/\\\\")',
            '__version__ = "{}"\n'.format(project_metadata["version"]),
        ]
        if lib_about_filepath.exists():
            current = lib_about_filepath.read_text()
            if current != "\n".join(metadata_file_lines):
                console.log(f"Updating {libname}/__about__.py")
                lib_about_filepath.unlink()
                lib_about_filepath.write_text(
                    "\n".join(metadata_file_lines), encoding="utf-8", newline="\n"
                )


@cli.command()
def update() -> None:
    """Update all dgpy-libs metadata files."""
    update_abouts()


@cli.command()
def patchall() -> None:
    """relock all dgpy-libs"""
    for libname, _pyproject_toml_dict in pyproject_tomls().items():
        dirpath = lib_dirpath(libname)
        console.log(f"Relocking {libname}")
        console.log(f"cd {dirpath}")
        sh.cd(dirpath)
        sh.do("uv", "version", "--bump", "patch", verbose=True, check=True)
    update_abouts()


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

    ts = graphlib.TopologicalSorter({
        v.name: v.dependencies for v in dgpylibs_deptree.values()
    })
    return list(ts.static_order())


@cli.command(name="ls", help="List dgpy-libs")
def ls() -> None:
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


def deps_tree() -> dict[str, DgpyLibInfo]:
    dgpylibs_deptree: dict[str, DgpyLibInfo] = {}
    for lib in DGPY_LIBS:
        console.print(f"lib: {lib}")
        pyproject_toml_dict = lib_pyproject_toml(lib)
        dgpylibs_deps = lib_pyproject_toml_2_deps(lib)
        lib_info = DgpyLibInfo(
            name=lib,
            version=pyproject_toml_dict["project"]["version"],
            dependencies=set(dgpylibs_deps),
            dependents=set(),
        )
        dgpylibs_deptree[lib] = lib_info
        pyproject_toml = lib_pyproject_toml(lib)
        console.print(Rule(f"lib: {lib}"))
        console.print(pyproject_toml)

    for lib, lib_info in dgpylibs_deptree.items():
        for dep in lib_info.dependencies:
            dgpylibs_deptree[dep].dependents.add(lib)

    return dgpylibs_deptree


def deps_tree_rich(deptree: dict[str, DgpyLibInfo]) -> Tree:
    def add_dependencies(
        node: Tree, lib_info: DgpyLibInfo, lib_dict: dict[str, DgpyLibInfo]
    ) -> None:
        for dep_name in lib_info.dependencies:
            if dep_name in lib_dict:
                dep_info = lib_dict[dep_name]
                dep_node = node.add(
                    f"{dep_name} (Version: {dep_info.version})", expanded=True
                )
                add_dependencies(dep_node, dep_info, lib_dict)

    def build_tree(lib_dict: dict[str, DgpyLibInfo]) -> Tree:
        tree = Tree("Libraries", expanded=True)
        for lib_name, lib_info in lib_dict.items():
            lib_node = tree.add(
                f"{lib_name} (Version: {lib_info.version})", expanded=True
            )
            deps_node = lib_node.add("Dependencies", expanded=True)
            add_dependencies(deps_node, lib_info, lib_dict)
        return tree

    return build_tree(deptree)


def dgpylibs_topo_sorted() -> list[str]:
    dgpylibs_deptree = deps_tree()
    return topo_sort(dgpylibs_deptree)


@cli.command()
def tree() -> None:
    """Print dependency tree

    possible grep???

    """
    dgpylibs_deptree = deps_tree()
    console.print(Rule("topo_sorted"))
    console.print(topo_sort(dgpylibs_deptree))
    console.print(Rule("deptree"))
    console.print({
        lib: lib_info.__json__() for lib, lib_info in dgpylibs_deptree.items()
    })

    rich_tree = deps_tree_rich(dgpylibs_deptree)
    console.print(rich_tree)


@cli.command()
def publish() -> None:
    """Publish all dgpy-libs to PyPI."""
    raise NotImplementedError("not implemented with uv")


@cli.command()
@click.argument(
    "version",
    type=click.Choice(
        ["patch", "minor", "major", "prepatch", "preminor", "premajor", "prerelease"],
        case_sensitive=False,
    ),
    default="patch",
    nargs=1,
    required=False,
)
@click.option(
    "--lib",
    "-l",
    type=click.Choice(DGPY_LIBS),
    required=True,
    help="lib to bump version for",
)
@click.option(
    "--dry-run",
    "-n",
    default=False,
    is_flag=True,
    help="dry run - don't actually do anything",
)
def version(
    lib: str,
    version: str | None = None,
    *,
    dry_run: bool = False,
) -> None:
    """Bump version of lib (TODO)"""
    console.print(f"lib: {lib}")
    console.print(f"version: {version}")
    console.print(f"dry_run: {dry_run}")
    raise NotImplementedError("TODO")


######################
# CHANGELOG COMMANDS #
######################
@dataclass
class Change:
    lib: str
    version: str
    msg: str
    timestamp: datetime.datetime = datetime.datetime.now()

    def __json__(self) -> Any:
        return {
            "lib": self.lib,
            "version": self.version,
            "msg": self.msg,
            "timestamp": self.timestamp.isoformat(),
        }

    def equiv_tuple(self) -> tuple[str, str, str]:
        return (self.lib, self.version, self.msg)

    def __hash__(self) -> int:
        return hash((self.lib, self.version, self.msg))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Change):
            return False
        return self.equiv(other)

    def equiv(self, other: Change) -> bool:
        return (
            self.lib == other.lib
            and self.version == other.version
            and self.msg == other.msg
        )

    def dedupe(self, other: Change) -> list[Change]:
        if self.equiv(other):
            return [self] if self.timestamp > other.timestamp else [other]
        return [self, other]


class Changelog(JsonBaseModel):
    updated: datetime.datetime = datetime.datetime.now()
    changes: list[Change]

    def most_recent_change(self) -> Change:
        if len(self.changes) == 0:
            raise ValueError("No changes in changelog")
        return max(self.changes, key=lambda change: change.timestamp)

    def new_updated_timestamp(self) -> datetime.datetime:
        try:
            most_recent_change = self.most_recent_change()
            return most_recent_change.timestamp
        except ValueError:
            return datetime.datetime.now()

    def check_similar_changes(self) -> None:
        unique_changes_ignoring_timestamp = set(
            it.chain.from_iterable(
                (a.dedupe(b) for a, b in it.combinations(self.changes, 2))
            )
        )
        self.changes = sorted(
            unique_changes_ignoring_timestamp, key=lambda change: change.timestamp
        )

    def update(self) -> None:
        self.check_similar_changes()
        self.updated = self.new_updated_timestamp()

    def write2fspath(self, filepath: FsPath) -> str:
        self.update()
        string = self.model_dump_json(indent=2)

        filepath.write_text(
            string,
            encoding="utf-8",
            newline="\n",
        )
        return string


@cli.command()
@click.option("--msg", "-m", type=str, required=True)
@click.option("--lib", "-l", type=click.Choice(DGPY_LIBS), required=False)
def change(
    msg: str,
    lib: str | None = None,
) -> None:
    """Make changelog message"""
    # ask which lib if not provided blah blah blah
    if lib is None:
        lib = Prompt.ask("Which lib?", choices=DGPY_LIBS)
    # if not exists create changelog dir in root of repo
    changelog_json_filepath = repo_root() / "changelog" / "changelog.json"
    sh.mkdirp(
        changelog_json_filepath.parent,
    )
    if not changelog_json_filepath.exists():
        console.log(f"Creating {changelog_json_filepath}")
        sh.write_json(
            changelog_json_filepath,
            {"changes": [], "updated": datetime.datetime.now().isoformat()},
        )
    # load changelog.json
    changelog_json = changelog_json_filepath.read_text()
    changelog = Changelog.from_json(changelog_json)

    isots = datetime.datetime.now().isoformat()
    change = Change(lib=lib, version=lib_version(lib), msg=msg, timestamp=isots)
    changelog.changes.append(change)

    # sort changes by timestamp
    changelog.changes.sort(key=lambda change: change.timestamp)
    changelog.write2fspath(changelog_json_filepath)

    # print the diff
    import difflib

    console.print(Rule("changelog diff"))
    console.print(
        "\n".join(
            difflib.unified_diff(
                changelog_json.splitlines(),
                changelog.model_dump_json(indent=2).splitlines(),
            )
        )
    )


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
