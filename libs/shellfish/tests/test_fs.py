from os import makedirs, path
from typing import Set

from jsonbourne.trydantic import dataclass
from shellfish import fs
from shellfish.fs import touch


@dataclass
class DummyDataDir:
    root: str
    files: Set[str]
    dirs: Set[str]


def dummy_data_dir_from_filepaths(root: str, filepaths: Set[str]) -> DummyDataDir:
    files = set()
    dirs = set()
    for filepath in filepaths:
        dirs.add(path.dirname(filepath))
        files.add(filepath)
    return DummyDataDir(root, files, dirs)


def test_scandir_gen() -> None:
    tmpdir = "test_scandir_gen"
    makedirs(tmpdir, exist_ok=True)
    filepath_parts = [
        ("dir", "file1.txt"),
        ("dir", "file2.txt"),
        ("dir", "file3.txt"),
        ("dir", "dir2", "file1.txt"),
        ("dir", "dir2", "file2.txt"),
        ("dir", "dir2", "file3.txt"),
        ("dir", "dir2a", "file1.txt"),
        ("dir", "dir2a", "file2.txt"),
        ("dir", "dir2a", "file3.txt"),
    ]
    expected_dirs_set = set()
    expected_files = []
    for f in filepath_parts:
        fspath = path.join(*f).replace("\\", "/")
        fspath = path.join(tmpdir, fspath).replace("\\", "/")
        dirpath = path.dirname(fspath)
        expected_files.append(fspath)
        expected_dirs_set.add(dirpath)
        makedirs(dirpath, exist_ok=True)
        touch(fspath)

    scanned = sorted(
        [el.path.replace("\\", "/") for el in fs.scandir_gen(path.join(tmpdir, "dir"))]
    )
    assert scanned == [
        "test_scandir_gen/dir/dir2",
        "test_scandir_gen/dir/dir2a",
        "test_scandir_gen/dir/file1.txt",
        "test_scandir_gen/dir/file2.txt",
        "test_scandir_gen/dir/file3.txt",
    ]

    scanned_dirs_only = sorted(
        [
            el.path.replace("\\", "/")
            for el in fs.scandir_gen(
                path.join(tmpdir, "dir"), dirs=True, files=False, symlinks=False
            )
        ]
    )
    assert scanned_dirs_only == [
        "test_scandir_gen/dir/dir2",
        "test_scandir_gen/dir/dir2a",
    ]

    scanned_files_only = sorted(
        [
            el.path.replace("\\", "/")
            for el in fs.scandir_gen(
                path.join(tmpdir, "dir"), dirs=False, files=True, symlinks=False
            )
        ]
    )
    assert scanned_files_only == [
        "test_scandir_gen/dir/file1.txt",
        "test_scandir_gen/dir/file2.txt",
        "test_scandir_gen/dir/file3.txt",
    ]

    #  RECURSIVE
    scanned_recursive = sorted(
        [
            el.path.replace("\\", "/")
            for el in fs.scandir_gen(path.join(tmpdir, "dir"), recursive=True)
        ]
    )
    assert scanned_recursive == [
        "test_scandir_gen/dir/dir2",
        "test_scandir_gen/dir/dir2/file1.txt",
        "test_scandir_gen/dir/dir2/file2.txt",
        "test_scandir_gen/dir/dir2/file3.txt",
        "test_scandir_gen/dir/dir2a",
        "test_scandir_gen/dir/dir2a/file1.txt",
        "test_scandir_gen/dir/dir2a/file2.txt",
        "test_scandir_gen/dir/dir2a/file3.txt",
        "test_scandir_gen/dir/file1.txt",
        "test_scandir_gen/dir/file2.txt",
        "test_scandir_gen/dir/file3.txt",
    ]

    scanned_recursive_files_only = sorted(
        [
            el.path.replace("\\", "/")
            for el in fs.scandir_gen(
                path.join(tmpdir, "dir"),
                recursive=True,
                files=True,
                dirs=False,
                symlinks=False,
            )
        ]
    )
    assert scanned_recursive_files_only == [
        "test_scandir_gen/dir/dir2/file1.txt",
        "test_scandir_gen/dir/dir2/file2.txt",
        "test_scandir_gen/dir/dir2/file3.txt",
        "test_scandir_gen/dir/dir2a/file1.txt",
        "test_scandir_gen/dir/dir2a/file2.txt",
        "test_scandir_gen/dir/dir2a/file3.txt",
        "test_scandir_gen/dir/file1.txt",
        "test_scandir_gen/dir/file2.txt",
        "test_scandir_gen/dir/file3.txt",
    ]

    scanned_recursive_dirs_only = sorted(
        [
            el.path.replace("\\", "/")
            for el in fs.scandir_gen(
                tmpdir,
                recursive=True,
                files=False,
                dirs=True,
                symlinks=False,
            )
        ]
    )
    assert scanned_recursive_dirs_only == [
        "test_scandir_gen/dir",
        "test_scandir_gen/dir/dir2",
        "test_scandir_gen/dir/dir2a",
    ]

    fs.rm(tmpdir, recursive=True)
