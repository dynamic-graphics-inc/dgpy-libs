# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
from lager._version import (
    VERSION_INFO,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    __version__,
)
from lager.const import LAGER_PORT, LOGURU_DEFAULT_FMT, TORNADO_FMT
from lager.core import LN, LOG, flog, handlers, ln, log, logger, loglevel


__all__ = [
    'LAGER_PORT',
    'VERSION_MAJOR',
    'VERSION_MINOR',
    'VERSION_PATCH',
    'VERSION_INFO',
    '__version__',
    'LOGURU_DEFAULT_FMT',
    'TORNADO_FMT',
    'loglevel',
    'logger',
    'LOG',
    'log',
    'LN',
    'ln',
]
