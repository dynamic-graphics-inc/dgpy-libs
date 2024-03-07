# -*- coding: utf-8 -*-
"""JSON callable module ~ jsonbourne"""

from __future__ import annotations

import sys

from jsonbourne import __version__, json
from jsonbourne.core import (
    JSON as _JSON,
    UNDEFINED as UNDEFINED,
    JsonDict as JsonDict,
    JSONModuleCls,
    JsonObj as JsonObj,
    JsonObjMutableMapping,
    Null as Null,
    null as null,
    undefined as undefined,
)
from jsonbourne.jsonlib import import_json

stringify = _JSON.stringify
dumps = _JSON.dumps
binify = _JSON.binify
dumpb = _JSON.dumpb
loads = _JSON.loads
parse = _JSON.parse
rjson = _JSON.rjson
wjson = _JSON.wjson
jsoncp = _JSON.jsoncp
json_lib = _JSON.json_lib
which = _JSON.which
use_orjson = _JSON.use_orjson
use_rapidjson = _JSON.use_rapidjson
use_json_stdlib = _JSON.use_json_stdlib
jsonify = _JSON.jsonify
unjsonify = _JSON.unjsonify
JSONDecodeError = _JSON.JSONDecodeError

__all__ = (
    "UNDEFINED",
    "JSONModuleCls",
    "JsonDict",
    "JsonObj",
    "JsonObjMutableMapping",
    "Null",
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
    "rjson",
    "stringify",
    "undefined",
    "unjsonify",
    "use_json_stdlib",
    "use_orjson",
    "use_rapidjson",
    "wjson",
)

if __name__ == "__main__":
    from jsonbourne.__main__ import main

    main()
else:  # if __name__ is NOT __main__, funkify module
    sys.modules["JSON"].__class__ = JSONModuleCls
