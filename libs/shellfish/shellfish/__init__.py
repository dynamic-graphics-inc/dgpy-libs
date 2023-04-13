# -*- coding: utf-8 -*-
"""shellfish ~ shell and file-system utils"""
from __future__ import annotations

from funkify import funkify as _funkify
from shellfish import dotenv as dotenv, fs as fs, process as process, sh as sh
from shellfish._meta import __version__ as __version__
from shellfish.process import env as env

_funkify(sh.do, key="shellfish.sh")
_funkify(sh.do, key="shellfish")

ps = process

__all__ = ("__version__", "dotenv", "env", "fs", "process", "ps", "sh")
