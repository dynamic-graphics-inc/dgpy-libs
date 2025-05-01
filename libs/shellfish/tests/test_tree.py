from __future__ import annotations

import os

from typing import TYPE_CHECKING

from shellfish import sh

if TYPE_CHECKING:
    from pathlib import Path

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


def mk_dummy_dir() -> None:
    sh.mkdirp(os.path.join("dir", "a", "b", "c"))
    sh.mkdirp(os.path.join("dir", "a", "b", "d"))
    sh.mkdirp(os.path.join("dir", "e", "f"))
    sh.wstring(os.path.join("dir", "a", "b", "c", "uno.txt"), "uno")
    sh.wstring(os.path.join("dir", "a", "b", "dos.txt"), "dos")
    sh.wstring(os.path.join("dir", "a", "b", "d", "three.txt"), "three")
    sh.wstring(os.path.join("dir", "e", "f", "quatro.txt"), "four")


def test_sh_tree_one(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    mk_dummy_dir()
    a = sh.tree("dir").strip("\n")
    expected = EXPECTED.strip("\n")
    assert expected == a
