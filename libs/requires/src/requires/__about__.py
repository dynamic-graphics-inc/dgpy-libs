# -*- coding: utf-8 -*-
"""Package metadata/info"""

from __future__ import annotations

__all__ = ("__description__", "__pkgroot__", "__title__", "__version__")
__title__ = "requires"
__description__ = "Runtime imports and dependency utils"
__pkgroot__ = __file__.replace("__about__.py", "").rstrip("/\\")
__version__ = "0.11.0"
