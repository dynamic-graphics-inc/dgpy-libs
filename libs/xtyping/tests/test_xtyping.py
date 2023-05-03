# -*- coding: utf-8 -*-
from os import path
from pprint import pformat
from typing import Tuple

import typing_extensions

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
        and not el.startswith("__")
        and el not in {"_typing", "_typing_extensions", "shed", "_meta", "npt"}
    ]
    xtyping_all = xtyping.__all__
    if not all(el in xtyping_all for el in non_typing_members):
        missing = sorted([el for el in non_typing_members if el not in xtyping_all])
        raise ValueError("MISSING from __all__: {}".format("\n".join(missing)))


def test_xtyping_imports() -> None:
    for el in xtyping.__all__:
        if el not in {"_typing", "_typing_extensions", "shed", "_meta"}:
            assert hasattr(xtyping, el)


def test_xtyping_imports_shed() -> None:
    missing = set()
    for el in xtyping.__all_shed__:
        if el not in {"_typing", "_typing_extensions", "shed", "_meta"} and not hasattr(
            xtyping, el
        ):
            missing.add(el)
    if missing:
        raise ValueError(f"MISSING from __all__: {str(tuple(missing))}")


def test_xtyping_imports_typing() -> None:
    missing = set()
    for el in xtyping.__all_typing__:
        if not hasattr(xtyping, el):
            missing.add(el)
    if missing:
        raise ValueError("MISSING from __all__: {}".format("\n".join(missing)))


def _test_module_all_tuple(
    mod_name: str, mod_all: Tuple[str, ...], check_sorted: bool = True
) -> None:
    assert isinstance(mod_all, tuple), "__all__ should be tuple"
    assert len(set(mod_all)) == len(mod_all)
    if check_sorted:
        sorted_all_tuple = tuple(sorted(mod_all))
        try:
            assert sorted_all_tuple == mod_all
        except AssertionError as e:
            print(f"{mod_name} should be:")  # noqa: T201
            if len(sorted_all_tuple) > 10:
                print("__all__ = " + str(sorted_all_tuple))  # noqa: T201
            else:
                print("__all__ = " + pformat(sorted_all_tuple))  # noqa: T201
            raise e


def test_root_has_everything() -> None:
    xtyping_all_set = set(xtyping.__all__)
    for el in xtyping.__all_typing__:
        assert el in xtyping_all_set
    for el in xtyping.__all_typing_extensions__:
        assert el in xtyping_all_set
    for el in xtyping.__all_shed__:
        assert el in xtyping_all_set


def test_xtyping_has_all_typing_extensions_members():
    all_typing = set(xtyping.__all_typing__)
    typing_extensions_all_list = list(typing_extensions.__all__)
    _typing_extensions_members = (
        set(list(typing_extensions_all_list) + list(xtyping.__all_typing_extensions__))
        - all_typing
        - set(xtyping.__all_typing_extensions_future__)
    )
    _xtyping_all_set = set(xtyping.__all_typing_extensions__) - all_typing
    assert (
        _xtyping_all_set == _typing_extensions_members
    ), "xtyping.__all_typing_extensions__ is missing: {} \n SHOULD BE: \n__all_typing_extensions__ = {}".format(
        tuple(sorted(set(_typing_extensions_members - _xtyping_all_set))),
        tuple(
            sorted(
                set(
                    list(_xtyping_all_set)
                    + list(_typing_extensions_members - _xtyping_all_set)
                )
            )
        ),
    )


def test_xtypting_all_list() -> None:
    _test_module_all_tuple("xtyping._typing.__all__", xtyping.__all_typing__)
    _test_module_all_tuple(
        "xtyping._typing_extensions.__all__", xtyping.__all_typing_extensions__
    )
    _test_module_all_tuple("xtyping.shed.__all__", xtyping.__all_shed__)
    _test_module_all_tuple("xtyping.__all__", xtyping.__all__)


def test_xtyping_shed_all_members() -> None:
    from xtyping import __all_shed__, __all_typing__, __all_typing_extensions__, shed

    builtin_members = {
        "__annotations__",
        "__builtins__",
        "__doc__",
        "__loader__",
        "__name__",
        "__package__",
        "__spec__",
        "__file__",
        "__all__",
        "__cached__",
    }
    shed_all_set = set(__all_shed__)
    tx_all_set = set(__all_typing_extensions__)
    typing_all_set = set(__all_typing__)

    missing_from_all = set()
    for k, _v in vars(shed).items():
        member = k
        if (
            member not in shed_all_set
            and member not in tx_all_set
            and member not in typing_all_set
            and member not in builtin_members
        ):
            missing_from_all.add(member)

    assert len(missing_from_all) == 0, "xtyping.shed is missing: {}".format(
        missing_from_all
    )


def test_all_typing_extensions_reexported() -> None:
    __xtyping_all__ = xtyping.__all__
    xtyping_all_set = set(__xtyping_all__)
    __typing_extensions_all__ = xtyping.__all_typing_extensions__
    for el in [
        t_el
        for t_el in __typing_extensions_all__
        if t_el not in {"Self", "NotRequired", "Required"}
    ]:
        assert el in xtyping_all_set
