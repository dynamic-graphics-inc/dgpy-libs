# -*- coding: utf-8 -*-
"""JSON callable module ~ jsonbourne"""
import sys

from jsonbourne import __version__, json
from jsonbourne.core import (
    JSON,
    UNDEFINED,
    JsonDict,
    JSONModuleCls,
    JsonObj,
    JsonObjMutableMapping,
    Null,
    null,
    undefined,
)
from jsonbourne.jsonlib import import_json

sys.modules["JSON"].__class__ = JSONModuleCls
stringify = JSON.stringify
dumps = JSON.dumps
binify = JSON.binify
dumpb = JSON.dumpb
loads = JSON.loads
parse = JSON.parse
jsoncp = JSON.jsoncp
json_lib = JSON.json_lib
which = JSON.which
use_orjson = JSON.use_orjson
use_rapidjson = JSON.use_rapidjson
use_json_stdlib = JSON.use_json_stdlib
jsonify = JSON.jsonify
unjsonify = JSON.unjsonify
JSONDecodeError = JSON.JSONDecodeError

__all__ = (
    "JSONModuleCls",
    "JsonDict",
    "JsonObj",
    "JsonObjMutableMapping",
    "Null",
    "UNDEFINED",
    "__version__",
    "binify",
    "dumpb",
    "dumps",
    "import_json",
    "json",
    "json_lib",
    "jsoncp",
    "jsonify",
    "loads",
    "null",
    "parse",
    "stringify",
    "undefined",
    "unjsonify",
    "use_json_stdlib",
    "use_orjson",
    "use_rapidjson",
)
