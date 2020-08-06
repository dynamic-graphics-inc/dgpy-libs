# -*- coding: utf-8 -*-
"""`jsonbourne` finds the best python-json-lib for the job

Dynamic Graphics Python
"""
from jsonbourne import json
from jsonbourne._import import import_json
from jsonbourne._version import (
    VERSION_INFO,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    __version__,
)
from jsonbourne.core import (
    JSON,
    JsonDict,
    JsonObj,
    JsonObjMutableMapping,
    parse,
    stringify,
)


JSONLIB = json.__name__

__all__ = [
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
    # Version stuff
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
