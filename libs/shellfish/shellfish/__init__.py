# -*- coding: utf-8 -*-
"""shellfish ~ shell and file-system utils"""
from __future__ import annotations

from funkify import funkify as _funkify
from shellfish import dotenv as dotenv, fs as fs, process as process, sh as sh
from shellfish._meta import __version__ as __version__
from shellfish._types import (
    FsPath as FsPath,
    PathLikeBytes as PathLikeBytes,
    PathLikeStr as PathLikeStr,
    PathLikeStrBytes as PathLikeStrBytes,
    PopenArg as PopenArg,
    PopenArgs as PopenArgs,
    PopenArgv as PopenArgv,
    PopenEnv as PopenEnv,
    SymlinkType as SymlinkType,
)
from shellfish.process import env as env

_funkify(sh.do, key="shellfish.sh")
_funkify(sh.do, key="shellfish")

ps = process

__all__ = (
    "FsPath",
    "PathLikeBytes",
    "PathLikeStr",
    "PathLikeStrBytes",
    "PopenArg",
    "PopenArgs",
    "PopenArgv",
    "PopenEnv",
    "SymlinkType",
    "__version__",
    "dotenv",
    "env",
    "fs",
    "process",
    "ps",
    "sh",
)
