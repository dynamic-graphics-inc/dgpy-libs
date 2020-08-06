# -*- coding: utf-8 -*-

import pytest

from jsonbourne import JsonObj, json


pytestmark = [pytest.mark.pydantic, pytest.mark.optdeps]


def test_dictainer_property_dgpy_base_obj() -> None:
    from jsonbourne.pydantic import JsonBaseModel

    class JsonSubObj(JsonBaseModel):
        herm: int

        def to_dict(self):
            return self.dict()

        def to_json(self, *args, **kwargs):
            return self.json()

        @classmethod
        def from_json(cls, json_string: str):
            return JsonSubObj(json.loads(json_string))

    class JsonObjModel(JsonBaseModel):
        a: int
        b: int
        c: str
        d: JsonObj
        e: JsonSubObj

        #
        @property
        def a_property(self) -> str:
            return "prop_value"

        def to_json(self, *args, **kwargs):
            return self.json()

        @classmethod
        def from_json(cls, json_string: str):
            return cls(**json.loads(json_string))

    thing_w_prop = JsonObjModel(
        **{"a": 1, "b": 2, "c": "herm", "d": {"nested": "nestedval"}, "e": {"herm": 2}}
    )
    print(thing_w_prop)
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    print("HERE WE ARE", thing_w_prop)
    print(dir(thing_w_prop))
    assert thing_w_prop["a_property"] == "prop_value"

    assert thing_w_prop.d.nested == "nestedval"
    print(dir(thing_w_prop))
    print(thing_w_prop.e, type(thing_w_prop.e))
