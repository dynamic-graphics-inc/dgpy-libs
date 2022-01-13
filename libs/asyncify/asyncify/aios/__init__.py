# -*- coding: utf-8 -*-
import os

from asyncify.aios import aios_path
from asyncify.core import asyncify

__all__ = (
    "stat",
    "rename",
    "rename",
    "replace",
    "mkdir",
    "makedirs",
    "rmdir",
    "removedirs",
    "path",
)

path = aios_path
stat = asyncify(os.stat)
rename = asyncify(os.rename)
replace = asyncify(os.replace)
remove = asyncify(os.remove)
mkdir = asyncify(os.mkdir)
makedirs = asyncify(os.makedirs)
rmdir = asyncify(os.rmdir)
removedirs = asyncify(os.removedirs)
