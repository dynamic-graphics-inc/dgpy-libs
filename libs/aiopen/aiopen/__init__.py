# -*- coding: utf-8 -*-
"""`aiopen` ~ Async version of python's built in open -- based on aiofiles"""
from aiopen._version import (
    VERSION_INFO,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    __version__,
)
from aiopen.core import aiopen
from funkify.core import funkify


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
