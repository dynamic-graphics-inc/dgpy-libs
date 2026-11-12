# -*- coding: utf-8 -*-
from __future__ import annotations

import inspect
import pickle
import typing

from typing import AnyStr

import pytest

import fmts

from fmts import anystr, anystr2anystr

_ANYSTR2ANYSTR_FUNCS = (
    fmts.camel2snake,
    fmts.pascal2camel,
    fmts.snake2camel,
    fmts.pascal2snake,
    fmts.kebab2pascal,
)
_ANYSTR_FUNCS = (fmts.is_snake, fmts.t9_str, fmts.t9)


@pytest.mark.parametrize("fn", _ANYSTR2ANYSTR_FUNCS, ids=lambda f: f.__name__)
def test_anystr2anystr_preserves_str_and_bytes(fn: typing.Any) -> None:
    as_str = fn("fooBar_baz-qux")
    as_bytes = fn(b"fooBar_baz-qux")
    assert isinstance(as_str, str)
    assert isinstance(as_bytes, bytes)
    assert as_bytes == as_str.encode()


@pytest.mark.parametrize(
    "fn", _ANYSTR2ANYSTR_FUNCS + _ANYSTR_FUNCS, ids=lambda f: f.__name__
)
def test_decorated_metadata(fn: typing.Any) -> None:
    assert fn.__module__ == "fmts"
    assert fn.__qualname__ == fn.__name__
    assert fn.__doc__


@pytest.mark.parametrize("fn", _ANYSTR2ANYSTR_FUNCS, ids=lambda f: f.__name__)
def test_anystr2anystr_runtime_signature(fn: typing.Any) -> None:
    sig = inspect.signature(fn)
    assert str(sig) == "(string: 'AnyStr') -> 'AnyStr'"
    hints = typing.get_type_hints(fn)
    assert hints == {"string": AnyStr, "return": AnyStr}


@pytest.mark.parametrize(
    "fn", _ANYSTR2ANYSTR_FUNCS + _ANYSTR_FUNCS, ids=lambda f: f.__name__
)
def test_decorated_funcs_pickle(fn: typing.Any) -> None:
    roundtripped = pickle.loads(pickle.dumps(fn))
    assert roundtripped is fn


def test_anystr_returns_fn_result_unchanged_for_bytes() -> None:
    assert fmts.t9_str(b"abc") == "222"
    assert fmts.is_snake(b"snake_case") is True


def test_decorators_on_local_function() -> None:
    def shout(string: str) -> str:
        """shout it"""
        return string.upper()

    def is_loud(string: str) -> bool:
        return string == string.upper()

    shout_any = anystr2anystr(shout)
    is_loud_any = anystr(is_loud)
    assert shout_any("a") == "A"
    assert shout_any(b"a") == b"A"
    assert shout_any.__doc__ == "shout it"
    assert is_loud_any(b"A") is True
    assert is_loud_any("a") is False


@pytest.mark.parametrize(
    ("template", "value", "expected"),
    [
        ("t", "v", "v"),
        ("t", b"v", "v"),
        (b"t", "v", b"v"),
        (b"t", b"v", b"v"),
    ],
)
def test_like(template: typing.Any, value: str | bytes, expected: str | bytes) -> None:
    assert fmts._like(template, value) == expected


@pytest.mark.parametrize(
    ("fn", "arg", "expected"),
    [
        (fmts.snake2pascal, "a1b_c", "A1BC"),
        (fmts.snake2pascal, b"a1b_c", b"A1bC"),
        (fmts.ensure_trailing_newline, "\nfoo", "foo\n"),
        (fmts.ensure_trailing_newline, b"\nfoo", b"\nfoo\n"),
        (fmts.indent, b"a\nb", b"    a\n    b"),
        (fmts.indent, "a\nb", "    a\n    b"),
    ],
)
def test_anystr_functions_behavior(
    fn: typing.Any, arg: str | bytes, expected: str | bytes
) -> None:
    assert fn(arg) == expected
