# -*- coding: utf-8 -*-
"""`jsonbourne` version"""
__version__ = "0.5.2"
VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH = [int(el) for el in __version__.split('.')]
VERSION_INFO = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

__all__ = [
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
