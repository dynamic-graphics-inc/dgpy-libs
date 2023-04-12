# -*- coding: utf-8 -*-
from __future__ import annotations

from shlex import quote as _quote
from typing import AnyStr, List, Union

from listless import flatten_strings as _flatten_strings
from shellfish.sp import PopenArgs


def argstr(string: AnyStr) -> AnyStr:
    """Return given string with quotes if needed"""
    if isinstance(string, bytes):
        return argstr(string.decode()).encode()
    return _quote(string) if " " in string else string


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
        else " ".join(map(argstr, map(str, args)))
    )


def flatten_args(*args: PopenArgs) -> List[str]:
    """Flatten possibly nested iterables of sequences to a list of strings

    Examples:
        >>> list(flatten_args("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(flatten_args("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(_flatten_strings(args))  # type: ignore[arg-type]
