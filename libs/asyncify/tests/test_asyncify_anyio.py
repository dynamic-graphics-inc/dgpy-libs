# -*- coding: utf-8 -*-
from __future__ import annotations

import pytest


@pytest.mark.anyio()
async def test_asyncify() -> None:
    from asyncify._anyio import asyncify

    @asyncify
    def add(a: float, b: float) -> float:
        return a + b

    res = await add(1, 5)
    assert res == 6


@pytest.mark.anyio()
async def test_asyncify_funkified() -> None:
    from asyncify._anyio import asyncify

    @asyncify
    def add(a: float, b: float) -> float:
        return a + b

    res = await add(1, 5)
    assert res == 6
