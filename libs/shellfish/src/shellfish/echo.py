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
