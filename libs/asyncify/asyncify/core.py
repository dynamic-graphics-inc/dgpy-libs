# -*- coding: utf-8 -*-
"""Asyncify core"""

import asyncio
import sys

from asyncio import AbstractEventLoop, get_event_loop
from functools import partial, wraps
from typing import Any, Awaitable, Callable, Optional, TypeVar, cast


AnyCallable = Callable[..., Any]
FuncType = Callable[..., Any]

T = TypeVar("T")
__all__ = ['asyncify', 'run']


def asyncify(funk: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    """Makes a sync function async

    Args:
        funk: Function to make into an async coroutine

    Returns:
        An asynchronous function

    Examples:
        >>> from asyncify import asyncify
        >>> def add(a, b):
        ...     return a + b
        >>> add(1, 5)
        6
        >>> @asyncify
        ... def add_async(a, b):
        ...     return a + b
        >>> from asyncio import run
        >>> run(add_async(1, 5))
        6

    """

    @wraps(funk)
    async def _async_funk(
        *args: Any,
        loop: Optional[AbstractEventLoop] = None,
        executor: Optional[Any] = None,
        **kwargs: Any,
    ) -> T:
        """Async wrapper function

        Args:
            *args: args to pass
            loop: Event loop in which to run/execute
            executor: Executor to with which to execute
            **kwargs: keyword arguments to be passed to the wrapped function

        Returns:
            An asynchronous coroutine

        """
        loop = loop if loop else get_event_loop()
        pfunc: Callable[..., T] = partial(funk, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return cast(Callable[..., Awaitable[T]], _async_funk)


def run(aw: Awaitable[T]) -> T:
    """Run an async/awaitable function (Polyfill asyncio.run)

    Emulate `asyncio.run()` for snakes below python 3.7; `asyncio.run` was
    added in python3.7.

    Returns:
        Return the result of running the async function

    Examples:
        >>> async def add(a, b):
        ...     return a + b
        ...
        >>> from asyncify.core import run as aiorun
        >>> aiorun(add(1, 4))
        5

    """
    if sys.version_info >= (3, 7):
        return asyncio.run(aw)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(aw)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
