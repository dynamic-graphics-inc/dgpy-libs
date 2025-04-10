# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typing-extensions==4.12.2",
#     "annotated-types",
# ]
# ///
from __future__ import annotations

import os
import sys

from subprocess import run

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from xtyping.shed import (
    __all_annotated_types__,
    __all_shed__,
    __all_typing__,
    __all_typing_extensions__,
)

PWD = os.path.dirname(os.path.abspath(__file__))
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


DEPRECATED_TYPES = {
    "ByteString",
}

NEVER_REEXPORT = {
    "__all__",
    "__version__",
}


def main():
    # typing + typing_extensions - deprecated types
    import_from_typing_extensions = {
        el
        for el in {
            *__all_typing_extensions__,
            *__all_typing__,
        }
        if el not in DEPRECATED_TYPES and el not in NEVER_REEXPORT
    }

    import_from_annotated_types = {
        el
        for el in __all_annotated_types__
        if el not in DEPRECATED_TYPES and el not in NEVER_REEXPORT
    }

    import_from_shed = {el for el in __all_shed__ if el not in DEPRECATED_TYPES}

    all_sorted = sorted(
        {
            el
            for el in [
                *[
                    "annotated_types",  # re-exported module
                    "typing",  # re-exported module
                    "typing_extensions",  # re-exported module
                    "__version__",  # xtyping version
                ],
                *import_from_typing_extensions,
                *import_from_annotated_types,
                *import_from_shed,
            ]
            if el not in DEPRECATED_TYPES
        }
    )

    from collections import Counter

    counts = Counter(all_sorted)
    any_duplicates = [item for item, count in counts.items() if count > 1]
    if any_duplicates:
        raise ValueError(f"Duplicate items found in all_sorted: {any_duplicates}")

    xtyping_all_dunder = [
        "__all__ = (",
        *(
            f"    '{el}',"
            for el in sorted(
                [
                    "__version__",
                    "typing",
                    "typing_extensions",
                    "annotated_types",
                ]
            )
        ),
        # typing + typing_extensions
        *(f"    '{el}'," for el in sorted(import_from_typing_extensions)),
        # annotated_types
        *(f"    '{el}'," for el in sorted(import_from_annotated_types)),
        # shed
        *(f"    '{el}'," for el in sorted(import_from_shed)),
        ")",
    ]

    #

    init_parts = [
        header,
        # typing + typing_extensions
        *[
            f"from typing_extensions import {el}"
            for el in import_from_typing_extensions
        ],
        # annotated_types
        *[f"from annotated_types import {el}" for el in import_from_annotated_types],
        # shed
        *[f"from xtyping.shed import {el}" for el in import_from_shed],
        # xtyping.__all__
        *xtyping_all_dunder,
    ]

    with open(os.path.join(PWD, "src", "xtyping", "__init__.py"), "w") as f:
        f.write("\n".join(init_parts))

    run(args=["just", "fmt"])


if __name__ == "__main__":
    main()
