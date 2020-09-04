# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
from funkify._version import (
    VERSION_INFO,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    __version__,
)
from funkify.core import _funkify, funkify


_funkify(funkify, name="funkify")

__all__ = [
    "funkify",
    # Version et al
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
