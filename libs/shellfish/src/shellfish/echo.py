# -*- coding: utf-8 -*-
"""Echo/Print"""

from __future__ import annotations

from typing import IO, Any

__all__ = ("echo",)


def echo(
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    file: IO[str] | None = None,
    flush: bool = False,
) -> None:
    r"""Print/echo function

    This function is basically the print function, and exists so that one can
    deliberately print without using the built-in print function which is not
    allowed by the `dgpy-libs` ruff rules.

    Args:
        *objects: Item(s) to print/echo
        sep: Separator to print with
        end: End of print suffix; defaults to `\n`
        file: File like object to write to if not stdout
        flush: Flush the file after writing

    Examples:
        >>> echo("shellfish")
        shellfish

    """
    print(*objects, sep=sep, end=end, file=file, flush=flush)
