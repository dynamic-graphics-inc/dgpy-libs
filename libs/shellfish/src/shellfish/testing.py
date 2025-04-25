# -*- coding: utf-8 -*-
from __future__ import annotations

import string

from os import getcwd, makedirs, path
from os.path import sep
from pathlib import Path
from random import choice as rand_choice, randint
from typing import TYPE_CHECKING, Dict, List, Optional

from shellfish.fs import wstring

if TYPE_CHECKING:
    from xtyping import FsPath

__all__ = (
    "assert_symlink_exists",
    "mk_random_dirtree",
    "random_directory_path",
    "random_string",
)


def assert_symlink_exists(fspath: FsPath, *, target: Optional[FsPath] = None) -> bool:
    _path = Path(fspath)
    try:
        assert _path.exists()
        assert _path.is_symlink()
        if target is not None:
            assert _path.resolve() == Path(target)
        return True
    except AssertionError:
        ...
    return False


def random_string(length: int = 10) -> str:
    """Return a random string of a given length (defaults to 10)

    Examples:
        >>> string = random_string(10)
        >>> len(string) == 10
        True

    """
    return "".join(
        rand_choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def random_directory_path(depth: int = 4) -> str:
    """Return a random directory path with a given depth (defaults to 4)

    Examples:
        >>> from os import sep
        >>> dirpath = random_directory_path(4)
        >>> len(dirpath.split(sep)) == 4
        True

    """
    return str(path.join(*(random_string(randint(1, 5)) for s in range(depth))))


def mk_random_dirtree(
    dest: Optional[str] = None,
    n_subdirectories: int = 8,
    max_subdirectory_files: int = 4,
    max_file_string_len: int = 100,
) -> Dict[str, List[str]]:
    """Make a random directory tree full of dummy files at a given dirpath"""
    dest = dest or getcwd()
    dirpaths = [random_directory_path() for i in range(n_subdirectories)]
    all_dirpaths = []
    for dp in dirpaths:
        all_dirpaths.append(dp)
        split_dp = dp.split(sep)
        for ix, _ in enumerate(split_dp, start=1):
            sub_dp = sep.join(split_dp[:ix])
            all_dirpaths.append(sub_dp)
    all_dirpaths = [path.join(dest, dp) for dp in all_dirpaths]
    all_filepaths = []
    for dp in all_dirpaths:
        makedirs(dp, exist_ok=True)
        for _i in range(randint(1, max_subdirectory_files)):
            file_string = random_string(randint(10, max_file_string_len))
            file_name = random_string(5) + ".txt"
            file_path = path.join(dp, file_name)
            all_filepaths.append(file_path)
            wstring(file_path, file_string)
    return {"dirpaths": all_dirpaths, "filepaths": all_filepaths}
