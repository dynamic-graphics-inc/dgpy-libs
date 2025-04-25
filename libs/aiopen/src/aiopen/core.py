# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by aiofiles
"""

from __future__ import annotations

import asyncio

from asyncio import AbstractEventLoop, BaseEventLoop
from functools import partial, singledispatch, wraps
from io import (
    BufferedRandom,
    BufferedReader,
    BufferedWriter,
    FileIO,
    TextIOBase,
    TextIOWrapper,
)
from typing import (
    TYPE_CHECKING,
    Any,
    AnyStr,
    AsyncContextManager,
    Awaitable,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from xtyping import ParamSpec

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from os import PathLike
    from types import TracebackType

P = ParamSpec("P")
T = TypeVar("T")

PathType = Union[str, "PathLike[Any]"]

_open = open
__all__ = ("aiopen",)


def aio_hoist(funk: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    @wraps(funk)
    async def _async_funk(self: Any, *args: P.args, **kwargs: P.kwargs) -> T:
        fn = getattr(self._file, funk.__name__)
        retval = await self._loop.run_in_executor(
            self._executor, partial(fn, *args, **kwargs)
        )
        return cast("T", retval)

    return cast("Callable[P, Awaitable[T]]", _async_funk)


class AsyncBase(Generic[AnyStr]):  # pragma: no cover
    _file: Union[BufferedWriter, TextIOWrapper, FileIO, BufferedRandom, BufferedReader]
    _loop: AbstractEventLoop
    _executor: Optional[BaseEventLoop] = None

    def __init__(
        self,
        file: Union[
            BufferedWriter,
            TextIOWrapper,
            FileIO,
            BufferedRandom,
            BufferedReader,
        ],
        loop: AbstractEventLoop,
        executor: None,
    ) -> None:
        self._file = file
        self._loop = loop
        self._executor = executor

    def __aiter__(self) -> "AsyncBase[AnyStr]":
        return self

    # async def __anext__(self) -> Union[bytes, str]:
    async def __anext__(self) -> AnyStr:
        """Simulate normal file iteration."""
        line = await self.readline()
        if line:
            return cast("AnyStr", line)
        else:
            raise StopAsyncIteration

    @aio_hoist
    def close(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def flush(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def isatty(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def read(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def readall(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def readinto(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def readline(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def readlines(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def seek(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def seekable(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def tell(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def truncate(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def writable(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def write(self, *args: Any, **kwargs: Any) -> Any: ...

    @aio_hoist
    def writelines(self, *args: Any, **kwargs: Any) -> Any: ...

    def fileno(self) -> int:
        return self._file.fileno()

    def readable(self) -> bool:
        return self._file.readable()

    @property
    def closed(self) -> bool:
        return self._file.closed

    def detach(self) -> None:
        # check if self._file is FileIO
        if not isinstance(self._file, FileIO):
            self._file.detach()
        else:
            raise AttributeError("detach() method is not available")

    @aio_hoist
    def peek(self, *args: Any, **kwargs: Any) -> Any:
        if isinstance(self._file, BufferedReader):
            return self._file.peek(*args, **kwargs)
        raise OSError("peek() method is not available")


# TODO: Fix generics...
class AsyncBaseDetachable(AsyncBase):  # type: ignore[type-arg]
    _file: Union[BufferedReader, BufferedRandom, BufferedWriter, TextIOWrapper]

    def detach(self) -> Any:
        return self._file.detach()


class TextIOWrapperAsync(AsyncBase[str]):
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


class BufferedIOAsyncBase(AsyncBaseDetachable):
    """Async version of io.BufferedWriter"""

    _file: Union[BufferedReader, BufferedRandom, BufferedWriter]

    @property
    def raw(self) -> Any:
        return self._file.raw


class BufferedReaderAsync(BufferedIOAsyncBase):
    """The asyncio executor version of io.BufferedReader and Random."""

    @aio_hoist
    def peek(self, *args: Any, **kwargs: Any) -> Any: ...


# TODO: Fix generics...
class FileIOAsync(AsyncBase):  # type: ignore[type-arg]
    """The asyncio executor version of io.FileIO."""

    _file: FileIO


@singledispatch
def _aiopen_dispatch(
    file: Union[
        TextIOBase, BufferedWriter, BufferedReader, BufferedRandom, FileIO, Any
    ],
    *,
    loop: AbstractEventLoop,
    executor: Any = None,
) -> Union[TextIOWrapperAsync, BufferedIOAsyncBase, BufferedReaderAsync, FileIOAsync]:
    raise TypeError(f"Unsupported io type: {file}.")


@_aiopen_dispatch.register(TextIOBase)
def _textio_base_dispatcher(
    file: FileIO, *, loop: AbstractEventLoop, executor: Any = None
) -> TextIOWrapperAsync:
    return TextIOWrapperAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedWriter)
def _buffered_io_base_async_dispatcher(
    file: BufferedWriter, *, loop: AbstractEventLoop, executor: Any = None
) -> BufferedIOAsyncBase:
    return BufferedIOAsyncBase(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(BufferedReader)
@_aiopen_dispatch.register(BufferedRandom)
def _buffered_reader_async_dispatcher(
    file: Union[BufferedReader, BufferedRandom],
    *,
    loop: AbstractEventLoop,
    executor: Any = None,
) -> BufferedReaderAsync:
    return BufferedReaderAsync(file, loop=loop, executor=executor)


@_aiopen_dispatch.register(FileIO)
def _fileio_async_dispatcher(
    file: FileIO, *, loop: AbstractEventLoop, executor: Any = None
) -> FileIOAsync:
    return FileIOAsync(file, loop, executor)


class AiopenContextManager(
    AsyncContextManager[
        Union[
            BufferedIOAsyncBase,
            BufferedReaderAsync,
            TextIOWrapperAsync,
            FileIOAsync,
        ]
    ]
):
    __slots__ = ("_coro", "_obj")

    def __init__(self, coro: Any) -> None:
        self._coro: Coroutine[Any, Any, Any] = coro
        self._obj: Optional[
            Union[
                BufferedIOAsyncBase,
                BufferedReaderAsync,
                TextIOWrapperAsync,
                FileIOAsync,
            ]
        ] = None

    def send(self, value: Any) -> Any:
        return self._coro.send(value)

    def throw(
        self,
        typ: Type[BaseException],
        val: Any = None,
        tb: Optional[TracebackType] = None,
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
        return self._coro.gi_frame  # type: ignore[attr-defined]

    @property
    def gi_running(self) -> bool:
        return self._coro.gi_running  # type: ignore[attr-defined, no-any-return]

    @property
    def gi_code(self) -> Any:
        return self._coro.gi_code  # type: ignore[attr-defined]

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
        BufferedIOAsyncBase,
        BufferedReaderAsync,
        TextIOWrapperAsync,
        FileIOAsync,
    ]:
        self._obj = await self._coro
        if self._obj is None:
            raise ValueError("Unable to aiopen")
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
    loop: Optional[AbstractEventLoop] = None,
    executor: Any = None,
) -> Union[FileIOAsync, BufferedIOAsyncBase, TextIOWrapperAsync, BufferedReaderAsync]:
    """Open an asyncio file."""
    _loop = loop if loop is not None else asyncio.get_event_loop()
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
    loop: Optional[AbstractEventLoop] = None,
    executor: Any = None,
) -> AiopenContextManager:
    """Async version of the `open` builtin

    Examples:
        >>> async def main():
        ...     async with aiopen("test.txt", "w") as f:
        ...         await f.write("test")
        ...     async with aiopen("test.txt", "r") as f:
        ...         assert await f.read() == "test"
        >>> asyncio.run(main())
        >>> import os
        >>> if os.path.exists("test.txt"):
        ...     os.remove("test.txt")

    """
    return AiopenContextManager(
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
