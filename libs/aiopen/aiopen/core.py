# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by the pip project aiofiles, but different
"""
import asyncio

from asyncio import BaseEventLoop  # type: ignore
from collections.abc import Coroutine
from functools import partial, singledispatch, wraps
from io import (
    BufferedRandom,
    BufferedReader,
    BufferedWriter,
    FileIO,
    TextIOBase,
    TextIOWrapper,
)
from os import PathLike
from types import TracebackType
from typing import (
    Any,
    AsyncContextManager,
    Awaitable,
    Callable,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)


T = TypeVar("T")

PathType = Union[str, PathLike]

_open = open
__all__ = ["aiopen"]


def aio_hoist(funk: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    @wraps(funk)
    async def _async_funk(self: Any, *args: Any, **kwargs: Any) -> T:
        fn = getattr(self._file, funk.__name__)
        retval = await self._loop.run_in_executor(
            self._executor, partial(fn, *args, **kwargs)
        )
        return cast(T, retval)

    return cast(Callable[..., Awaitable[T]], _async_funk)


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
    def close(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def flush(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def isatty(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def read(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def readall(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def readinto(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def readline(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def readlines(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def seek(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def seekable(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def tell(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def truncate(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def writable(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def write(self, *args: Any, **kwargs: Any) -> Any:
        ...

    @aio_hoist
    def writelines(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def fileno(self) -> int:
        return self._file.fileno()

    def readable(self) -> bool:
        return self._file.readable()

    @property
    def closed(self) -> bool:
        return self._file.closed


class BaseAsyncDetachable(BaseAsync):
    _file: Union[BufferedReader, BufferedRandom, BufferedWriter, TextIOWrapper]

    def detach(self) -> Any:
        return self._file.detach()


class TextIOWrapperAsync(BaseAsyncDetachable):
    """Async version of io.TextIOWrapper"""

    _file: TextIOWrapper

    @property
    def encoding(self) -> str:
        return self._file.encoding

    @property
    def buffer(self) -> Any:
        return self._file.buffer

    @property
    def errors(self) -> Any:
        return self._file.errors

    @property
    def line_buffering(self) -> Any:
        return self._file.line_buffering

    @property
    def newlines(self) -> Any:
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
    def peek(self, *args: Any, **kwargs: Any) -> Any:
        ...


class FileIOAsync(BaseAsync):
    """The asyncio executor version of io.FileIO."""

    _file: FileIO


@singledispatch
def _aiopen_dispatch(
    file: Union[
        TextIOBase, BufferedWriter, BufferedReader, BufferedRandom, FileIO, Any
    ],
    *,
    loop: BaseEventLoop,
    executor: Any = None,
) -> Union[TextIOWrapperAsync, BufferedIOBaseAsync, BufferedReaderAsync, FileIOAsync]:
    raise TypeError("Unsupported io type: {}.".format(file))


@_aiopen_dispatch.register(TextIOBase)
def _textio_base_dispatcher(
    file: FileIO, *, loop: BaseEventLoop, executor: Any = None
) -> TextIOWrapperAsync:
    return TextIOWrapperAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedWriter)
def _buffered_io_base_async_dispatcher(
    file: BufferedWriter, *, loop: BaseEventLoop, executor: Any = None
) -> BufferedIOBaseAsync:
    return BufferedIOBaseAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedReader)
@_aiopen_dispatch.register(BufferedRandom)
def _buffered_reader_async_dispatcher(
    file: Union[BufferedReader, BufferedRandom],
    *,
    loop: BaseEventLoop,
    executor: Any = None,
) -> BufferedReaderAsync:
    return BufferedReaderAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(FileIO)
def _fileio_async_dispatcher(
    file: FileIO, *, loop: BaseEventLoop, executor: Any = None
) -> FileIOAsync:
    return FileIOAsync(file, loop, executor)


class ContextManagerAsync(
    AsyncContextManager[
        Union[
            BufferedIOBaseAsync,
            BufferedReaderAsync,
            TextIOWrapperAsync,
            FileIOAsync,
            None,
        ]
    ]
):
    __slots__ = ("_coro", "_obj")

    def __init__(self, coro: Any) -> None:
        self._coro: Coroutine[Any, Any, Any] = coro
        self._obj: Optional[
            Union[
                BufferedIOBaseAsync,
                BufferedReaderAsync,
                TextIOWrapperAsync,
                FileIOAsync,
            ]
        ] = None

    def send(self, value: Any) -> Any:
        return self._coro.send(value)

    def throw(
        self, typ: Any, val: Any = None, tb: Optional[TracebackType] = None
    ) -> Any:
        if val is None:
            return self._coro.throw(typ)
        elif tb is None:
            return self._coro.throw(typ, val)
        else:
            return self._coro.throw(typ, val, tb)

    def close(self) -> Any:
        return self._coro.close()

    @property
    def gi_frame(self) -> Any:
        return self._coro.gi_frame  # type: ignore

    @property
    def gi_running(self) -> bool:
        return self._coro.gi_running  # type: ignore

    @property
    def gi_code(self) -> Any:
        return self._coro.gi_code  # type: ignore

    def __next__(self) -> Any:
        return self.send(None)

    def __iter__(self) -> Any:
        resp = yield self._coro
        return resp

    async def __aiter__(self) -> Any:
        resp = await self._coro
        return resp

    def __await__(self) -> Any:
        return self._coro.__await__()

    async def __anext__(self) -> Any:
        resp = await self._coro
        return resp

    async def __aenter__(
        self,
    ) -> Union[
        BufferedIOBaseAsync, BufferedReaderAsync, TextIOWrapperAsync, FileIOAsync, None
    ]:
        self._obj = await self._coro
        return self._obj

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        if self._obj:
            await self._obj.close()
        self._obj = None


async def _aiopen(
    file: PathType,
    mode: str = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: None = None,
    *,
    loop: Optional[BaseEventLoop] = None,
    executor: Any = None,
) -> Union[FileIOAsync, BufferedIOBaseAsync, TextIOWrapperAsync, BufferedReaderAsync]:
    """Open an asyncio file."""
    if loop is None:
        _loop = asyncio.get_event_loop()
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
    f = await _loop.run_in_executor(executor, cb)
    return _aiopen_dispatch(f, loop=_loop, executor=executor)


def aiopen(
    file: PathType,
    mode: str = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: None = None,
    *,
    loop: Optional[BaseEventLoop] = None,
    executor: Any = None,
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
