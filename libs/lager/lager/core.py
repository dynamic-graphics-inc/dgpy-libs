# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
import asyncio
import atexit as _atexit
import sys as _sys

from functools import wraps
from time import time
from typing import Any, Dict, Union

from loguru import _defaults, logger
from loguru._handler import Handler
from loguru._logger import Core as _Core, Logger as _Logger

from lager.const import LOG_LEVELS


__all__ = ['loglevel', 'flog', 'handlers', 'logger', 'log', 'LOG', 'ln', 'LN']

try:
    import orjson  # type: ignore

    def _stringify_new_line(serializable: Any) -> str:
        return orjson.dumps(serializable, option=orjson.OPT_APPEND_NEWLINE).decode(
            'utf-8'
        )

    def _stringify_no_new_line(serializable: Any) -> str:
        return f"{orjson.dumps(serializable).decode('utf-8')}\n"

    _stringify = (
        _stringify_new_line
        if hasattr(orjson, "OPT_APPEND_NEWLINE")
        else _stringify_no_new_line
    )

    def _serialize_record(text: str, record: Dict[str, Any]) -> str:
        exception = record["exception"]

        if exception is not None:
            exception = {
                "type": None if exception.type is None else exception.type.__name__,
                "value": exception.value,
                "traceback": bool(record["exception"].traceback),
            }

        serializable = {
            "text": text,
            "record": {
                "elapsed": {
                    "repr": record["elapsed"],
                    "seconds": record["elapsed"].total_seconds(),
                },
                "exception": exception,
                "extra": record["extra"],
                "file": {"name": record["file"].name, "path": record["file"].path},
                "function": record["function"],
                "level": {
                    "icon": record["level"].icon,
                    "name": record["level"].name,
                    "no": record["level"].no,
                },
                "line": record["line"],
                "message": record["message"],
                "module": record["module"],
                "name": record["name"],
                "process": {"id": record["process"].id, "name": record["process"].name},
                "thread": {"id": record["thread"].id, "name": record["thread"].name},
                "time": {
                    "repr": record["time"],
                    "timestamp": record["time"].timestamp(),
                },
            },
        }
        return _stringify(serializable)

    Handler._serialize_record = staticmethod(_serialize_record)
except ModuleNotFoundError:
    pass

logger = _Logger(_Core(), None, 0, False, False, False, False, True, None, {})
if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    logger.add(_sys.stderr)

_atexit.register(logger.remove)

# commonly used dgpy aliases
log = logger
LOG = logger
# ln => natural log
ln = logger
LN = logger


def loglevel(level: Union[str, int]) -> str:
    """Convert log-level abrev to a valid loguru log level"""
    return LOG_LEVELS[str(level).strip("'").strip('"').lower()]


def flog(funk=None, level: str = "debug", enter: bool = True, exit: bool = True):
    """Log function (sync/async) enter and exit using this decorator

    Args:
        funk (Callable): Function to decorate
        level (Union[int, str]): Log level
        enter (bool): Log function entry if True
        exit (bool): Log function exit if False

    Returns:
        A wrapped function that now has logging!

    Usage:
        # SYNC
        @flog
        def add(a, b):
            return a + b
        add(1, 4)

        # ASYNC
        @flog
        async def add_async(a, b):
            return a + b
        import asyncio
        asyncio.run(add_async(1, 4))

    """

    def _flog(funk):
        name = funk.__name__

        @wraps(funk)
        def _flog_decorator(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if enter:
                logger_.log(
                    loglevel(level),
                    "FLOG-ENTER > '{}' (args={}, kwargs={})",
                    name,
                    args,
                    kwargs,
                )
            ti = time()
            result = funk(*args, **kwargs)
            tf = time()
            if exit:
                logger_.log(
                    loglevel(level),
                    "FLOG-EXIT < '{}' (return={}, dt_sec={})",
                    name,
                    result,
                    tf - ti,
                )
            return result

        @wraps(funk)
        async def _flog_decorator_async(*args, **kwargs):
            logger_ = logger.opt(depth=7)
            if enter:
                logger_.log(
                    loglevel(level),
                    "FLOG-ENTER > '{}' (args={}, kwargs={})",
                    name,
                    args,
                    kwargs,
                )
            ti = time()
            result = await funk(*args, **kwargs)
            tf = time()
            if exit:
                logger_.log(
                    loglevel(level),
                    "FLOG-EXIT < '{}' (return={}, dt_sec={})",
                    name,
                    result,
                    tf - ti,
                )
            return result

        if asyncio.iscoroutinefunction(funk) or asyncio.iscoroutine(funk):
            return _flog_decorator_async
        return _flog_decorator

    return _flog(funk) if funk else _flog


def handlers() -> Dict[int, Handler]:
    """Return all handlers"""
    return logger._core.handlers  # type: ignore
