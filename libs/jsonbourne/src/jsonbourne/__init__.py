# -*- coding: utf-8 -*-
"""jsonbourne the best undercover json lib

Dynamic Graphics Python
"""

from __future__ import annotations

from jsonbourne import jsonlib
from jsonbourne.__about__ import __version__
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

__all__ = (
    "JSON",  # js/ts JSON (THE ONE TO USE)
    "UNDEFINED",
    "JsonDict",
    "JsonObj",
    # core
    "JsonObjMutableMapping",
    "__version__",
    # import
    "import_json",
    "json",  # json compat lib
    "jsonlib",  # json compat lib
    "parse",
    "rm_js_comments",
    # util funks
    "stringify",
    # undefined
    "undefined",
)
