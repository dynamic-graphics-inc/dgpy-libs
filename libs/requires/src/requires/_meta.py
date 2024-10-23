# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

import warnings

from requires.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "requires._meta is deprecated, use requires.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
