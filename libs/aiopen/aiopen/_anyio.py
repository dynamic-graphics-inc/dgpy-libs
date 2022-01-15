# -*- coding: utf-8 -*-
"""Async io base functions and utilities

Inspired by aiofiles
"""

from types import TracebackType
from typing import AnyStr, Awaitable, Callable, Type, Union, overload

from anyio._core._fileio import AsyncFile, PathLike, open_file
from xtyping import Generic, OpenBinaryMode, OpenTextMode, Optional


class AsyncFileCtx(Generic[AnyStr]):
    obj: Optional[AsyncFile[AnyStr]] = None
    __slots__ = ("_coro", "_obj")

    def __init__(self, coro: Awaitable[AsyncFile[AnyStr]]):
        self._coro = coro
        self._obj = None

    async def __aenter__(self) -> AsyncFile[AnyStr]:
        _obj = await self._coro
        self._obj = _obj
        return _obj

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._obj.__aexit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)


@overload
def aiopen(
    file: Union[str, PathLike, int],
    mode: OpenBinaryMode = ...,
    buffering: int = ...,
    encoding: Optional[str] = ...,
    errors: Optional[str] = ...,
    newline: Optional[str] = ...,
    closefd: bool = ...,
    opener: Optional[Callable[[str, int], int]] = ...,
) -> AsyncFileCtx[bytes]:
    ...


@overload
def aiopen(
    file: Union[str, PathLike, int],
    mode: OpenTextMode = ...,
    buffering: int = ...,
    encoding: Optional[str] = ...,
    errors: Optional[str] = ...,
    newline: Optional[str] = ...,
    closefd: bool = ...,
    opener: Optional[Callable[[str, int], int]] = ...,
) -> AsyncFileCtx[str]:
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
) -> AsyncFileCtx[AnyStr]:
    return AsyncFileCtx(
        coro=open_file(
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
