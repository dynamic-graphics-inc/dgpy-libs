# -*- coding: utf-8 -*-
import pytest


@pytest.mark.asyncio
async def test_asyncify() -> None:
    from asyncify import asyncify

    @asyncify
    def add(a, b):
        return a + b

    res = await add(1, 5)
    assert res == 6


@pytest.mark.asyncio
async def test_asyncify_funkified() -> None:
    import asyncify

    @asyncify
    def add(a, b):
        return a + b

    res = await add(1, 5)
    assert res == 6


if __name__ == "__main__":
    pass
