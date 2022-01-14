# -*- coding: utf-8 -*-
"""Asyncify"""
from asyncify._meta import __version__
from asyncify.core import asyncify, await_or_return, is_async, run

from funkify import funkify

funkify(asyncify, key="asyncify")

__all__ = ("__version__", "asyncify", "run", "await_or_return", "is_async")
