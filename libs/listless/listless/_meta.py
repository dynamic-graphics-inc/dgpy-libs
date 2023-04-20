# -*- coding: utf-8 -*-
"""Package metadata/info"""
import warnings

from listless.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "listless._meta is deprecated, use listless.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__title__", "__description__", "__pkgroot__", "__version__")
