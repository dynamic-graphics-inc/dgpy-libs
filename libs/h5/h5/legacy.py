# -*- coding: utf-8 -*-
"""Legacy; to be deprecated"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Tuple, TypeVar, Union
from warnings import warn

from typing_extensions import ParamSpec

from h5.core import (
    attrs_dict,
    attrs_gen,
    attrs_gen_from_fspath,
    datasets_dict,
    datasets_gen,
    datasets_gen_from_fspath,
)

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt

    from h5py import AttributeManager, Dataset, File, Group

    from h5._types import FsPath, H5pyAttributesDict

_P = ParamSpec("_P")
_R = TypeVar("_R")

__all__ = (
    "h5_attrs_dict",
    "h5_attrs_gen",
    "h5_attrs_gen_from_fspath",
    "h5_datasets_dict",
    "h5_datasets_gen",
    "h5_datasets_gen_from_fspath",
)


def _h5_deprecated(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    """Decorator to mark a function as deprecated"""

    @wraps(fn)
    def _fn(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        warn(
            f"Function {fn.__name__} is deprecated; move",
            DeprecationWarning,
            stacklevel=2,
        )
        return fn(*args, **kwargs)

    return _fn


@_h5_deprecated
def h5_attrs_dict(fspath: str, h5_path: str = "") -> Dict[str, H5pyAttributesDict]:
    """Alias for h5.attrs_dict"""
    return attrs_dict(h5_obj=fspath, h5_path=h5_path)


@_h5_deprecated
def h5_datasets_dict(
    fspath: str, h5_path: str = ""
) -> Dict[str, Union[npt.NDArray[Any], np.int8, np.float64]]:
    """Alias for h5.datasets_dict"""
    return datasets_dict(h5_obj=fspath, h5_path=h5_path)


@_h5_deprecated
def h5_attrs_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Alias for h5.datasets_gen"""
    return attrs_gen(h5_obj=h5_obj, h5_path=h5_path)


@_h5_deprecated
def h5_attrs_gen_from_fspath(
    fspath: FsPath, h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (FsPath): fspath to h5 format file
        h5_path (str, optional): h5 path to start from. Defaults to "".

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    return attrs_gen_from_fspath(fspath, h5_path)


@_h5_deprecated
def h5_datasets_gen_from_fspath(
    fspath: str, h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file
        h5_path (str, optional): h5 path to start from. Defaults to "".

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.Dataset) tuples

    """
    yield from datasets_gen_from_fspath(fspath, h5_path=h5_path)


@_h5_deprecated
def h5_datasets_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Alias for h5.datasets_gen"""
    return datasets_gen(h5_obj=h5_obj, h5_path=h5_path)
