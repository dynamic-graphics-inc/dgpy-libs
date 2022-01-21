from pprint import pformat

import pytest

import shellfish

from shellfish import aios, dotenv, fs, process, sh
from shellfish.aios import _path as aiospath
from shellfish.fs import promises as fsp

modules = [shellfish, fs, sh, dotenv, process, fsp, aiospath, aios]


def _test_module_all_tuple(mod, check_sorted: bool = True) -> None:
    assert hasattr(mod, "__all__"), f"{mod} has no __all__"
    mod_all = getattr(mod, "__all__")
    mod_name = mod.__name__
    assert isinstance(mod_all, tuple), "__all__ should be tuple"
    assert len(set(mod_all)) == len(mod_all), "all should be " + str(
        tuple(sorted(set(mod_all)))
    )
    if check_sorted:
        sorted_all_tuple = tuple(sorted(mod_all))
        try:
            assert sorted_all_tuple == mod_all
        except AssertionError as e:
            print("{} should be:".format(mod_name))  # noqa: T001
            if len(sorted_all_tuple) > 10:
                print("__all__ = " + str(sorted_all_tuple))  # noqa: T001
            else:
                print("__all__ = " + pformat(sorted_all_tuple))  # noqa: T001
            raise e


@pytest.mark.parametrize("mod", modules)
def test_module_exports(mod) -> None:
    _test_module_all_tuple(mod, check_sorted=True)
