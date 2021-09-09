# -*- coding: utf-8 -*-
"""Rapidjson tests"""
import os

import pytest

from jsonbourne import import_json


os.path.dirname(os.path.abspath(__file__))

pytestmark = [pytest.mark.rapidjson, pytest.mark.optdeps]


def test_uno() -> None:
    from jsonbourne import json

    dictionary = {"a": 1, "b": 2, "c": 3}
    string = json.dumps(dictionary)
    assert dictionary == json.loads(string)


def test_rapidjson() -> None:
    libname = "rapidjson"
    _rapidjson = import_json((libname,))
    dictionary = {"a": 1, "b": 2, "c": 3}
    string = _rapidjson.dumps(dictionary)
    assert dictionary == _rapidjson.loads(string)
    assert _rapidjson.__name__.lower() in {libname, "json", 'RAPIDJSON'}
