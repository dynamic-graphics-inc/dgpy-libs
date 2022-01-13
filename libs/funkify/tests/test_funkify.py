import asyncio
import sys

from os import path

import pytest

from xtyping import Awaitable, T

PWD = path.split(path.realpath(__file__))[0]


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


def test_funkify_module_sync() -> None:
    from . import sync_fn

    assert sync_fn.main() == 123
    assert sync_fn() == 123


def test_funkify_module_async() -> None:
    from . import async_fn

    res_fn = run(async_fn.main())
    assert res_fn == 123

    res_mod = run(async_fn())
    assert res_fn == 123
    assert res_mod == 123


def test_funkify_no_such_module() -> None:
    with pytest.raises(ValueError):
        from . import no_such_module

        assert no_such_module() == 123


def test_funkify_non_callable_static_export() -> None:
    with pytest.raises(ValueError):
        from . import static_export

        assert static_export() == "default_export"


def test_funkify_non_callable_no_name() -> None:
    with pytest.raises(AttributeError):
        from . import static_export_no_name

        assert static_export_no_name() == "default_export"
