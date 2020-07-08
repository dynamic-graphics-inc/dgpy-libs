# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by the pip project aiofiles, but different
"""
import asyncio
from asyncio import BaseEventLoop  # type: ignore
from collections.abc import Coroutine
from functools import partial
from functools import singledispatch
from functools import wraps
from io import BufferedRandom
from io import BufferedReader
from io import BufferedWriter
from io import FileIO
from io import TextIOBase
from io import TextIOWrapper
from os import PathLike
from typing import Any
from typing import Optional
from typing import Union

import funkify


PathType = Union[str, PathLike]

_open = open
__all__ = ["aiopen"]


def aio_hoist(funk):
    @wraps(funk)
    async def _async_funk(self, *args, **kwargs):
        fn = getattr(self._file, funk.__name__)
        return await self._loop.run_in_executor(
            self._executor, partial(fn, *args, **kwargs)
        )

    return _async_funk


class BaseAsync:
    _file: Union[BufferedWriter, TextIOWrapper, FileIO, BufferedRandom, BufferedReader]
    _loop: BaseEventLoop
    _executor: Optional[BaseEventLoop] = None

    def __init__(
        self,
        file: Union[
            BufferedWriter, TextIOWrapper, FileIO, BufferedRandom, BufferedReader
        ],
        loop: BaseEventLoop,
        executor: None,
    ) -> None:
        self._file = file
        self._loop = loop
        self._executor = executor

    def __aiter__(self) -> "BaseAsync":
        return self

    async def __anext__(self) -> Union[bytes, str]:
        """Simulate normal file iteration."""
        line = await self.readline()  # type: ignore
        if line:
            return line  # type: ignore
        else:
            raise StopAsyncIteration

    @aio_hoist
    def close(self, *args, **kwargs):
        ...

    @aio_hoist
    def flush(self, *args, **kwargs):
        ...

    @aio_hoist
    def isatty(self, *args, **kwargs):
        ...

    @aio_hoist
    def read(self, *args, **kwargs):
        ...

    @aio_hoist
    def readall(self, *args, **kwargs):
        ...

    @aio_hoist
    def readinto(self, *args, **kwargs):
        ...

    @aio_hoist
    def readline(self, *args, **kwargs):
        ...

    @aio_hoist
    def readlines(self, *args, **kwargs):
        ...

    @aio_hoist
    def seek(self, *args, **kwargs):
        ...

    @aio_hoist
    def seekable(self, *args, **kwargs):
        ...

    @aio_hoist
    def tell(self, *args, **kwargs):
        ...

    @aio_hoist
    def truncate(self, *args, **kwargs):
        ...

    @aio_hoist
    def writable(self, *args, **kwargs):
        ...

    @aio_hoist
    def write(self, *args, **kwargs):
        ...

    @aio_hoist
    def writelines(self, *args, **kwargs):
        ...

    def fileno(self):
        return self._file.fileno()

    def readable(self) -> bool:
        return self._file.readable()

    @property
    def closed(self):
        return self._file.closed


class BaseAsyncDetachable(BaseAsync):
    _file: Union[BufferedReader, BufferedRandom, BufferedWriter, TextIOWrapper]

    def detach(self):
        return self._file.detach()


# def _hoist_method(attr_name):
#     def method(self, *args, **kwargs):
#         return getattr(self._file, attr_name)(*args, **kwargs)
#
#
#     return method
#
#
# def hoist_method(*attrs):
#     def _mk_methods(cls):
#         for attr_name in attrs:
#             setattr(cls, attr_name, _hoist_method(attr_name))
#         return cls
#
#
#     return _mk_methods
#
#
# def _hoist_property(attr_name: "str") -> property:
#     def proxy_property(self):
#         return getattr(self._file, attr_name)
#
#
#     return property(proxy_property)
#
#
# def hoist_property(*attrs):
#     def cls_builder(cls):
#         for attr_name in attrs:
#             setattr(cls, attr_name, _hoist_property(attr_name))
#         return cls
#
#
#     return cls_builder


class TextIOWrapperAsync(BaseAsyncDetachable):
    """Async version of io.TextIOWrapper"""

    _file: TextIOWrapper

    @property
    def encoding(self):
        return self._file.encoding

    @property
    def buffer(self):
        return self._file.buffer

    @property
    def errors(self):
        return self._file.errors

    @property
    def line_buffering(self):
        return self._file.line_buffering

    @property
    def newlines(self):
        return self._file.newlines


class BufferedIOBaseAsync(BaseAsyncDetachable):
    """Async version of io.BufferedWriter"""

    _file: Union[BufferedReader, BufferedRandom, BufferedWriter]

    @property
    def raw(self) -> Any:
        return self._file.raw


class BufferedReaderAsync(BufferedIOBaseAsync):
    """The asyncio executor version of io.BufferedReader and Random."""

    @aio_hoist
    def peek(self, *args, **kwargs):
        ...


class FileIOAsync(BaseAsync):
    """The asyncio executor version of io.FileIO."""

    _file: FileIO


@singledispatch
def _aiopen_dispatch(
    file, *, loop=None, executor=None
) -> Union[TextIOWrapperAsync, BufferedIOBaseAsync, BufferedReaderAsync, FileIOAsync]:
    raise TypeError("Unsupported io type: {}.".format(file))


@_aiopen_dispatch.register(TextIOBase)
def _textio_base_dispatcher(
    file: FileIO, *, loop=None, executor=None
) -> TextIOWrapperAsync:
    return TextIOWrapperAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedWriter)
def _buffered_io_base_async_dispatcher(
    file, *, loop=None, executor=None
) -> BufferedIOBaseAsync:
    return BufferedIOBaseAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedReader)
@_aiopen_dispatch.register(BufferedRandom)
def _buffered_reader_async_dispatcher(
    file, *, loop=None, executor=None
) -> BufferedReaderAsync:
    return BufferedReaderAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(FileIO)
def _fileio_async_dispatcher(file, *, loop=None, executor=None) -> FileIOAsync:
    return FileIOAsync(file, loop, executor)


class ContextManagerAsync(Coroutine):
    __slots__ = ("_coro", "_obj")

    def __init__(self, coro) -> None:
        self._coro: Coroutine = coro
        self._obj: Optional[
            Union[
                BufferedIOBaseAsync,
                BufferedReaderAsync,
                TextIOWrapperAsync,
                FileIOAsync,
            ]
        ] = None

    def send(self, value):
        return self._coro.send(value)

    def throw(self, typ, val=None, tb=None):
        if val is None:
            return self._coro.throw(typ)
        elif tb is None:
            return self._coro.throw(typ, val)
        else:
            return self._coro.throw(typ, val, tb)

    def close(self):
        return self._coro.close()

    @property
    def gi_frame(self):
        return self._coro.gi_frame

    @property
    def gi_running(self):
        return self._coro.gi_running

    @property
    def gi_code(self):
        return self._coro.gi_code

    def __next__(self):
        return self.send(None)

    def __iter__(self):
        resp = yield from self._coro
        return resp

    async def __aiter__(self):
        resp = await self._coro
        return resp

    def __await__(self):
        return self._coro.__await__()

    async def __anext__(self):
        resp = await self._coro
        return resp

    # Union[BufferedIOBaseAsync, BufferedReaderAsync, TextIOWrapperAsync, FileIOAsync, None]
    async def __aenter__(
        self,
    ) -> Union[
        BufferedIOBaseAsync, BufferedReaderAsync, TextIOWrapperAsync, FileIOAsync, None
    ]:
        self._obj = await self._coro
        return self._obj

    async def __aexit__(self, exc_type: None, exc: None, tb: None) -> None:
        if self._obj:
            await self._obj.close()
        self._obj = None


# def _asyncify_method(attr_name):
#     async def _async_funk(self, *args, **kwargs):
#         return await self._loop.run_in_executor(
#             self._executor, partial(getattr(self._file, attr_name), *args, **kwargs)
#             )
#
#
#     return _async_funk
#
#
# def asyncify_method(*attrs):
#     def cls_builder(cls):
#         for attr_name in attrs:
#             setattr(cls, attr_name, _asyncify_method(attr_name))
#         return cls
#
#
#     return cls_builder


async def _aiopen(
    file: PathType,
    mode: str = "r",
    buffering: int = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: None = None,
    *,
    loop=None,
    executor=None,
) -> Union[FileIOAsync, BufferedIOBaseAsync, TextIOWrapperAsync, BufferedReaderAsync]:
    """Open an asyncio file."""
    if loop is None:
        loop = asyncio.get_event_loop()
    cb = partial(
        _open,
        str(file),
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
    )
    f = await loop.run_in_executor(executor, cb)
    return _aiopen_dispatch(f, loop=loop, executor=executor)


def aiopen(
    file: PathType,
    mode: str = "r",
    buffering: int = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: None = None,
    *,
    loop=None,
    executor=None,
) -> ContextManagerAsync:
    """Async version of the `open` builtin"""
    return ContextManagerAsync(
        _aiopen(
            str(file),
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
            loop=loop,
            executor=executor,
        )
    )
