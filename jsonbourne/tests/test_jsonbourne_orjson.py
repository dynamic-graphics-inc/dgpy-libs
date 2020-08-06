# -*- coding: utf-8 -*-
import pytest

from jsonbourne import import_json


pytestmark = [pytest.mark.orjson, pytest.mark.optdeps]


def test_uno():
    from jsonbourne import json

    dictionary = {"a": 1, "b": 2, "c": 3}
    string = json.dumps(dictionary)
    assert dictionary == json.loads(string)


def test_orjson():
    libname = "orjson"
    _orjson = import_json((libname,))
    dictionary = {"a": 1, "b": 2, "c": 3}
    string = _orjson.dumps(dictionary)
    assert dictionary == _orjson.loads(string)
    assert _orjson.__name__.lower() in {libname, "json_stdlib"}
