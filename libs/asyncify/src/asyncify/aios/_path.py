# -*- coding: utf-8 -*-
"""aios = asyncio + os"""

from os import path

from asyncify import asyncify

__all__ = (
    "exists",
    "getatime",
    "getctime",
    "getmtime",
    "getsize",
    "isdir",
    "isfile",
    "islink",
    "samefile",
    "sameopenfile",
)

exists = asyncify(path.exists)
getatime = asyncify(path.getatime)
getctime = asyncify(path.getctime)
getmtime = asyncify(path.getmtime)
getsize = asyncify(path.getsize)
isdir = asyncify(path.isdir)
isfile = asyncify(path.isfile)
islink = asyncify(path.islink)
samefile = asyncify(path.samefile)
sameopenfile = asyncify(path.sameopenfile)
