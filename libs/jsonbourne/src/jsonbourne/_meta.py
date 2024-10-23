# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

import warnings

from jsonbourne.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "jsonbourne._meta is deprecated, use jsonbourne.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
