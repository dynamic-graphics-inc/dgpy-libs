# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, List, Union

import pytest

from jsonbourne import JSON

pytestmark = [pytest.mark.pydantic, pytest.mark.optdeps]

try:
    from jsonbourne.pydantic import JsonBaseModel, TJsonObjPydantic

    class JsonSubObj(JsonBaseModel):
        herm: int

        def to_dict(self) -> dict[str, int]:
            return self.dict()

        def to_json(self, *args: Any, **kwargs: Any) -> str:
            return self.json()

        @classmethod
        def from_json(cls, json_string: Union[str, bytes]) -> JsonSubObj:
            d = JSON.loads(json_string)
            return cls(**d)

    class JsonObjModel(JsonBaseModel):
        a: int
        b: int
        c: str
        d: TJsonObjPydantic
        e: JsonSubObj

        @property
        def a_property(self) -> str:
            return "prop_value"

        def to_json(self, *args: Any, **kwargs: Any) -> str:
            return self.json()

        @classmethod
        def from_json(cls, json_string: Union[str, bytes]) -> "JsonObjModel":
            return cls(**JSON.loads(json_string))

    def test_json_base_model_w_prop() -> None:
        try:
            thing_w_prop = JsonObjModel(
                **{
                    "a": 1,
                    "b": 2,
                    "c": "herm",
                    "d": {"nested": "nestedval"},
                    "e": {"herm": 2},
                }
            )
        except Exception as e:
            raise e

        c_getattr = thing_w_prop.c
        c_getitem = thing_w_prop["c"]
        assert c_getattr == c_getitem
        assert thing_w_prop.a_property == "prop_value"
        assert thing_w_prop["a_property"] == "prop_value"

        assert thing_w_prop.d.nested == "nestedval"

    @pytest.mark.skip(reason="pydantic v2 does not support __root__")
    def test_json_base_model_root_type() -> None:
        from jsonbourne.pydantic import JsonBaseModel

        class JsonModelNoRootType(JsonBaseModel):
            x: int
            y: int

        class JsonModelHasRootType(JsonBaseModel):
            __root__: List[str]

        assert not JsonModelNoRootType.__custom_root_type__
        assert JsonModelHasRootType.__custom_root_type__
        obj = JsonModelHasRootType(__root__=["a", "b", "c"])

        obj2 = JsonModelHasRootType(["a", "b", "c"])  # type: ignore[misc,call-arg]
        assert obj == obj2

except ModuleNotFoundError:
    pass
