# -*- coding: utf-8 -*-
import pytest

from jsonbourne import import_json

pytestmark = [pytest.mark.basic]


def test_uno() -> None:
    from jsonbourne import json

    dictionary = {"a": 1, "b": 2, "c": 3}
    string = json.dumps(dictionary)
    assert dictionary == json.loads(string)


def test_stdlibjson() -> None:
    libname = "json"
    _stdlibjson = import_json((libname,))
    dictionary = {"a": 1, "b": 2, "c": 3}
    string = _stdlibjson.dumps(dictionary)
    assert dictionary == _stdlibjson.loads(string)
    assert _stdlibjson.__name__ in {libname, "JSON_STDLIB"}
