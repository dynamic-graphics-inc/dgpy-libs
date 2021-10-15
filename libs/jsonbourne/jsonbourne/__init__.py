# -*- coding: utf-8 -*-
"""jsonbourne the best undercover json lib

Dynamic Graphics Python
"""
from jsonbourne import jsonlib
from jsonbourne._meta import __version__
from jsonbourne.core import (
    JSON,
    UNDEFINED,
    JsonDict,
    JsonObj,
    JsonObjMutableMapping,
    parse,
    stringify,
    undefined,
)
from jsonbourne.helpers import rm_js_comments
from jsonbourne.jsonlib import import_json


json = jsonlib

JSONLIB = jsonlib.__name__

__all__ = [
    "__version__",
    "JSON",  # js/ts JSON (THE ONE TO USE)
    "jsonlib",  # json compat lib
    "json",  # json compat lib
    # core
    "JsonObjMutableMapping",
    "JsonObj",
    "JsonDict",
    # import
    "import_json",
    # util funks
    "stringify",
    "parse",
    "rm_js_comments",
    # undefined
    "undefined",
    "UNDEFINED",
]
