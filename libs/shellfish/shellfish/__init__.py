# -*- coding: utf-8 -*-
"""shellfish ~ shell and file-system utils"""

from . import dotenv, fs, process, sh
from ._meta import __version__

ps = process

__all__ = (
    "__version__",
    "fs",
    "ps",
    "process",
    "sh",
    "dotenv",
)
