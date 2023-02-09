# -*- coding: utf-8 -*-
# noqa: F821
# pyright: reportUndefinedVariable=false

from typing import TYPE_CHECKING, Any, Dict, Tuple

import pytest

from requires.core import (
    Requirement,
    RequirementAttributeError,
    RequirementError,
    requires,
    string2requirement,
)


def test_parse_import_xxx() -> None:
    s = "import json"
    a = string2requirement(s)
    assert a._import == "json"
    assert a._as is None
    assert a._from is None


def test_parse_from_xxx_import_yyy() -> None:
    s = "from json import dumps"
    a = string2requirement(s)
    assert a._import == "dumps"
    assert a._as is None
    assert a._from == "json"

    s = "from    json import dumps"
    a = string2requirement(s)
    assert a._import == "dumps"
    assert a._as is None
    assert a._from == "json"


def test_parse_from_xxx_import_yyy_as_zzz() -> None:
    s = "from json import dumps as DUMPIT"
    a = string2requirement(s)
    assert a._import == "dumps"
    assert a._as == "DUMPIT"
    assert a._from == "json"
    assert a.alias == "DUMPIT"
    assert a.pkg_basename == "json"


def test_parse_from_xxx_import_yyy_as_zzz_nested() -> None:
    s = "from os.path import join as os_path_join"
    a = string2requirement(s)
    assert a._import == "join"
    assert a._as == "os_path_join"
    assert a._from == "os.path"
    assert a.alias == "os_path_join"
    assert a.pkg_basename == "os"


def test_parse_from_xxx_import_yyy_deeper_import() -> None:
    s = "import os.path.join as os_path_join"
    a = string2requirement(s)
    assert a._import == "os.path.join"
    assert a._as == "os_path_join"
    assert a._from is None
    assert a.alias == "os_path_join"
    assert a.pkg_basename == "os"


def test_requirement_import_str__from_json_import_dumps_as_dumps_funk() -> None:
    req = Requirement(_import="dumps", _from="json", _as="dumps_funk")
    assert req.import_string == "from json import dumps as dumps_funk"


def test_requirement_import_str__from_json_import_dumps() -> None:
    req = Requirement(_import="dumps", _from="json")
    assert req.import_string == "from json import dumps"


def test_requirement_import_str__import_json() -> None:
    req = Requirement(_import="json")
    assert req.import_string == "import json"


def test_requirement_import_str__import_json_as_jsonmod() -> None:
    req = Requirement(_import="json", _as="jsonmod")
    assert req.import_string == "import json as jsonmod"


def test_requirement_import_str_rapidjson() -> None:
    req = Requirement(
        _import="rapidjson",
        pip="python-rapidjson",
        conda="python-rapidjson",
        conda_forge="python-rapidjson",
    )
    assert req._pip_install_str().endswith("python-rapidjson")
    assert req._conda_forge_install_str().endswith("python-rapidjson")
    assert req._conda_install_str().endswith("python-rapidjson")


def test_requirement_import_str_numpy_install_str() -> None:
    req = Requirement(_import="numpy", pip=True, conda_forge=True, conda=True)
    assert req._pip_install_str().endswith("numpy")
    assert req._conda_forge_install_str().endswith("numpy")
    assert req._conda_install_str().endswith("numpy")


def test_jsonthing() -> None:
    import json

    @requires("json")
    def fn() -> str:
        d = {"herm": 1}
        s = json.dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_json_not_imported() -> None:
    @requires("json")
    def fn() -> str:
        d = {"herm": 1}
        s = json.dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_requirement_as_decorator() -> None:
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)

    @json_dumps_req
    def fn() -> str:
        d = {"herm": 1}
        s = dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_requirement_as_decorator_multiple_xfail() -> None:
    with pytest.raises(NameError):

        def fn() -> Tuple[str, Any]:
            d = {"herm": 1}
            s = dumps(d)
            f = loads(s)
            return s, f

        s, f = fn()
        assert s == '{"herm": 1}'

        assert f == {"herm": 1}


