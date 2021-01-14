# -*- coding: utf-8 -*-
"""`jsonbourne` finds the best python-json-lib for the job

Dynamic Graphics Python
"""
from jsonbourne import json
from jsonbourne._import import import_json
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


JSONLIB = json.__name__

__all__ = [
    "__version__",
    "JSON",  # js/ts JSON (THE ONE TO USE)
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
