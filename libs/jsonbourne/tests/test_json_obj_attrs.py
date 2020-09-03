# -*- coding: utf-8 -*-

import pytest

from jsonbourne import JsonObj


pytestmark = [pytest.mark.attrs, pytest.mark.optdeps]

try:
    from attr import attrs


except:
    pass


def test_dictainer_property_attrs() -> None:
    @attrs(auto_attribs=True)
    class ThingyWithPropertyAndAttrs(JsonObj):
        a: int
        b: int
        c: str
        d: dict

        @property
        def a_property(self) -> str:
            return "prop_value"

    thing_w_prop = ThingyWithPropertyAndAttrs(
        **{"a": 1, "b": 2, "c": "herm", "d": {"nested": "nestedval"}}
    )
    assert thing_w_prop.c == thing_w_prop["c"]
    assert thing_w_prop.a_property == "prop_value"
    assert thing_w_prop["a_property"] == "prop_value"
    print(thing_w_prop.d, type(thing_w_prop.d))
    assert thing_w_prop.d.nested == "nestedval"


EXPECTED_STRING = """ThingyWithPropertyAndAttrsStrTests(**{
    'a': 1,
    'b': 2,
    'c': 'herm',
    'd': {'nested': 'nestedval',
          'ok_0': 0,
          'ok_1': 1,
          'ok_10': 10,
          'ok_11': 11,
          'ok_12': 12,
          'ok_13': 13,
          'ok_14': 14,
          'ok_15': 15,
          'ok_16': 16,
          'ok_17': 17,
          'ok_18': 18,
          'ok_19': 19,
          'ok_2': 2,
          'ok_3': 3,
          'ok_4': 4,
          'ok_5': 5,
          'ok_6': 6,
          'ok_7': 7,
          'ok_8': 8,
          'ok_9': 9},
    'stuff': {'herm_0': 0,
              'herm_1': 1,
              'herm_2': 2,
              'herm_3': 3,
              'herm_4': 4,
              'herm_5': 5,
              'herm_6': 6,
              'herm_7': 7,
              'herm_8': 8,
              'herm_9': 9}
})"""


def test_dictainer_property_attrs_str() -> None:
    @attrs(auto_attribs=True)
    class ThingyWithPropertyAndAttrsStrTests(JsonObj):
        a: int
        b: int
        c: str
        d: dict
        stuff: dict

        @property
        def a_property(self):
            return "prop_value"

    thing_w_prop = ThingyWithPropertyAndAttrsStrTests(
        **{
            "a": 1,
            "b": 2,
            "c": "herm",
            "stuff": {"herm_" + str(i): i for i in range(10)},
            "d": {"nested": "nestedval", **{"ok_" + str(i): i for i in range(20)}},
        }
    )
    print(thing_w_prop)
    assert str(thing_w_prop) == EXPECTED_STRING


if __name__ == "__main__":
    pass
    # from doctest import testmod
    # testmod()
