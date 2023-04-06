# -*- coding: utf-8 -*-
"""h5.cli"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

import click
import numpy as np

from globsters import globster
from rich.console import Console
from typing_extensions import TypeGuard

import h5

from h5 import dev as h5dev

console = Console()

__all__ = (
    "cli",
    "H5CliConfig",
)


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

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def make_globster(
    include: Optional[Tuple[str, ...]] = None, exclude: Optional[Tuple[str, ...]] = None
) -> globster:
    patterns: List[str] = []
    if include:
        patterns.extend(include)
    if exclude:
        patterns.extend(f"!{el}" for el in exclude)
    return globster(patterns)


@dataclass
class H5CliConfig:
    datasets: bool
    attributes: bool
    groups: bool

    @classmethod
    def from_cli(cls, datasets: bool, attributes: bool, groups: bool) -> H5CliConfig:
        return (
            cls(datasets=True, attributes=True, groups=True)
            if not any((datasets, attributes, groups))
            else cls(datasets, attributes, groups)
        )


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option("--debug", envvar="DGPYDEBUG", is_flag=True, default=False)
def cli(debug: bool = False) -> None:
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
    console.print_json(data=data, default=_json_default)

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
    default=("**/.*",),
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
    exclude: Tuple[str, ...] = ("**/.*",),
) -> None:
    H5CliConfig.from_cli(datasets=datasets, attributes=attributes, groups=groups)
    matcher = make_globster(include=include, exclude=exclude)
    h5dev.H5File.from_fspath(fspath)
    with h5.File(fspath, "r") as f:
        data = {
            key: h5dev.h5py_obj_info(value)
            for key, value in h5.h5iter(f)
            if matcher(key)
        }
        data_dump = {key: value.dump() for key, value in data.items()}
    console.print_json(data=data_dump, default=_json_default)


@cli.command(
    help="HDF5 file as tree",
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
    file_info = h5dev.H5File.from_fspath(fspath)

    if json_:
        console.print_json(data=file_info.dict(), default=_json_default)
    else:
        console.print(file_info)


def _keys(fspath: str, dump_cfg: H5CliConfig) -> List[str]:
    file_keys: List[str] = []
    with h5.File(fspath) as f:
        if dump_cfg.datasets and dump_cfg.groups:
            file_keys.extend(h5.h5py_obj_keys_gen(f))
        elif dump_cfg.datasets and not dump_cfg.groups:
            file_keys.extend((k for k, v in h5.datasets(f)))
        elif not dump_cfg.datasets and dump_cfg.groups:
            file_keys.extend((k for k, v in h5.groups(f)))
    return file_keys


@cli.command(help="dump keys as JSON array", name="keys")
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
    dump_cfg = H5CliConfig.from_cli(datasets=datasets, attributes=False, groups=groups)
    file_keys = _keys(fspath, dump_cfg)
    console.print_json(data=file_keys, default=_json_default)


@cli.command(help="List keys as JSON array", name="ls")
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
def list(
    fspath: str,
    datasets: bool = False,
    groups: bool = False,
    json_: bool = False,
) -> None:
    dump_cfg = H5CliConfig.from_cli(datasets=datasets, attributes=False, groups=groups)
    file_keys = _keys(fspath, dump_cfg)
    if json_:
        console.print_json(data=file_keys, default=_json_default)
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
    dump_cfg = H5CliConfig.from_cli(datasets=datasets, attributes=False, groups=groups)
    attrs = {}
    with h5.File(fspath) as f:
        for _h5path, h5obj in h5.h5py_obj_gen(f):
            if dump_cfg.groups and isinstance(h5obj, h5.Group):
                attrs[h5obj.name] = {**h5obj.attrs}
            elif dump_cfg.datasets and isinstance(h5obj, h5.Dataset):
                attrs[h5obj.name] = {**h5obj.attrs}
    console.print_json(data=attrs, default=_json_default)


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
