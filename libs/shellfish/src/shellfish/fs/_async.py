# -*- coding: utf-8 -*-
"""async file-system utils"""

from __future__ import annotations

import os

from collections.abc import AsyncIterable, AsyncIterator, Iterable
from os import fspath as _fspath
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from aiopen import aiopen
from jsonbourne import JSON
from shellfish import aios
from shellfish._internal import deprecated_alias

if TYPE_CHECKING:
    from shellfish._types import FsPath

__all__ = (
    "dir_exists_async",
    "exists_async",
    "file_exists_async",
    "filesize_async",
    "is_dir_async",
    "is_file_async",
    "is_link_async",
    "isdir_async",
    "isfile_async",
    "islink_async",
    "lbytes_async",
    "lbytes_gen_async",
    "listdir_async",
    "ljson_async",
    "lstat_async",
    "lstr_async",
    "lstring_async",
    "mkdir_async",
    "mkdirp_async",
    "rbin_async",
    "rbin_gen_async",
    "rbytes_async",
    "rbytes_gen_async",
    "read_bytes_async",
    "read_bytes_gen_async",
    "read_json_async",
    "read_str_async",
    "rjson_async",
    "rstr_async",
    "rstring_async",
    "sbin_async",
    "sbytes_async",
    "sbytes_gen_async",
    "sjson_async",
    "sstr_async",
    "sstring_async",
    "stat_async",
    "wbin_async",
    "wbin_gen_async",
    "wbytes_async",
    "wbytes_gen_async",
    "wjson_async",
    "write_bytes_async",
    "write_bytes_gen_async",
    "write_json_async",
    "write_str_async",
    "wstr_async",
    "wstring_async",
)


async def isfile_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await aios.path.isfile(_fspath(fspath))


async def is_file_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await isfile_async(fspath)


async def isdir_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await aios.path.isdir(_fspath(fspath))


async def is_dir_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await isdir_async(fspath)


async def islink_async(fspath: FsPath) -> bool:
    """Return True if the given path is a link; False otherwise"""
    return await aios.path.islink(_fspath(fspath))


async def is_link_async(fspath: FsPath) -> bool:
    """Return True if the given path is a link; False otherwise"""
    return await islink_async(fspath)


async def exists_async(fspath: FsPath) -> bool:
    return await aios.path.exists(_fspath(fspath))


async def stat_async(fspath: FsPath) -> os.stat_result:
    """Async version of `os.lstat`"""
    return await aios.stat(str(fspath))


async def lstat_async(fspath: FsPath) -> os.stat_result:
    """Async version of `os.lstat`"""
    return await aios.lstat(str(fspath))


async def filesize_async(fspath: FsPath) -> int:
    """Return the size of the file at the given fspath

    Examples:
        >>> from asyncio import run as aiorun
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tmpdir:
        ...     tmpdir = Path(tmpdir)
        ...     fpath = tmpdir / "test.txt"
        ...     written = fpath.write_text("hello world")
        ...     aiorun(filesize_async(fpath))
        11

    """
    _stat_res = await aios.stat(str(fspath))
    return _stat_res.st_size


async def file_exists_async(fspath: FsPath) -> bool:
    """Return True if the file exists; False otherwise"""
    return await aios.path.isfile(_fspath(fspath))


async def dir_exists_async(fspath: FsPath) -> bool:
    """Return True if the directory exists; False otherwise"""
    return await aios.path.isdir(_fspath(fspath))


async def listdir_async(fspath: FsPath) -> list[str]:
    """Async version of `os.listdir`"""
    return await aios.listdir(_fspath(fspath))


async def mkdir_async(
    fspath: FsPath, *, parents: bool = False, p: bool = False, exist_ok: bool = False
) -> None:
    """Make directory at given fspath (async)

    Args:
        fspath (FsPath): Directory path to create
        parents (bool): Make parent dirs if True; do not make parent dirs if False
        p (bool): Make parent dirs if True; do not make parent dirs if False (alias of parents)
        exist_ok (bool): Throw error if directory exists and exist_ok is False

    Returns:
         None

    """
    _parents = parents or p
    if _parents or exist_ok:
        return await aios.makedirs(_fspath(fspath), exist_ok=_parents or exist_ok)
    return await aios.mkdir(_fspath(fspath))


async def mkdirp_async(fspath: FsPath) -> None:
    """Make directory and parents (async)"""
    return await aios.makedirs(_fspath(fspath), exist_ok=True)


# IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO #
async def write_bytes_async(
    filepath: FsPath,
    bites: bytes,
    *,
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """(ASYNC) Write/Save bytes to a fspath

    The parameter 'bites' is used instead of 'bytes' so as to not redefine
    the built-in python bytes object.

    Args:
        append (bool): Append to the fspath if True; otherwise overwrite
        filepath: fspath to write to
        bites: Bytes to be written
        chmod: chmod the fspath to this mode after writing

    Returns:
        None

    Examples:
        >>> from shellfish.fs._async import read_bytes_async, write_bytes_async
        >>> from asyncio import run as aiorun
        >>> fspath = "wbytes_async.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> aiorun(write_bytes_async(fspath, bites_to_save))
        20
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> aiorun(read_bytes_async(fspath))
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    _write_mode = "ab" if append else "wb"
    async with aiopen(filepath, _write_mode) as fd:
        nbytes = await fd.write(bites)
    if chmod is not None:
        await aios.chmod(str(filepath), chmod)
    return int(nbytes)


async def read_bytes_async(filepath: FsPath) -> bytes:
    """(ASYNC) Load/Read bytes from a fspath

    Args:
        filepath: fspath read as bytes

    Returns:
        bytes from the fspath

    Examples:
        >>> from shellfish.fs._async import read_bytes_async, write_bytes_async
        >>> from asyncio import run as aiorun
        >>> fspath = "rbytes_async.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> aiorun(write_bytes_async(fspath, bites_to_save))
        20
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> aiorun(read_bytes_async(fspath))
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    async with aiopen(filepath, "rb") as file:
        b = await file.read()
    return bytes(b)


async def read_bytes_gen_async(
    filepath: FsPath, blocksize: int = 65536
) -> AsyncIterable[bytes]:
    """Yield (asynchronously) bytes from a given fspath

    Args:
        filepath: fspath to read from
        blocksize (int): size of the block to read

    Yields:
        bytes from AsyncIterable[bytes] of the file bytes

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> from shellfish.fs._async import write_bytes_gen_async, read_bytes_gen_async
        >>> fspath = 'rbytes_gen_async.doctest.txt'
        >>> bites_to_save = (b"These are some bytes... ", b"more bytes!")
        >>> bites_to_save
        (b'These are some bytes... ', b'more bytes!')
        >>> run(write_bytes_gen_async(fspath, bites_to_save))
        35
        >>> async def read():
        ...     async for b in read_bytes_gen_async(fspath, blocksize=4):
        ...         print(b)
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)
        >>> async def async_gen():
        ...     for b in bites_to_save:
        ...        yield b
        >>> run(write_bytes_gen_async(fspath, bites_to_save))
        35
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)
        >>> class AsyncIterable:
        ...     def __aiter__(self):
        ...         return async_gen()
        >>> run(write_bytes_gen_async(fspath, AsyncIterable()))
        35
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)

    """
    async with aiopen(filepath, "rb") as f:
        while True:
            data = await f.read(blocksize)
            if not data:
                break
            yield data


async def write_bytes_gen_async(
    filepath: FsPath,
    bytes_gen: Union[Iterable[bytes], AsyncIterable[bytes]],
    *,
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """Write/save bytes to a filepath from an (async)iterable/iterator of bytes

    Args:
        filepath: fspath to write to
        bytes_gen: AsyncIterable/Iterator of bytes to write
        append: Append to the fspath if True; otherwise overwrite
        chmod: chmod the fspath if not None

    Returns:
        int: number of bytes written

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> from shellfish.fs._async import write_bytes_gen_async, read_bytes_gen_async
        >>> fspath = 'wbytes_gen_async.doctest.txt'
        >>> bites_to_save = (b"These are some bytes... ", b"more bytes!")
        >>> bites_to_save
        (b'These are some bytes... ', b'more bytes!')
        >>> run(write_bytes_gen_async(fspath, bites_to_save))
        35
        >>> async def read():
        ...     async for b in read_bytes_gen_async(fspath, blocksize=4):
        ...         print(b)
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)
        >>> async def async_gen():
        ...     for b in bites_to_save:
        ...        yield b
        >>> run(write_bytes_gen_async(fspath, bites_to_save))
        35
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)
        >>> class AsyncIterable:
        ...     def __aiter__(self):
        ...         return async_gen()
        >>> run(write_bytes_gen_async(fspath, AsyncIterable()))
        35
        >>> run(read())
        b'Thes'
        b'e ar'
        b'e so'
        b'me b'
        b'ytes'
        b'... '
        b'more'
        b' byt'
        b'es!'
        >>> remove(fspath)


    """
    _bytes_written = 0
    async with aiopen(filepath, "ab" if append else "wb") as f:
        if isinstance(bytes_gen, AsyncIterator):
            async for b in bytes_gen:
                _bytes_written += await f.write(b)
        elif isinstance(bytes_gen, AsyncIterable):
            async for b in bytes_gen.__aiter__():
                _bytes_written += await f.write(b)
        else:
            for b in bytes_gen:
                _bytes_written += await f.write(b)
    if chmod is not None:  # pragma: nocov
        await aios.chmod(filepath, chmod)
    return _bytes_written


async def read_str_async(filepath: FsPath, encoding: str = "utf-8") -> str:
    r"""(ASYNC) Load/Read a string given a fspath

    Args:
        filepath: Filepath for file to read
        encoding (str): File encoding (Default='utf-8')

    Returns:
        str: String read from given fspath

    """
    return (await read_bytes_async(filepath)).decode(encoding=encoding)


async def write_str_async(
    filepath: FsPath,
    string: str,
    *,
    encoding: str = "utf-8",
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """(ASYNC) Save/Write a string to fspath

    Args:
        filepath: fspath to write to
        string (str): string to be written
        encoding (str): File encoding (Default='utf-8')
        append (bool): Append to the fspath if True; default is False
        chmod (Optional[int]): chmod the fspath if not None

    Returns:
        int: number of bytes written

    """
    return await write_bytes_async(
        filepath=filepath,
        bites=string.encode(encoding),
        append=append,
        chmod=chmod,
    )


async def read_json_async(filepath: FsPath) -> Any:
    """Load/Read-&-parse json data given a fspath

    Args:
        filepath: Filepath to load/read data from

    Returns:
        Parsed JSON data

    Examples:
        Imports:

        >>> from asyncio import run
        >>> from shellfish.fs._async import read_json_async, write_json_async

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "rjson_async_dict.doctest.json"
        >>> run(write_json_async(fspath, data))
        19
        >>> run(read_json_async(fspath))
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "rjson_async_list.doctest.json"
        >>> run(write_json_async(fspath, data))
        25
        >>> run(read_json_async(fspath))
        [['a', 1], ['b', 2], ['c', 3]]

        >>> import os; os.remove(fspath)

    """
    json_string = await read_bytes_async(filepath)
    return JSON.loads(json_string)


async def write_json_async(
    filepath: FsPath,
    data: Any,
    *,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    append: bool = False,
    chmod: Optional[int] = None,
    **kwargs: Any,
) -> int:
    """Save/Write json-serial-ize-able data to a fspath

    Args:
        filepath: fspath to write to
        data (Any): json-serial-ize-able data
        fmt (bool): Indented (2 spaces) or minify data (default=False)
        pretty (bool): Indented (2 spaces) or minify data (default=False)
        sort_keys (bool): Sort the data keys if the data is a dictionary.
        append_newline (bool): Sort the data keys if the data is a dictionary.
        default: default function hook
        append (bool): Append to the fspath if True; default is False
        chmod (Optional[int]): chmod the fspath if not None
        **kwargs: Additional keyword arguments to pass to jsonbourne.JSON.dump

    Returns:
        int: Number of bytes written

    Examples:
        Imports:

        >>> from asyncio import run
        >>> from shellfish.fs._async import read_json_async, write_json_async

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "wjson_async_dict.doctest.json"
        >>> run(write_json_async(fspath, data))
        19
        >>> run(read_json_async(fspath))
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "wjson_async_list.doctest.json"
        >>> run(write_json_async(fspath, data))
        25
        >>> run(read_json_async(fspath))
        [['a', 1], ['b', 2], ['c', 3]]

        >>> import os; os.remove(fspath)

    """
    return await write_bytes_async(
        filepath=filepath,
        bites=JSON.dumpb(
            data=data,
            fmt=fmt,
            pretty=pretty,
            append_newline=append_newline,
            default=default,
            sort_keys=sort_keys,
            **kwargs,
        ),
        append=append,
        chmod=chmod,
    )


ljson_async = rjson_async = deprecated_alias(read_json_async)
sjson_async = wjson_async = deprecated_alias(write_json_async)
lbytes_async = rbin_async = rbytes_async = deprecated_alias(read_bytes_async)
sbytes_async = wbin_async = sbin_async = wbytes_async = deprecated_alias(
    write_bytes_async
)
lstring_async = rstr_async = lstr_async = rstring_async = deprecated_alias(
    read_str_async
)
sstring_async = wstr_async = sstr_async = wstring_async = deprecated_alias(
    write_str_async
)
lbytes_gen_async = rbin_gen_async = rbytes_gen_async = deprecated_alias(
    read_bytes_gen_async
)
sbytes_gen_async = wbin_gen_async = wbytes_gen_async = deprecated_alias(
    write_bytes_gen_async
)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
