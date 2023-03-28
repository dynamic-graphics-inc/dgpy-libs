# -*- coding: utf-8 -*-
"""HDF5 functions, and utils, and generators, OH MY!"""
from functools import lru_cache
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Union

import numpy as np
import numpy.typing as npt

from h5py import AttributeManager, Dataset, File, Group, __version__ as __h5py_version__
from typing_extensions import TypeGuard

FsPath = Union[str, Path, PathLike]
T_GroupLike = Union[Group, File]
T_DatasetOrGroup = Union[Dataset, Group]
T_FsPathOrGroupLike = Union[FsPath, T_GroupLike]


__all__ = (
    "AttributeManager",
    "File",
    "Group",
    "__h5py_version__",
    "attrs_dict",
    "attrs_gen",
    "attrs_gen_from_fspath",
    "datasets",
    "datasets_dict",
    "datasets_gen",
    "datasets_gen_from_fspath",
    "datasets_keys_list",
    "fmt_h5_path",
    "groups",
    "groups_gen",
    "groups_gen_from_fspath",
    "groups_keys_list",
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
    "h5py_obj_keys_gen",
    "is_dataset",
    "is_file",
    "is_fspath",
    "is_group",
    "is_group_like",
    "is_h5py_dataset",
    "is_h5py_file",
    "is_h5py_group",
    "keys_list",
)


def is_fspath(path: Any) -> TypeGuard[FsPath]:
    return isinstance(path, (str, Path, PathLike))


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


def is_group_like(obj: Any) -> TypeGuard[T_GroupLike]:
    return isinstance(obj, (Group, File))


def is_file(obj: Any) -> TypeGuard[File]:
    """h5py.File type guard"""
    return is_h5py_file(obj)


def is_dataset(obj: Any) -> TypeGuard[Dataset]:
    """h5py.Dataset type guard"""
    return is_h5py_dataset(obj)


def _leading_slash(string: str) -> str:
    return f"/{string}"


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
    h5py_obj: Union[File, Group], h5_path: str = "", root: bool = True
) -> Iterable[Tuple[str, Union[Dataset, Group, File]]]:
    """Recursive h5 datset/group generator.


    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    if root:
        yield (h5py_obj.name, h5py_obj)
    yield from chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item) for key, item in h5py_obj.items()
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_gen(item, item.name, root=False)
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def h5py_obj_keys_gen(
    h5py_obj: Union[File, Group], h5_path: str = "", root: bool = True
) -> Iterable[str]:
    """Recursive h5 datset generator.

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    if root:
        yield h5py_obj.name
    yield from chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            # (fmt_h5_path(h5_path, key), item) for key, item in h5py_obj.items()
            item.name
            for item in h5py_obj.values()
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_keys_gen(item, item.name, root=False)
            # fmt_h5_path(h5_path, key))
            for item in h5py_obj.values()
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
    h5py_obj: Union[File, Group], h5_path: str = "", root: bool = True
) -> Iterable[Tuple[str, Group]]:
    """Recursive h5 groups generator.

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    if root:
        yield h5py_obj.name, h5py_obj
    yield from chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item)
            for key, item in h5py_obj.items()
            if isinstance(item, (Group, File))
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_groups_gen(item, fmt_h5_path(h5_path, key), root=False)
            for key, item in h5py_obj.items()
            if isinstance(item, (Group, File))
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
    h5py_obj: Union[File, Group], h5_path: str = "", root: bool = True
) -> Iterable[Tuple[str, AttributeManager]]:
    """Recursive h5py.AttributeManager generator.

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.AttributeManager)

    """
    if root:
        yield (h5py_obj.name, h5py_obj.attrs)

    yield from chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset or Group
            (fmt_h5_path(h5_path, key), item.attrs)
            for key, item in h5py_obj.items()
            if isinstance(item, (Dataset, Group))
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_attrs_gen(item, fmt_h5_path(h5_path, key), root=False)
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

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.Dataset)

    """
    return chain(  # Chain of generators into one generator
        (  # Generator object if the current h5py object is a Dataset
            (item.name, item) for item in h5py_obj.values() if isinstance(item, Dataset)
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_dataset_gen(item, h5_path or item.name)
            for item in h5py_obj.values()
            if isinstance(item, Group)
        ),
    )


def keys_list(h5py_obj: Union[File, Group, FsPath]) -> List[str]:
    """Return a list of all keys/paths for an h5py object.

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.Dataset)

    """
    if is_group(h5py_obj):
        keys = [h5py_obj.name]
        h5py_obj.visit(lambda key: keys.append(_leading_slash(key)))
        return keys
    with File(str(h5py_obj), mode="r") as f:
        return keys_list(f)


def groups_keys_list(h5py_obj: Union[File, Group, FsPath]) -> List[str]:
    if is_group(h5py_obj):
        keys: List[str] = [h5py_obj.name]

        def _fn(key: str, value: Union[File, Group, Dataset]) -> None:
            if is_h5py_group(value):
                keys.append(_leading_slash(key))

        h5py_obj.visititems(_fn)
        return keys

    with File(str(h5py_obj), mode="r") as f:
        return groups_keys_list(f)


def datasets_keys_list(h5py_obj: Union[File, Group, FsPath]) -> List[str]:
    """Return a list of all keys/paths for an h5py object.

    Args:
        h5py_obj: h5-h5py group object
        h5_path: path so far (Default value = "")

    Returns:
        Generator that yields tuples; (h5-path, h5py.Dataset)

    """
    if is_group(h5py_obj):
        keys = []

        def _fn(key: str, value: Union[File, Group, Dataset]) -> None:
            if is_h5py_dataset(value):
                keys.append(_leading_slash(key))

        h5py_obj.visititems(_fn)
        return keys
    with File(str(h5py_obj), mode="r") as f:
        return datasets_keys_list(f)


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
    if isinstance(h5_obj, (str, Path, PathLike)):
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
) -> Dict[str, Union[npt.NDArray[Any], np.int8, np.float64]]:
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
) -> Dict[str, Union[npt.NDArray[Any], np.int8, np.float64]]:
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
