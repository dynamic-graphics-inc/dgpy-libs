# -*- coding: utf-8 -*-
"""Constants go here!"""

from __future__ import annotations

from typing import Dict

LAGER_PORT = 52437

TORNADO_FMT = "".join(
    [
        "<level>",
        "[{level.name[0]} ",
        "{time:YYMMDDTHH:mm:ss} ",
        "{name}:{module}:{line}]",
        "</level> ",
        "{message}",
    ]
)

LOGURU_DEFAULT_FMT = "".join(
    [
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>",
        " | ",
        "<level>{level: <8}</level>",
        " | ",
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
        " - ",
        "<level>{message}</level>",
    ]
)

LOG_LEVELS: Dict[str, str] = {
    "notset": "NOTSET",
    "n": "NOTSET",
    "debug": "DEBUG",
    "d": "DEBUG",
    "info": "INFO",
    "i": "INFO",
    "s": "SUCCESS",
    "success": "SUCCESS",
    "warning": "WARNING",
    "warn": "WARNING",
    "w": "WARNING",
    "error": "ERROR",
    "e": "ERROR",
    "critical": "CRITICAL",
    "fatal": "CRITICAL",
    "c": "CRITICAL",
    # enum/enum-strings
    "0": "NOTSET",
    "10": "DEBUG",
    "20": "INFO",
    "25": "SUCCESS",
    "30": "WARNING",
    "40": "ERROR",
    "50": "CRITICAL",
}
