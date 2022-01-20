# -*- coding: utf-8 -*-
import os

from asyncify.aios import _path
from asyncify.core import asyncify

__all__ = (
    "makedirs",
    "mkdir",
    "path",
    "remove",
    "removedirs",
    "rename",
    "replace",
    "rmdir",
    "stat",
)

path = _path

makedirs = asyncify(os.makedirs)
rename = asyncify(os.rename)
replace = asyncify(os.replace)
remove = asyncify(os.remove)
removedirs = asyncify(os.removedirs)
mkdir = asyncify(os.mkdir)
rmdir = asyncify(os.rmdir)
stat = asyncify(os.stat)
lstat = asyncify(os.lstat)
