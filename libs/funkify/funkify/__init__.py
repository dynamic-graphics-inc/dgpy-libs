# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
from funkify.core import _funkify, funkify
from funkify._version import VERSION_INFO
from funkify._version import VERSION_MAJOR
from funkify._version import VERSION_MINOR
from funkify._version import VERSION_PATCH
from funkify._version import __version__

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
