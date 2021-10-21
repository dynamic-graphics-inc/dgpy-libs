# -*- coding: utf-8 -*-
from os import path

import xtyping


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for _ in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            version = (
                [ln for ln in open(_filepath).read().split("\n") if "version" in ln][0]
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    assert xtyping.__version__ == _get_version()


def test_xtyping_all() -> None:
    members = dir(xtyping)
    non_typing_members = [
        el
        for el in members
        if el not in set(xtyping.__all_typing__)
        and not el.startswith('__')
        and el not in {'_typing', '_typing_extensions', 'shed', '_meta'}
    ]
    xtyping_all = xtyping.__all__
    if not all(el in xtyping_all for el in non_typing_members):
        missing = sorted([el for el in non_typing_members if el not in xtyping_all])
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))


def test_xtyping_imports() -> None:
    for el in xtyping.__all__:
        if el not in {'_typing', '_typing_extensions', 'shed', '_meta'}:
            assert hasattr(xtyping, el)


def test_xtyping_imports_shed() -> None:
    missing = set()
    for el in xtyping.__all_shed__:
        if el not in {'_typing', '_typing_extensions', 'shed', '_meta'}:
            if not hasattr(xtyping, el):
                missing.add(el)
    if missing:
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))


def test_xtyping_imports_typing() -> None:
    missing = set()
    for el in xtyping.__all_typing__:
        if not hasattr(xtyping, el):
            missing.add(el)
    if missing:
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))
