# -*- coding: utf-8 -*-

from os import path

from asyncify.core import asyncify

__all__ = (
    "exists",
    "isfile",
    "isdir",
    "getsize",
    "getmtime",
    "getatime",
    "getctime",
    "samefile",
    "sameopenfile",
)

exists = asyncify(path.exists)
isfile = asyncify(path.isfile)
isdir = asyncify(path.isdir)
getsize = asyncify(path.getsize)
getmtime = asyncify(path.getmtime)
getatime = asyncify(path.getatime)
getctime = asyncify(path.getctime)
samefile = asyncify(path.samefile)
sameopenfile = asyncify(path.sameopenfile)
