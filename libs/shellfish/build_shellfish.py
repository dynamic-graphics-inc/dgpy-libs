# -*- coding: utf-8 -*-
import subprocess as sp

from os import path

from shellfish.fs._async import __all__ as fs_async_all

PWD = path.dirname(path.abspath(__file__))
ENCODING = "# -*- coding: utf-8 -*-"


def build_fs_promises():
    imports = [
        "from shellfish.fs._async import " + el + " as " + el.replace("_async", "")
        for el in fs_async_all
    ]
    all_elements = tuple(
        sorted(set('"' + el.replace("_async", "") + '"' for el in fs_async_all))
    )
    promises_all_lines = ["__all__ = (", "    " + ",\n    ".join(all_elements), ")"]

    lines = [
        ENCODING,
        '"""shellfish.fs.promises"""\n',
        *imports,
        "\n",
        *promises_all_lines,
    ]
    promises_filepath = path.join(PWD, "shellfish", "fs", "promises.py")
    promises_string = "\n".join(lines)
    with open(
        promises_filepath,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(promises_string)


def make_fmt():
    sp.run(["make", "fmt"])


def main():
    build_fs_promises()
    make_fmt()


if __name__ == "__main__":
    main()
