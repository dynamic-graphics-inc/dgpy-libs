# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List, Optional, Tuple, Type, Union

from jsonbourne.jsonlib.base import JsonLibABC


if TYPE_CHECKING:
    from jsonbourne.jsonlib._json_stdlib import JSON_STDLIB
    from jsonbourne.jsonlib._orjson import ORJSON
    from jsonbourne.jsonlib._rapidjson import RAPIDJSON

_json_libs = ['orjson', 'rapidjson']


def _import_rapidjson() -> "Type[RAPIDJSON]":
    from jsonbourne.jsonlib import _rapidjson

    if not _rapidjson.rapidjson:
        raise ImportError('rapidjson')
    return _rapidjson.RAPIDJSON


def _import_orjson() -> "Type[ORJSON]":
    from jsonbourne.jsonlib import _orjson

    if not _orjson.orjson:
        raise ImportError('orjson')
    return _orjson.ORJSON


def _import_json_stdlib() -> "Type[JSON_STDLIB]":
    from jsonbourne.jsonlib._json_stdlib import JSON_STDLIB

    return JSON_STDLIB


def import_json(
    jsonlibs: Optional[Union[Tuple[str], List[str]]] = None
) -> "Type[JsonLibABC]":
    lib2funk = {
        "rapidjson": _import_rapidjson,
        "orjson": _import_orjson,
        "json": _import_json_stdlib,
    }
    jsonlibs = jsonlibs or _json_libs

    for mod in jsonlibs:
        try:
            return lib2funk[mod]()
        except (ImportError, ModuleNotFoundError):
            pass

    return _import_json_stdlib()
