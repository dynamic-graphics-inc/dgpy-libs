# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

import warnings

from xtyping.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "xtyping._meta is deprecated, use xtyping.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
