# -*- coding: utf-8 -*-
"""h5.dev ~ Under construction!"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain
from os import path
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)

import h5py
import numpy as np

from h5py import File, Group

from h5.core import FsPath

FileOrGroup = Union[File, Group]
MaybeFileOrGroup = Union[File, Group, FsPath]
TH5Group = TypeVar("TH5Group", bound="H5Group")
H5pyCompression = Literal["gzip", "lzf", "szip"]


def tuple_split(stringl: str, sep: str = "/") -> Tuple[str, ...]:
    return tuple(stringl.split(sep))


def h5path_split(h5path: str) -> Tuple[str, ...]:
    """Split h5path into parent path and name"""
    if h5path == "" or h5path == "/":
        return tuple(
            "",
        )
    return tuple_split(h5path)


class H5DatasetDict(TypedDict):
    h5type: Literal["dataset"]
    attrs: Dict[str, Any]
    key: str
    shape: Tuple[int, ...]
    ndim: int
    dtype: str
    dtype_str: str
    size: int
    nbytes: int
    compression: Optional[H5pyCompression]
    compression_opts: Optional[Union[Tuple[int, int], int]]
    maxshape: Optional[Tuple[int, ...]]
    chunks: Optional[Tuple[int, ...]]


class H5GroupDict(TypedDict):
    h5type: Literal["group"]
    key: str
    groups: Dict[str, H5GroupDict]
    attrs: Dict[str, Any]
    datasets: Dict[str, H5DatasetDict]


class H5FileDict(TypedDict):
    h5type: Literal["file"]
    fspath: str
    fssize: int
    key: str
    groups: Dict[str, H5GroupDict]
    attrs: Dict[str, Any]
    datasets: Dict[str, H5DatasetDict]


class H5GroupDumpDict(TypedDict):
    h5type: Literal["group"]
    key: str
    groups: List[str]
    attrs: Dict[str, Any]
    datasets: List[str]


class H5FileDumpDict(TypedDict):
    h5type: Literal["file"]
    fspath: str
    fssize: int
    key: str
    groups: List[str]
    attrs: Dict[str, Any]
    datasets: List[str]


H5TypedDict = Union[H5DatasetDict, H5GroupDict, H5FileDict]
TTypedDict = TypeVar("TTypedDict", bound=H5TypedDict)


class H5ABC(ABC):
    key: str

    @abstractmethod
    def dict(self) -> Any:
        ...

    # abstyract prop
    @property
    @abstractmethod
    def name(self) -> str:
        return self.key


class H5Mixin(H5ABC):
    attrs: Dict[str, Any]

    def attributes_unnumpy(self) -> Dict[str, Any]:
        return {
            k: v.tolist() if isinstance(v, np.ndarray) else v
            for k, v in self.attrs.items()
        }

    def __init__(self, key: str) -> None:
        self.key = key

    @property
    def name(self) -> str:
        return self.key

    @name.setter
    def name(self, value: str) -> None:
        self.key = value

    @property
    def basename(self) -> str:
        return path.basename(self.key)

    @property
    def dirname(self) -> str:
        return path.dirname(self.key)


@dataclass
class H5Dataset(H5Mixin):
    key: str
    attrs: Dict[str, Any]
    shape: Tuple[int, ...]
    ndim: int
    dtype: str
    dtype_str: str
    size: int
    nbytes: int
    h5type: Literal["dataset"] = "dataset"
    compression: Optional[H5pyCompression] = None
    compression_opts: Optional[Union[Tuple[int, int], int]] = None
    maxshape: Optional[Tuple[int, ...]] = None
    chunks: Optional[Tuple[int, ...]] = None

    def dict(self, attributes: bool = True) -> H5DatasetDict:
        return {
            "h5type": self.h5type,
            "attrs": self.attrs if attributes else {},
            "key": self.key,
            "shape": self.shape,
            "ndim": self.ndim,
            "dtype": self.dtype,
            "dtype_str": self.dtype_str,
            "size": self.size,
            "nbytes": self.nbytes,
            "compression": self.compression,
            "compression_opts": self.compression_opts,
            "maxshape": self.maxshape,
            "chunks": self.chunks,
        }

    def dump(self, attributes: bool = True) -> H5DatasetDict:
        return self.dict(
            attributes=attributes,
        )

    @classmethod
    def from_h5py_dataset(cls, h5py_dataset: h5py.Dataset) -> H5Dataset:
        return cls(
            h5type="dataset",
            attrs=dict(h5py_dataset.attrs),
            key=h5py_dataset.name,
            size=h5py_dataset.size,
            shape=h5py_dataset.shape,
            ndim=h5py_dataset.ndim,
            dtype=str(h5py_dataset.dtype),
            dtype_str=h5py_dataset.dtype.str,
            nbytes=h5py_dataset.nbytes,
            compression=h5py_dataset.compression,
            compression_opts=h5py_dataset.compression_opts,
            maxshape=h5py_dataset.maxshape,
            chunks=h5py_dataset.chunks,
        )


@dataclass
class H5GroupLike(H5Mixin):
    groups: Dict[str, "H5Group"]
    attrs: Dict[str, Any]
    datasets: Dict[str, H5Dataset]

    def __contains__(self, item: str) -> bool:
        return item in self.groups or item in self.datasets

    def __len__(self) -> int:
        return len(self.groups) + len(self.datasets)

    def __getitem__(self, item: str) -> Union[H5Group, H5Dataset]:
        if item in self.groups:
            return self.groups[item]
        elif item in self.datasets:
            return self.datasets[item]
        raise KeyError(f"{item} not found in {self.key}")

    def get(
        self, item: str, default: Optional[Union[H5Group, H5Dataset]] = None
    ) -> Union[H5Group, H5Dataset]:
        if not default:
            return self[item]
        try:
            return self[item]
        except KeyError as ke:
            if default is None:
                raise ke
            if not isinstance(default, (H5Group, H5Dataset)):
                raise TypeError(
                    f"default must be a H5Group or H5Dataset, not {type(default)}"
                )
            return default

    def _set_dataset(self, key: str, value: H5Dataset) -> None:
        if key in self.groups:
            raise KeyError(f"{key} already exists as a group")
        self.datasets[key] = value

    def _set_group(self, key: str, value: H5Group) -> None:
        if key in self.datasets:
            raise KeyError(f"{key} already exists as a dataset")
        self.groups[key] = value

    def __setitem__(self, key: str, value: Union[H5Group, H5Dataset]) -> None:
        if isinstance(value, H5Group):
            return self._set_group(key, value)
        elif isinstance(value, H5Dataset):
            return self._set_dataset(key, value)
        valid_class_names = (
            H5Group.__class__.__name__,
            H5Dataset.__class__.__name__,
        )
        raise TypeError(
            " ".join(
                (
                    f"Can't set {key} to {value} of type {type(value)};",
                    f"must be one of {valid_class_names}",
                )
            )
        )

    def iter(self, groups: bool = True, datasets: bool = True) -> Iterable[str]:
        if groups and datasets:
            return chain(self.groups.keys(), self.datasets.keys())
        elif groups and not datasets:
            return self.groups.keys()
        elif not groups and datasets:
            return self.datasets.keys()
        raise ValueError("Must set either groups or datasets to True")

    def __iter__(self) -> Iterator[str]:
        yield from self.iter()

    def keys(self, datasets: bool = True, groups: bool = True) -> Iterable[str]:
        if datasets:
            yield from self.datasets.keys()
        if groups:
            yield from self.groups.keys()


@dataclass
class H5Group(H5GroupLike):
    key: str
    h5type: Literal["group"]

    def dict(
        self, attributes: bool = True, datasets: bool = True, groups: bool = True
    ) -> H5GroupDict:
        return {
            "h5type": self.h5type,
            "key": self.key,
            "groups": {
                k: v.dict(attributes=attributes, datasets=datasets, groups=groups)
                for k, v in self.groups.items()
            }
            if groups
            else {},
            "attrs": self.attrs if attributes else {},
            "datasets": {
                k: v.dict(
                    attributes=attributes,
                )
                for k, v in self.datasets.items()
            }
            if datasets
            else {},
        }

    def dump(self, attributes: bool = True) -> H5GroupDumpDict:
        return {
            "h5type": self.h5type,
            "key": self.key,
            "attrs": self.attrs if attributes else {},
            "groups": [k.key for k in self.groups.values()],
            "datasets": [k.name for k in self.datasets.values()],
        }

    def dump_gen(
        self, attributes: bool = True, unnumpy: bool = False
    ) -> Iterable[Union[H5GroupDumpDict, H5DatasetDict]]:
        yield self.dump(attributes=attributes)
        for group in self.groups.values():
            yield from group.dump_gen(attributes=attributes)
        for dataset in self.datasets.values():
            yield dataset.dict(attributes=attributes)

    @classmethod
    def from_h5py_group(cls, h5py_group: h5py.Group) -> H5Group:
        datasets = {}
        groups = {}
        for key, value in h5py_group.items():
            if isinstance(value, h5py.Group):
                groups[key] = H5Group.from_h5py_group(value)
            elif isinstance(value, h5py.Dataset):
                datasets[key] = H5Dataset.from_h5py_dataset(value)
            else:
                raise TypeError(f"Unknown type: {type(value)}")
        attrs = dict(h5py_group.attrs)
        key = h5py_group.name
        return cls(
            h5type="group", key=key, groups=groups, attrs=attrs, datasets=datasets
        )

    @classmethod
    def from_fspath(cls, fspath: str) -> H5Group:
        with h5py.File(fspath, "r") as f:
            return cls.from_h5py_group(f.get("/"))

    def items(
        self, datasets: bool = True, groups: bool = True
    ) -> Iterable[Tuple[str, Union[H5Dataset, H5Group]]]:
        if datasets:
            yield from self.datasets.items()
        if groups:
            yield from self.groups.items()


@dataclass
class H5File(H5GroupLike):
    fspath: str
    fssize: int
    key: str
    groups: Dict[str, H5Group]
    attrs: Dict[str, Any]
    datasets: Dict[str, H5Dataset]
    h5type: Literal["file"]

    @property
    def basename(self) -> str:
        return path.basename(self.fspath)

    @property
    def dirname(self) -> str:
        return path.dirname(self.fspath)

    def dict(
        self, attributes: bool = True, datasets: bool = True, groups: bool = True
    ) -> H5FileDict:
        return {
            "h5type": self.h5type,
            "fspath": self.fspath,
            "fssize": self.fssize,
            "key": self.key,
            "groups": {
                k: v.dict(attributes=attributes, datasets=datasets, groups=groups)
                for k, v in self.groups.items()
            }
            if groups
            else {},
            "attrs": self.attrs if attributes else {},
            "datasets": {
                k: v.dict(attributes=attributes) for k, v in self.datasets.items()
            }
            if datasets
            else {},
        }

    @classmethod
    def from_h5py_file(cls, h5py_group: h5py.File) -> H5File:
        """

        could do with dict-comprehension, but  not readable (imo)

        ```
        datasets_and_groups = {
            obj.name: H5Group.from_h5py_group(obj)
            if isinstance(obj, Group)
            else H5Dataset.from_h5py_dataset(obj)
            for obj in h5py_group.values()
        }
        ```
        """
        datasets = {}
        groups = {}
        for key, value in h5py_group.items():
            if isinstance(value, h5py.Group):
                groups[key] = H5Group.from_h5py_group(value)
            elif isinstance(value, h5py.Dataset):
                datasets[key] = H5Dataset.from_h5py_dataset(value)
            else:
                raise TypeError(f"Unknown type: {type(value)}")
        attrs = dict(h5py_group.attrs)
        key = h5py_group.name
        fssize = path.getsize(h5py_group.file.filename)
        return cls(
            h5type="file",
            key=key,
            groups=groups,
            attrs=attrs,
            datasets=datasets,
            fspath=h5py_group.file.filename,
            fssize=fssize,
        )

    @classmethod
    def from_fspath(cls, fspath: str) -> H5File:
        with h5py.File(fspath, "r") as f:
            return cls.from_h5py_file(f)

    def dump(self, attributes: bool = True) -> H5FileDumpDict:
        return {
            "h5type": self.h5type,
            "fspath": self.fspath,
            "fssize": self.fssize,
            "key": self.key,
            "attrs": self.attrs if attributes else {},
            "groups": [k.key for k in self.groups.values()],
            "datasets": [k.name for k in self.datasets.values()],
        }

    def values(
        self, datasets: bool = True, groups: bool = True
    ) -> Iterable[Union[H5Dataset, H5Group, H5File]]:
        yield self
        if datasets:
            yield from self.datasets.values()
        if groups:
            yield from self.groups.values()

    def items(
        self,
        datasets: bool = True,
        groups: bool = True,
    ) -> Iterable[Tuple[str, Union[H5File, H5Dataset, H5Group]]]:
        if datasets:
            yield from ((val.key, val) for val in self.datasets.values())
        if groups:
            yield from ((val.key, val) for val in self.groups.values())

    def dump_gen(
        self, attributes: bool = True
    ) -> Iterable[Union[H5FileDumpDict, H5GroupDumpDict, H5DatasetDict]]:
        yield self.dump(attributes=attributes)
        for group in self.groups.values():
            yield from group.dump_gen(attributes=attributes)
        for dataset in self.datasets.values():
            yield dataset.dict(attributes=attributes)


def h5py_obj_info(
    obj: Union[h5py.Group, h5py.Dataset, h5py.File]
) -> Union[H5Group, H5Dataset, H5File]:
    if isinstance(obj, h5py.Group):
        return H5Group.from_h5py_group(obj)
    elif isinstance(obj, h5py.Dataset):
        return H5Dataset.from_h5py_dataset(obj)
    elif isinstance(obj, h5py.File):
        return H5File.from_h5py_file(obj.get("/"))
    else:
        raise TypeError(f"Unknown type: {type(obj)}")


def info(
    file: Union[str, Path, h5py.File, h5py.Group, h5py.Dataset]
) -> Union[H5Group, H5Dataset, H5File]:
    if isinstance(file, (str, Path)):
        return H5File.from_fspath(str(file))
    return h5py_obj_info(file)
