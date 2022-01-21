# -*- coding: utf-8 -*-
"""Asyncify"""
from asyncify._meta import __version__
from asyncify.core import (
    ANYIO,
    aiterable,
    anyio_asyncify,
    anyio_run,
    asyncify,
    await_or_return,
    is_async,
    run,
)
from funkify import funkify

funkify(asyncify, key="asyncify")

__all__ = (
    "ANYIO",
    "__version__",
    "aiterable",
    "anyio_asyncify",
    "anyio_run",
    "asyncify",
    "await_or_return",
    "is_async",
    "run",
)
