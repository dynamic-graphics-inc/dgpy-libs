# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio

from os import path
from typing import TYPE_CHECKING, TypeVar

import pytest

if TYPE_CHECKING:
    from collections.abc import Awaitable

PWD = path.split(path.realpath(__file__))[0]

T = TypeVar("T")


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
    return asyncio.run(aw)  # type: ignore[arg-type]


def test_funkify_module_sync() -> None:
    from . import sync_fn

    assert sync_fn.main() == 123
    assert sync_fn() == 123  # type: ignore[operator]


def test_funkify_module_async() -> None:
    from . import async_fn

    res_fn = run(async_fn.main())
    assert res_fn == 123

    res_mod = run(async_fn())  # type: ignore[operator]
    assert res_fn == 123
    assert res_mod == 123


def test_funkify_no_such_module() -> None:
    with pytest.raises(ValueError, match=r"no_such_module not found in sys.modules"):
        exec("from . import no_such_module")


def test_funkify_non_callable_static_export() -> None:
    with pytest.raises(ValueError, match=r"static_export not found in sys.modules"):
        exec("from . import static_export")


def test_funkify_non_callable_no_name() -> None:
    with pytest.raises(AttributeError):
        exec("from . import static_export_no_name")
