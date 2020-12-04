# -*- coding: utf-8 -*-
"""Python lager brewed by a loguru"""
from lager import logging
from lager._meta import __version__
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
    'handlers',
    'flog',
    'logger',
    'logging',
    'LOG',
    'log',
    'LN',
    'ln',
]
