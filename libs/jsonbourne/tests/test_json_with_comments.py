# -*- coding: utf-8 -*-
from __future__ import annotations

import json

from os import path

import pytest

from jsonbourne import JSON
from jsonbourne.helpers import rm_js_comments

PWD = path.dirname(path.abspath(__file__))


def _lib_installed(libname: str) -> bool:
    """Check if a library is installed."""
    try:
        __import__(libname)
        return True
    except ImportError:
        return False


def test_strip_comments_from_json() -> None:
    rush_with_comments_filepath = path.join(PWD, "data", "rush.comments.json")
    rush_no_comments_filepath = path.join(PWD, "data", "rush.no-comments.json")

    with open(rush_with_comments_filepath) as f:
        rush_with_comments_string = f.read()

    with open(rush_no_comments_filepath) as f:
        rush_no_comments_string = f.read()

    removed_comments_str = json.dumps(
        json.loads(rm_js_comments(rush_with_comments_string)),
        sort_keys=True,
        indent=2,
    )
    expected = json.dumps(json.loads(rush_no_comments_string), sort_keys=True, indent=2)
    assert removed_comments_str == expected


@pytest.mark.skipif(not _lib_installed("jsonc2json"), reason="jsonc2json not installed")
def test_loads_jsonc() -> None:
    rush_with_comments_filepath = path.join(PWD, "data", "rush.comments.json")
    rush_no_comments_filepath = path.join(PWD, "data", "rush.no-comments.json")

    with open(rush_with_comments_filepath) as f:
        rush_with_comments_string = f.read()

    with open(rush_no_comments_filepath) as f:
        rush_no_comments_string = f.read()

    removed_comments_str = JSON.dumps(
        JSON.loads(rush_with_comments_string, jsonc=True),
        sort_keys=True,
        fmt=True,
    )
    expected = JSON.dumps(JSON.loads(rush_no_comments_string), sort_keys=True, fmt=True)
    assert removed_comments_str == expected
