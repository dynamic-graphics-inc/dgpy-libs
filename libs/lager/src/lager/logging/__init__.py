# -*- coding: utf-8 -*-
"""Lager/Loguru + std logging"""

from __future__ import annotations

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
    Handler as _Handler,
    Logger as _Logger,
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
from types import TracebackType
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type, Union

from typing_extensions import Literal, Self, TypeAlias

from lager.core import LOG, loglevel

__all__ = (
    "BASIC_FORMAT",
    "CRITICAL",
    "DEBUG",
    "ERROR",
    "FATAL",
    "INFO",
    "NOTSET",
    "WARN",
    "WARNING",
    "BufferingFormatter",
    "FileHandler",
    "Filter",
    "Formatter",
    "Handler",
    "LogRecord",
    "Logger",
    "LoggerAdapter",
    "NullHandler",
    "StdLoggingHandler",
    "StreamHandler",
    # lager.logging members
    "__aliases__",
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
    "intercept",
    "intercept_all",
    "lastResort",
    "last_resort",
    "log",
    "loggers_dict",
    "makeLogRecord",
    "make_log_record",
    "patch_logging",
    "raiseExceptions",
    "raise_exceptions",
    "setLogRecordFactory",
    "setLoggerClass",
    "set_log_record_factory",
    "set_logger_class",
    "shutdown",
    "warn",
    "warning",
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

_SysExcInfoType: TypeAlias = Union[
    Tuple[Type[BaseException], BaseException, Union[TracebackType, None]],
    Tuple[None, None, None],
]
_ExcInfoType: TypeAlias = Union[None, bool, _SysExcInfoType, BaseException]
_ArgsType: TypeAlias = Union[Tuple[object, ...], Mapping[str, object]]
_FilterType: TypeAlias = Union[Filter, Callable[[LogRecord], bool]]
_Level: TypeAlias = Union[int, str]
_FormatStyle: TypeAlias = Literal["%", "{", "$"]


class Logger(_Logger):
    def __init__(self, name: str, level: _Level = 0) -> None:
        super().__init__(name, level)

    def set_level(self, level: _Level) -> None:
        """snake_case alias for setLevel"""
        self.setLevel(level)

    def is_enabled_for(self, level: int) -> bool:
        """snake_case alias for isEnabledFor"""
        return self.isEnabledFor(level)

    def get_effective_level(self) -> int:
        """snake_case alias for getEffectiveLevel"""
        return self.getEffectiveLevel()

    def get_child(self, suffix: str) -> Self:
        """snake_case alias for getChild"""
        return self.getChild(suffix)

    def find_caller(
        self, stack_info: bool = False, stacklevel: int = 1
    ) -> Tuple[str, int, str, Union[str, None]]:
        """snake_case alias for findCaller"""
        return self.findCaller(stack_info, stacklevel)

    def add_handler(self, hdlr: Handler) -> None:
        """snake_case alias for addHandler"""
        return self.addHandler(hdlr)

    def remove_handler(self, hdlr: Handler) -> None:
        """snake_case alias for removeHandler"""
        return self.removeHandler(hdlr)

    def make_record(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: _ArgsType,
        exc_info: Union[_SysExcInfoType, None],
        func: Optional[str] = None,
        extra: Union[Mapping[str, object], None] = None,
        sinfo: Optional[str] = None,
    ) -> LogRecord:
        return self.makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )

    def has_handlers(self) -> bool:
        """snake_case alias for hasHandlers"""
        return self.hasHandlers()

    def call_handlers(self, record: LogRecord) -> None:
        """snake_case alias for callHandlers"""
        return self.callHandlers(record)


class Handler(_Handler):
    def __init__(self, level: _Level = 0) -> None:
        super().__init__(level)

    def create_lock(self) -> None:
        """snake_case alias for createLock"""
        return self.createLock()

    def set_level(self, level: _Level) -> None:
        """snake_case alias for setLevel"""
        return self.setLevel(level)

    def set_formatter(self, fmt: Union[Formatter, None]) -> None:
        """snake_case alias for setFormatter"""
        return self.setFormatter(fmt)

    def handle_error(self, record: LogRecord) -> None:
        """snake_case alias for handleError"""
        return self.handleError(record)


# =====================================================================================


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
            frame.f_code.co_filename  # pyright: ignore[reportOptionalMemberAccess]
            == logging.__file__
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
