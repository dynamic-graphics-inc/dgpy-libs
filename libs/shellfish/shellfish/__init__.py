# -*- coding: utf-8 -*-
"""shellfish ~ shell and file-system utils"""
from __future__ import annotations

from funkify import funkify
from shellfish import dotenv, fs, process, sh
from shellfish._meta import __version__

funkify(sh.do, key="shellfish.sh")
funkify(sh.do, key="shellfish")

ps = process

__all__ = ("__version__", "dotenv", "fs", "process", "ps", "sh")
