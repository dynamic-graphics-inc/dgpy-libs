# -*- coding: utf-8 -*-
"""Lager/Loguru + std logging"""
import logging

from typing import Any, Dict, List

from lager.core import LOG, loglevel


class StdLoggingHandler(logging.Handler):
    """Logging intercept handler"""

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = LOG.level(record.levelname).name
        except AttributeError:
            level = loglevel(record.levelno)

        # Find caller from where originated the logging call
        frame = logging.currentframe()
        depth = 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        LOG.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _logger_dict() -> Any:
    return logging.root.manager.loggerDict  # type: ignore


def loggers_dict() -> Dict[str, logging.Logger]:
    return {name: logging.getLogger(name) for name in _logger_dict()}  # type: ignore


def intercept(loggers: List[str]) -> None:
    for logger in loggers:
        std_logger = logging.getLogger(logger)
        std_logger.handlers = [StdLoggingHandler()]


def intercept_all() -> None:
    intercept(list(loggers_dict().keys()))
