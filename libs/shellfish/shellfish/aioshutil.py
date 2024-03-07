# -*- coding: utf-8 -*-
"""aios = asyncio + shutil"""

from __future__ import annotations

import shutil

from asyncify import asyncify

__all__ = (
    "copy",
    "copy2",
    "copyfile",
    "copymode",
    "copystat",
    "copytree",
    "rmtree",
    "which",
)
copy = asyncify(shutil.copy)
copy2 = asyncify(shutil.copy2)
copyfile = asyncify(shutil.copyfile)
copymode = asyncify(shutil.copymode)
copystat = asyncify(shutil.copystat)
copytree = asyncify(shutil.copytree)
rmtree = asyncify(shutil.rmtree)
which = asyncify(shutil.which)
