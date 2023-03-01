# -*- coding: utf-8 -*-
"""Echo/Print"""
from typing import IO, Any, Optional

__all__ = ("echo",)


def echo(
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    file: Optional[IO[str]] = None,
    flush: bool = False,
) -> None:
    """Print/echo function

    Args:
        *args: Item(s) to print/echo
        sep: Separator to print with
        end: End of print suffix; defaults to `\n`
        file: File like object to write to if not stdout

    """
    print(*objects, sep=sep, end=end, file=file, flush=flush)  # ruff: noqa: T201
