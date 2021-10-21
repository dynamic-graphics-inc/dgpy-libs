import datetime
import pathlib

from decimal import Decimal

import pytest


try:
    from jsonbourne.jsonlib import JSON_STDLIB, ORJSON, RAPIDJSON
except (ImportError, ModuleNotFoundError):
    pass

pytestmark = [pytest.mark.jsonlibs, pytest.mark.optdeps]

D = {
    "key": "value",
    "list": [1, 2, 3, 4, 5],
    "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    "sub": {
        'b': 3,
        'key': 'val',
        'a': 1,
    },
    "apath": pathlib.Path.home(),
    "Decimal": Decimal(1.4),
    "timedelta": datetime.timedelta(days=2),
}


def test_basic() -> None:
    rj = RAPIDJSON.dumps(D)
    oj = ORJSON.dumps(D)
    sj = JSON_STDLIB.dumps(D)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty() -> None:
    rj = RAPIDJSON.dumps(D, pretty=True)
    oj = ORJSON.dumps(D, pretty=True)
    sj = JSON_STDLIB.dumps(D, pretty=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_sort_keys() -> None:
    rj = RAPIDJSON.dumps(D, sort_keys=True)
    oj = ORJSON.dumps(D, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_append_newline() -> None:
    rj = RAPIDJSON.dumps(D, append_newline=True)
    oj = ORJSON.dumps(D, append_newline=True)
    sj = JSON_STDLIB.dumps(D, append_newline=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_sort_keys() -> None:
    rj = RAPIDJSON.dumps(D, pretty=True, sort_keys=True)
    oj = ORJSON.dumps(D, pretty=True, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, pretty=True, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_dump_numpy_array() -> None:
    import numpy as np

    arr = np.array([[1, 2], [3, 4]])
    rj = RAPIDJSON.dumps(arr)
    oj = ORJSON.dumps(arr)
    sj = JSON_STDLIB.dumps(arr)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_datetime() -> None:
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


def test_import_rapidjson() -> None:
    from jsonbourne.jsonlib import _import_rapidjson

    rj = _import_rapidjson()
    assert rj


def test_import_orjson() -> None:
    from jsonbourne.jsonlib import _import_orjson

    oj = _import_orjson()
    assert oj
