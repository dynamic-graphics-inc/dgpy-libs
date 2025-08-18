# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from typing import cast

import pytest

from jsonbourne import JsonObj

pytestmark = [pytest.mark.pydantic, pytest.mark.optdeps]


try:
    from pydantic import BaseModel, ConfigDict

    _extra = "allow" if "pytest" in sys.modules else "ignore"
    _model_config = cast("ConfigDict", {"extra": _extra})

    class PydanticJsonObj(BaseModel, JsonObj[str | int]):  # type: ignore[misc]
        a: int
        b: int
        c: str

        @property
        def a_property(self) -> str:
            return "prop_value"

        model_config = _model_config

    class PydanticJsonObjPropertySetter(BaseModel, JsonObj):  # type: ignore[misc]
        a: int
        b: int
        c: str

        #
        @property
        def aprop(self) -> int:
            return self.a

        @aprop.setter
        def aprop(self, value: int) -> None:
            self.a = value

        model_config = _model_config

except Exception:
    pass


def test_jsonobj_property_pydantic() -> None:
    thing_w_prop = PydanticJsonObj(**{"a": 1, "b": 2, "c": "herm"})
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"


def test_jsonobj_property_pydantic_setattr_hasattr() -> None:
    thing_w_prop = PydanticJsonObj(**{"a": 1, "b": 2, "c": "herm"})
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"


def test_jsonobj_property_with_setter_pydantic() -> None:
    thing_w_prop = PydanticJsonObjPropertySetter(**{"a": 1, "b": 2, "c": "herm"})
    assert thing_w_prop.a == 1
    thing_w_prop.a = 123
    assert thing_w_prop.a == 123
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.aprop == 123
