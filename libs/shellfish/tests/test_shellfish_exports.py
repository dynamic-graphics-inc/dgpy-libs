# -*- coding: utf-8 -*-
from collections import Counter
from pprint import pformat
from types import ModuleType

import pytest

import shellfish

from shellfish import aios, dotenv, fs, process, sh
from shellfish.aios import _path as aiospath
from shellfish.fs import promises as fsp

modules = [shellfish, fs, sh, dotenv, process, fsp, aiospath, aios, fsp]


def _test_module_all_tuple(mod: ModuleType, check_sorted: bool = True) -> None:
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
            print("{} should be:".format(mod_name))  # noqa: T201
            if len(sorted_all_tuple) > 10:
                print("__all__ = " + str(sorted_all_tuple))  # noqa: T201
            else:
                print("__all__ = " + pformat(sorted_all_tuple))  # noqa: T201
            raise e


@pytest.mark.parametrize("mod", modules)
def test_module_exports(mod: ModuleType) -> None:
    check_sorted = mod.__name__ not in {
        "shellfish.sh",
    }

    _test_module_all_tuple(mod, check_sorted=check_sorted)


@pytest.mark.parametrize("member", fs.__all__)
def test_sh_exports_fs_member(member: str) -> None:
    member_val = getattr(sh, member)
    assert member_val is not None, f"{member} is not exported by sh"


def test_everything_in_fs_exported_by_sh() -> None:
    for member_name in fs.__all__:
        member_val = getattr(sh, member_name)
        assert member_val is not None, f"{member_name} is not exported by sh"
