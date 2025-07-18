from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

import h5
import h5._info as h5info

from h5 import core as h5core

if TYPE_CHECKING:
    from types import ModuleType

H5_ALL_SET = set(h5.__all__)
H5_CORE_ALL_SET = set(h5core.__all__)
H5_INFO_ALL_SET = set(h5info.__all__)


def is_dunder(string: str) -> bool:
    return string.startswith("__") and string.endswith("__")


def obj_module_name(obj: Any) -> Optional[str]:
    return getattr(obj, "__module__", None)


def module_members(
    module: ModuleType, include_dunders: bool = False, include_private: bool = False
) -> List[str]:
    module_name = module.__name__
    members = dict(vars(module).items())
    if not include_dunders:
        members = {key: attr for key, attr in members.items() if not is_dunder(key)}
    if not include_private:
        members = {
            key: attr for key, attr in members.items() if not key.startswith("_")
        }
    return [k for k, v in members.items() if obj_module_name(v) == module_name]


def test_h5_core_exports() -> None:
    members = module_members(h5core)
    missing_members = [el for el in members if el not in H5_CORE_ALL_SET]
    assert not missing_members, f"missing members: {missing_members}"

    incorrectly_exported = [
        el
        for el in H5_CORE_ALL_SET
        if el not in members
        and el
        not in {"File", "Group", "__h5py_version__", "Dataset", "AttributeManager"}
    ]
    assert not incorrectly_exported, (
        f"incorrectly exported members: {incorrectly_exported}"
    )


def test_h5_info_exports() -> None:
    members = module_members(h5info)
    missing_members = [el for el in members if el not in H5_INFO_ALL_SET]
    assert not missing_members, f"missing members: {missing_members}"

    incorrectly_exported = [
        el
        for el in H5_INFO_ALL_SET
        if el not in members
        and el
        not in {"File", "Group", "__h5py_version__", "Dataset", "AttributeManager"}
    ]
    assert not incorrectly_exported, (
        f"incorrectly exported members: {incorrectly_exported}"
    )


def test_h5_exports() -> None:
    exported_from_h5_core = H5_CORE_ALL_SET
    missing_from_h5 = [el for el in exported_from_h5_core if el not in H5_ALL_SET]
    assert not missing_from_h5, f"missing from h5: {missing_from_h5}"

    def try_to_import(member_name: str) -> bool:
        try:
            exec(f"from h5 import {member_name}")
            return True
        except ImportError:
            ...
        return False

    # check that each member is importable from h5
    not_importable = [el for el in H5_ALL_SET if not try_to_import(el)]
    assert not not_importable, f"not importable: {not_importable}"
