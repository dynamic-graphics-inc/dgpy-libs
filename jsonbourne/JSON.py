# -*- coding: utf-8 -*-
"""JSON callable module ~ jsonbourne"""
import sys

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
    JSONModuleCls,
    JsonObj,
    JsonObjMutableMapping,
)


sys.modules['JSON'].__class__ = JSONModuleCls
stringify = JSON.stringify
dumps = JSON.dumps
binify = JSON.binify
dumpb = JSON.dumpb
loads = JSON.loads
parse = JSON.parse
json_lib = JSON.json_lib

__all__ = [
    "json",  # json compat lib
    # core
    "JsonObjMutableMapping",
    "JsonObj",
    "JsonDict",
    # import
    "import_json",
    # util funks
    "stringify",
    "binify",
    "dumps",
    "dumpb",
    "loads",
    "json_lib",
    "parse",
    # Version stuff
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
