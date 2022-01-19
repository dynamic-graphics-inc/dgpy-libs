# -*- coding: utf-8 -*-
# =============================================================================
#  (c) Copyright 2022, Dynamic Graphics, Inc.
#  ALL RIGHTS RESERVED
#  Permission to use, copy, modify, or distribute this software for any
#  purpose is prohibited without specific, written prior permission from
#  Dynamic Graphics, Inc.
# =============================================================================

import os

from asyncio import run as aiorun
from os import environ, mkdir, path, sep
from pathlib import Path
from typing import Set

import pytest

from shellfish import fs, sh

PWD = path.split(path.realpath(__file__))[0]


def mk_dummy_dir() -> None:
    os.makedirs(os.path.join("dir", "a", "b", "c"), exist_ok=True)
    os.makedirs(os.path.join("dir", "a", "b", "d"), exist_ok=True)
    os.makedirs(os.path.join("dir", "e", "f"), exist_ok=True)
    fs.sstring(os.path.join("dir", "a", "b", "c", "uno.txt"), "uno")
    fs.sstring(os.path.join("dir", "a", "b", "dos.txt"), "dos")
    fs.sstring(os.path.join("dir", "a", "b", "d", "three.txt"), "three")
    fs.sstring(os.path.join("dir", "e", "f", "quatro.txt"), "four")


def test_mv_uno(tmp_path: Path) -> None:
    sh.cd(tmp_path)
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
    for f in filepath_parts:
        filepath = path.join(tmp_path, *f)
        sh.touch(filepath)
    files = sorted(fs.files_gen(tmp_path))
    sh.cd(tmp_path)
    mkdir("out")
    sh.mv("dir", "out")
    files = sorted(
        (e.replace(str(tmp_path), "").strip(sep) for e in fs.files_gen(tmp_path))
    )

    expected: Set[str] = {path.join("out", *f) for f in filepath_parts}
    got = set(files)
    assert expected == got


def test_mv_multi(tmp_path: Path) -> None:
    sh.cd(tmp_path)
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
    for f in filepath_parts:
        filepath = path.join(tmp_path, *f)
        sh.touch(filepath)
    files = sorted(fs.files_gen(tmp_path))
    sh.cd(tmp_path)
    mkdir("out")
    sh.mv("dir/*", "out")
    files = sorted(
        (e.replace(str(tmp_path), "").strip(sep) for e in fs.files_gen(tmp_path))
    )

    expected = {
        path.join("out", *f).replace(sep + "dir" + sep, sep) for f in filepath_parts
    }

    got = set(files)
    assert expected == got


def test_export_single_key() -> None:
    key_str = "ENVARTESTSINGLEKEY"
    key = "ENVARTESTSINGLEKEY=pood"

    assert key_str not in environ
    sh.export(key)
    assert key_str in environ
    assert environ[key_str] == "pood"
    del environ[key_str]


def test_export_key_val() -> None:
    key_str = "ENVARTEST2PARAMS"
    key, val = key_str, "pood"
    from os import environ

    assert key_str not in environ
    sh.export(key, val)
    assert key_str in environ


@pytest.fixture(
    params=[
        "file.txt",
        path.join("dir", "file.txt"),
        path.join("dir1", "dir2", "file.txt"),
        path.join("dir1", "dir2", "dir3", "file.txt"),
        path.join("dir1", "dir2", "dir3", "dir4", "file.txt"),
    ]
)
def dummy_filepath(request):
    return request.param


def test_touch(dummy_filepath: str, tmp_path: Path) -> None:
    fdpath = path.join(tmp_path, dummy_filepath)
    assert not path.exists(fdpath)
    sh.touch(fdpath)
    assert path.exists(fdpath)


def test_rm_multi(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    test_files = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "a", "s", "d"]
    mkdir("test_env")
    sh.cd("test_env")
    test_files = [x + ".txt" for x in test_files]
    for x in test_files:
        with open(x, "w") as f:
            f.write(" ")
    expected = []
    sh.cd(tmp_path)
    sh.rm("test_env/*.txt")
    actual = os.listdir("test_env")
    assert expected == actual


def test_rm_para(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    test_files = ["q", "w", "e"]
    mkdir("test_env")
    sh.cd("test_env")
    test_files = [x + ".txt" for x in test_files]
    for x in test_files:
        with open(x, "w") as f:
            f.write(" ")
    sh.cd(tmp_path)
    sh.rm("test_env", r=True)
    assert not os.path.exists("test_env")


def test_cp(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    test_files = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "a", "s", "d"]
    mkdir("test_env")
    sh.cd("test_env")
    test_files = [x + ".txt" for x in test_files]
    for x in test_files:
        with open(x, "w") as f:
            f.write(" ")
    sh.cd(tmp_path)
    os.mkdir("cp_dir")
    sh.cp("test_env/*.txt", "cp_dir")

    actual = os.listdir("cp_dir")
    assert set(test_files) == set(actual)


def test_cp_dir(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    test_files = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "a", "s", "d"]
    mkdir("test_env")
    sh.cd("test_env")
    test_files = [x + ".txt" for x in test_files]
    for x in test_files:
        with open(x, "w") as f:
            f.write(" ")
    sh.cd(tmp_path)
    sh.cp("test_env", "cp_dir", r=True)
    actual = os.listdir("cp_dir")
    assert set(test_files) == set(actual)


### TEST TREE


EXPECTED = """
dir/
├── a/
│   └── b/
│       ├── c/
│       │   └── uno.txt
│       ├── d/
│       │   └── three.txt
│       └── dos.txt
└── e/
    └── f/
        └── quatro.txt"""


def test_sh_tree_one(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    mk_dummy_dir()
    a = sh.tree("dir").strip("\n")
    expected = EXPECTED.strip("\n")
    assert expected == a


def test_sh_ls_files_n_ls_dirs(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    mk_dummy_dir()
    os.makedirs("a", exist_ok=True)
    os.makedirs("b", exist_ok=True)
    os.makedirs("c", exist_ok=True)
    os.makedirs("herm", exist_ok=True)
    fs.sstring("f1.txt", "f1")
    fs.sstring("f2.txt", "f2")
    fs.sstring("f3.txt", "f3")
    files_abs, dirs_abs = sh.ls_files_dirs(tmp_path, abspath=True)
    files_not_abs, dirs_not_abs = sh.ls_files_dirs(tmp_path, abspath=False)
    _f1 = [os.path.split(el)[-1] for el in files_abs]
    _f2 = [os.path.split(el)[-1] for el in files_not_abs]
    _d1 = [os.path.split(el)[-1] for el in dirs_abs]
    _d2 = [os.path.split(el)[-1] for el in dirs_not_abs]
    assert _f1 == _f2
    assert _d1 == _d2


def test_do_and_do_async():
    sh.cd(PWD)
    proc_sync = sh.do(["ls"])
    proc_async = aiorun(sh.do_async(["ls"]))
    assert proc_sync.stdout == proc_async.stdout
    assert proc_sync.async_proc is False
    assert proc_async.async_proc


#
