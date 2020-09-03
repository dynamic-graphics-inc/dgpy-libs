import datetime
import pathlib

from decimal import Decimal

import pytest


try:
    from jsonbourne.jsonlib._json_stdlib import JSON_STDLIB
    from jsonbourne.jsonlib._orjson import ORJSON
    from jsonbourne.jsonlib._rapidjson import RAPIDJSON
except (ImportError, ModuleNotFoundError):
    pass

pytestmark = [pytest.mark.jsonlibs, pytest.mark.optdeps]

D = {
    "key": "value",
    "list": [1, 2, 3, 4, 5],
    "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    "sub": {'b': 3, 'key': 'val', 'a': 1,},
    "apath": pathlib.Path.home(),
    "Decimal": Decimal(1.4),
    "timedelta": datetime.timedelta(days=2),
}


def test_basic():
    rj = RAPIDJSON.dumps(D)
    oj = ORJSON.dumps(D)
    sj = JSON_STDLIB.dumps(D)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty():
    rj = RAPIDJSON.dumps(D, pretty=True)
    oj = ORJSON.dumps(D, pretty=True)
    sj = JSON_STDLIB.dumps(D, pretty=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_sort_keys():
    rj = RAPIDJSON.dumps(D, sort_keys=True)
    oj = ORJSON.dumps(D, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_pretty_sort_keys():
    rj = RAPIDJSON.dumps(D, pretty=True, sort_keys=True)
    oj = ORJSON.dumps(D, pretty=True, sort_keys=True)
    sj = JSON_STDLIB.dumps(D, pretty=True, sort_keys=True)
    a = [rj, oj, sj]
    assert len(set(a)) == 1


def test_datetime():
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


def test_import_rapidjson():
    from jsonbourne._import import _import_rapidjson

    rj = _import_rapidjson()


def test_import_orjson():
    from jsonbourne._import import _import_orjson

    oj = _import_orjson()
