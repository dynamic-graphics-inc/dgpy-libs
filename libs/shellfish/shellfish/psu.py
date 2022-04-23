# -*- coding: utf-8 -*-
"""psutils-utils"""

try:
    import psutil

    PSUTIL_AVAILABLE = True
    __psutil_version__ = psutil.__version__
except ImportError:
    PSUTIL_AVAILABLE = False
    __psutil_version__ = "?.?.?"

__all__ = (
    "PSUTIL_AVAILABLE",
    "__psutil_version__",
)
