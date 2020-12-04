# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
from funkify._meta import __version__
from funkify.core import _funkify, funkify


_funkify(funkify, name="funkify")

__all__ = [
    "__version__",
    "funkify",
]
