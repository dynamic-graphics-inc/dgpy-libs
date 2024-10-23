# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""

from __future__ import annotations

import asyncio
import sys as _sys

from functools import wraps
from time import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union

from loguru import logger as logger
from loguru._handler import Handler

from lager.const import LOG_LEVELS

T = TypeVar("T")

try:
    import orjson

    def _stringify_new_line(serializable: Any) -> str:
        return orjson.dumps(serializable, option=orjson.OPT_APPEND_NEWLINE).decode(
            "utf-8"
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
                "file": {
                    "name": record["file"].name,
                    "path": record["file"].path,
                },
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
                "process": {
                    "id": record["process"].id,
                    "name": record["process"].name,
                },
                "thread": {
                    "id": record["thread"].id,
                    "name": record["thread"].name,
                },
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

# lager/logger aliases
log = LOG = logger
lager = LAGER = logger
ln = LN = logger  # ln => natural log


def loglevel(level: Union[str, int]) -> str:
    """Convert log-level abrev to a valid loguru log level"""
    return str(LOG_LEVELS[str(level).strip("'").strip('"').lower()])


def flog(
    funk: Optional[Callable[..., T]] = None,
    level: Union[str, int] = "debug",
    enter: bool = True,
    exit: bool = True,
) -> T:
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

    def _flog(funk: Callable[..., T]) -> Callable[..., T]:
        name = funk.__name__

        @wraps(funk)
        def _flog_decorator(*args: Any, **kwargs: Any) -> T:
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
        async def _flog_decorator_async(*args: Any, **kwargs: Any) -> T:
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
            result: T = await funk(*args, **kwargs)  # type: ignore[misc]
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
            return _flog_decorator_async  # type: ignore[return-value]
        return _flog_decorator

    return _flog(funk) if funk else _flog  # type: ignore[return-value]


def handlers() -> Dict[int, Handler]:
    """Return all handlers"""
    return logger._core.handlers  # type: ignore[no-any-return]


def reset(level: Optional[Union[str, int]] = None) -> None:
    logger.remove()
    logger.add(_sys.stderr, level=loglevel(level or "debug"))


__hoisted__ = (
    "_change_activation",
    "_core",
    "_dynamic_level",
    "_find_iter",
    "_log",
    "_options",
    "add",
    "bind",
    "catch",
    "complete",
    "configure",
    "contextualize",
    "critical",
    "debug",
    "disable",
    "enable",
    "error",
    "exception",
    "info",
    "level",
    "opt",
    "parse",
    "patch",
    "remove",
    "start",
    "stop",
    "success",
    "trace",
    "warning",
)
_change_activation = LAGER._change_activation
_core = LAGER._core
_find_iter = LAGER._find_iter
_log = LAGER._log
_options = LAGER._options
add = LAGER.add
bind = LAGER.bind
catch = LAGER.catch
complete = LAGER.complete
configure = LAGER.configure
contextualize = LAGER.contextualize
critical = LAGER.critical
debug = LAGER.debug
disable = LAGER.disable
enable = LAGER.enable
error = LAGER.error
exception = LAGER.exception
info = LAGER.info
level = LAGER.level
opt = LAGER.opt
parse = LAGER.parse
patch = LAGER.patch
remove = LAGER.remove
start = LAGER.start
stop = LAGER.stop
success = LAGER.success
trace = LAGER.trace
warning = LAGER.warning

__all__ = (
    "LAGER",
    "LOG",
    "_change_activation",
    "_core",
    "_find_iter",
    "_log",
    "_options",
    "add",
    "bind",
    "catch",
    "complete",
    "configure",
    "contextualize",
    "critical",
    "debug",
    "disable",
    "enable",
    "error",
    "exception",
    "flog",
    "handlers",
    "info",
    "lager",
    "level",
    "ln",
    "log",
    "logger",
    "loglevel",
    "opt",
    "parse",
    "patch",
    "remove",
    "start",
    "stop",
    "success",
    "trace",
    "warning",
)
