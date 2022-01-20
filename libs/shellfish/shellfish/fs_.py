# -*- coding: utf-8 -*-
"""async file-system utils"""
import os

from os import fspath as _fspath
from typing import AsyncIterable, cast

from typing_extensions import AsyncGenerator, AsyncIterator

from aiopen import aiopen
from asyncify import aios
from xtyping import (
    Any,
    Callable,
    FsPath,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
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


is_dir_async = isdir_async
is_file_async = isfile_async
is_link_async = islink_async

# IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO # IO #
async def wbytes_async(
    filepath: FsPath,
    bites: bytes,
    append: bool = False,
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
        >>> from shellfish.fs_ import rbytes_async, wbytes_async
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
    return nbytes


async def rbytes_async(filepath: FsPath) -> bytes:
    """(ASYNC) Load/Read bytes from a fspath

    Args:
        filepath: fspath read as bytes

    Returns:
        bytes from the fspath

    Examples:
        >>> from shellfish.fs_ import rbytes_async, wbytes_async
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

    Returns:
        AsyncIterable[bytes] of the file bytes

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> from shellfish.fs_ import wbytes_gen_async, rbytes_gen_async
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
    append: bool = False,
) -> int:
    """Write/save bytes to a filepath from an (async)iterable/iterator of bytes

    Args:
        filepath: fspath to write to
        bytes_gen: AsyncIterable/Iterator of bytes to write
        append: Append to the fspath if True; otherwise overwrite

    Returns:
        int: number of bytes written

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> from shellfish.fs_ import wbytes_gen_async, rbytes_gen_async
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
    return _bytes_written


async def rstring_async(filepath: FsPath) -> str:
    r"""(ASYNC) Load/Read a string given a fspath

    Args:
        filepath: Filepath for file to read

    Returns:
        str: String read from given fspath

    """
    return (await rbytes_async(filepath)).decode()


async def wstring_async(
    filepath: FsPath,
    string: str,
    *,
    encoding: str = "utf-8",
    append: bool = False,
) -> int:
    """(ASYNC) Save/Write a string to fspath

    Args:
        filepath: fspath to write to
        string (str): string to be written
        encoding (str): File encoding (Default='utf-8')
        append (bool): Append to the fspath if True; default is False

    Returns:
        int: number of bytes written

    """
    return await wbytes_async(
        filepath=filepath,
        bites=string.encode(encoding),
        append=append,
    )


if __name__ == "__main__":

    import doctest

    doctest.testmod()
