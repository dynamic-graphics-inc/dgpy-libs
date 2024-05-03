# -*- coding: utf-8 -*-
from __future__ import annotations

from shlex import quote as _quote
from typing import TYPE_CHECKING, AnyStr, List, Union

from listless import flatten_strings as _flatten_strings

if TYPE_CHECKING:
    from shellfish._types import PopenArgs


def arganystr(string: AnyStr) -> AnyStr:
    """Return given string with quotes if needed

    Examples:
        >>> arganystr("a b")
        "'a b'"
        >>> arganystr("a b c")
        "'a b c'"
        >>> arganystr(b"a b")
        b"'a b'"

    """
    if isinstance(string, bytes):
        return arganystr(string.decode()).encode()
    return _quote(string) if " " in string else string


def argstr(string: Union[str, bytes]) -> str:
    """Return given string with quotes if needed

    Examples:
        >>> argstr("a b")
        "'a b'"
        >>> argstr("a b c")
        "'a b c'"
        >>> argstr(b"a b")
        "'a b'"

    """
    return arganystr(string if isinstance(string, str) else string.decode())


def flatten_args(*args: PopenArgs) -> List[str]:
    """Flatten possibly nested iterables of sequences to a list of strings

    Examples:
        >>> list(flatten_args("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(flatten_args("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(_flatten_strings(args))  # type: ignore[arg-type]


def args2cmd(args: PopenArgs) -> Union[str, bytes]:
    """Return single command string from given popenargs

    Examples:
        >>> args2cmd(["ls", "-l"])
        'ls -l'
        >>> args2cmd(["ls", "-l", "a b"])
        "ls -l 'a b'"
        >>> args2cmd(["ls", "-l", "a b", "c d"])
        "ls -l 'a b' 'c d'"

    """
    return (
        args
        if isinstance(args, (bytes, str))
        else " ".join(map(argstr, map(str, flatten_args(args))))
    )
