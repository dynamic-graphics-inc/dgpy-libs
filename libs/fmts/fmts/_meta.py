# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

import warnings

from fmts.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "fmts._meta is deprecated, use fmts.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
