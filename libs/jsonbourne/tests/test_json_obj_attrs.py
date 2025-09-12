# -*- coding: utf-8 -*-
# type: ignore
from __future__ import annotations

import pytest

from jsonbourne import JsonObj

pytestmark = [pytest.mark.attrs, pytest.mark.optdeps]

try:
    from attr import attrs


except ModuleNotFoundError:
    ...


def test_jsonobj_property_attrs() -> None:
    @attrs(auto_attribs=True)
    class ThingyWithPropertyAndAttrs(JsonObj[int | str | dict[str, str]]):
        a: int
        b: int
        c: str
        d: JsonObj[str]

        @property
        def a_property(self) -> str:
            return "prop_value"

    thing_w_prop = ThingyWithPropertyAndAttrs(**{
        "a": 1,
        "b": 2,
        "c": "herm",
        "d": {"nested": "nestedval"},
    })
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"
    assert thing_w_prop.d.nested == "nestedval"


def test_jsonobj_property_attrs_str() -> None:
    @attrs(auto_attribs=True)
    class ThingyWithPropertyAndAttrsStrTests(JsonObj):
        a: int
        b: int
        c: str
        d: dict
        stuff: dict

        @property
        def a_property(self) -> str:
            return "prop_value"

    thing_w_prop = ThingyWithPropertyAndAttrsStrTests(**{
        "a": 1,
        "b": 2,
        "c": "herm",
        "stuff": {"herm_" + str(i): i for i in range(10)},
        "d": {
            "nested": "nestedval",
            **{f"ok_{i!s}": i for i in range(20)},
        },
    })
    evaluated_version = eval(thing_w_prop.__str__())
    assert isinstance(evaluated_version, ThingyWithPropertyAndAttrsStrTests)
    assert evaluated_version == thing_w_prop
