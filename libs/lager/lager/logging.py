# -*- coding: utf-8 -*-
"""Lager/Loguru + std logging"""
import logging

from logging import (
    BASIC_FORMAT,
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
    BufferingFormatter,
    FileHandler,
    Filter,
    Formatter,
    Handler,
    Logger,
    LoggerAdapter,
    LogRecord,
    NullHandler,
    StreamHandler,
    addLevelName,
    basicConfig,
    captureWarnings,
    critical,
    debug,
    disable,
    error,
    exception,
    fatal,
    getLevelName,
    getLogger,
    getLoggerClass,
    getLogRecordFactory,
    info,
    lastResort,
    log,
    makeLogRecord,
    raiseExceptions,
    setLoggerClass,
    setLogRecordFactory,
    shutdown,
    warn,
    warning,
)
from typing import Any, Dict, List

from lager.core import LOG, loglevel

__all__ = (
    "BASIC_FORMAT",
    "BufferingFormatter",
    "CRITICAL",
    "DEBUG",
    "ERROR",
    "FATAL",
    "FileHandler",
    "Filter",
    "Formatter",
    "Handler",
    "INFO",
    "LogRecord",
    "Logger",
    "LoggerAdapter",
    "NOTSET",
    "NullHandler",
    "StreamHandler",
    "WARN",
    "WARNING",
    "addLevelName",
    "add_level_name",
    "basicConfig",
    "basic_config",
    "captureWarnings",
    "capture_warnings",
    "critical",
    "debug",
    "disable",
    "error",
    "exception",
    "fatal",
    "getLevelName",
    "getLogRecordFactory",
    "getLogger",
    "getLoggerClass",
    "get_level_name",
    "get_log_record_factory",
    "get_logger",
    "get_logger_class",
    "info",
    "lastResort",
    "last_resort",
    "log",
    "makeLogRecord",
    "make_log_record",
    "raiseExceptions",
    "raise_exceptions",
    "setLogRecordFactory",
    "setLoggerClass",
    "set_log_record_factory",
    "set_logger_class",
    "shutdown",
    "warn",
    "warning",
    # lager.logging members
    "__aliases__",
    "StdLoggingHandler",
    "loggers_dict",
    "intercept",
    "intercept_all",
    "patch_logging",
)

__aliases__ = {
    "add_level_name": "addLevelName",
    "basic_config": "basicConfig",
    "capture_warnings": "captureWarnings",
    "get_level_name": "getLevelName",
    "get_log_record_factory": "getLogRecordFactory",
    "get_logger": "getLogger",
    "get_logger_class": "getLoggerClass",
    "last_resort": "lastResort",
    "make_log_record": "makeLogRecord",
    "raise_exceptions": "raiseExceptions",
    "set_log_record_factory": "setLogRecordFactory",
    "set_logger_class": "setLoggerClass",
}

# logging snake_case aliases bc I cannot stand camelCase
add_level_name = addLevelName
basic_config = basicConfig
capture_warnings = captureWarnings
get_level_name = getLevelName
get_log_record_factory = getLogRecordFactory
get_logger = getLogger
get_logger_class = getLoggerClass
last_resort = lastResort
make_log_record = makeLogRecord
raise_exceptions = raiseExceptions
set_log_record_factory = setLogRecordFactory
set_logger_class = setLoggerClass


def patch_logging() -> None:
    for k, v in __aliases__.items():
        setattr(logging, k, getattr(logging, v))


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
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        LOG.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _logger_dict() -> Any:
    return logging.root.manager.loggerDict


def loggers_dict() -> Dict[str, logging.Logger]:
    return {name: logging.getLogger(name) for name in _logger_dict()}


def intercept(loggers: List[str]) -> None:
    for logger in loggers:
        std_logger = logging.getLogger(logger)
        std_logger.handlers = [StdLoggingHandler()]


def intercept_all() -> None:
    intercept(list(loggers_dict().keys()))
