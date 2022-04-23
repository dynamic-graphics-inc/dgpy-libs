# -*- coding: utf-8 -*-
"""dot.env utils"""
from __future__ import annotations

import re

from os import getcwd, path
from shlex import split as shplit

from shellfish.fs import rstring
from xtyping import Dict, FsPath, Optional

__all__ = ("ldotenv", "parse_dotenv", "parse_env", "strip_comments")


def strip_comments(string: str) -> str:
    """Remove comments from python/shell scripts given the script as a string

    Args:
        string (str): string with `#` comments

    Returns:
        str: input string with comments striped out

    Examples:
        Here is an example of stripping comments from a python-ish script:

        >>> python_script_ish = r'''# some encoding
        ... # this is a comment
        ... # this is another comment
        ... print('hello bob')
        ... print('hello bobert')  # bob is short for bobert
        ... '''
        >>> a = strip_comments(python_script_ish)
        >>> a.splitlines(keepends=False)
        ['', '', '', "print('hello bob')", "print('hello bobert')  "]

        Here is an example of stripping comments from a bash/shell-ish script:

        >>> bash_script_ish = r'''#!/bin/bash
        ... # this is a comment
        ... # this is another comment
        ... echo "hello"
        ... echo "hello again" # comment
        ... '''
        >>> a = strip_comments(bash_script_ish)
        >>> a.splitlines(keepends=False)
        ['', '', '', 'echo "hello"', 'echo "hello again" ']

    """
    filelines = string.splitlines(keepends=False)
    comment_re = re.compile(r'(?:"(?:[^"\\]|\\.)*"|[^"#])*(#|$)')

    def _strip_comments_line(line: str) -> str:
        comment_re_match = comment_re.match(line)
        if comment_re_match:
            return line[: comment_re_match.start(1)]
        return line

    return "\n".join((_strip_comments_line(line) for line in filelines))


def parse_dotenv(string: str) -> Dict[str, str]:
    """Parse env string to dictionary"""
    return {
        key: " ".join(shplit(val))
        for key, _, val in (
            el.partition("=")
            for el in filter(
                None,
                strip_comments(string.replace("\r\n", "\n").strip("\n")).splitlines(
                    keepends=False
                ),
            )
        )
    }


def parse_env(string: str) -> Dict[str, str]:
    """Parse env string to dictionary"""
    return parse_dotenv(string)


def ldotenv(fspath: Optional[FsPath] = None) -> Dict[str, str]:
    """Load a dotenv file from a fspath and return the keyvalues as a dict"""
    if fspath:
        if path.exists(str(fspath)):
            if path.isfile(str(fspath)):
                return {
                    key: " ".join(shplit(val))
                    for key, _, val in (
                        el.partition("=")
                        for el in filter(
                            None,
                            strip_comments(
                                rstring(fspath).replace("\r\n", "\n").strip("\n")
                            ).split("\n"),
                        )
                    )
                }
            if path.isdir(str(fspath)):
                dotenv_filepath = path.join(str(fspath), ".env")
                if path.exists(dotenv_filepath):
                    return ldotenv(dotenv_filepath)
        raise ValueError(f"Given fspath/dirpath does not exist: {str(fspath)}")
    return ldotenv(getcwd())


if __name__ == "__main__":
    from doctest import testmod

    testmod()
