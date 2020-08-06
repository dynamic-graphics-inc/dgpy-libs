import pytest

from jsonbourne import import_json


pytestmark = [pytest.mark.basic]


def test_uno():
    from jsonbourne import json

    dictionary = {"a": 1, "b": 2, "c": 3}
    string = json.dumps(dictionary)
    assert dictionary == json.loads(string)


def test_stdlibjson():
    libname = "json"
    _stdlibjson = import_json((libname,))
    dictionary = {"a": 1, "b": 2, "c": 3}
    string = _stdlibjson.dumps(dictionary)
    assert dictionary == _stdlibjson.loads(string)
    assert _stdlibjson.__name__ in {libname, 'JSON_STDLIB'}


#### MAYBE SOME DAY!
# def test_orjson():
#     libname = "orjson"
#     _orjson = import_json((libname,))
#     dictionary = {"a": 1, "b": 2, "c": 3}
#     string = _orjson.dumps(dictionary)
#     assert dictionary == _orjson.loads(string)
#     assert _orjson.__name__ in {libname, "json"}
#
#
# def test_simplejson():
#     libname = "simplejson"
#     _simplejson = import_json((libname,))
#     dictionary = {"a": 1, "b": 2, "c": 3}
#     string = _simplejson.dumps(dictionary)
#     assert dictionary == _simplejson.loads(string)
#     assert _simplejson.__name__ in {libname, "json"}
#
# def test_ujson():
#     libname = "ujson"
#     _ujson = import_json((libname,))
#     dictionary = {"a": 1, "b": 2, "c": 3}
#     string = _ujson.dumps(dictionary)
#     assert dictionary == _ujson.loads(string)
#     assert _ujson.__name__ in {libname, "json"}
