# -*- coding: utf-8 -*-
"""Lager/Loguru + std logging"""
import logging

from logging import (
    BASIC_FORMAT as BASIC_FORMAT,
    CRITICAL as CRITICAL,
    DEBUG as DEBUG,
    ERROR as ERROR,
    FATAL as FATAL,
    INFO as INFO,
    NOTSET as NOTSET,
    WARN as WARN,
    WARNING as WARNING,
    BufferingFormatter as BufferingFormatter,
    FileHandler as FileHandler,
    Filter as Filter,
    Formatter as Formatter,
    Handler as Handler,
    Logger as Logger,
    LoggerAdapter as LoggerAdapter,
    LogRecord as LogRecord,
    NullHandler as NullHandler,
    StreamHandler as StreamHandler,
    addLevelName as addLevelName,
    addLevelName as add_level_name,
    basicConfig as basicConfig,
    basicConfig as basic_config,
    captureWarnings as captureWarnings,
    captureWarnings as capture_warnings,
    critical as critical,
    debug as debug,
    disable as disable,
    error as error,
    exception as exception,
    fatal as fatal,
    getLevelName as getLevelName,
    getLevelName as get_level_name,
    getLogger as getLogger,
    getLogger as get_logger,
    getLoggerClass as getLoggerClass,
    getLoggerClass as get_logger_class,
    getLogRecordFactory as getLogRecordFactory,
    getLogRecordFactory as get_log_record_factory,
    info as info,
    lastResort as lastResort,
    lastResort as last_resort,
    log as log,
    makeLogRecord as makeLogRecord,
    makeLogRecord as make_log_record,
    raiseExceptions as raiseExceptions,
    raiseExceptions as raise_exceptions,
    setLoggerClass as setLoggerClass,
    setLoggerClass as set_logger_class,
    setLogRecordFactory as setLogRecordFactory,
    setLogRecordFactory as set_log_record_factory,
    shutdown as shutdown,
    warn as warn,
    warning as warning,
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

# logging snake_case aliases bc I cannot stand camelCase
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
        while (
            frame.f_code.co_filename
            == logging.__file__  # pyright: ignore[reportOptionalMemberAccess]
        ):
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
