# -*- coding: utf-8 -*-
"""HDF5 functions, and utils, and generators, OH MY!"""
from h5._meta import __version__
from h5.core import (
    __h5py_version__,
    attrs_dict,
    attrs_gen,
    attrs_gen_from_fspath,
    datasets_dict,
    datasets_gen,
    datasets_gen_from_fspath,
    h5_attrs_dict,
    h5_attrs_gen,
    h5_attrs_gen_from_fspath,
    h5_datasets_dict,
    h5_datasets_gen,
    h5_datasets_gen_from_fspath,
    h5py_obj_attrs_gen,
    h5py_obj_dataset_gen,
)


__all__ = [
    "__version__",
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
