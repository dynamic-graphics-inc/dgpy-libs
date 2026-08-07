# -*- coding: utf-8 -*-
"""aios = asyncio + os"""
# ruff: noqa: RUF067

from __future__ import annotations

import os

from typing import TYPE_CHECKING, AnyStr, Generic

from asyncify import asyncify
from shellfish.aios import _path

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

__all__ = (
    "DirEntryAsync",
    "chmod",
    "listdir",
    "lstat",
    "makedirs",
    "mkdir",
    "path",
    "readlink",
    "remove",
    "removedirs",
    "rename",
    "renames",
    "replace",
    "rmdir",
    "scandir",
    "stat",
    "truncate",
)

path = _path

chmod = asyncify(os.chmod)
listdir = asyncify(os.listdir)
lstat = asyncify(os.lstat)
makedirs = asyncify(os.makedirs)
mkdir = asyncify(os.mkdir)
readlink = asyncify(os.readlink)
remove = asyncify(os.remove)
removedirs = asyncify(os.removedirs)
rename = asyncify(os.rename)
renames = asyncify(os.renames)
replace = asyncify(os.replace)
rmdir = asyncify(os.rmdir)
stat = asyncify(os.stat)
truncate = asyncify(os.truncate)


class DirEntryAsync(Generic[AnyStr]):
    """DirEntryAsync ~ `os.DirEntry` + async

    Notes:
        Signature of `os.DirEntry`:

        ```python
        @final
        class DirEntry(Generic[AnyStr]):
            # This is what the scandir iterator yields
            # The constructor is hidden

            @property
            def name(self) -> AnyStr: ...
            @property
            def path(self) -> AnyStr: ...
            def inode(self) -> int: ...
            def is_dir(self, *, follow_symlinks: bool = True) -> bool: ...
            def is_file(self, *, follow_symlinks: bool = True) -> bool: ...
            def is_symlink(self) -> bool: ...
            def stat(self, *, follow_symlinks: bool = True) -> stat_result: ...
            def __fspath__(self) -> AnyStr: ...
            if sys.version_info >= (3, 9):
                def __class_getitem__(cls, item: Any) -> GenericAlias: ...
        ```

    """

    __slots__ = ("_dir_entry",)
    _dir_entry: os.DirEntry[AnyStr]

    def __init__(self, dir_entry: os.DirEntry[AnyStr]) -> None:
        """Wrap an `os.DirEntry` object

        Args:
            dir_entry: `os.DirEntry` object to wrap

        """
        self._dir_entry = dir_entry

    @property
    def name(self) -> AnyStr:
        """Base name of the entry, relative to its parent directory

        Returns:
            AnyStr: Base name of the entry (relative to its parent directory)

        """
        return self._dir_entry.name

    @property
    def path(self) -> AnyStr:
        """Path of the entry

        Returns:
            AnyStr: Entry path (the scandir `path` argument joined with `name`)

        """
        return self._dir_entry.path

    async def inode(self) -> int:
        """Async version of `os.DirEntry.inode`

        Returns:
            int: Inode number of the entry

        """
        return await asyncify(self._dir_entry.inode)()

    async def is_dir(self, *, follow_symlinks: bool = True) -> bool:
        """Async version of `os.DirEntry.is_dir`

        Args:
            follow_symlinks: Follow symlinks when checking (Default value = True)

        Returns:
            bool: True if the entry is a directory; False otherwise

        """
        return await asyncify(self._dir_entry.is_dir)(follow_symlinks=follow_symlinks)

    async def is_file(self, *, follow_symlinks: bool = True) -> bool:
        """Async version of `os.DirEntry.is_file`

        Args:
            follow_symlinks: Follow symlinks when checking (Default value = True)

        Returns:
            bool: True if the entry is a file; False otherwise

        """
        return await asyncify(self._dir_entry.is_file)(follow_symlinks=follow_symlinks)

    async def is_symlink(self) -> bool:
        """Async version of `os.DirEntry.is_symlink`

        Returns:
            bool: True if the entry is a symlink; False otherwise

        """
        return await asyncify(self._dir_entry.is_symlink)()

    async def stat(self, *, follow_symlinks: bool = True) -> os.stat_result:
        """Async version of `os.DirEntry.stat`

        Args:
            follow_symlinks: Follow symlinks when stat-ing (Default value = True)

        Returns:
            os.stat_result: Stat result for the entry

        """
        return await asyncify(self._dir_entry.stat)(follow_symlinks=follow_symlinks)

    def __fspath__(self) -> AnyStr:
        """Return the entry's path as required by `os.PathLike`

        Returns:
            AnyStr: Entry path

        """
        return self._dir_entry.__fspath__()


async def scandir(path: AnyStr) -> AsyncIterator[DirEntryAsync[AnyStr]]:  # noqa: RUF029
    """Async version of `os.scandir`

    Args:
        path: Directory path to scan

    Yields:
        DirEntryAsync: Async-wrapped `os.DirEntry` objects

    Notes:
        Signature of `os.scandir`:

        ```python
        def scandir(path: AnyStr) -> Iterator[DirEntry[AnyStr]]: ...
        ```

    """
    # for dir_entry in map(_dir_entry_async, os.scandir(path)):
    for dir_entry in (DirEntryAsync(el) for el in os.scandir(path)):
        yield dir_entry
