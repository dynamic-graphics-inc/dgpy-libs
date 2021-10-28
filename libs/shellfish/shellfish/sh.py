# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import IO, Any, Optional


class _FlagMeta(type):
    """Meta class"""

    @staticmethod
    @lru_cache(maxsize=None)
    def attr2flag(string: str) -> str:
        """Convert and return attr to string"""
        return string.replace('_', '-')

    def __getattr__(self, name: str) -> str:
        return self.attr2flag(string=name)


class Flag(metaclass=_FlagMeta):
    """Flag obj

    Examples:
        >>> Flag.__help
        '--help'
        >>> Flag._v
        '-v'

    """

    ...


def echo(
    *args: Any, sep: str = ' ', end: str = '\n', file: Optional[IO[Any]] = None
) -> None:
    """Print/echo function

    Args:
        *args: Item(s) to print/echo
        sep: Separator to print with
        end: End of print suffix; defaults to `\n`
        file: File like object to write to if not stdout

    """
    print(*args, sep=sep, end=end, file=file)  # noqa: T001


if __name__ == "__main__":
    from doctest import testmod

    testmod()
