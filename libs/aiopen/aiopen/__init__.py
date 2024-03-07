# -*- coding: utf-8 -*-
"""`aiopen` ~ Async version of python's built in open -- based on aiofiles"""

from __future__ import annotations

from aiopen.__about__ import __version__
from aiopen.core import aiopen
from funkify import funkify

funkify(aiopen, key="aiopen")

__all__ = (
    "__version__",
    "aiopen",
)
