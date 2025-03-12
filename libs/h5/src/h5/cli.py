# -*- coding: utf-8 -*-
"""h5.cli"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Callable, List, Optional, Tuple, Union

import click
import numpy as np
import ry

from rich.console import Console
from typing_extensions import TypeGuard

import h5

console = Console()

__all__ = (
    "H5CliConfig",
    "cli",
)

Matcher = Union[Callable[[str], bool], ry.Globster]


def is_np_integer(obj: Any) -> TypeGuard[np.integer]:
    return isinstance(obj, np.integer)


def is_np_floating(obj: Any) -> TypeGuard[np.floating]:
    return isinstance(obj, np.floating)


def _json_default(obj: Any) -> Any:
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if is_np_floating(obj):
        return float(obj)
    if is_np_integer(obj):
        return int(obj)
    if isinstance(obj, (np.bytes_, bytes)):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _print_json(data: Any) -> None:
    console.print_json(data=data, default=_json_default)


def true(string: str) -> bool:
    return True


@lru_cache(maxsize=16)
def make_globster(
    include: Optional[Tuple[str, ...]] = ("**/*",),
    exclude: Optional[Tuple[str, ...]] = None,
) -> Union[Callable[[str], bool], ry.Globster]:
    patterns: List[str] = []
    if include:
        patterns.extend(include)
    if exclude:
        patterns.extend(f"!{el}" for el in exclude)
    return ry.globster(patterns)


@dataclass
class H5CliConfig:
    datasets: bool
    attributes: bool
    groups: bool
    include: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None

    def filter_is_none(self) -> bool:
        """Check if filter is None"""
        return (self.include is None or self.include == ("**/*",)) and (
            self.exclude is None
        )

    def globster(self) -> Matcher:
        if self.include is None and self.exclude is None:
            return true
        return make_globster(self.include or ("**/*",), self.exclude)

    def matcher(self) -> Optional[Matcher]:
        if self.filter_is_none():
            return None
        return self.globster()

    @classmethod
    def from_cli(
        cls,
        datasets: bool,
        attributes: bool,
        groups: bool,
        include: Optional[Tuple[str, ...]] = ("**/*",),
        exclude: Optional[Tuple[str, ...]] = None,
    ) -> H5CliConfig:
        return (
            cls(
                datasets=True,
                attributes=True,
                groups=True,
                include=include,
                exclude=exclude,
            )
            if not any((datasets, attributes, groups))
            else cls(datasets, attributes, groups, include=include, exclude=exclude)
        )


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option("--debug", envvar="DGPYDEBUG", is_flag=True, default=False)
def cli(debug: bool = False) -> None:
    """h5 command line interface"""
    if debug:
        click.echo("h5-debug: on")


@cli.command(
    help="Check if path is an HDF5 file",
    name="is",
)
@click.argument(
    "fspaths",
    nargs=-1,
    type=click.Path(exists=True),
)
@click.option(
    "--exit/--no-exit",
    "exit_",
    is_flag=True,
    default=True,
    help="Exit with non-zero exit code if any of the paths are not HDF5 files",
)
def is_hdf5(
    fspaths: Tuple[str, ...],
    exit_: bool = False,
) -> None:
    data = {filepath: h5.is_hdf5(filepath) for filepath in fspaths}
    _print_json(data)

    # if any of the paths are not HDF5 files, exit with a non-zero exit code
    if exit_:
        not_hdf5 = [filepath for filepath, is_hdf5 in data.items() if not is_hdf5]
        if not_hdf5:
            click.secho(
                f"Not HDF5: {', '.join(not_hdf5)}", fg="red", err=True, bold=True
            )
            click.get_current_context().exit(1)


@cli.command(
    help="Dump HDF5 file",
    name="dump",
)
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "--json/--no-json", "json_", is_flag=True, default=True, help="Output JSON"
)
@click.option(
    "-d",
    "--datasets",
    "datasets",
    is_flag=True,
    default=False,
    help="dump datasets",
)
@click.option(
    "-a",
    "--attributes",
    "attributes",
    is_flag=True,
    default=False,
    help="dump attributes",
)
@click.option(
    "-g",
    "--groups",
    "groups",
    is_flag=True,
    default=False,
    help="dump groups",
)
@click.option(
    "-i",
    "--include",
    "include",
    default=("**/*",),
    help="include pattern(s)",
    multiple=True,
)
@click.option(
    "-e",
    "--exclude",
    "exclude",
    default=(),
    help="exclude pattern(s)",
    multiple=True,
)
def dump(
    fspath: str,
    json_: bool = False,
    datasets: bool = False,
    attributes: bool = False,
    groups: bool = False,
    include: Tuple[str, ...] = ("**/*",),
    exclude: Optional[Tuple[str, ...]] = None,
) -> None:
    config = H5CliConfig.from_cli(
        datasets=datasets,
        attributes=attributes,
        groups=groups,
        include=include,
        exclude=exclude,
    )
    matcher = config.globster()
    with h5.File(fspath, "r") as f:
        data = {key: h5.info(value) for key, value in h5.h5iter(f) if matcher(key)}
        data_dump = {key: value.dump() for key, value in data.items()}
    _print_json(data_dump)


@cli.command(
    help="HDF5 file as tree",
    name="tree",
)
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "--json/--no-json", "json_", is_flag=True, default=True, help="Output JSON"
)
@click.option(
    "-d",
    "--datasets",
    "datasets",
    is_flag=True,
    default=False,
    help="dump datasets",
)
@click.option(
    "-a",
    "--attrs",
    "--attributes",
    "attributes",
    is_flag=True,
    default=False,
    help="dump attributes",
)
@click.option(
    "-g",
    "--groups",
    "groups",
    is_flag=True,
    default=False,
    help="dump groups",
)
def tree(
    fspath: str,
    json_: bool = False,
    datasets: bool = False,
    attributes: bool = False,
    groups: bool = False,
) -> None:
    H5CliConfig.from_cli(datasets=datasets, attributes=attributes, groups=groups)
    file_info = h5.FileInfo.from_fspath(fspath)
    if json_:
        _print_json(file_info.dict())
    else:
        console.print(file_info)


def _keys(fspath: str, clicfg: H5CliConfig) -> List[str]:
    file_keys: List[str] = []
    matcher = clicfg.matcher()
    with h5.File(fspath) as f:
        if clicfg.datasets and clicfg.groups:
            file_keys.extend(h5.h5py_obj_keys_gen(f))
        elif clicfg.datasets and not clicfg.groups:
            file_keys.extend((k for k, v in h5.datasets(f)))
        elif not clicfg.datasets and clicfg.groups:
            file_keys.extend((k for k, v in h5.groups(f)))
    if matcher is None:
        return file_keys
    return list(filter(matcher, file_keys))


@cli.command(help="Dump keys as JSON array", name="keys")
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "-d",
    "--datasets",
    "datasets",
    is_flag=True,
    default=False,
    help="dump datasets",
)
@click.option(
    "-g",
    "--groups",
    "groups",
    is_flag=True,
    default=False,
    help="dump groups",
)
def keys(
    fspath: str,
    datasets: bool = False,
    groups: bool = False,
) -> None:
    cfg = H5CliConfig.from_cli(datasets=datasets, attributes=False, groups=groups)
    file_keys = _keys(fspath, cfg)
    _print_json(file_keys)


@cli.command(help="List keys", name="ls")
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "-d",
    "--datasets",
    "datasets",
    is_flag=True,
    default=False,
    help="dump datasets",
)
@click.option(
    "-g",
    "--groups",
    "groups",
    is_flag=True,
    default=False,
    help="dump groups",
)
@click.option(
    "-j",
    "--json",
    "json_",
    is_flag=True,
    default=False,
    help="Output JSON",
)
@click.option(
    "-i",
    "--include",
    "include",
    default=("**/*",),
    help="include pattern(s)",
    multiple=True,
)
@click.option(
    "-e",
    "--exclude",
    "exclude",
    default=(),
    help="exclude pattern(s)",
    multiple=True,
)
def ls(
    fspath: str,
    datasets: bool = False,
    groups: bool = False,
    json_: bool = False,
    include: Tuple[str, ...] = ("**/*",),
    exclude: Optional[Tuple[str, ...]] = None,
) -> None:
    cfg = H5CliConfig.from_cli(
        datasets=datasets,
        attributes=False,
        groups=groups,
        include=include,
        exclude=exclude,
    )
    file_keys = _keys(fspath, cfg)
    if json_:
        _print_json(file_keys)
    else:
        console.print("\n".join(file_keys))


@cli.command(help="List datasets", name="lsd")
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "-j",
    "--json",
    "json_",
    is_flag=True,
    default=False,
    help="Output JSON",
)
@click.option(
    "-i",
    "--include",
    "include",
    default=("**/*",),
    help="include pattern(s)",
    multiple=True,
)
@click.option(
    "-e",
    "--exclude",
    "exclude",
    default=(),
    help="exclude pattern(s)",
    multiple=True,
)
def lsd(
    fspath: str,
    json_: bool = False,
    include: Tuple[str, ...] = ("**/*",),
    exclude: Optional[Tuple[str, ...]] = None,
) -> None:
    """List datasets"""
    cfg = H5CliConfig.from_cli(
        datasets=True, attributes=False, groups=False, include=include, exclude=exclude
    )
    file_keys = _keys(fspath, cfg)
    if json_:
        _print_json(file_keys)
    else:
        console.print("\n".join(file_keys))


@cli.command(help="List groups", name="lsg")
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "-j",
    "--json",
    "json_",
    is_flag=True,
    default=False,
    help="Output JSON",
)
@click.option(
    "-i",
    "--include",
    "include",
    default=("**/*",),
    help="include pattern(s)",
    multiple=True,
)
@click.option(
    "-e",
    "--exclude",
    "exclude",
    default=(),
    help="exclude pattern(s)",
    multiple=True,
)
def lsg(
    fspath: str,
    json_: bool = False,
    include: Tuple[str, ...] = ("**/*",),
    exclude: Optional[Tuple[str, ...]] = None,
) -> None:
    """List groups"""
    cfg = H5CliConfig.from_cli(
        datasets=False, attributes=False, groups=True, include=include, exclude=exclude
    )
    file_keys = _keys(fspath, cfg)
    if json_:
        _print_json(file_keys)
    else:
        console.print("\n".join(file_keys))


@cli.command(help="Dump attrs")
@click.argument(
    "fspath",
    type=click.Path(exists=True),
)
@click.option(
    "-d",
    "--datasets",
    "datasets",
    is_flag=True,
    default=False,
    help="dump datasets",
)
@click.option(
    "-g",
    "--groups",
    "groups",
    is_flag=True,
    default=False,
    help="dump groups",
)
def attrs(
    fspath: str,
    datasets: bool = False,
    groups: bool = False,
) -> None:
    cfg = H5CliConfig.from_cli(datasets=datasets, attributes=False, groups=groups)
    attrs = {}
    with h5.File(fspath) as f:
        for _h5path, h5obj in h5.h5py_obj_gen(f):
            if (cfg.groups and isinstance(h5obj, h5.Group)) or (
                cfg.datasets and isinstance(h5obj, h5.Dataset)
            ):
                attrs[h5obj.name] = {**h5obj.attrs}
    _print_json(attrs)


def _command_not_implemented(cmd: str) -> None:
    console.print(f"Command not implemented: {cmd}")
    click.get_current_context().exit(1)


@cli.command(help="copy datasets/groups", name="cp", hidden=True)
def cp() -> None:
    _command_not_implemented("cp")


@cli.command(help="move datasets/groups", name="mv", hidden=True)
def mv() -> None:
    _command_not_implemented("mv")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
