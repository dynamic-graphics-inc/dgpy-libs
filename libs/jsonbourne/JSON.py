# -*- coding: utf-8 -*-
"""JSON callable module ~ jsonbourne"""
import sys

from jsonbourne import json, __version__
from jsonbourne._import import import_json
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
    "__version__",
    "json",  # json compat lib
    # core
    "JsonObjMutableMapping",
    "JsonObj",
    "JsonDict",
    "JSONModuleCls",
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
]
