# -*- coding: utf-8 -*-
import json

from os import path

from jsonbourne.helpers import rm_js_comments


PWD = path.dirname(path.abspath(__file__))


def test_strip_comments_from_json() -> None:
    rush_with_comments_filepath = path.join(PWD, 'data', 'rush.comments.json')
    rush_no_comments_filepath = path.join(PWD, 'data', 'rush.no-comments.json')

    with open(rush_with_comments_filepath) as f:
        rush_with_comments_string = f.read()

    with open(rush_no_comments_filepath) as f:
        rush_no_comments_string = f.read()

    removed_comments_str = json.dumps(
        json.loads(rm_js_comments(rush_with_comments_string)), sort_keys=True, indent=2
    )
    expected = json.dumps(json.loads(rush_no_comments_string), sort_keys=True, indent=2)
    assert removed_comments_str == expected
