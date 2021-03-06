# -*- coding: utf-8 -*-
"""`aiopen` ~ Async version of python's built in open -- based on aiofiles"""
from aiopen._meta import __version__
from aiopen.core import aiopen
from funkify.core import funkify


funkify(aiopen, name="aiopen")

__all__ = [
    "__version__",
    "aiopen",
]
