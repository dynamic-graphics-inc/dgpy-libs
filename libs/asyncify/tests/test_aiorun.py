from __future__ import annotations

import pytest

from asyncify import aiorun, aiorun_anyio, aiorun_asyncio


async def add_async(x: int, y: int) -> int:
    return x + y


def test_aiorun_anyio() -> None:
    assert aiorun_anyio(add_async, 1, 2) == 3
    assert aiorun_anyio(add_async(1, 3)) == 4
    with pytest.raises(ValueError):
        assert aiorun_anyio(add_async(1, 3), 1, 2)


def test_aiorun_asyncio() -> None:
    assert aiorun_asyncio(add_async, 1, 2) == 3
    assert aiorun_asyncio(add_async(1, 3)) == 4
    with pytest.raises(ValueError):
        assert aiorun_asyncio(add_async(1, 3), 1, 2)


def test_aiorun() -> None:
    assert aiorun(add_async, 1, 2) == 3
    assert aiorun(add_async(1, 3)) == 4
    with pytest.raises(ValueError):
        assert aiorun(add_async(1, 3), 1, 2)
