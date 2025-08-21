# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by aiofiles
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    AnyStr,
    Generic,
    cast,
    overload,
)

from anyio import AsyncFile, open_file

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from os import PathLike
    from types import TracebackType

    from _typeshed import OpenBinaryMode, OpenTextMode, ReadableBuffer, WriteableBuffer
else:
    ReadableBuffer = OpenBinaryMode = OpenTextMode = WriteableBuffer = object


class AsyncFileContextManager(Generic[AnyStr]):
    __slots__ = ("_coro", "_obj")
    _coro: Awaitable[AsyncFile[AnyStr]]
    _obj: AsyncFile[AnyStr] | None

    def __init__(self, coro: Awaitable[AsyncFile[AnyStr]]) -> None:
        self._coro = coro
        self._obj = None

    @property
    def obj(self) -> AsyncFile[AnyStr]:
        if self._obj is not None:
            return self._obj
        raise RuntimeError("AsyncFileContextManager not initialized")

    async def init_async(self) -> AsyncFile[AnyStr]:
        if self._obj is None:
            _obj = await self._coro
            self._obj = _obj
            return _obj
        return self._obj

    async def __aenter__(self) -> AsyncFile[AnyStr]:
        _obj = await self.init_async()
        return _obj

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        obj = self.obj
        await obj.__aexit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)


@overload
def aiopen(
    file: str | PathLike[str] | int,
    mode: OpenBinaryMode = ...,
    *,
    buffering: int = ...,
    encoding: str | None = ...,
    errors: str | None = ...,
    newline: str | None = ...,
    closefd: bool = ...,
    opener: Callable[[str, int], int] | None = ...,
) -> AsyncFileContextManager[bytes]: ...


@overload
def aiopen(
    file: str | PathLike[str] | int,
    mode: OpenTextMode = ...,
    *,
    buffering: int = ...,
    encoding: str | None = ...,
    errors: str | None = ...,
    newline: str | None = ...,
    closefd: bool = ...,
    opener: Callable[[str, int], int] | None = ...,
) -> AsyncFileContextManager[str]: ...


def aiopen(
    file: str | PathLike[str] | int,
    mode: str | OpenBinaryMode | OpenTextMode = "r",
    *,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener: Callable[[str, int], int] | None = None,
) -> AsyncFileContextManager[Any]:
    return AsyncFileContextManager(
        coro=open_file(
            file=file,
            mode=cast("OpenBinaryMode | OpenTextMode", mode),  # pyright: ignore[reportGeneralTypeIssues]
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        )
    )
