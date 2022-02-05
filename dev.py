# -*- coding: utf-8 -*-
from graphlib import TopologicalSorter
from os import chdir, listdir, path
from pathlib import Path
from subprocess import run
from typing import TypeVar

from shellfish import fs

_T = TypeVar("_T")
_K = TypeVar("_K")

PWD = path.dirname(path.abspath(__file__))
REPO_ROOT = Path(PWD)
LIBS_DIR = REPO_ROOT / "libs"

LIBS = (
    "aiopen",
    "asyncify",
    "fmts",
    "funkify",
    "h5",
    "jsonbourne",
    "lager",
    "listless",
    "requires",
    "shellfish",
    "xtyping",
)

LIBS_GRAPH = {
    # no inter deps
    "fmts": {},
    "funkify": {},
    "h5": {},
    "lager": {},
    "listless": {},
    "xtyping": {},
    # has inter deps
    "jsonbourne": {"xtyping"},
    "aiopen": {"funkify", "xtyping"},
    "asyncify": {"funkify", "xtyping"},
    "requires": {"funkify", "xtyping"},
    "shellfish": {
        "aiopen",
        "asyncify",
        "funkify",
        "jsonbourne",
        "listless",
        "xtyping",
    },
}

DONT_PUBLISH = {
    "xtyping",
}
ts = TopologicalSorter(LIBS_GRAPH)
static_order = ts.static_order()

assert sorted(tuple(set(LIBS))) == listdir(LIBS_DIR)


def check_encoding():
    pyfiles = (
        Path(filepath)
        for filepath in fs.files_gen()
        if filepath.endswith(".py")
           and "nox" not in filepath
           and ".venv" not in filepath
    )
    ENCODING = "# -*- coding: utf-8 -*-"

    for pyfile in pyfiles:
        print("Pyfile:", pyfile)
        txt = pyfile.read_text(encoding="utf-8")

        if ENCODING not in txt:
            print(f"{pyfile} is not encoded in utf-8")
            _txt = ENCODING + "\n" + txt
            pyfile.write_text(_txt, encoding="utf-8")


def main():
    for el in static_order:
        print("==========")
        print(el)
        print(LIBS_DIR / el)
        chdir(LIBS_DIR / el)
        run(
            args=["poetry", "update", "--lock"],
            shell=True,
        )

        run(
            args=["poetry", "version", "patch"],
            shell=True,
        )
        chdir(REPO_ROOT)
        run(args=["nox", "-s", "update_metadata"], shell=True, capture_output=True)
        run(args=["make", "fmt"], shell=True)
        chdir(LIBS_DIR / el)

        run(args=["make", "test"], shell=True)

        if el not in DONT_PUBLISH:
            run(args=["poetry", "publish", "--build", "--no-interaction", "--dry-run"], shell=True)


if __name__ == "__main__":
    main()
