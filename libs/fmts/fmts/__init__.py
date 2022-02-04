# -*- coding: utf-8 -*-
"""String utils"""
import re
from functools import lru_cache

from binascii import hexlify
from datetime import datetime, timedelta, timezone
from difflib import unified_diff
from functools import wraps
from os import path, stat, urandom
from random import choice
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, printable
from textwrap import indent as _indent
from typing import (
    Any,
    AnyStr,
    Callable,
    Dict,
    ItemsView,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from fmts._meta import __version__

# END IMPORTS

_R = TypeVar("_R")

# characters strings
CAMEL_CHARACTERS: str = ascii_letters + digits + "_"  # also works for pascal case
KEBAB_CHARACTERS: str = ascii_lowercase + digits + "-"
SNAKE_CHARACTERS: str = ascii_lowercase + digits + "_"

# regular expressions
FIRST_CAP_RE = re.compile("(.)([A-Z][a-z]+)")
ALL_CAP_RE = re.compile("([a-z0-9])([A-Z])")


def anystr2anystr(fn: Callable[[str], str]) -> Callable[[AnyStr], AnyStr]:
    """Convert a str-to-str function to allow for `AnyStr`

    Args:
        fn: function to convert

    Returns:
        Callable[[AnyStr], AnyStr]: function that accepts any string type

    """

    @wraps(fn)
    def _anystr2anystr(string: AnyStr) -> AnyStr:
        if isinstance(string, bytes):
            return fn(string.decode()).encode()
        return fn(string)

    return _anystr2anystr


def anystr(fn: Callable[[str], _R]) -> Callable[[AnyStr], _R]:
    """Convert a given function to accept any string type

    Args:
        fn: function to convert

    Returns:
        Callable[[AnyStr], R]: function that accepts one arg that is a string

    """

    @wraps(fn)
    def _anystr(string: AnyStr) -> _R:
        if isinstance(string, bytes):
            return fn(string.decode())
        return fn(string)

    return _anystr


@anystr2anystr
def dos2unix(string: str) -> str:
    r"""Replace CRLF line endings with LF line endings for a given string

    Examples:
        >>> dos2unix('hello\r\nworld')
        'hello\nworld'
        >>> type(b'hello\r\nworld')
        <class 'bytes'>
        >>> dos2unix(b'hello\r\nworld')
        b'hello\nworld'
        >>> type(dos2unix(b'hello\r\nworld'))
        <class 'bytes'>

    """
    return string.replace("\r\n", "\n")


def bytes2str(bites: bytes, encoding: str = "utf-8") -> str:
    """Convert bytes to a string

    Args:
        bites: bytes to convert to string
        encoding (str): encoding as a string; defaults to 'utf-8'

    Returns:
        str: The bytes as a string

    """
    return bites.decode(encoding)


@lru_cache(maxsize=1)
def camel_characters_set() -> Set[str]:
    """Return a set of all the characters that are allowed in camel case

    Examples:
        >>> CAMEL_CHARACTERS
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        >>> camel_characters_set() == {c for c in CAMEL_CHARACTERS}
        True

    """
    return set(CAMEL_CHARACTERS)


@lru_cache(maxsize=1)
def kebab_characters_set() -> Set[str]:
    """Return a set of all the characters that are allowed in camel case

    Examples:
        >>> KEBAB_CHARACTERS
        'abcdefghijklmnopqrstuvwxyz0123456789-'
        >>> kebab_characters_set() == {c for c in KEBAB_CHARACTERS}
        True

    """
    return set(KEBAB_CHARACTERS)


@lru_cache(maxsize=1)
def printable_characters_set() -> Set[str]:
    return set(printable)


@lru_cache(maxsize=1)
def snake_characters_set() -> Set[str]:
    return set(SNAKE_CHARACTERS)


@anystr
def is_snake(string: AnyStr) -> bool:
    """Check if a given string is snake_case

    Args:
        string: string to check

    Returns:
        >>> is_snake('snake_case')
        True
        >>> is_snake('kebab-case')
        False
        >>> is_snake(b'snake_case')
        True
        >>> is_snake(b'kebab-case')
        False

    """
    if isinstance(string, bytes):
        return is_snake(string.decode())
    return all(c in snake_characters_set() for c in set(string))


def snake2kebab(string: AnyStr) -> AnyStr:
    """Convert a given snake_case string to kebab-case

    Args:
        string: snake case string

    Returns:
        >>> snake2kebab('kebab_case')
        'kebab-case'
        >>> snake2kebab(b'kebab_case')
        b'kebab-case'

    """
    if isinstance(string, bytes):
        return string.replace(b"_", b"-")
    return string.replace("_", "-")


def kebab2snake(string: AnyStr) -> AnyStr:
    """Convert a given kebab-case string to snake_case

    Args:
        string: kebab case string

    Returns:
        >>> kebab2snake('kebab-case')
        'kebab_case'
        >>> kebab2snake(b'kebab-case')
        b'kebab_case'

    """
    if isinstance(string, bytes):
        return string.replace(b"-", b"_")
    return string.replace("-", "_")


@anystr2anystr
def camel2snake(string: str) -> str:
    """Convert a 'camelCase' string to a 'snake_case' string

    Args:
        string (str): a camelCase string

    Returns:
        snake_case string

    Examples:
        >>> camel2snake('camelCase')
        'camel_case'
        >>> camel2snake(b'camelCase')
        b'camel_case'
        >>> camel2snake('PascalCase')
        'pascal_case'

    """
    return ALL_CAP_RE.sub(r"\1_\2", FIRST_CAP_RE.sub(r"\1_\2", string)).lower()


@anystr2anystr
def pascal2camel(string: str) -> str:
    """Convert a 'PascalCase' string to a 'camelCase' string

    Args:
        string (str): a PascalCase string

    Returns:
        camelCase string

    Examples:
        >>> pascal2camel('PascalCase')
        'pascalCase'
        >>> pascal2camel(b'PascalCase')
        b'pascalCase'

    """
    return string[0].lower() + string[1:]


def snake2pascal(string: AnyStr) -> AnyStr:
    """Convert a given snake_case string to PascalCase

    Args:
        string: snake case string

    Returns:
        PascalCase string

    Examples:
        >>> snake2pascal('pascal_case')
        'PascalCase'
        >>> snake2pascal(b'pascal_case')
        b'PascalCase'

    """
    if isinstance(string, bytes):
        return b"".join(x.capitalize() for x in string.split(b"_"))
    return "".join(x.title() for x in string.split("_"))


@anystr2anystr
def _snake2camel(string: str) -> str:
    return f"{string[0].lower()}{snake2pascal(string)[1:]}"


def snake2camel(string: AnyStr) -> AnyStr:
    """Convert a given snake_case string to camelCase

    Args:
        string: snake case string

    Returns:
        >>> snake2camel('camel_case')
        'camelCase'
        >>> snake2camel(b'camel_case')
        b'camelCase'

    """
    return _snake2camel(string)


def ensure_trailing_newline(string: AnyStr) -> AnyStr:
    """Return a string that has only one trailing new line"""
    if isinstance(string, bytes):
        return string.rstrip(b"\n") + b"\n"
    return "{}\n".format(string.strip("\n"))


def nbytes_str(nbytes: Union[int, float]) -> str:
    """Format nbytesber of bytes to human readable form

    Args:
        nbytes: number of bytes

    Returns:
        str: nbytesber of bytes formatted

    Raises:
        ValueError: If given nbytesber of bytes is invalid/negative

    Examples:
        >>> nbytes_str(100)
        '100.0 bytes'
        >>> nbytes_str(1000)
        '1000.0 bytes'
        >>> nbytes_str(10000)
        '9.8 KB'
        >>> nbytes_str(100000)
        '97.7 KB'
        >>> nbytes_str(1000000)
        '976.6 KB'
        >>> nbytes_str(10_000_000)
        '9.5 MB'
        >>> nbytes_str(100_000_000)
        '95.4 MB'
        >>> nbytes_str(1000000000)
        '953.7 MB'
        >>> nbytes_str(10000000000)
        '9.3 GB'
        >>> nbytes_str(100000000000)
        '93.1 GB'
        >>> nbytes_str(1000000000000)
        '931.3 GB'
        >>> nbytes_str(10000000000000)
        '9.1 TB'
        >>> nbytes_str(100000000000000)
        '90.9 TB'

    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if nbytes < 1024.0 or x == "TB":
            _str = f"{nbytes:3.1f} {x}"
            return _str
        nbytes /= 1024.0
    raise ValueError(f"Invalid nbytesber of bytes: {nbytes}")


def filesize_str(filepath: str) -> str:
    """Get the human readable filesize string for a file given its path

    Args:
        filepath (str): path to file

    Returns:
        str: Size of the file

    Raises:
        FileNotFoundError: If the given fspath does not exist

    Examples:
        >>> fspath = "filesize_str.doctest.txt"
        >>> with open(fspath, "w") as f:
        ...     f.write("dummy file with some stuff")
        26
        >>> filesize_str(fspath)
        '26.0 bytes'
        >>> from os import remove; remove(fspath)

    """
    if path.isfile(filepath):
        file_info = stat(filepath)
        return nbytes_str(file_info.st_size)
    raise FileNotFoundError(filepath)


def nseconds(nsec: float) -> str:
    """Format a number of seconds as a human readable string

    Formats nsec if t2 is None as a string; Calculates the time and formats
    the time t2-nsec if t2 is not None.

    Args:
        nsec (float): Timestamp epoch seconds

    Returns:
        str: Formatted time duration string readable by humans

    Examples:
        Less than or equal to one second
        >>> for i in range(0, 10, 2):
        ...     (10**-i, nseconds(10**(-i)))
        ...
        (1, '1.000 sec')
        (0.01, '10.000 ms')
        (0.0001, '100.000 μs')
        (1e-06, '1.000 μs')
        (1e-08, '10.000 ns')

        Greater than or equal to one second
        >>> for i in range(0, 5):
        ...     (f"{10**i} seconds", nseconds(10**i))
        ...
        ('1 seconds', '1.000 sec')
        ('10 seconds', '10.000 sec')
        ('100 seconds', '01:40 (mm:ss)')
        ('1000 seconds', '16:40 (mm:ss)')
        ('10000 seconds', '02:46:40 (hh:mm:ss)')

    """
    if nsec == 0.0:
        return "0 sec"
    elif 0.000001 > nsec >= 0.000000001:
        return f"{(10 ** 9) * nsec:.3f} ns"
    elif 0.001 > nsec >= 0.000001:
        return f"{(10 ** 6) * nsec:.3f} μs"
    elif 1 > nsec >= 0.001:
        return f"{(10 ** 3) * nsec:.3f} ms"
    elif nsec < 60:
        return f"{nsec:.3f} sec"
    elif 3600 > nsec >= 60:
        minutes = nsec // 60
        nsec %= 60
        return f"{minutes:02d}:{nsec:02d} (mm:ss)"
    else:
        hours = nsec // (60 * 60)
        nsec %= 60 * 60
        minutes = nsec // 60
        nsec %= 60
        return f"{hours:02d}:{minutes:02d}:{nsec:02d} (hh:mm:ss)"


def dseconds(ti: Union[float, int], tf: Union[float, int]) -> str:
    """Format time duration given initial and final timestamps in seconds

    Args:
        ti: Initial time in seconds
        tf: Final time in seconds

    Returns:
        str: Formatted time duration string readable by humans

    Examples:
        Less than or equal to one second

        >>> for i in range(0, 10, 2):
        ...     (10**-i, dseconds(0, 10**(-i)))
        ...
        (1, '1.000 sec')
        (0.01, '10.000 ms')
        (0.0001, '100.000 μs')
        (1e-06, '1.000 μs')
        (1e-08, '10.000 ns')

        Greater than or equal to one second

        >>> for i in range(0, 5):
        ...     (f"{10**i} seconds", dseconds(0, 10**i))
        ...
        ('1 seconds', '1.000 sec')
        ('10 seconds', '10.000 sec')
        ('100 seconds', '01:40 (mm:ss)')
        ('1000 seconds', '16:40 (mm:ss)')
        ('10000 seconds', '02:46:40 (hh:mm:ss)')

    """
    return nseconds(abs(tf - ti))


def binstr(number: int) -> str:
    """Convert an integer to a binary string

    Args:
        number (int): Number to convert

    Returns:
        str: binary string for the given number

    Examples:
        >>> binstr(200)
        '11001000'
        >>> binstr(10)
        '1010'

    """
    return bin(number)[2:]


@anystr2anystr
def strip_ascii(string: str) -> str:
    """Remove all ascii characters from a string

    Args:
        string (str): string with non-ascii characters

    Returns:
        string of only the non-ascii characters

    Examples:
        >>> string_w_non_ascii_chars = 'Three fourths: ¾'
        >>> strip_ascii(string_w_non_ascii_chars)
        '¾'

    """
    return "".join(filter(lambda x: ord(x) > 128, string))


@anystr2anystr
def strip_non_ascii(s: str) -> str:
    """Remove all ascii characters from a string

    Args:
        s (str): string with non-ascii characters

    Returns:
        string of only the non-ascii characters

    Examples:
        >>> string_w_non_ascii_chars = 'Three fourths: ¾'
        >>> strip_non_ascii(string_w_non_ascii_chars)
        'Three fourths: '

    """
    return "".join(filter(lambda x: ord(x) <= 128, s))


def randhexstr(length: int = 4) -> str:
    """Return a random hex string

    Args:
        length (int): length of desired random string (defaults to 4)

    Returns:
        str: random hex string

    Examples:
        >>> a = randhexstr()
        >>> isinstance(a, str)
        True
        >>> len(a) == 8
        True

    """
    return bytes2str(hexlify(urandom(length)))


def random_string(length: int = 4, hex: bool = False) -> str:
    """Return a random ascii string (length=str_len; default=4)"""
    if hex:
        return randhexstr(length)
    letters = ascii_lowercase + ascii_uppercase
    return "".join(choice(letters) for _ in range(length))


@anystr2anystr
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
    r = re.compile(r'(?:"(?:[^"\\]|\\.)*"|[^"#])*(#|$)')

    def _strip_comments_line(line: str) -> str:
        try:
            return line[: r.match(line).start(1)]  # type: ignore
        except AttributeError:
            return line

    return "\n".join((_strip_comments_line(line) for line in filelines))  # type: ignore


def multi_replace(
    string: str,
    replacements: Union[
        List[Tuple[str, str]], List[List[str]], Dict[str, str], ItemsView[str, str]
    ],
) -> str:
    """Replace multiple patterns in a string

    Args:
        string: Strint to apply
        replacements: Replacement combos

    Returns:
        str: Input string with all the replacements applied in order

    Examples:
        Works with a list of lists!

        >>> replacements = [['hello', 'goodbye'], ['world', 'earth']]
        >>> multi_replace('hello, world', replacements)
        'goodbye, earth'

        Works with a list of tuples!

        >>> replacements = [('hello', 'goodbye'), ('world', 'earth')]
        >>> multi_replace('hello, world', replacements)
        'goodbye, earth'

        Works with a dictionary where all keys and values are strings!

        >>> replacements = {'hello': 'goodbye', 'world': 'earth'}
        >>> multi_replace('hello, world', replacements)
        'goodbye, earth'

    """
    if isinstance(replacements, dict):
        return multi_replace(string, replacements.items())
    for rep in replacements:
        string = string.replace(*rep)
    return string


def rm_character(string: str, split_str: str, join_str: str) -> str:
    """Remove a character in a string globally

    Args:
        string: string to remove characters from
        split_str: character to remove
        join_str: character to join the split-string on

    Returns:
        String with the character/string given by split_str removed

    """
    return join_str.join(el for el in string.split(split_str) if el != "")


def rm_whitespace(string: str, join_str: str = " ") -> str:
    """Replace n>=2 spaces with a single underscore

    Args:
        join_str (str): String to join on; defaults to a space (' ')
        string: String to remove spaces from

    Returns:
        String with no spaces and underscores where there were spaces

    Examples:
        >>> rm_whitespace('there are lots of    spaces')
        'there are lots of spaces'
        >>> rm_whitespace('there are lots of    spaces', join_str='_')
        'there_are_lots_of_spaces'

    """
    return rm_character(string, split_str=" ", join_str=join_str)


@anystr2anystr
def rm_dunderscore(string: str) -> str:
    """Replace n>=2 underscores with a single underscore

    Args:
        string: String to remove double underscores from

    Returns:
        String with no adjacent underscores

    Examples:
        >>> rm_dunderscore('there____are___many____double_______underscores')
        'there_are_many_double_underscores'

    """
    return rm_character(string=string, split_str="_", join_str="_")


@anystr2anystr
def rm_b(string: str) -> str:
    """Remove the b'' from binary strings and sub-strings that contain b''

    Taken from 'pupy' (Pretty Useful Python (which jesse wrote))

    Args:
        string (str): A string surrounded by b'' or a sub-string with b''

    Returns:
        str: A string without binary b'' quotes surround it

    Examples:
        >>> rm_b("b'a_string'")
        'a_string'

    """
    return re.sub("b'([^']*)'", r"\1", string)


@anystr2anystr
def rm_u(string: str) -> str:
    """Remove the u'' from unicode strings and sub-strings that contain u''

    Args:
        string (str): A string surrounded by u'' or a sub-string with u''

    Returns:
        str:A string without unicode u'' quotes surround it

    Examples:
        >>> a = "u'a_string'"
        >>> rm_u(a)
        'a_string'

    """
    return re.sub("u'([^']*)'", r"\1", string)


@anystr2anystr
def overscore_carrots(string: str) -> str:
    r"""Add underscores on a line above a string and carrots on a line below

    Args:
        string: Input string to overscore and carrot

    Returns:
        'Over-scored' and carroted string

    Examples:
        >>> overscore_carrots("A TITLE")
        '_______\nA TITLE\n^^^^^^^'
        >>> print(overscore_carrots("A TITLE"))
        _______
        A TITLE
        ^^^^^^^

    """
    _n = longest_line(string)
    return "\n".join(["_" * _n, string, "^" * _n])


def truncate_string(
    string: str, maxlines: int = 120, max_characters: int = 4096
) -> str:
    """Truncate a string at either a max number of lines or characters

    Args:
        string: String to truncate
        maxlines: Max number of lines the truncated string can have; default is 120
        max_characters: Max number of characters the string can have; default is 4096

    Returns:
        Truncated string

    """
    string_lines = string.replace("\r\n", "\n").split("\n")
    if len(string_lines) > maxlines:
        string_lines = string_lines[:maxlines]
        line_lengths = [len(line) for line in string_lines]
        total_characters = sum(line_lengths)
        if total_characters < max_characters:
            string_lines.extend(
                [
                    "_____________________________",
                    f"... Truncated @ {maxlines} lines... ",
                    "-----------------------------",
                ]
            )
            string_lines.append(
                overscore_carrots(f"... Truncated @ {maxlines} lines... ")
            )
            truncated_string = "\n".join(string_lines)
        else:
            truncated_string = "\n".join(string_lines)[:4096]
            trunc_str = overscore_carrots(
                f"... Truncated @ {max_characters} characters ..."
            )
            truncated_string += trunc_str
    else:
        truncated_string = "\n".join(string_lines)

    while "\n\n" in truncated_string:
        truncated_string = truncated_string.replace("\n\n", "\n")
    return truncated_string


def udiff(
    a_lines: Sequence[str],
    b_lines: Sequence[str],
    fromfile: str = "A",
    tofile: str = "B",
    n: int = 0,
    maxlines: int = 120,
    max_characters: int = 4096,
) -> str:
    """Return universal-diff as a string

    Args:
        a_lines: First set of lines as strings
        b_lines: Second set of lines as strings
        fromfile: Name or label of the first file/lines (Default = 'A')
        tofile: Name or label of the second file/lines (Default = 'B')
        n: Number of context lines to give in diff (Default = 0)
        maxlines: Number of diff lines to truncate at (Default = 120)
        max_characters: Number of characters to truncate at (Default = 4096)

    Returns:
        universal diff string that is truncated if too long

    """
    diff_string = "\n".join(
        filter(
            lambda string: string != "",
            unified_diff(
                a=a_lines,
                b=b_lines,
                fromfile=fromfile,
                tofile=tofile,
                n=n,  # number of context lines
            ),
        )
    )
    if maxlines <= 0 and max_characters <= 0:
        return diff_string
    return truncate_string(
        diff_string, maxlines=maxlines, max_characters=max_characters
    )


def striterable(string: str) -> Iterable[str]:
    r"""Yield 'clean' sub-strings from an input string

    This method takes a string (like the string that would be a dat file) and
    yields strings from that string separated by some delimeter.

    Delimeters:
        - <space>
        - <tab>
        - <new-line> (unix AND dos!)

    Args:
        string (str): string to be turned into a striterable

    Returns:
        Filter/generator of 'clean' strings for comparison

    Examples:
        Simple spaces example:

        >>> string_w_spaces = 'this is a string with spaces'
        >>> list(striterable(string_w_spaces))
        ['this', 'is', 'a', 'string', 'with', 'spaces']

        Leading and trailing spaces example:

        >>> string_w_spaces = '     this is a string with spaces     '
        >>> list(striterable(string_w_spaces))
        ['this', 'is', 'a', 'string', 'with', 'spaces']

        Tabs example:

        >>> strings = ['string', 'separated', 'by', 'tabs']
        >>> tab_separated = '\t'.join(strings)
        >>> list(striterable(tab_separated))
        ['string', 'separated', 'by', 'tabs']

    """
    string = string.replace("\r\n", " ")  # handle DOS line endings
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    return (s.lower() for s in filter(lambda s: s != "", string.split(" ")))


# =====================================
# Aliases (for backwards compatibility)
# =====================================
camel_to_snake = camel2snake
snake_to_pascal = snake2pascal
snake_to_camel = snake2camel
snake_to_kebab = snake2kebab

randstr = random_string
rhex_str = randhexstr


def string_sanitize(string: str) -> str:
    """Clean up a string

    Args:
        string (str): String to sanitize

    Returns:
        input string sanitized

    Examples:
        >>> string_sanitize('5/9999((5')
        '599995'
        >>> string_sanitize('question????,')
        'question'

    """
    return strip_non_ascii(re.sub(r"[()\"/;:<>{}`=~|!?,]", "", string).strip("."))


def longest_line(string: str) -> int:
    """Return the length of the longest line in a string

    Args:
        string (str): String that has either one or more lines

    Returns:
        int: The length of the longest line in the string

    """
    if "\n" in string:
        return max(len(line) for line in string.splitlines(keepends=False))
    return len(string)


def rm_multilines(string: str) -> str:
    """Remove blank lines from a string

    Args:
        string: string possibly containing blank lines

    Returns:
        string without blank lines

    """
    return "\n".join(
        (ll.rstrip() for ll in string.replace("\r\n", "\n").split("\n") if ll.strip())
    )


def ensure_utf8(string: AnyStr) -> str:
    """Return a string that ensured to be utf-8.

    This is often needed for those rare cases where some weird non-unicode
    character or escape sequence is present within a string; This method
    protects against the possibility of a UnicodeDecodeError.

    Args:
        string: A string which you/one would like the unicode version of

    Returns:
        The unicode-encoded version of a string

    """
    if isinstance(string, bytes):
        try:
            return str(string, encoding="utf-8")
        except UnicodeDecodeError:
            return str(string, encoding="latin2")
        except TypeError:
            pass
    return str(string)


def body_contents(html_string: str) -> List[str]:
    """Parse the innertext for body tags in an html string

    Args:
        html_string (str): html to parse

    Returns:
        str: the inner text for the body tags

    """
    return re.findall("<body>(.*?)</body>", html_string, re.DOTALL)


class pstr(str):
    """Pretty-string subclass"""

    def __new__(cls, content: str) -> "pstr":
        """Create and return new pstr from a str"""
        if "\n" in content and (content[0] == "\n" or content[-1] == "\n"):
            return str.__new__(cls, content.strip("\n"))  # type: ignore
        return str.__new__(cls, content)  # type: ignore

    def _repr_parts(self) -> str:
        string = f'"""{self}"""' if "\n" in self else f"'{self}'"
        if self.__class__.__name__ != "pstr":
            string = f"{str(self.__class__.__name__)}({string})"
        return string

    def _repr_pretty_(self, p: Any, cycle: Any = False) -> None:
        p.text(self._repr_parts())


def indent(
    string: AnyStr,
    prefix: str = "    ",
    predicate: Optional[Callable[[str], bool]] = None,
) -> AnyStr:
    r"""Indent a string a given number of spaces

    Args:
        string: string to indent
        prefix: prefix to use for indentation; defaults to 4 spaces
        predicate: Optional predicate to determine whether to indent a line;

    Returns:
        Indented string

    Examples:
        >>> s = "this is a string"
        >>> indent(s)
        '    this is a string'
        >>> s = "this is a\nmultiline string"
        >>> indent(s)
        '    this is a\n    multiline string'
        >>> print(indent(s))
            this is a
            multiline string
        >>> s = "this is a\nmultiline string"
        >>> print(indent(s, '  '))
          this is a
          multiline string

    """
    if isinstance(string, bytes):
        return indent(string.decode("utf-8"), prefix, predicate).encode("utf-8")
    return _indent(string, prefix, predicate)


@anystr2anystr
def dedent(string: str) -> str:
    r"""Dedent a string

    Args:
        string: Input string to dedent

    Returns:
        Dedented string

    Examples:
        >>> s = '    this is a string'
        >>> dedent(s)
        'this is a string'
        >>> s = '        this is a string'
        >>> dedent(s)
        '    this is a string'
        >>> s = "    this is a string\n    with 2 lines"
        >>> print(dedent(s))
        this is a string
        with 2 lines

    """
    return "\n".join(
        s if not s.startswith("    ") else s[4:] for s in string.split("\n")
    )


def timestamp(ts: Optional[Union[float, datetime]] = None) -> str:
    """Time stamp string w/ format yyyymmdd-HHMMSS

    Args:
        ts: datetime or float

    Returns:
        timestamp string

    Examples:
        >>> from datetime import datetime
        >>> stamps = ['20190225-161151', '20190225-081151']
        >>> timestamp(1551111111.111111) in stamps
        True
        >>> datetime.now().strftime("%Y%m%d-%H%M%S") == timestamp()
        True
        >>> timestamp(datetime.now()) == timestamp()
        True

    """
    if isinstance(ts, float):
        return datetime.fromtimestamp(ts).strftime("%Y%m%d-%H%M%S")
    if isinstance(ts, datetime):
        return ts.strftime("%Y%m%d-%H%M%S")
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def long_timestamp_string(timestamp_sec: float) -> str:
    """Return a 'long-form' timestamp string given epoch-seconds float"""
    return datetime.fromtimestamp(
        timestamp_sec, tz=timezone(timedelta(hours=-8))
    ).strftime("%A, %d. %B %Y %I:%M%p")


class HTML:
    """HTML formatting utils staticmethod container"""

    @staticmethod
    def html_tag(tag_str: str, string: str = "") -> str:
        """Return an HTML tag with a string as the innerHTML"""
        return f"<{tag_str}>{string}</{tag_str}>"

    @staticmethod
    def th(string: str) -> str:
        """Return an string surrounded with 'th-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.th("string")
            '<th>string</th>'

        """
        return HTML.html_tag("th", string)

    @staticmethod
    def td(string: str) -> str:
        """Return an string surrounded with 'td-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.td("string")
            '<td>string</td>'

        """
        return HTML.html_tag("td", string)

    @staticmethod
    def tr(string: str) -> str:
        """Return an string surrounded with 'tr-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.tr("string")
            '<tr>string</tr>'

        """
        return HTML.html_tag("tr", string)

    @staticmethod
    def thead(string: str) -> str:
        """Return an string surrounded with 'thead-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.thead("string")
            '<thead>string</thead>'

        """
        return HTML.html_tag("thead", string)

    @staticmethod
    def tablehead(string: str) -> str:
        """Return an string surrounded with 'thead-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.tablehead("string")
            '<thead>string</thead>'

        """
        return HTML.html_tag("thead", string)

    @staticmethod
    def tbody(string: str) -> str:
        """Return an string surrounded with 'tbody-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.tbody("string")
            '<tbody>string</tbody>'

        """
        return HTML.html_tag("tbody", string)

    @staticmethod
    def tablebody(string: str) -> str:
        """Return an string surrounded with 'tbody-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.tablebody("string")
            '<tbody>string</tbody>'

        """
        return HTML.html_tag("tbody", string)

    @staticmethod
    def table(string: str) -> str:
        """Return an string surrounded with 'table-HTML' tags

        Args:
            string: Input string

        Returns:
            Formatted string

        Examples:
            >>> HTML.table("string")
            '<table>string</table>'

        """
        return HTML.html_tag("table", string)


@anystr2anystr
def carrots(string: str) -> str:
    r"""Add carrots on a line below given a string

    Args:
        string: Input string to under-carrot

    Returns:
        'carrot-ed-scored' string

    Examples:
        >>> carrots("A TITLE")
        'A TITLE\n^^^^^^^'
        >>> print(carrots("A TITLE"))
        A TITLE
        ^^^^^^^

    """
    return "\n".join([string, "^" * longest_line(string)])


@anystr2anystr
def overscore(string: str) -> str:
    r"""Add underscores on a line above the given string

    Args:
        string: Input string to overscore

    Returns:
        'Over-scored' string

    Examples:
        >>> overscore("A TITLE")
        '_______\nA TITLE'
        >>> print(overscore("A TITLE"))
        _______
        A TITLE

    """
    return "\n".join(["_" * longest_line(string), string])


def b64_html_img(b64_string: Union[str, bytes], img_format: str) -> str:
    """Return an img tag given a base64-jpeg-image-string"""
    try:
        if isinstance(b64_string, bytes):
            b64_string = b64_string.decode("utf-8")
    except UnicodeDecodeError as ude:
        raise ValueError(
            "bytes given instead of string;\n"
            "tried to decode but got UnicodeDecodeError:\n{}".format(str(ude))
        )
    return f'<img src="data:image/{img_format};base64,{b64_string}">'


def b64_html_png(b64_string: str) -> str:
    """Return a HTML base64 png image tag

    Args:
        b64_string (str): Base64 image string

    Returns:
        str: base64 html image tag

    Examples:
        >>> b64_html_png("BASE64_STRING")
        '<img src="data:image/png;base64,BASE64_STRING">'

    """
    return b64_html_img(b64_string, "png")


def b64_html_jpg(b64_string: str) -> str:
    """Return a HTML base64 jpg image tag

    Args:
        b64_string (str): Base64 jpg image string

    Returns:
        str: base64 html jpg image tag

    Examples:
        >>> b64_html_jpg("BASE64_STRING")
        '<img src="data:image/jpg;base64,BASE64_STRING">'

    """
    return b64_html_img(b64_string, "jpg")


def b64_html_gif(b64_string: str) -> str:
    """Return a HTML base64 gif image tag

    Args:
        b64_string (str): Base64 gif image string

    Returns:
        str: base64 html image tag

    Examples:
        >>> b64_html_gif("BASE64_STRING")
        '<img src="data:image/gif;base64,BASE64_STRING">'

    """
    return b64_html_img(b64_string, "gif")


def base64_jpg_html(b64_string: Union[str, bytes]) -> str:
    """Return an img tag given a base64-jpeg-image-string"""
    try:
        if isinstance(b64_string, bytes):
            b64_string = b64_string.decode("utf-8")
    except UnicodeDecodeError as ude:
        raise ValueError(
            "bytes given instead of string;\n"
            "tried to decode but got UnicodeDecodeError:\n{}".format(str(ude))
        )
    return f'<img src="data:image/jpeg;base64,{str(b64_string)}">'


def enum_strings(strings: List[str]) -> Iterable[str]:
    """Return a generator with enumerated strings"""
    _count = len(str(len(strings)))
    return (f"{str(ix).zfill(_count)}) {s}" for ix, s in enumerate(strings, start=1))


def space_pad_strings(strings: List[str]) -> List[str]:
    """Space pads strings to match the string with the max length"""
    _max_len = max(len(s) for s in strings)
    return [s.ljust(_max_len) for s in strings]


__all__ = (
    "ALL_CAP_RE",
    "CAMEL_CHARACTERS",
    "FIRST_CAP_RE",
    "HTML",
    "KEBAB_CHARACTERS",
    "SNAKE_CHARACTERS",
    "anystr",
    "anystr2anystr",
    "b64_html_gif",
    "b64_html_img",
    "b64_html_jpg",
    "b64_html_png",
    "base64_jpg_html",
    "binstr",
    "body_contents",
    "bytes2str",
    "camel2snake",
    "camel_characters_set",
    "camel_to_snake",
    "carrots",
    "dedent",
    "dos2unix",
    "dseconds",
    "ensure_trailing_newline",
    "ensure_utf8",
    "enum_strings",
    "filesize_str",
    "indent",
    "is_snake",
    "kebab2snake",
    "kebab_characters_set",
    "long_timestamp_string",
    "longest_line",
    "multi_replace",
    "nbytes_str",
    "nseconds",
    "overscore",
    "overscore_carrots",
    "pascal2camel",
    "printable_characters_set",
    "pstr",
    "randhexstr",
    "random_string",
    "randstr",
    "rhex_str",
    "rm_b",
    "rm_character",
    "rm_dunderscore",
    "rm_multilines",
    "rm_u",
    "rm_whitespace",
    "snake2camel",
    "snake2kebab",
    "snake2pascal",
    "snake_characters_set",
    "snake_to_camel",
    "snake_to_kebab",
    "snake_to_pascal",
    "space_pad_strings",
    "string_sanitize",
    "strip_ascii",
    "strip_comments",
    "strip_non_ascii",
    "striterable",
    "timestamp",
    "truncate_string",
    "udiff",
)
