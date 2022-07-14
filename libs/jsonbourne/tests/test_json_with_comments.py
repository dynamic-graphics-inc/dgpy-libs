# -*- coding: utf-8 -*-
import json

from os import path

import pytest

from jsonbourne import JSON
from jsonbourne.helpers import rm_js_comments

PWD = path.dirname(path.abspath(__file__))


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


def test_loads_jsonc() -> None:
    rush_with_comments_filepath = path.join(PWD, "data", "rush.comments.json")
    rush_no_comments_filepath = path.join(PWD, "data", "rush.no-comments.json")

    with open(rush_with_comments_filepath) as f:
        rush_with_comments_string = f.read()

    with open(rush_no_comments_filepath) as f:
        rush_no_comments_string = f.read()

    if JSON.rapidjson_useable():
        removed_comments_str = JSON.dumps(
            JSON.loads(rush_with_comments_string, jsonc=True),
            sort_keys=True,
            fmt=True,
        )
        expected = JSON.dumps(
            JSON.loads(rush_no_comments_string), sort_keys=True, fmt=True
        )
        assert removed_comments_str == expected
    else:
        with pytest.raises(NotImplementedError):
            JSON.loads(rush_with_comments_string, jsonc=True),
