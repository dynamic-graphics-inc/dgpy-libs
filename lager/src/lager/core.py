# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
import asyncio

from functools import wraps
from time import time
from typing import Union

from loguru import logger

from lager.const import LOG_LEVELS


__all__ = ['loglevel', 'flog', 'handlers', 'logger', 'log', 'LOG', 'ln', 'LN']

logger.t = logger.trace
logger.d = logger.debug
logger.i = logger.info
logger.s = logger.success
logger.w = logger.warning
logger.e = logger.error
logger.c = logger.critical

# commonly used dgpy aliases
log = logger
LOG = logger
# ln => natural log
ln = logger
LN = logger


def loglevel(level: Union[str, int]) -> str:
    """Convert log-level abrev to a valid loguru log level"""
    return LOG_LEVELS[str(level).strip("'").strip('"').lower()]


def flog(funk=None, level="debug", enter=True, exit=True):
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


def handlers():
    """Return all handlers"""
    return logger._core.handlers
