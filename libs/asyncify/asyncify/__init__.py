# -*- coding: utf-8 -*-
"""Asyncify"""
from asyncify.__about__ import __version__
from asyncify.core import (
    ANYIO,
    aiorun,
    aiorun_anyio,
    aiorun_asyncio,
    aiterable,
    anyio_asyncify,
    anyio_run,
    asyncify,
    await_or_return,
    is_async,
    run,
)
from funkify import funkify

funkify(asyncify, key="asyncify")  # type: ignore[arg-type]

__all__ = (
    "ANYIO",
    "__version__",
    "aiterable",
    "aiorun",
    "aiorun_anyio",
    "aiorun_asyncio",
    "anyio_asyncify",
    "anyio_run",
    "asyncify",
    "await_or_return",
    "is_async",
    "run",
)
