# -*- coding: utf-8 -*-
"""FastAPI logging"""

from __future__ import annotations

from typing import List, Optional, Set, Tuple, Union

from lager.logging import intercept

__all__ = ("FASTAPI_LOGGERS", "fastapi_intercept")

FASTAPI_LOGGERS = [
    "gunicorn",
    "gunicorn.errors",
    "uvicorn",
    "uvicorn.error",
    "fastapi",
    "sqlalchemy",
]


def fastapi_intercept(
    loggers: Optional[Union[List[str], Set[str], Tuple[str, ...]]] = None,
) -> None:
    _loggers2intercept = (
        FASTAPI_LOGGERS if not loggers else sorted(set(*(*FASTAPI_LOGGERS, loggers)))
    )
    intercept(_loggers2intercept)
