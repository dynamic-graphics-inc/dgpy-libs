# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import Counter
from pprint import pformat
from typing import TYPE_CHECKING, Any

import pytest

import shellfish

from shellfish import _types as shellfish_types, aios, dotenv, fs, process, sh
from shellfish.aios import _path as aiospath
from shellfish.fs import _async as fs_async, promises as fsp

if TYPE_CHECKING:
    from types import ModuleType

modules = [shellfish, fs, sh, dotenv, process, fsp, aiospath, aios, fsp, fs_async]


def _test_module_members_missing_from_all(mod: ModuleType) -> None:
    mod_name = mod.__name__
    members = [e for e in dir(mod) if not e.startswith("_")]
    dunder_all_public = [e for e in mod.__all__ if not e.startswith("_")]
    missing_members = [m for m in dunder_all_public if m not in members]
    assert not missing_members, (
        f"missing members in {mod_name}.__all__: {missing_members}"
    )


def _is_defined_under_shellfish(member: Any, mod: ModuleType = shellfish) -> bool:
    if not hasattr(member, "__module__"):
        return False
    mod_name = member.__module__
    if not isinstance(mod_name, str):
        return False
    return mod_name == mod.__name__ or mod_name.startswith(mod.__name__ + ".")


def _test_module_all_missing_members(mod: ModuleType) -> None:
    mod_name = mod.__name__
    members = [e for e in dir(mod) if not e.startswith("_")]
    dunder_all_public = [e for e in mod.__all__ if not e.startswith("_")]
    missing_all = [
        m
        for m in members
        if m not in dunder_all_public
        and _is_defined_under_shellfish(getattr(mod, m), mod)
    ]
    assert not missing_all, f"missing members in {mod_name}: {missing_all}"


def _test_module_all_tuple(
    mod: ModuleType,
    check_sorted: bool = False,  # now handled by RUF022
) -> None:
    assert hasattr(mod, "__all__"), f"{mod} has no __all__"
    mod_all = getattr(mod, "__all__")  # noqa: B009
    mod_name = mod.__name__
    assert isinstance(mod_all, tuple), "__all__ should be tuple"

    members_count = Counter(mod_all)
    duplicates = [el for el, count in members_count.items() if count > 1]
    assert not duplicates, f"duplicates in __all__: {duplicates}"
    assert len(set(mod_all)) == len(mod_all), "all should be " + str(
        tuple(sorted(set(mod_all)))
    )
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


@pytest.mark.parametrize("mod", modules)
def test_module_exports(mod: ModuleType) -> None:
    _test_module_all_tuple(mod, check_sorted=False)
    _test_module_members_missing_from_all(mod)
    _test_module_all_missing_members(mod)


@pytest.mark.parametrize("member", fs.__all__)
def test_sh_exports_fs_member(member: str) -> None:
    member_val = getattr(sh, member)
    assert member_val is not None, f"{member} is not exported by sh"


@pytest.mark.parametrize("member", shellfish_types.__all__)
def test_shellfish_exports_types_member(member: str) -> None:
    member_val = getattr(shellfish, member)
    assert member_val is not None, f"{member} is not exported by shellfish"
