# -*- coding: utf-8 -*-
import sys

import pytest

from jsonbourne import JsonObj


pytestmark = [pytest.mark.pydantic, pytest.mark.optdeps]


try:

    from pydantic import BaseModel

    class PydanticJsonDict(BaseModel, JsonObj):
        a: int
        b: int
        c: str

        #
        @property
        def a_property(self) -> str:
            return "prop_value"

        class Config:
            extra = "allow" if "pytest" in sys.modules else "ignore"


except:
    pass


def test_dictainer_property_pydantic() -> None:
    thing_w_prop = PydanticJsonDict(**{"a": 1, "b": 2, "c": "herm"})
    print(thing_w_prop)
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"

    print(dir(thing_w_prop))


def test_dictainer_property_pydantic_setattr_hasattr() -> None:
    thing_w_prop = PydanticJsonDict(**{"a": 1, "b": 2, "c": "herm"})
    print(thing_w_prop)
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"

    thing_w_prop.some_attr = "attr_value"
    assert thing_w_prop.some_attr == "attr_value"
    assert thing_w_prop["some_attr"] == "attr_value"
