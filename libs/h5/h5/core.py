# -*- coding: utf-8 -*-
"""HDF5 functions, and utils, and generators, OH MY!"""
from functools import lru_cache
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple, Union

import numpy as np

from h5py import AttributeManager, Dataset, File, Group, __version__ as __h5py_version__
from typing_extensions import TypeGuard

FsPath = Union[str, Path, PathLike]

__all__ = (
    "__h5py_version__",
    "AttributeManager",
    "Group",
    "File",
    "attrs_dict",
    "attrs_gen",
    "attrs_gen_from_fspath",
    "chain",
    "datasets",
    "datasets_dict",
    "datasets_gen",
    "datasets_gen_from_fspath",
    "groups",
    "groups_gen",
    "groups_gen_from_fspath",
    "h5_attrs_dict",
    "h5_attrs_gen",
    "h5_attrs_gen_from_fspath",
    "h5_datasets_dict",
    "h5_datasets_gen",
    "h5_datasets_gen_from_fspath",
    "h5iter",
    "h5py_obj_attrs_gen",
    "h5py_obj_dataset_gen",
    "h5py_obj_gen",
    "h5py_obj_groups_gen",
    "is_dataset",
    "is_file",
    "is_group",
    "is_h5py_dataset",
    "is_h5py_file",
    "is_h5py_group",
)


def is_h5py_group(obj: Any) -> TypeGuard[Group]:
    """h5py.Group type guard"""
    return isinstance(obj, Group)


def is_h5py_file(obj: Any) -> TypeGuard[File]:
    """h5py.File type guard"""
    return isinstance(obj, File)


def is_h5py_dataset(obj: Any) -> TypeGuard[Dataset]:
    """h5py.Dataset type guard"""
    return isinstance(obj, Dataset)


def is_group(obj: Any) -> TypeGuard[Group]:
    """h5py.Group type guard"""
    return is_h5py_group(obj)


def is_file(obj: Any) -> TypeGuard[File]:
    """h5py.File type guard"""
    return is_h5py_file(obj)


def is_dataset(obj: Any) -> TypeGuard[Dataset]:
    """h5py.Dataset type guard"""
    return is_h5py_dataset(obj)


@lru_cache(maxsize=128)
def _ensure_single_leading_slash(path: str) -> str:
    if path.startswith("/"):
        return _ensure_single_leading_slash(path.lstrip("/"))
    return f"/{path}"


@lru_cache(maxsize=128)
def fmt_h5_path(head: str, tail: str) -> str:
    """Format function for HDF5-path-strings

    Example:
        >>> fmt_h5_path("foo", "bar")
        '/foo/bar'

    """
    return _ensure_single_leading_slash(f"{head}/{tail}")


