import pytest
from requires.core import string2requirement, Requirement
from requires.core import RequirementError
from requires.core import requires


def test_parse_import_xxx():
    s = "import json"
    a = string2requirement(s)
    print(a)
    assert a._import == "json"
    assert a._as == None
    assert a._from == None


def test_parse_from_xxx_import_yyy():
    s = "from json import dumps"
    a = string2requirement(s)
    print(a)
    assert a._import == "dumps"
    assert a._as == None
    assert a._from == "json"

    s = "from    json import dumps"
    a = string2requirement(s)
    print(a)
    assert a._import == "dumps"
    assert a._as == None
    assert a._from == "json"


def test_parse_from_xxx_import_yyy_as_zzz():
    s = "from json import dumps as DUMPIT"
    a = string2requirement(s)
    print(a)
    assert a._import == "dumps"
    assert a._as == "DUMPIT"
    assert a._from == "json"
    assert a.alias == "DUMPIT"
    assert a.pkg_basename == "json"


def test_parse_from_xxx_import_yyy_as_zzz_nested():
    s = "from os.path import join as os_path_join"
    a = string2requirement(s)
    print(a)
    assert a._import == "join"
    assert a._as == "os_path_join"
    assert a._from == "os.path"
    assert a.alias == "os_path_join"
    assert a.pkg_basename == "os"


def test_parse_from_xxx_import_yyy():
    s = "import os.path.join as os_path_join"
    a = string2requirement(s)
    print(a)
    assert a._import == "os.path.join"
    assert a._as == "os_path_join"
    assert a._from == None
    assert a.alias == "os_path_join"
    assert a.pkg_basename == "os"

def test_requirement_import_str__from_json_import_dumps_as_dumps_funk():
    req = Requirement(_import='dumps', _from='json', _as='dumps_funk')
    assert req.import_string == 'from json import dumps as dumps_funk'

def test_requirement_import_str__from_json_import_dumps():
    req = Requirement(_import='dumps', _from='json')
    assert req.import_string == 'from json import dumps'

def test_requirement_import_str__import_json():
    req = Requirement(_import='json')
    assert req.import_string == 'import json'

def test_requirement_import_str__import_json_as_jsonmod():
    req = Requirement(_import='json', _as='jsonmod')
    assert req.import_string == 'import json as jsonmod'

def test_requirement_import_str_rapidjson():
    req = Requirement(_import='rapidjson', pip='python-rapidjson', conda='python-rapidjson', conda_forge='python-rapidjson')
    assert req._pip_install_str().endswith('python-rapidjson')
    assert req._conda_forge_install_str().endswith('python-rapidjson')
    assert req._conda_install_str().endswith('python-rapidjson')


def test_jsonthing():
    import json

    @requires("json")
    def fn():
        d = {
            "herm": 1
            }
        s = json.dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_json_not_imported():
    #     import requires

    @requires("json")
    def fn():
        d = {
            "herm": 1
            }
        s = json.dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_requirement_as_decorator():
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)


    @json_dumps_req
    def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_requirement_as_decorator_multiple_xfail():
    with pytest.raises(NameError):
        def fn():
            d = {
                "herm": 1
                }
            s = dumps(d)
            f = loads(s)
            return s, f


        s, f = fn()
        assert s == '{"herm": 1}'

        assert f == {
            "herm": 1
            }


def test_requirement_as_decorator_multiple():
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads"
    json_loads_req = string2requirement(import_loads_string)


    @json_dumps_req
    @json_loads_req
    def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        f = loads(s)
        return s, f


    s, f = fn()
    assert s == '{"herm": 1}'

    assert f == {
        "herm": 1
        }


def test_requirement_as_decorator_multiple_aliases():
    import_string = "from json import dumps as dumps2"
    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads as loads2"
    json_loads_req = string2requirement(import_loads_string)


    @json_dumps_req
    @json_loads_req
    def fn():
        d = {
            "herm": 1
            }
        s = dumps2(d)
        f = loads2(s)
        return s, f


    s, f = fn()
    assert s == '{"herm": 1}'

    assert f == {
        "herm": 1
        }


def test_requirement_as_decorator_multiple_async_xfail():
    import asyncio
    import sys

    print(list(sys.modules.keys()))
    print(list(el for el in sys.modules.keys() if "dump" in el))

    with pytest.raises(NameError) as re:
        print(re)


        async def fn2():
            d = {
                "herm": 1
                }
            f = somefunction(s)
            return s, f


        s, f = asyncio.run(fn2())
        assert s == '{"herm": 1}'

        assert f == {
            "herm": 1
            }
        #


