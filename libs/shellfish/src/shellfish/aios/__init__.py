# -*- coding: utf-8 -*-
"""aios = asyncio + os"""

from __future__ import annotations

import os

from typing import AnyStr, AsyncIterator, Generic

from asyncify import asyncify
from shellfish.aios import _path

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
    """DirEntryAsync os.DirEntry + async

    Signature of os.DirEntry:
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
        self._dir_entry = dir_entry

    @property
    def name(self) -> AnyStr:
        return self._dir_entry.name

    @property
    def path(self) -> AnyStr:
        return self._dir_entry.path

    async def inode(self) -> int:
        return await asyncify(self._dir_entry.inode)()

    async def is_dir(self, *, follow_symlinks: bool = True) -> bool:
        return await asyncify(self._dir_entry.is_dir)(follow_symlinks=follow_symlinks)

    async def is_file(self, *, follow_symlinks: bool = True) -> bool:
        return await asyncify(self._dir_entry.is_file)(follow_symlinks=follow_symlinks)

    async def is_symlink(self) -> bool:
        return await asyncify(self._dir_entry.is_symlink)()

    async def stat(self, *, follow_symlinks: bool = True) -> os.stat_result:
        return await asyncify(self._dir_entry.stat)(follow_symlinks=follow_symlinks)

    def __fspath__(self) -> AnyStr:
        return self._dir_entry.__fspath__()


async def scandir(path: AnyStr) -> AsyncIterator[DirEntryAsync[AnyStr]]:
    """Async version of os.scandir

    Signature of os.scandir:
        ```python
        def scandir(path: AnyStr) -> Iterator[DirEntry[AnyStr]]: ...
        ```
    """
    # for dir_entry in map(_dir_entry_async, os.scandir(path)):
    for dir_entry in (DirEntryAsync(el) for el in os.scandir(path)):
        yield dir_entry
