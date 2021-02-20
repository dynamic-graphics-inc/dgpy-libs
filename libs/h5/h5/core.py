# -*- coding: utf-8 -*-
"""HDF5 functions, and utils, and generators, OH MY!"""
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Tuple, Union

from h5py import AttributeManager, Dataset, File, Group, __version__ as __h5py_version__
from numpy import float64, int8, ndarray


FsPath = Union[str, Path]

__all__ = [
    "__h5py_version__",
    "h5py_obj_attrs_gen",
    "h5py_obj_dataset_gen",
    "attrs_gen",
    "datasets_gen",
    "datasets_dict",
    "datasets_gen_from_fspath",
    "attrs_dict",
    "attrs_gen_from_fspath",
    "h5_attrs_gen",
    "h5_datasets_gen",
    "h5_datasets_dict",
    "h5_datasets_gen_from_fspath",
    "h5_attrs_dict",
    "h5_attrs_gen_from_fspath",
]


def _fmt_h5_path(head: str, tail: str) -> str:
    """Format function for HDF5-path-strings"""
    return f"{head}/{tail}"


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
            (_fmt_h5_path(h5_path, key), item.attrs)
            for key, item in h5py_obj.items()
            if isinstance(item, (Dataset, Group))
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_attrs_gen(item, _fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def attrs_gen_from_fspath(fspath: FsPath) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    return h5py_obj_attrs_gen(File(str(fspath), mode="r"))


def h5_attrs_gen_from_fspath(fspath: FsPath) -> Iterable[Tuple[str, AttributeManager]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.AttributeManager) tuples

    """
    return h5py_obj_attrs_gen(File(str(fspath), mode="r"))


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
            (_fmt_h5_path(h5_path, key), item)
            for key, item in h5py_obj.items()
            if isinstance(item, Dataset)
        ),
        *(  # Unpack a generator that generates generators recursively
            h5py_obj_dataset_gen(item, _fmt_h5_path(h5_path, key))
            for key, item in h5py_obj.items()
            if isinstance(item, Group)
        ),
    )


def datasets_gen_from_fspath(fspath: str) -> Iterable[Tuple[str, Dataset]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.Dataset) tuples

    """
    return h5py_obj_dataset_gen(File(fspath, mode="r"))


def h5_datasets_gen_from_fspath(fspath: str) -> Iterable[Tuple[str, Dataset]]:
    """Given a fspath to an h5, yield (h5-path, h5py.Dataset) tuples

    Args:
        fspath (str): fspath to h5 format file

    Returns:
        Generator that yields tuples of the form (h5-path, h5py.Dataset) tuples

    """
    return h5py_obj_dataset_gen(File(fspath, mode="r"))


def datasets_gen(h5_obj: Union[FsPath, File, Group]) -> Iterable[Tuple[str, Dataset]]:
    """Return a generator that yields tuples with: (HDF5-path, Dataset)"""
    if isinstance(h5_obj, (str, Path)):
        return h5_datasets_gen_from_fspath(str(h5_obj))
    return h5py_obj_dataset_gen(h5_obj)


def h5_datasets_gen(
    h5_obj: Union[FsPath, File, Group]
) -> Iterable[Tuple[str, Dataset]]:
    """Alias for h5.datasets_gen"""
    return datasets_gen(h5_obj=h5_obj)


def attrs_gen(
    h5_obj: Union[FsPath, File, Group]
) -> Iterable[Tuple[str, AttributeManager]]:
    """Return a generator that yields tuples with: (HDF5-path, HDF5-attr)"""
    if isinstance(h5_obj, (Path, str)):
        return h5_attrs_gen_from_fspath(str(h5_obj))
    return h5py_obj_attrs_gen(h5_obj)


def h5_attrs_gen(
    h5_obj: Union[FsPath, File, Group]
) -> Iterable[Tuple[str, AttributeManager]]:
    """Alias for h5.datasets_gen"""
    return attrs_gen(h5_obj=h5_obj)


def datasets_dict(
    fspath: str,
) -> Dict[str, Union[ndarray, int8, float64]]:
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
    return {
        h5_path: h5_dataset[()]
        for h5_path, h5_dataset in h5py_obj_dataset_gen(File(fspath, mode="r"))
    }


def h5_datasets_dict(
    fspath: str,
) -> Dict[str, Union[ndarray, int8, float64]]:
    """Alias for h5.datasets_dict"""
    return datasets_dict(fspath=fspath)


def attrs_dict(
    fspath: str,
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
    return {
        h5_path: h5_attr
        for h5_path, h5_attr in h5py_obj_attrs_gen(File(fspath, mode="r"))
    }


def h5_attrs_dict(
    fspath: str,
) -> Dict[str, AttributeManager]:
    """Alias for h5.attrs_dict"""
    return attrs_dict(fspath=fspath)
