import os

from subprocess import run

from xtyping.shed import (
    __all_annotated_types__,
    __all_shed__,
    __all_typing__,
    __all_typing_extensions__,
)

include_in_all = {
    "__version__",
    "typing",
    "typing_extensions",
    "annotated_types",
}
header = '''# -*- coding: utf-8 -*-
"""typing + typing_extensions + misc types/aliases"""
import typing

import annotated_types
import typing_extensions

from xtyping.__about__ import __version__
'''


def main():
    imports = {
        "typing": (el for el in __all_typing__ if el not in __all_typing_extensions__),
        "typing_extensions": __all_typing_extensions__,
        "annotated_types": __all_annotated_types__,
        "shed": __all_shed__,
    }

    init_all = [
        "__all__ = (",
        *[
            f"    '{el}',"
            for el in sorted(
                {
                    *__all_typing__,
                    *__all_typing_extensions__,
                    *__all_annotated_types__,
                    *__all_shed__,
                    *include_in_all,
                }
            )
        ],
        ")",
    ]
    init_parts = [
        header,
        *[f"from typing import {el}" for el in imports["typing"]],
        *[f"from typing_extensions import {el}" for el in imports["typing_extensions"]],
        *[f"from annotated_types import {el}" for el in imports["annotated_types"]],
        *[f"from xtyping.shed import {el}" for el in imports["shed"]],
        *init_all,
    ]

    with open(os.path.join("xtyping", "__init__.py"), "w") as f:
        f.write("\n".join(init_parts))

    run(args=["make", "fmt"])


if __name__ == "__main__":
    main()
