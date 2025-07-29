# -*- coding: utf-8 -*-
# pyright: reportUndefinedVariable=false
from __future__ import annotations

import json

from typing import Any

import orjson
import pytest


def test_requires_json_n_rapid_json() -> None:
    from requires import requires

    @requires("json")
    def uno() -> str:
        return json.dumps({"a": 1, "b": 2})

    @requires(
        _import="orjson",
        pip="orjson",
        conda_forge="orjson",
    )
    def tres() -> Any:
        return orjson.dumps({"a": 1, "b": 2}).decode()

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
        _import="orjson",
        pip="orjson",
        conda_forge="orjson",
    )
    def tres() -> str:
        return orjson.dumps({"a": 1, "b": 2}).decode()

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e
