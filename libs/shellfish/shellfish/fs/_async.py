# -*- coding: utf-8 -*-
"""async file-system utils"""
from __future__ import annotations

import os

from os import fspath as _fspath
from typing import Any, AsyncIterable, Callable, Optional

from aiopen import aiopen
from jsonbourne import JSON
from shellfish import aios
from xtyping import AsyncIterator, FsPath, Iterable, Union

__all__ = (
    "exists_async",
    "is_dir_async",
    "is_file_async",
    "is_link_async",
    "isdir_async",
    "isfile_async",
    "islink_async",
    "lbytes_async",
    "lbytes_gen_async",
    "lstat_async",
    "lstr_async",
    "lstring_async",
    "rbin_async",
    "rbin_gen_async",
    "rbytes_async",
    "rbytes_gen_async",
    "rstr_async",
    "rstring_async",
    "sbin_async",
    "sbytes_async",
    "sbytes_gen_async",
    "sstr_async",
    "sstring_async",
    "stat_async",
    "wbin_async",
    "wbin_gen_async",
    "wbytes_async",
    "wbytes_gen_async",
    "wstr_async",
    "wstring_async",
    "ljson_async",
    "rjson_async",
    "sjson_async",
    "wjson_async",
)


async def isfile_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await aios.path.isfile(_fspath(fspath))


async def isdir_async(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return await aios.path.isfile(_fspath(fspath))


async def islink_async(fspath: FsPath) -> bool:
    """Return True if the given path is a link; False otherwise"""
    return await aios.path.islink(_fspath(fspath))


async def exists_async(fspath: FsPath) -> bool:
    return await aios.path.exists(_fspath(fspath))


async def stat_async(fspath: FsPath) -> os.stat_result:
    """Async version of `os.lstat`"""
    return await aios.stat(str(fspath))


async def lstat_async(fspath: FsPath) -> os.stat_result:
    """Async version of `os.lstat`"""
    return await aios.lstat(str(fspath))


async def filesize_async(fspath: FsPath) -> int:
    """Return the size of the file at the given fspath"""
    _stat_res = await aios.stat(str(fspath))
    return _stat_res.st_size


is_dir_async = isdir_async
is_file_async = isfile_async
is_link_async = islink_async


# IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO #
async def wbytes_async(
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

    Returns:
        None

    Examples:
        >>> from shellfish.fs._async import rbytes_async, wbytes_async
        >>> from asyncio import run as aiorun
        >>> fspath = "wbytes_async.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> aiorun(wbytes_async(fspath, bites_to_save))
        20
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> aiorun(rbytes_async(fspath))
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    _write_mode = "ab" if append else "wb"
    async with aiopen(filepath, _write_mode) as fd:
        nbytes = await fd.write(bites)
    if chmod is not None:
        await aios.chmod(str(filepath), chmod)
    return int(nbytes)


async def rbytes_async(filepath: FsPath) -> bytes:
    """(ASYNC) Load/Read bytes from a fspath

    Args:
        filepath: fspath read as bytes

    Returns:
        bytes from the fspath

    Examples:
        >>> from shellfish.fs._async import rbytes_async, wbytes_async
        >>> from asyncio import run as aiorun
        >>> fspath = "rbytes_async.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> aiorun(wbytes_async(fspath, bites_to_save))
        20
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> aiorun(rbytes_async(fspath))
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    async with aiopen(filepath, "rb") as file:
        b = await file.read()
    return bytes(b)


async def rbytes_gen_async(
    filepath: FsPath, blocksize: int = 65536
) -> AsyncIterable[Union[bytes, str]]:
    """Yield (asynchronously) bytes from a given fspath

    Args:
        filepath: fspath to read from
        blocksize (int): size of the block to read

    Yields:
        bytes from AsyncIterable[bytes] of the file bytes

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> from shellfish.fs._async import wbytes_gen_async, rbytes_gen_async
        >>> fspath = 'rbytes_gen_async.doctest.txt'
        >>> bites_to_save = (b"These are some bytes... ", b"more bytes!")
        >>> bites_to_save
        (b'These are some bytes... ', b'more bytes!')
        >>> run(wbytes_gen_async(fspath, bites_to_save))
        35
        >>> async def read():
        ...     async for b in rbytes_gen_async(fspath, blocksize=4):
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
        >>> run(wbytes_gen_async(fspath, bites_to_save))
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
        >>> run(wbytes_gen_async(fspath, AsyncIterable()))
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


async def wbytes_gen_async(
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
        >>> from shellfish.fs._async import wbytes_gen_async, rbytes_gen_async
        >>> fspath = 'wbytes_gen_async.doctest.txt'
        >>> bites_to_save = (b"These are some bytes... ", b"more bytes!")
        >>> bites_to_save
        (b'These are some bytes... ', b'more bytes!')
        >>> run(wbytes_gen_async(fspath, bites_to_save))
        35
        >>> async def read():
        ...     async for b in rbytes_gen_async(fspath, blocksize=4):
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
        >>> run(wbytes_gen_async(fspath, bites_to_save))
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
        >>> run(wbytes_gen_async(fspath, AsyncIterable()))
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
    if chmod is not None:
        await aios.chmod(filepath, chmod)
    return _bytes_written


async def rstring_async(filepath: FsPath, encoding: str = "utf-8") -> str:
    r"""(ASYNC) Load/Read a string given a fspath

    Args:
        filepath: Filepath for file to read

    Returns:
        str: String read from given fspath

    """
    return (await rbytes_async(filepath)).decode(encoding=encoding)


async def wstring_async(
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
    return await wbytes_async(
        filepath=filepath,
        bites=string.encode(encoding),
        append=append,
        chmod=chmod,
    )


async def rjson_async(filepath: FsPath) -> Any:
    """Load/Read-&-parse json data given a fspath

    Args:
        filepath: Filepath to load/read data from

    Returns:
        Parsed JSON data

    Examples:
        Imports:

        >>> from asyncio import run
        >>> from shellfish.fs._async import rjson_async, wjson_async

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "rjson_async_dict.doctest.json"
        >>> run(wjson_async(fspath, data))
        19
        >>> run(rjson_async(fspath))
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "rjson_async_list.doctest.json"
        >>> run(wjson_async(fspath, data))
        25
        >>> run(rjson_async(fspath))
        [['a', 1], ['b', 2], ['c', 3]]

        >>> import os; os.remove(fspath)

    """
    json_string = await rbytes_async(filepath)
    return JSON.loads(json_string)


async def wjson_async(
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
        >>> from shellfish.fs._async import rjson_async, wjson_async

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "wjson_async_dict.doctest.json"
        >>> run(wjson_async(fspath, data))
        19
        >>> run(rjson_async(fspath))
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "wjson_async_list.doctest.json"
        >>> run(wjson_async(fspath, data))
        25
        >>> run(rjson_async(fspath))
        [['a', 1], ['b', 2], ['c', 3]]

        >>> import os; os.remove(fspath)

    """
    return await wbytes_async(
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


ljson_async = rjson_async
sjson_async = wjson_async
lbytes_async = rbin_async = rbytes_async
sbytes_async = wbin_async = sbin_async = wbytes_async
lstring_async = rstr_async = lstr_async = rstring_async
sstring_async = wstr_async = sstr_async = wstring_async
lbytes_gen_async = rbin_gen_async = rbytes_gen_async
sbytes_gen_async = wbin_gen_async = wbytes_gen_async

if __name__ == "__main__":
    import doctest

    doctest.testmod()
