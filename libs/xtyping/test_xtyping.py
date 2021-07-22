# -*- coding: utf-8 -*-
from os import path

import xtyping


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for i in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        print(_filepath)
        if path.exists(_filepath):
            version = (
                [l for l in open(_filepath).read().split("\n") if "version" in l][0]
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version():
    assert xtyping.__version__ == _get_version()


def test_xtyping_all():
    members = dir(xtyping)
    a = xtyping.__all_typing__
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


def test_xtyping_imports():
    for el in xtyping.__all__:
        if el not in {'_typing', '_typing_extensions', 'shed', '_meta'}:
            assert hasattr(xtyping, el)


def test_xtyping_imports_shed():
    missing = set()
    for el in xtyping.__all_shed__:
        if el not in {'_typing', '_typing_extensions', 'shed', '_meta'}:
            if not hasattr(xtyping, el):
                missing.add(el)
    if missing:
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))


def test_xtyping_imports_typing():
    missing = set()
    for el in xtyping.__all_typing__:
        if not hasattr(xtyping, el):
            missing.add(el)
    if missing:
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))


# def test_all_correct_order_no_dups():
# correct_order = [
#     *xtyping.__all_typing__,
#     *xtyping.__all_typing_extensions__,
#     *xtyping.__all_shed__,
# ]
# seen = set()
# seen_add = seen.add
# ordered_no_dupes = [x for x in correct_order if not (x in seen or seen_add(x))]
# assert ordered_no_dupes == xtyping.__all__
# assert len(correct_order) == len(set(correct_order))
