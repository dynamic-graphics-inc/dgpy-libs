# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import pathlib
import uuid

from decimal import Decimal
from typing import NamedTuple, Type

import pytest

from jsonbourne.jsonlib import JSON_STDLIB, ORJSON, RAPIDJSON, JsonLibABC

pytestmark = [pytest.mark.jsonlibs, pytest.mark.optdeps]


LIBS: list[Type[JsonLibABC]] = [
    e
    for e in [
        ORJSON,
        RAPIDJSON,
    ]
    if e.usable()
]


class Point3d(NamedTuple):
    x: int
    y: int
    z: int


class Point3dDumpable(NamedTuple):
    x: int
    y: int
    z: int

    def __dumpable__(self) -> tuple[int, ...]:
        return tuple(self)


class Point3dJsonInterface(NamedTuple):
    x: int
    y: int
    z: int

    def __json_interface__(self) -> tuple[int, ...]:
        return tuple(self)


class Point3dJsonInterfaceProperty(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def __json_interface__(self) -> tuple[int, ...]:
        return tuple(self)


D = {
    "key": "value",
    "list": [1, 2, 3, 4, 5],
    "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    "sub": {
        "b": 3,
        "key": "val",
        "a": 1,
    },
    "apath": pathlib.Path.home(),
    "Decimal": Decimal(1.4),
    "timedelta": datetime.timedelta(days=2),
    "point": Point3d(1, 2, 3),
    "point_dumpable": Point3dDumpable(1, 2, 3),
    "point_json_interface": Point3dJsonInterface(1, 2, 3),
    "point_json_interface_property": Point3dJsonInterfaceProperty(1, 2, 3),
    "uuid": uuid.UUID("12345678-1234-1234-1234-123456789012"),
}


def test_is_tuple() -> None:
    point = Point3d(1, 2, 3)
    assert isinstance(point, tuple)


def test_jsoncp() -> None:
    _d = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": {
            "key": "value",
        },
    }

    oj = ORJSON.jsoncp(_d)
    assert oj == _d
    sj = JSON_STDLIB.jsoncp(_d)
    assert sj == _d
    if RAPIDJSON.usable():
        rj = RAPIDJSON.jsoncp(_d)
        assert rj == _d


# fixture that provides a jsonlibrary
@pytest.fixture(
    params=[pytest.param(jsonlib, id=jsonlib.__name__.lower()) for jsonlib in LIBS]
)
def jsonlib(request: pytest.FixtureRequest) -> JsonLibABC:
    """Fixture that provides a json library."""
    return request.param


# dumps tests
def test_basic_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D),
        JSON_STDLIB.dumps(D),
    ]
    assert len(set(a)) == 1


def test_fmt_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, fmt=True),
        JSON_STDLIB.dumps(D, fmt=True),
    ]
    assert len(set(a)) == 1


def test_pretty_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, pretty=True),
        JSON_STDLIB.dumps(D, pretty=True),
    ]
    assert len(set(a)) == 1


def test_sort_keys_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, sort_keys=True),
        JSON_STDLIB.dumps(D, sort_keys=True),
    ]
    assert len(set(a)) == 1


def test_append_newline_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, append_newline=True),
        JSON_STDLIB.dumps(D, append_newline=True),
    ]
    assert len(set(a)) == 1


def test_pretty_sort_keys_dumps(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, pretty=True, sort_keys=True),
        JSON_STDLIB.dumps(D, pretty=True, sort_keys=True),
    ]
    assert len(set(a)) == 1


def test_dump_numpy_array_dumps(jsonlib: JsonLibABC) -> None:
    import numpy as np

    arr = np.array([[1, 2], [3, 4]])
    json_bytes = [
        jsonlib.dumps(arr),
        JSON_STDLIB.dumps(arr),
    ]
    assert len(set(json_bytes)) == 1


def test_datetime_dumps(jsonlib: JsonLibABC) -> None:
    data = {
        "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    }
    json_strings = [
        jsonlib.dumps(data),
        JSON_STDLIB.dumps(data),
    ]
    assert len(set(json_strings)) == 1

    assert all(isinstance(el, str) for el in json_strings)
    json_bytes = [jsonlib.dumpb(data), JSON_STDLIB.dumpb(data)]
    assert len(set(json_bytes)) == 1
    assert all(isinstance(el, bytes) for el in json_bytes)


# dumpb tests
def test_basic_dumpb(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D),
        JSON_STDLIB.dumps(D),
    ]
    assert len(set(a)) == 1


def test_pretty_dumpb(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, pretty=True),
        JSON_STDLIB.dumps(D, pretty=True),
    ]
    assert len(set(a)) == 1


def test_sort_keys_dumpb(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, sort_keys=True),
        JSON_STDLIB.dumps(D, sort_keys=True),
    ]
    assert len(set(a)) == 1


def test_append_newline_dumpb(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, append_newline=True),
        JSON_STDLIB.dumps(D, append_newline=True),
    ]
    assert len(set(a)) == 1


def test_pretty_sort_keys_dumpb(jsonlib: JsonLibABC) -> None:
    a = [
        jsonlib.dumps(D, pretty=True, sort_keys=True),
        JSON_STDLIB.dumps(D, pretty=True, sort_keys=True),
    ]
    assert len(set(a)) == 1


def test_dump_numpy_array_dumpb(jsonlib: JsonLibABC) -> None:
    import numpy as np

    arr = np.array([[1, 2], [3, 4]])

    json_bytes = [
        jsonlib.dumps(arr),
        JSON_STDLIB.dumps(arr),
    ]
    assert len(set(json_bytes)) == 1


def test_datetime_dumpb(jsonlib: JsonLibABC) -> None:
    data = {
        "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    }

    json_bytes = [
        jsonlib.dumps(data),
        JSON_STDLIB.dumps(data),
    ]
    assert len(set(json_bytes)) == 1
    assert all(isinstance(el, str) for el in json_bytes)

    json_str = [
        jsonlib.dumpb(data),
        JSON_STDLIB.dumpb(data),
    ]
    assert all(isinstance(el, bytes) for el in json_str)
    assert len(set(json_str)) == 1


# library import tests


def test_import_rapidjson() -> None:
    from jsonbourne.jsonlib import _import_rapidjson

    if not RAPIDJSON.usable():
        with pytest.raises(
            ImportError, match=r"rapidjson \(python-rapidjson\) not installed"
        ):
            _import_rapidjson()
    else:
        rj = _import_rapidjson()
        assert rj


def test_import_orjson() -> None:
    from jsonbourne.jsonlib import _import_orjson

    oj = _import_orjson()
    assert oj
