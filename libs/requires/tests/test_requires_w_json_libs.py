# -*- coding: utf-8 -*-
# pyright: reportUndefinedVariable=false
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import json

    import rapidjson


def test_requires_json_n_rapid_json() -> None:
    from requires import requires

    @requires("json")
    def uno():
        return json.dumps({"a": 1, "b": 2})

    @requires(
        _import="rapidjson",
        pip="python-rapidjson",
        conda_forge="python-rapidjson",
    )
    def tres():
        return rapidjson.dumps({"a": 1, "b": 2})

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e


def test_requires_json_n_rapid_json_pkg_callable() -> None:
    import requires

    @requires("json")  # type: ignore[operator]
    def uno() -> str:
        return json.dumps({"a": 1, "b": 2})

    @requires(  # type: ignore[operator]
        _import="rapidjson",
        pip="python-rapidjson",
        conda_forge="python-rapidjson",
    )
    def tres() -> str:
        return rapidjson.dumps({"a": 1, "b": 2})  # type: ignore[no-any-return]

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e
