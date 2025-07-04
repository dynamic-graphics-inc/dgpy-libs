from __future__ import annotations

from os import stat_result as os_stat_result
from typing import TYPE_CHECKING

import pytest

from shellfish import sh
from shellfish.aios import scandir as aioscandir

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.asyncio()
async def test_scandir_async(tmp_path: Path) -> None:
    # Create a temporary directory with some files and sub-directories
    sh.cd(tmp_path)
    sh.write_string("a.txt", "a")
    sh.write_string("b.txt", "b")
    sh.mkdirp("dir1")
    sh.mkdirp("dir2")

    # Scan the directory contents and check each entry
    async for entry in aioscandir("."):
        # Check that the entry name is one of the expected names
        assert entry.name in ["a.txt", "b.txt", "dir1", "dir2"]

        # Check that the entry is a directory if it's one of the
        # expected directory names
        if entry.name == "dir1" or entry.name == "dir2":
            assert await entry.is_dir()
        else:
            assert await entry.is_file()

        # Check that the inode is a valid value
        entry_inode = await entry.inode()
        assert entry_inode > 0

        # Check that the entry is not a symbolic link
        _entry_is_link = await entry.is_symlink()
        assert not _entry_is_link

        # Check that the stat() result has the expected type
        entry_stat = await entry.stat()
        assert isinstance(entry_stat, os_stat_result)

        # Check that the path is the same as the path returned by
        # the __fspath__() method
        assert entry.path == entry.__fspath__()
