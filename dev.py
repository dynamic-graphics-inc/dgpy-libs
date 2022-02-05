# -*- coding: utf-8 -*-
from graphlib import TopologicalSorter
from os import chdir, listdir, path
from pathlib import Path
from subprocess import run
from typing import Callable, Iterable, List, Optional, Tuple, TypeVar

from listless import unique
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
ENCODING = "# -*- coding: utf-8 -*-"


def sorted_unique(
    iterable: Iterable[_T], key: Optional[Callable[[_T], _K]] = None
) -> List[_T]:
    return list(sorted(unique(iterable, key=key), key=key))


def sorted_tuple(
    iterable: Iterable[_T],
    unique: bool = False,
    key: Optional[Callable[[_T], _K]] = None,
) -> Tuple[_T, ...]:
    if unique:
        return tuple(sorted_unique(iterable, key=key))
    return tuple(sorted(iterable))


assert sorted(tuple(set(LIBS))) == listdir(LIBS_DIR)

pyfiles = (
    Path(filepath)
    for filepath in fs.files_gen()
    if filepath.endswith(".py") and "nox" not in filepath and ".venv" not in filepath
)

for pyfile in pyfiles:
    print("Pyfile:", pyfile)
    txt = pyfile.read_text(encoding="utf-8")
    if ENCODING not in txt:
        print(f"{pyfile} is not encoded in utf-8")
        _txt = ENCODING + "\n" + txt
        pyfile.write_text(_txt, encoding="utf-8")

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


ts = TopologicalSorter(LIBS_GRAPH)
static_order = ts.static_order()

for el in static_order:
    print("==========")
    print(el)
    print(LIBS_DIR / el)
    chdir(LIBS_DIR / el)
    run(
        args=["poetry", "update"],
        shell=True,
    )
