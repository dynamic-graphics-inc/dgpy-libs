# -*- coding: utf-8 -*-
from jsonbourne.jsonlib.base import JsonLib


def _import_rapidjson():
    from jsonbourne.jsonlib import _rapidjson

    if not _rapidjson.rapidjson:
        raise ImportError('rapidjson')
    return _rapidjson.RAPIDJSON


def _import_orjson():
    from jsonbourne.jsonlib import _orjson

    if not _orjson.orjson:
        raise ImportError('orjson')
    return _orjson.ORJSON


def _import_json_stdlib():
    from jsonbourne.jsonlib._json_stdlib import JSON_STDLIB

    return JSON_STDLIB


def import_json(jsonlibs=["orjson", "rapidjson"]) -> JsonLib:
    lib2funk = {
        "rapidjson": _import_rapidjson,
        "orjson": _import_orjson,
        "json": _import_json_stdlib,
    }

    for mod in jsonlibs:
        try:
            return lib2funk[mod]()
        except (ImportError, ModuleNotFoundError):
            pass

    return _import_json_stdlib()
