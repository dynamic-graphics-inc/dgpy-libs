"""Testing shelfish.fs"""

from collections import Counter
from os import path
from pathlib import Path
from typing import Callable, Iterable

import pytest

from shellfish import sh


def test_is_file_dir_link(tmp_path: Path) -> None:
    """Test is_file"""
    sh.cd(tmp_path)
    test_filename = "file1.txt"
    test_dirname = "dir1"
    assert not sh.dir_exists(test_filename)
    assert not sh.exists(test_filename)
    assert not sh.file_exists(test_filename)
    assert not sh.is_dir(test_filename)
    assert not sh.is_file(test_filename)
    assert not sh.is_link(test_filename)
    assert not sh.isdir(test_filename)
    assert not sh.isfile(test_filename)
    assert not sh.islink(test_filename)

    # make dir and file
    sh.mkdir(test_dirname)
    sh.touch(test_filename)

    assert sh.is_file(test_filename)
    assert sh.isfile(test_filename)
    assert sh.is_dir(test_dirname)
    assert sh.isdir(test_dirname)
    assert sh.exists(test_dirname)
    assert sh.exists(test_filename)

    assert not sh.is_dir(test_filename)
    assert not sh.is_file(test_dirname)
    assert not sh.is_link(test_dirname)
    assert not sh.is_link(test_filename)
    assert not sh.isdir(test_filename)
    assert not sh.isfile(test_dirname)
    assert not sh.islink(test_dirname)
    assert not sh.islink(test_filename)


@pytest.mark.asyncio
async def test_is_file_dir_link_async(tmp_path: Path) -> None:
    """Test is_file"""
    sh.cd(tmp_path)
    _filename = "file1.txt"
    _dirname = "dir1"
    assert not await sh.exists_async(_filename)
    assert not await sh.dir_exists_async(_filename)
    assert not await sh.file_exists_async(_filename)
    assert not await sh.is_file_async(_filename)
    assert not await sh.is_link_async(_filename)
    assert not await sh.is_dir_async(_filename)
    assert not await sh.isfile_async(_filename)
    assert not await sh.islink_async(_filename)
    assert not await sh.isdir_async(_filename)

    # make dir and file
    sh.mkdir(_dirname)
    sh.touch(_filename)

    assert await sh.is_file_async(_filename)
    assert await sh.isfile_async(_filename)
    assert await sh.is_dir_async(_dirname)
    assert await sh.isdir_async(_dirname)

    assert not sh.is_dir(_filename)
    assert not sh.is_file(_dirname)
    assert not sh.is_link(_dirname)
    assert not sh.is_link(_filename)
    assert not sh.isdir(_filename)
    assert not sh.isfile(_dirname)
    assert not sh.islink(_dirname)
    assert not sh.islink(_filename)

    stat_res = await sh.stat_async(_filename)
    assert stat_res.st_size == 0


@pytest.mark.asyncio
async def test_listdir_async(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    sh.mkdir("a-dir")
    for i in range(3):
        sh.touch(
            path.join("a-dir", f"file{i}.txt"),
        )
    items = await sh.listdir_async("a-dir")
    assert sorted(items) == ["file0.txt", "file1.txt", "file2.txt"]


@pytest.mark.parametrize(
    "gen",
    [
        pytest.param(sh.dirs_gen, id="dirs_gen"),
        pytest.param(sh.files_gen, id="files_gen"),
        pytest.param(sh.walk_gen, id="walk_gen"),
    ],
)
def test_fs_generator_duplicates(gen: Callable[..., Iterable[str]]) -> None:
    pkg_root = Path(__file__).parent.parent
    gen_count = Counter(gen(pkg_root))
    duplicates = {k: v for k, v in gen_count.items() if v > 1}
    assert not duplicates, f"duplicates: {duplicates}"