def test_requirement_as_decorator_multiple() -> None:
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads"
    json_loads_req = string2requirement(import_loads_string)

    @json_dumps_req
    @json_loads_req
    def fn() -> Tuple[str, Any]:
        d = {"herm": 1}
        s = dumps(d)
        f = loads(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'

    assert f == {"herm": 1}


def test_requirement_as_decorator_multiple_aliases() -> None:
    import_string = "from json import dumps as dumps2"

    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads as loads2"
    json_loads_req = string2requirement(import_loads_string)

    @json_dumps_req
    @json_loads_req
    def fn():
        d = {"herm": 1}
        s = dumps2(d)
        f = loads2(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'

    assert f == {"herm": 1}


def test_requirement_as_decorator_multiple_async_xfail() -> None:
    import asyncio

    with pytest.raises(NameError) as re:
        assert re

        async def fn2():
            _f = somefunction(s)  # type: ignore[name-defined]
            return s, _f

        s, f = asyncio.run(fn2())  # type: ignore[no-untyped-call]
        assert s == '{"herm": 1}'

        assert f == {"herm": 1}


def test_requirement_as_decorator_multiple_async() -> None:
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads"
    json_loads_req = string2requirement(import_loads_string)

    @json_dumps_req
    @json_loads_req
    async def fn():
        d = {"herm": 1}
        s = dumps(d)
        f = loads(s)
        return s, f

    import asyncio

    s, f = asyncio.run(fn())
    assert s == '{"herm": 1}'

    assert f == {"herm": 1}


def test_from_json_import_dumps() -> None:
    @requires("from json import dumps")
    def fn() -> str:
        d = {"herm": 1}
        s = dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_alias() -> None:
    @requires("from json import dumps as dumpz")
    def fn() -> str:
        d = {"herm": 1}
        s = dumpz(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_module_alias() -> None:
    @requires("import json as jason")
    def fn() -> str:
        d = {"herm": 1}
        s = jason.dumps(d)
        return s

    assert fn() == '{"herm": 1}'


@pytest.mark.asyncio()
async def test_from_json_import_dumps_async() -> None:
    @requires("from json import dumps")
    async def fn() -> str:
        d = {"herm": 1}
        s = dumps(d)
        return s

    result = await fn()
    assert result == '{"herm": 1}'


def test_from_json_import_dumps_via_kwargs() -> None:
    @requires(_from="json", _import="dumps")
    def fn() -> str:
        d = {"herm": 1}
        s = dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_dict() -> None:
    @requires({"from": "json", "import": "dumps"})
    def fn() -> str:
        d = {"herm": 1}
        s = dumps(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_dict_simple() -> None:
    @requires({"_from": "json", "_import": "dumps", "_as": "dumps_test_dict"})
    def fn():
        d = {"herm": 1}
        s = dumps_test_dict(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_dicts() -> None:
    @requires(
        {"_from": "json", "_import": "dumps", "_as": "dumps_test_dicts"},
        {"from": "json", "import": "loads", "as": "loads_test_dicts"},
    )
    def fn():
        d = {"herm": 1}
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {"herm": 1}


def test_from_json_import_dumps_as_via_dict() -> None:
    @requires({"_from": "json", "_import": "dumps", "_as": "dumps_test_dicts"})
    def fn():
        d = {"herm": 1}
        s = dumps_test_dicts(d)
        from json import loads

        f = loads(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {"herm": 1}


def test_from_json_import_dumps_via_dicts_multi_single_dec() -> None:
    @requires(**{"_from": "json", "_import": "loads", "_as": "loads_test_dicts"})
    @requires(**{"_from": "json", "_import": "dumps", "_as": "dumps_test_dicts"})
    def fn() -> Tuple[str, Dict[str, int]]:
        d = {"herm": 1}
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {"herm": 1}


def test_from_json_import_dumps_via_dicts_multi() -> None:
    @requires(**{"_from": "json", "_import": "loads", "_as": "loads_test_dicts"})
    @requires(**{"_from": "json", "_import": "dumps", "_as": "dumps_test_dicts"})
    def fn() -> Tuple[str, Dict[str, int]]:
        d = {"herm": 1}
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        return s, f

    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {"herm": 1}


def test_from_json_import_dumps_as_dumpit() -> None:
    @requires("from json import dumps as DUMPIT")
    def fn() -> str:
        d = {"herm": 1}
        s = DUMPIT(d)
        return s

    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_as_xxx_non_importable() -> None:
    try:

        @requires("from json import DUMPSNOTANATTR")
        def fn():
            d = {"herm": 1}
            s = DUMPSNOTANATTR(d)  # type: ignore[name-defined]
            return s

        assert fn() == '{"herm": 1}'
    except Exception as e:
        assert isinstance(e, (RequirementAttributeError,))
        assert "AttributeError" in e.__str__()


def test_requires() -> None:
    @requires("a_fake_module")
    def fn():
        return 123

    assert fn() == 123


def test_requires_name_error() -> None:
    with pytest.raises(RequirementError) as re:
        assert re

        @requires("a_fake_module")
        def fn():
            _some_value = a_fake_module.a_fake_function()  # type: ignore[name-defined]
            return _some_value

        fn()


@pytest.mark.asyncio()
async def test_requires_name_error_async() -> None:
    with pytest.raises(RequirementError) as re:
        assert re

        @requires("a_fake_module")
        async def fn():
            _some_value = a_fake_module.a_fake_function()  # type: ignore[name-defined]
            return _some_value

        await fn()


def test_requires_err_msg() -> None:
    with pytest.raises(RequirementError) as re:
        assert re

        @requires("a_fake_module")
        def fn():
            return a_fake_module.a_fake_function()  # type: ignore[name-defined]

        fn()


def test_stacked_requirements() -> None:
    requires_ruamel_yaml = Requirement(
        _import="ruamel.yaml",
        pip="ruamel.yaml",
        conda=False,
        conda_forge="ruamel_yaml",
    )

    @requires("json")
    @requires("from os import path")
    @requires_ruamel_yaml
    def jsonify(d):
        return json.dumps(d)

    data = {"herm": 123}
    assert '{"herm": 123}' == jsonify(data)


def test_module_wrap() -> None:
    np_requirement = Requirement(_import="numpy", _as="np")
    np = np_requirement.__requirement__

    @requires(_import="numpy", _as="np")
    def mkvec(vector):
        vector = np.ndarray(vector)
        return vector

    try:
        _v = mkvec([12, 3])
        assert _v is not None

    except ModuleNotFoundError as e:
        with pytest.raises(RequirementError) as re:
            raise e
            mkvec([12, 3])
        assert "could not import: `import numpy as np`" in str(re.value)


if __name__ == "__main__":
    pytest.main()
