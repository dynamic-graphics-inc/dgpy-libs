# -*- coding: utf-8 -*-
"""shellfish ~ shell and file-system utils"""

from shellfish import dotenv, fs, process, sh
from shellfish._meta import __version__

ps = process

__all__ = (
    '__version__',
    # modules
    'fs',
    'ps',
    'sh',
    'dotenv',
)