def h5py_obj_gen(
    h5py_obj: Union[File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Union[Dataset, Group]]]:
    """Recursive h5 datset generator.

    Given an h5 group, which is what one gets after loading an h5 file
    via h5py, this function yields tuples containing (1.) a path (h5_path) to
    a dataset in the group, and (2.) the dataset itself as a numpy array.

    This is a pretty cool method and is the only recursive generator I know of!

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    return chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item) for key, item in h5py_obj.items()
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_attrs_gen(item, fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def h5iter(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Union[Dataset, Group]]]:
    if isinstance(h5_obj, (str, Path, PathLike)):
        with File(h5_obj, "r") as h5_obj:
            yield from h5py_obj_gen(h5_obj, h5_path=h5_path)
    else:
        yield from h5py_obj_gen(h5_obj, h5_path=h5_path)


def h5py_obj_groups_gen(
    h5py_obj: Union[File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Group]]:
    """Recursive h5 datset generator.

    Given an h5 group, which is what one gets after loading an h5 file
    via h5py, this function yields tuples containing (1.) a path (h5_path) to
    a dataset in the group, and (2.) the dataset itself as a numpy array.

    This is a pretty cool method and is the only recursive generator I know of!

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    return chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item)
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_attrs_gen(item, fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def groups_gen_from_fspath(
    fspath: FsPath, h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (FsPath): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    with File(str(fspath), mode="r") as f:
        yield from h5py_obj_groups_gen(f, h5_path)


def h5py_obj_attrs_gen(
    h5py_obj: Union[File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Recursive h5 datset generator.

    Given an h5 group, which is what one gets after loading an h5 file
    via h5py, this function yields tuples containing (1.) a path (h5_path) to
    a dataset in the group, and (2.) the dataset itself as a numpy array.

    This is a pretty cool method and is the only recursive generator I know of!

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    return chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item.attrs)
            for key, item in h5py_obj.items()
            if isinstance(item, (Dataset, Group))
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_attrs_gen(item, fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def attrs_gen_from_fspath(
    fspath: FsPath, h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (FsPath): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    with File(str(fspath), mode="r") as f:
        yield from h5py_obj_attrs_gen(f, h5_path)


def h5_attrs_gen_from_fspath(
    fspath: FsPath, h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (FsPath): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    return attrs_gen_from_fspath(fspath, h5_path)


def h5py_obj_dataset_gen(
    h5py_obj: Union[File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Recursive h5 datset generator.

    Given an h5 group, which is what one gets after loading an h5 file
    via h5py, this function yields tuples containing (1.) a path (h5_path) to
    a dataset in the group, and (2.) the dataset itself as a numpy array.

    This is a pretty cool method and is the only recursive generator I know of!

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.Dataset)

    """
    return chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset
            (fmt_h5_path(h5_path, key), item)
            for key, item in h5py_obj.items()
            if isinstance(item, Dataset)
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_dataset_gen(item, fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def datasets_gen_from_fspath(
    fspath: str, h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.Dataset) tuples

    """
    with File(fspath, mode="r") as h5_obj:
        yield from h5py_obj_dataset_gen(h5_obj, h5_path=h5_path)


def h5_datasets_gen_from_fspath(
    fspath: str, h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.Dataset) tuples

    """
    yield from datasets_gen_from_fspath(fspath, h5_path=h5_path)


def datasets(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Return a generator that yields tuples with: (HDF5-path, Dataset)"""
    if isinstance(h5_obj, (str, Path)):
        yield from h5_datasets_gen_from_fspath(str(h5_obj), h5_path=h5_path)
    else:
        yield from h5py_obj_dataset_gen(h5_obj, h5_path=h5_path)


def datasets_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Return a generator that yields tuples with: (HDF5-path, Dataset)"""
    yield from datasets(h5_obj, h5_path)


def h5_datasets_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, Dataset]]:
    """Alias for h5.datasets_gen"""
    return datasets_gen(h5_obj=h5_obj, h5_path="")


def attrs_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Return a generator that yields tuples with: (HDF5-path, HDF5-attr)"""
    if isinstance(h5_obj, (Path, str)):
        yield from h5_attrs_gen_from_fspath(str(h5_obj), h5_path=h5_path)
    else:
        yield from h5py_obj_attrs_gen(h5_obj, h5_path=h5_path)


def groups(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Return a generator that yields tuples with: (HDF5-path, h5py.Group)"""
    if isinstance(h5_obj, (Path, str)):
        yield from groups_gen_from_fspath(str(h5_obj), h5_path=h5_path)
    else:
        yield from h5py_obj_groups_gen(h5_obj, h5_path=h5_path)


def groups_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Return a generator that yields tuples with: (HDF5-path, h5py.Group)"""
    yield from groups(h5_obj=h5_obj, h5_path=h5_path)


def h5_attrs_gen(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Iterable[Tuple[str, AttributeManager]]:
    """Alias for h5.datasets_gen"""
    return attrs_gen(h5_obj=h5_obj, h5_path=h5_path)


def datasets_dict(
    h5_obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Dict[str, Union[np.ndarray, np.int8, np.float64]]:
    """Load an HDF5 file from a fspath into a dictionary

    Given a fspath this method loads an HDF5 file into a dictionary where the
    key => value pairs are the HDF5-path => HDF5-dataset for the file. This
    method relies on the h5_dataset_gen that is in this very module to
    generate tuples of the form (HDF5-path, HDF5-dataset).

    Args:
        fspath (str): Filepath to an HDF5 format file

    Returns:
        Dictionary with key => value paris of HDF5-path => HDF5-dataset

    """
    if isinstance(h5_obj, (Path, str)):
        with File(h5_obj, mode="r") as h5file:
            datasets_dict = {
                h5_path: h5_dataset[()]
                for h5_path, h5_dataset in h5py_obj_dataset_gen(h5file, h5_path)
            }
            return datasets_dict
    else:
        return {
            h5_path: h5_dataset[()]
            for h5_path, h5_dataset in h5py_obj_dataset_gen(h5_obj, h5_path)
        }


def h5_datasets_dict(
    fspath: str, h5_path: str = ""
) -> Dict[str, Union[np.ndarray, np.int8, np.float64]]:
    """Alias for h5.datasets_dict"""
    return datasets_dict(h5_obj=fspath, h5_path=h5_path)


def attrs_dict(
    h5obj: Union[FsPath, File, Group], h5_path: str = ""
) -> Dict[str, AttributeManager]:
    """Load an HDF5 file from a fspath into a dictionary

    Given a fspath this method loads an HDF5 file into a dictionary where the
    key => value pairs are the HDF5-path => HDF5-dataset for the file. This
    method relies on the h5_dataset_gen that is in this very module to
    generate tuples of the form (HDF5-path, HDF5-dataset).

    Args:
        fspath (str): Filepath to an HDF5 format file

    Returns:
        Dictionary with key => value paris of HDF5-path => HDF5-dataset

    """
    if isinstance(h5obj, (Path, str)):
        with File(str(h5obj), mode="r") as h5file:
            return attrs_dict(h5obj=h5file, h5_path=h5_path)
    return {k: {**v} for k, v in h5py_obj_attrs_gen(h5obj, h5_path=h5_path)}


def h5_attrs_dict(fspath: str, h5_path: str = "") -> Dict[str, AttributeManager]:
    """Alias for h5.attrs_dict"""
    return attrs_dict(h5obj=fspath, h5_path=h5_path)
