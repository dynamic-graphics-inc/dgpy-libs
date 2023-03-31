# -*- coding: utf-8 -*-
"""Python builtin data structure utils"""
import datetime

from decimal import Decimal

import pytest

from jsonbourne import JSON, JsonObj

pytestmark = [pytest.mark.basic]


def test_dot_access_attr_vs_item() -> None:
    jd = JSON({"socket.io": "data"})
    assert jd["socket.io"] == "data"
    with pytest.raises(AttributeError):
        _data = jd.socket.io
        if _data:
            raise AssertionError("should not get here")


def test_dot_access_nested() -> None:
    jd = JSON({"socket.io": {"key": "value", "two": 2}})
    expected_dot_keys_list = [("socket.io", "key"), ("socket.io", "two")]
    assert jd.dot_keys_list() == expected_dot_keys_list
    assert jd.dot_items_list() == [
        (("socket.io", "key"), "value"),
        (("socket.io", "two"), 2),
    ]
    with pytest.raises(AttributeError):
        _data = jd.socket.io
        if _data:
            raise AssertionError("should not get here")


class Thingy(JsonObj):
    @property
    def herm(self) -> str:
        return "hermproperty"


def test_json_obj_basic() -> None:
    thing = Thingy({"a": 1, "b": 2, "c": 3})
    assert thing.a == thing["a"]

    thing2 = Thingy({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing2.c.herm == thing2["c"]["herm"]


def test_jsonobj_basic_unpacking() -> None:
    thing = Thingy({"a": 1, "b": 2, "c": 3, "d": ["list"]})
    thing2 = Thingy({"b": 2, "c": 3, "d": ["different list"], "a": 234})
    assert thing.a == thing["a"]

    assert {**thing} == {"a": 1, "b": 2, "c": 3, "d": ["list"]}
    assert {**thing2} == {"a": 234, "b": 2, "c": 3, "d": ["different list"]}

    merged = {**thing, **thing2}
    assert merged["a"] == 234
    merged_jsonobj = JsonObj({**thing, **thing2})
    assert {**merged_jsonobj} == merged


@pytest.mark.skip(reason="no longer the impl")
def test_jsonobj_breaks() -> None:
    thing2 = Thingy({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing2.c.herm == thing2["c"]["herm"]
    with pytest.raises(ValueError) as err:
        thing2["herm herm herm import"] = "should break"
        assert err


class ThingyWithMethod(JsonObj):
    def a_property(self) -> str:
        return "prop_value"


def test_json_obj_method() -> None:
    thing_w_prop = ThingyWithMethod({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property() == "prop_value"
    assert thing_w_prop["a_property"]() == "prop_value"


def test_json_obj_method_set_attr() -> None:
    thing_w_prop = ThingyWithMethod({"a": 1, "b": 2, "c": {"herm": 23}})
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property() == "prop_value"
    assert thing_w_prop["a_property"]() == "prop_value"
    thing_w_prop.some_attr = "attr_value"
    assert thing_w_prop.some_attr == "attr_value"
    assert thing_w_prop["some_attr"] == "attr_value"
    assert hasattr(thing_w_prop, "some_attr")


class ThingyWithProperty(JsonObj):
    @property
    def a_property(self) -> str:
        return "prop_value"


def test_json_obj_property() -> None:
    thing_w_prop = ThingyWithProperty(
        **{"a": 1, "b": 2, "c": {"herm": 23}, "d": {"nested": "nestedval"}}
    )
    assert thing_w_prop.c.herm == thing_w_prop["c"]["herm"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"
    assert thing_w_prop.d.nested == "nestedval"


def test_protected_attrs_slash_members() -> None:
    j: JsonObj = JsonObj()
    j.key = "value"
    j["12"] = "twelve"
    with pytest.raises(ValueError):
        j.items = [1, 2, 3, 4]  # type: ignore[assignment]
    j["items"] = [1, 2, 3, 4]
    assert j.items != [1, 2, 3, 4]  # type: ignore[comparison-overlap]
    assert j["items"] == [1, 2, 3, 4]


def test_number_keys() -> None:
    j = JsonObj[str]()
    j.key = "value"
    j["12"] = "twelve"
    assert j["12"] == "twelve"


data = {
    "id": 1,
    "code": None,
    "subd": {"a": 23, "b": {"herm": 2}},
    "type": "foo",
    "root": {
        "string_list": ["one", "two", "octopus", "what_is_up"],
        "mixed_dict": {
            "num": 123,
            "obj": {"k": "v"},
            "list": ["s", 123, {"k": "v"}],
        },
    },
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}


def test_dot_items() -> None:
    jd: JsonObj = JSON(data)

    expected = [
        (("id",), 1),
        (("code",), None),
        (("subd", "a"), 23),
        (("subd", "b", "herm"), 2),
        (("type",), "foo"),
        (("root", "string_list"), ["one", "two", "octopus", "what_is_up"]),
        (("root", "mixed_dict", "num"), 123),
        (("root", "mixed_dict", "obj", "k"), "v"),
        (("root", "mixed_dict", "list"), ["s", 123, JsonObj(**{"k": "v"})]),
        (
            ("bars",),
            [
                JsonObj(**{"id": 6934900}),
                JsonObj(**{"id": 6934977}),
                JsonObj(**{"id": 6934992}),
                JsonObj(**{"id": 6934993}),
                JsonObj(**{"id": 6935014}),
            ],
        ),
        (("n",), 10),
        (("date_str",), "2013-07-08 00:00:00"),
        (("float_here",), 0.454545),
        (
            ("complex",),
            [
                JsonObj(
                    **{
                        "id": 83865,
                        "goal": Decimal("2.000000"),
                        "state": "active",
                    }
                )
            ],
        ),
        (("profile_id",), None),
        (("state",), "active"),
    ]
    expected_strings = [
        ("id", 1),
        ("code", None),
        ("subd.a", 23),
        ("subd.b.herm", 2),
        ("type", "foo"),
        ("root.string_list", ["one", "two", "octopus", "what_is_up"]),
        ("root.mixed_dict.num", 123),
        ("root.mixed_dict.obj.k", "v"),
        ("root.mixed_dict.list", ["s", 123, JsonObj(**{"k": "v"})]),
        (
            "bars",
            [
                JsonObj(**{"id": 6934900}),
                JsonObj(**{"id": 6934977}),
                JsonObj(**{"id": 6934992}),
                JsonObj(**{"id": 6934993}),
                JsonObj(**{"id": 6935014}),
            ],
        ),
        ("n", 10),
        ("date_str", "2013-07-08 00:00:00"),
        ("float_here", 0.454545),
        (
            "complex",
            [
                JsonObj(
                    **{
                        "id": 83865,
                        "goal": Decimal("2.000000"),
                        "state": "active",
                    }
                )
            ],
        ),
        ("profile_id", None),
        ("state", "active"),
    ]

    assert [(".".join(el[0]), el[1]) for el in expected] == expected_strings

    dkl = jd.dot_items_list()
    assert expected == dkl

    expected_json_str = JSON.stringify(expected, sort_keys=True, pretty=True)
    output_json_str = JSON.stringify(dkl, sort_keys=True, pretty=True)
    assert output_json_str == expected_json_str
    try:
        from deepdiff import DeepDiff

        assert not DeepDiff(expected, dkl)
    except ModuleNotFoundError:
        ...


d1 = {
    "id": 1,
    "code": None,
    "subd": {"a": 23, "b": {"herm": 2}},
    "type": "foo",
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}

d2 = {
    "id": "2",
    "code": None,
    "type": "foo",
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": Decimal("2.000000"), "state": "active"}],
    "profile_id": None,
    "state": "active",
}


def test_dotlookup() -> None:
    d = JsonObj(d1)
    dot_get = d.subd.a
    dot_lookup = d.dot_lookup("subd.a")
    assert dot_lookup == dot_get


def test_dotlookup_no_dots() -> None:
    d = JsonObj(d1)
    dot_get = d.n
    dot_lookup = d.dot_lookup("n")
    assert dot_lookup == dot_get


def test_dotlookup_dont_exist() -> None:
    d = JsonObj(d1)
    with pytest.raises(KeyError):
        d["subd.a.hermhermherm.ohno"]


def test_dot_iter_keys() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    dot_keys_set = set(d.dot_keys())
    expected_tuples_set = {tuple(el.split(".")) for el in expected}
    assert dot_keys_set == expected_tuples_set


def test_dot_list_keys() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    assert {tuple(el.split(".")) for el in expected} == set(d.dot_keys_list())


def test_dot_list_keys_sorted() -> None:
    d = JsonObj(d1)
    expected = [
        "id",
        "code",
        "subd.a",
        "subd.b.herm",
        "type",
        "bars",
        "n",
        "date_str",
        "float_here",
        "complex",
        "profile_id",
        "state",
    ]
    assert [tuple(el.split(".")) for el in sorted(expected)] == d.dot_keys_list(
        sort_keys=True
    )


def test_json_dict_reject_non_string_key() -> None:
    t1 = {1: None, 2: 2}
    with pytest.raises(ValueError):
        JsonObj(t1)  # type: ignore[arg-type]


def test_filter_none() -> None:
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result: JsonObj = JsonObj(t1).filter_none()
    assert result == JsonObj(
        **{
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
            "b": 2,
            "c": {
                "d": "herm",
                "e": None,
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_none_recursive() -> None:
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(t1).filter_none(recursive=True)
    assert result == JsonObj(
        **{
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
            "b": 2,
            "c": {
                "d": "herm",
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_false() -> None:
    t1 = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(t1).filter_false()
    assert result == JsonObj(
        **{
            "b": 2,
            "c": {
                "d": "herm",
                "e": None,
                "falsey_dict": {},
                "falsey_list": [],
                "falsey_string": "",
                "is_false": False,
            },
        }
    )


def test_filter_falsey_recursive() -> None:
    d = {
        "falsey_dict": {},
        "falsey_list": [],
        "falsey_string": "",
        "is_false": False,
        "a": None,
        "b": 2,
        "c": {
            "d": "herm",
            "e": None,
            "falsey_dict": {},
            "falsey_list": [],
            "falsey_string": "",
            "is_false": False,
        },
    }
    result = JsonObj(d).filter_false(recursive=True)
    assert result == JsonObj(**{"b": 2, "c": {"d": "herm"}})


def test_lookup_ops() -> None:
    data = {
        "key": "value",
        "list": [1, 2, 3, 4, 5],
        "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
        "sub": {
            "b": 3,
            "key": "val",
            "a": 1,
        },
        "timedelta": datetime.timedelta(days=2),
    }

    d = JSON(data)

    assert d.dot_lookup("sub.key") == "val"
    assert d.dot_lookup(("sub", "key")) == "val"
    assert "val" == d["sub.key"]
    assert "val" == d["sub", "key"]
    assert "val" == d[("sub", "key")]


def test_cycle_eject() -> None:
    a = JsonObj(**{"a": "c", "herm": 123})
    b = JsonObj(**{"c": "c", "d": a})
    a.circle = b
    astring = str(a)
    assert isinstance(astring, str)


def test_cycle_stringify() -> None:
    a = JsonObj(**{"a": "c", "herm": 123})
    b = JsonObj(**{"c": "c", "d": a})
    a.circle = b
    with pytest.raises((TypeError, ValueError)):
        json_str = a.to_json()
        assert isinstance(json_str, str)


def test_dataclass_stringify() -> None:
    a = JsonObj(**{"a": "c", "herm": 123})

    from dataclasses import dataclass

    @dataclass()
    class DataThing:
        n: int
        s: str

    data = DataThing(n=1, s="stringy")
    data_string = JSON.stringify(data)
    assert data_string == '{"n":1,"s":"stringy"}'
    a.data = data
    nested_str = JSON.stringify(a)
    assert nested_str == '{"a":"c","herm":123,"data":{"n":1,"s":"stringy"}}'
