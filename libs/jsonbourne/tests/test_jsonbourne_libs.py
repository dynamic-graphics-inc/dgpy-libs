# -*- coding: utf-8 -*-
import datetime
import pathlib
import uuid

from decimal import Decimal

import pytest

from xtyping import NamedTuple, Tuple

try:
    from jsonbourne.jsonlib import JSON_STDLIB, ORJSON, RAPIDJSON
except (ImportError, ModuleNotFoundError):
    pass

pytestmark = [pytest.mark.jsonlibs, pytest.mark.optdeps]


class Point3d(NamedTuple):
    x: int
    y: int
    z: int


class Point3dDumpable(NamedTuple):
    x: int
    y: int
    z: int

    def __dumpable__(self) -> Tuple[int, ...]:
        return tuple(self)


class Point3dJsonInterface(NamedTuple):
    x: int
    y: int
    z: int

    def __json_interface__(self) -> Tuple[int, ...]:
        return tuple(self)


class Point3dJsonInterfaceProperty(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def __json_interface__(self) -> Tuple[int, ...]:
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
    "poin_json_interface": Point3dJsonInterface(1, 2, 3),
    "poin_json_interface_property": Point3dJsonInterfaceProperty(1, 2, 3),
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
    rj = RAPIDJSON.jsoncp(_d)
    assert rj == _d
    oj = ORJSON.jsoncp(_d)
    assert oj == _d
    sj = JSON_STDLIB.jsoncp(_d)
    assert sj == _d


# dumps tests
def test_basic_dumps() -> None:
    rj = RAPIDJSON.dumps(D)
    oj = ORJSON.dumps(D)
    sj = JSON_STDLIB.dumps(D)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_fmt_dumps() -> None:
    rj = RAPIDJSON.dumps(D, fmt=True)
    oj = ORJSON.dumps(D, fmt=True)
    sj = JSON_STDLIB.dumps(D, fmt=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_dumps() -> None:
    rj = RAPIDJSON.dumps(D, pretty=True)
    oj = ORJSON.dumps(D, pretty=True)
    sj = JSON_STDLIB.dumps(D, pretty=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_sort_keys_dumps() -> None:
    rj = RAPIDJSON.dumps(D, sort_keys=True)
    oj = ORJSON.dumps(D, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_append_newline_dumps() -> None:
    rj = RAPIDJSON.dumps(D, append_newline=True)
    oj = ORJSON.dumps(D, append_newline=True)
    sj = JSON_STDLIB.dumps(D, append_newline=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_sort_keys_dumps() -> None:
    rj = RAPIDJSON.dumps(D, pretty=True, sort_keys=True)
    oj = ORJSON.dumps(D, pretty=True, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, pretty=True, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_dump_numpy_array_dumps() -> None:
    import numpy as np

    arr = np.array([[1, 2], [3, 4]])
    rj = RAPIDJSON.dumps(arr)
    oj = ORJSON.dumps(arr)
    sj = JSON_STDLIB.dumps(arr)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_datetime_dumps() -> None:
    data = {
        "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    }
    rj = RAPIDJSON.dumps(data)
    oj = ORJSON.dumps(data)
    sj = JSON_STDLIB.dumps(data)
    a = [rj, oj, sj]

    assert all(isinstance(el, str) for el in a)
    assert len(set(a)) == 1
    rj_bin = RAPIDJSON.dumpb(data)
    oj_bin = ORJSON.dumpb(data)
    sj_bin = JSON_STDLIB.dumpb(data)
    b = [rj_bin, oj_bin, sj_bin]
    assert all(isinstance(el, bytes) for el in b)


# dumpb tests
def test_basic_dumpb() -> None:
    rj = RAPIDJSON.dumpb(D)
    oj = ORJSON.dumpb(D)
    sj = JSON_STDLIB.dumpb(D)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_dumpb() -> None:
    rj = RAPIDJSON.dumpb(D, pretty=True)
    oj = ORJSON.dumpb(D, pretty=True)
    sj = JSON_STDLIB.dumpb(D, pretty=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_sort_keys_dumpb() -> None:
    rj = RAPIDJSON.dumpb(D, sort_keys=True)
    oj = ORJSON.dumpb(D, sort_keys=True)
    sj = JSON_STDLIB.dumpb(D, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_append_newline_dumpb() -> None:
    rj = RAPIDJSON.dumpb(D, append_newline=True)
    oj = ORJSON.dumpb(D, append_newline=True)
    sj = JSON_STDLIB.dumpb(D, append_newline=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_sort_keys_dumpb() -> None:
    rj = RAPIDJSON.dumpb(D, pretty=True, sort_keys=True)
    oj = ORJSON.dumpb(D, pretty=True, sort_keys=True)
    sj = JSON_STDLIB.dumpb(D, pretty=True, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_dump_numpy_array_dumpb() -> None:
    import numpy as np

    arr = np.array([[1, 2], [3, 4]])
    rj = RAPIDJSON.dumpb(arr)
    oj = ORJSON.dumpb(arr)
    sj = JSON_STDLIB.dumpb(arr)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_datetime_dumpb() -> None:
    data = {
        "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    }
    rj = RAPIDJSON.dumpb(data)
    oj = ORJSON.dumpb(data)
    sj = JSON_STDLIB.dumpb(data)
    a = [rj, oj, sj]

    assert all(isinstance(el, bytes) for el in a)
    assert len(set(a)) == 1
    rj_bin = RAPIDJSON.dumpb(data)
    oj_bin = ORJSON.dumpb(data)
    sj_bin = JSON_STDLIB.dumpb(data)
    b = [rj_bin, oj_bin, sj_bin]
    assert all(isinstance(el, bytes) for el in b)


# library import tests


def test_import_rapidjson() -> None:
    from jsonbourne.jsonlib import _import_rapidjson

    rj = _import_rapidjson()
    assert rj


def test_import_orjson() -> None:
    from jsonbourne.jsonlib import _import_orjson

    oj = _import_orjson()
    assert oj
