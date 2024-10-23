# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

import warnings

from h5.__about__ import __description__, __pkgroot__, __title__, __version__

warnings.warn(
    "h5._meta is deprecated, use h5.__about__ instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
