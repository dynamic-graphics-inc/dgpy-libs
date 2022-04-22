# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by aiofiles
"""
from __future__ import annotations

from types import TracebackType
from typing import AnyStr, Awaitable, Callable, Type, Union, overload

from anyio._core._fileio import (  # type: ignore[attr-defined]
    AsyncFile,
    PathLike,
    open_file,
)

from xtyping import Generic, OpenBinaryMode, OpenTextMode, Optional


class AsyncFileContextManager(Generic[AnyStr]):
    __slots__ = ("_coro", "_obj")
    _coro: Awaitable[AsyncFile[AnyStr]]
    _obj: Optional[AsyncFile[AnyStr]]

    def __init__(self, coro: Awaitable[AsyncFile[AnyStr]]):
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
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        obj = self.obj
        await obj.__aexit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)


@overload
def aiopen(  # type: ignore[misc]
    file: Union[str, PathLike[str], int],
    mode: OpenBinaryMode = ...,
    buffering: int = ...,
    encoding: Optional[str] = ...,
    errors: Optional[str] = ...,
    newline: Optional[str] = ...,
    closefd: bool = ...,
    opener: Optional[Callable[[str, int], int]] = ...,
) -> AsyncFileContextManager[bytes]:
    ...


@overload
def aiopen(
    file: Union[str, PathLike[str], int],
    mode: OpenTextMode = ...,
    buffering: int = ...,
    encoding: Optional[str] = ...,
    errors: Optional[str] = ...,
    newline: Optional[str] = ...,
    closefd: bool = ...,
    opener: Optional[Callable[[str, int], int]] = ...,
) -> AsyncFileContextManager[str]:
    ...


def aiopen(
    file: Union[str, PathLike, int],
    mode: str = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    closefd: bool = True,
    opener: Optional[Callable[[str, int], int]] = None,
) -> AsyncFileContextManager[AnyStr]:
    return AsyncFileContextManager(
        coro=open_file(  # type: ignore[call-overload, misc]
            file=file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        )
    )
