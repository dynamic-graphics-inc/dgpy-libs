# -*- coding: utf-8 -*-
"""`aiopen` ~ Async version of python's built in open -- based on aiofiles"""
from funkify.core import funkify

from aiopen._version import VERSION_INFO
from aiopen._version import VERSION_MAJOR
from aiopen._version import VERSION_MINOR
from aiopen._version import VERSION_PATCH
from aiopen._version import __version__
from aiopen.core import aiopen

funkify(aiopen, name="aiopen")

__all__ = [
    "aiopen",
    # Version et al
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
