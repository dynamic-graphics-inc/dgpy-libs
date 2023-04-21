# -*- coding: utf-8 -*-
"""Package metadata/info"""
import warnings

from funkify.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "funkify._meta is deprecated, use funkify.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__title__", "__description__", "__pkgroot__", "__version__")
