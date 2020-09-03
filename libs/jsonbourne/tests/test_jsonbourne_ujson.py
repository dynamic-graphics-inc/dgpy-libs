# -*- coding: utf-8 -*-
import pytest

from jsonbourne import import_json


pytestmark = [pytest.mark.ujson, pytest.mark.optdeps]

#
# def test_uno():
#     from jsonbourne import json
#
#     dictionary = {"a": 1, "b": 2, "c": 3}
#     string = json.dumps(dictionary)
#     assert dictionary == json.loads(string)
#
#
# def test_ujson():
#     libname = "ujson"
#     _ujson = import_json((libname,))
#     dictionary = {"a": 1, "b": 2, "c": 3}
#     string = _ujson.dumps(dictionary)
#     assert dictionary == _ujson.loads(string)
#     assert _ujson.__name__ in {libname, "json"}