def test_requirement_as_decorator_multiple_async():
    import_string = "from json import dumps"
    json_dumps_req = string2requirement(import_string)
    import_loads_string = "from json import loads"
    json_loads_req = string2requirement(import_loads_string)


    @json_dumps_req
    @json_loads_req
    async def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        f = loads(s)
        return s, f


    import asyncio

    s, f = asyncio.run(fn())
    assert s == '{"herm": 1}'

    assert f == {
        "herm": 1
        }


def test_from_json_import_dumps():
    @requires("from json import dumps")
    def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_kwargs():
    @requires(_from="json", _import="dumps")
    def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_kwargs():
    @requires({
                  "from"  : "json",
                  "import": "dumps"
                  })
    def fn():
        d = {
            "herm": 1
            }
        s = dumps(d)
        return s


    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_dict():
    @requires({
                  "_from"  : "json",
                  "_import": "dumps",
                  "_as"    : "dumps_test_dict"
                  })
    def fn():
        d = {
            "herm": 1
            }
        s = dumps_test_dict(d)
        return s


    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_via_dicts():
    @requires(
        {
            '_from'  : 'json',
            '_import': 'dumps',
            '_as'    : 'dumps_test_dicts'
            },
        {
            'from'  : 'json',
            'import': 'loads',
            'as'    : 'loads_test_dicts'
            }
        )
    def fn():
        d = {
            "herm": 1
            }
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        return s, f
    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {
        "herm": 1
        }
def test_from_json_import_dumps_via_dict():
    @requires({
                  "_from"  : "json",
                  "_import": "dumps",
                  "_as"    : "dumps_test_dicts"
                  })
    def fn():
        d = {
            "herm": 1
            }
        s = dumps_test_dicts(d)
        from json import loads

        f = loads(s)
        return s, f


    from pprint import pprint

    pprint(fn.__globals__)
    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {
        "herm": 1
        }


def test_from_json_import_dumps_via_dicts_multi_single_dec():
    @requires(**{
        "_from"  : "json",
        "_import": "loads",
        "_as"    : "loads_test_dicts"
        })
    @requires(**{
        "_from"  : "json",
        "_import": "dumps",
        "_as"    : "dumps_test_dicts"
        })
    def fn():
        d = {
            "herm": 1
            }
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        # from json import loads
        # f = loads(s)
        print(s, f)
        return s, f


    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {
        "herm": 1
        }


def test_from_json_import_dumps_via_dicts_multi():
    @requires(**{
        "_from"  : "json",
        "_import": "loads",
        "_as"    : "loads_test_dicts"
        })
    @requires(**{
        "_from"  : "json",
        "_import": "dumps",
        "_as"    : "dumps_test_dicts"
        })
    def fn():
        d = {
            "herm": 1
            }
        s = dumps_test_dicts(d)
        f = loads_test_dicts(s)
        # from json import loads
        # f = loads(s)
        print(s, f)
        return s, f


    s, f = fn()
    assert s == '{"herm": 1}'
    assert f == {
        "herm": 1
        }


def test_from_json_import_dumps_as_dumpit():
    @requires("from json import dumps as DUMPIT")
    def fn():
        d = {
            "herm": 1
            }
        s = DUMPIT(d)
        return s


    assert fn() == '{"herm": 1}'


def test_from_json_import_dumps_as_xxx_non_importable():
    try:
        @requires("from json import DUMPSNOTANATTR")
        def fn():
            d = {
                "herm": 1
                }
            s = DUMPSNOTANATTR(d)
            return s


        assert fn() == '{"herm": 1}'
    except Exception as e:
        assert isinstance(e, RequirementError)
        assert "AttributeError" in e.__str__()


def test_requires():
    #     import requires

    @requires("a_fake_module")
    def fn():
        return 123


    assert fn() == 123


def test_requires_name_error():
    with pytest.raises(RequirementError) as re:
        @requires("a_fake_module")
        def fn():
            some_value = a_fake_module.a_fake_function()
            return 123


        assert fn() == 123


def test_requires_err_msg():
    with pytest.raises(RequirementError) as re:
        @requires("a_fake_module")
        def fn():
            some_value = a_fake_module.a_fake_function()
            return 123


        assert fn() == 123


if __name__ == "__main__":
    pytest.main()
