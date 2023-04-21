# -*- coding: utf-8 -*-
"""Package metadata/info"""
import warnings

from asyncify.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "asyncify._meta is deprecated, use asyncify.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__title__", "__description__", "__pkgroot__", "__version__")
