# -*- coding: utf-8 -*-

from shellfish import sh


def test_done_parse_json():
    print_some_json = "import json; print(json.dumps({'a': 1, 'b': 2, 'c': 3}))"
    done = sh.do(
        f'python -c "{print_some_json}"',
    )
    expected_stdout = '{"a": 1, "b": 2, "c": 3}\n'
    assert done.stdout == expected_stdout
    assert done.parse_json() == {"a": 1, "b": 2, "c": 3}
