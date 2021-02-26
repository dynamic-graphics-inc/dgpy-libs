# -*- coding: utf-8 -*-
"""Asyncify"""
from asyncify._meta import __version__
from asyncify.core import asyncify, run

from funkify import funkify


funkify(asyncify, name="asyncify")

__all__ = ["__version__", "asyncify", "run"]
