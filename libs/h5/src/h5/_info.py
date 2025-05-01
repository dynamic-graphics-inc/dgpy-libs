# -*- coding: utf-8 -*-
"""h5._info ~ Info objs!"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain
from os import path
from pathlib import Path
from typing import (
    TYPE_CHECKING,
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

if TYPE_CHECKING:
    from h5._types import H5pyCompression

__all__ = (
    "H5ABC",
    "DatasetInfo",
    "DatasetInfoDict",
    "FileInfo",
    "FileInfoDict",
    "FileInfoDumpDict",
    "GroupInfo",
    "GroupInfoDict",
    "GroupInfoDumpDict",
    "GroupLikeInfo",
    "H5Mixin",
    "TTypedDict",
    "T_GroupInfo",
    "h5py_obj_info",
    "info",
)

T_GroupInfo = TypeVar("T_GroupInfo", bound="GroupInfo")


class DatasetInfoDict(TypedDict):
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


class GroupInfoDict(TypedDict):
    h5type: Literal["group"]
    key: str
    groups: Dict[str, GroupInfoDict]
    attrs: Dict[str, Any]
    datasets: Dict[str, DatasetInfoDict]


class FileInfoDict(TypedDict):
    h5type: Literal["file"]
    fspath: str
    fssize: int
    key: str
    groups: Dict[str, GroupInfoDict]
    attrs: Dict[str, Any]
    datasets: Dict[str, DatasetInfoDict]


class GroupInfoDumpDict(TypedDict):
    h5type: Literal["group"]
    key: str
    groups: List[str]
    attrs: Dict[str, Any]
    datasets: List[str]


class FileInfoDumpDict(TypedDict):
    h5type: Literal["file"]
    fspath: str
    fssize: int
    key: str
    groups: List[str]
    attrs: Dict[str, Any]
    datasets: List[str]


H5TypedDict = Union[DatasetInfoDict, GroupInfoDict, FileInfoDict]
TTypedDict = TypeVar("TTypedDict", bound=H5TypedDict)


class H5ABC(ABC):
    key: str

    @abstractmethod
    def dict(self) -> Any: ...

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
class DatasetInfo(H5Mixin):
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

    def dict(self, *, attributes: bool = True) -> DatasetInfoDict:
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

    def dump(self, attributes: bool = True) -> DatasetInfoDict:
        return self.dict(
            attributes=attributes,
        )

    @classmethod
    def from_h5py_dataset(cls, h5py_dataset: h5py.Dataset) -> DatasetInfo:
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
class GroupLikeInfo(H5Mixin):
    groups: Dict[str, "GroupInfo"]
    attrs: Dict[str, Any]
    datasets: Dict[str, DatasetInfo]

    def __contains__(self, item: str) -> bool:
        return item in self.groups or item in self.datasets

    def __len__(self) -> int:
        return len(self.groups) + len(self.datasets)

    def __getitem__(self, item: str) -> Union[GroupInfo, DatasetInfo]:
        if item in self.groups:
            return self.groups[item]
        elif item in self.datasets:
            return self.datasets[item]
        raise KeyError(f"{item} not found in {self.key}")

    def get(
        self, item: str, default: Optional[Union[GroupInfo, DatasetInfo]] = None
    ) -> Union[GroupInfo, DatasetInfo]:
        if not default:
            return self[item]
        try:
            return self[item]
        except KeyError as ke:
            if not isinstance(default, (GroupInfo, DatasetInfo)):
                raise TypeError(
                    f"default must be a H5Group or H5Dataset, not {type(default)}"
                ) from ke
            return default

    def _set_dataset(self, key: str, value: DatasetInfo) -> None:
        if key in self.groups:
            raise KeyError(f"{key} already exists as a group")
        self.datasets[key] = value

    def _set_group(self, key: str, value: GroupInfo) -> None:
        if key in self.datasets:
            raise KeyError(f"{key} already exists as a dataset")
        self.groups[key] = value

    def __setitem__(self, key: str, value: Union[GroupInfo, DatasetInfo]) -> None:
        if isinstance(value, GroupInfo):
            return self._set_group(key, value)
        elif isinstance(value, DatasetInfo):
            return self._set_dataset(key, value)
        valid_class_names = (
            GroupInfo.__class__.__name__,
            DatasetInfo.__class__.__name__,
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
class GroupInfo(GroupLikeInfo):
    key: str
    h5type: Literal["group"]

    def dict(
        self, *, attributes: bool = True, datasets: bool = True, groups: bool = True
    ) -> GroupInfoDict:
        return {
            "h5type": self.h5type,
            "key": self.key,
            "groups": (
                {
                    k: v.dict(attributes=attributes, datasets=datasets, groups=groups)
                    for k, v in self.groups.items()
                }
                if groups
                else {}
            ),
            "attrs": self.attrs if attributes else {},
            "datasets": (
                {
                    k: v.dict(
                        attributes=attributes,
                    )
                    for k, v in self.datasets.items()
                }
                if datasets
                else {}
            ),
        }

    def dump(self, attributes: bool = True) -> GroupInfoDumpDict:
        return {
            "h5type": self.h5type,
            "key": self.key,
            "attrs": self.attrs if attributes else {},
            "groups": [k.key for k in self.groups.values()],
            "datasets": [k.name for k in self.datasets.values()],
        }

    def dump_gen(
        self, attributes: bool = True, unnumpy: bool = False
    ) -> Iterable[Union[GroupInfoDumpDict, DatasetInfoDict]]:
        yield self.dump(attributes=attributes)
        for group in self.groups.values():
            yield from group.dump_gen(attributes=attributes)
        for dataset in self.datasets.values():
            yield dataset.dict(attributes=attributes)

    @classmethod
    def from_h5py_group(cls, h5py_group: h5py.Group) -> GroupInfo:
        datasets = {}
        groups = {}
        for key, value in h5py_group.items():
            if isinstance(value, h5py.Group):
                groups[key] = GroupInfo.from_h5py_group(value)
            elif isinstance(value, h5py.Dataset):
                datasets[key] = DatasetInfo.from_h5py_dataset(value)
            else:
                raise TypeError(f"Unknown type: {type(value)}")
        attrs = dict(h5py_group.attrs)
        key = h5py_group.name
        return cls(
            h5type="group", key=key, groups=groups, attrs=attrs, datasets=datasets
        )

    @classmethod
    def from_fspath(cls, fspath: str) -> GroupInfo:
        with h5py.File(fspath, "r") as f:
            return cls.from_h5py_group(f.get("/"))

    def items(
        self, datasets: bool = True, groups: bool = True
    ) -> Iterable[Tuple[str, Union[DatasetInfo, GroupInfo]]]:
        if datasets:
            yield from self.datasets.items()
        if groups:
            yield from self.groups.items()


@dataclass
class FileInfo(GroupLikeInfo):
    fspath: str
    fssize: int
    key: str
    groups: Dict[str, GroupInfo]
    attrs: Dict[str, Any]
    datasets: Dict[str, DatasetInfo]
    h5type: Literal["file"]

    @property
    def basename(self) -> str:
        return path.basename(self.fspath)

    @property
    def dirname(self) -> str:
        return path.dirname(self.fspath)

    def dict(
        self, *, attributes: bool = True, datasets: bool = True, groups: bool = True
    ) -> FileInfoDict:
        return {
            "h5type": self.h5type,
            "fspath": self.fspath,
            "fssize": self.fssize,
            "key": self.key,
            "groups": (
                {
                    k: v.dict(attributes=attributes, datasets=datasets, groups=groups)
                    for k, v in self.groups.items()
                }
                if groups
                else {}
            ),
            "attrs": self.attrs if attributes else {},
            "datasets": (
                {k: v.dict(attributes=attributes) for k, v in self.datasets.items()}
                if datasets
                else {}
            ),
        }

    @classmethod
    def from_h5py_file(cls, h5py_group: h5py.File) -> FileInfo:
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
                groups[key] = GroupInfo.from_h5py_group(value)
            elif isinstance(value, h5py.Dataset):
                datasets[key] = DatasetInfo.from_h5py_dataset(value)
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
    def from_fspath(cls, fspath: str) -> FileInfo:
        with h5py.File(fspath, "r") as f:
            return cls.from_h5py_file(f)

    def dump(self, attributes: bool = True) -> FileInfoDumpDict:
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
    ) -> Iterable[Union[DatasetInfo, GroupInfo, FileInfo]]:
        yield self
        if datasets:
            yield from self.datasets.values()
        if groups:
            yield from self.groups.values()

    def items(
        self,
        datasets: bool = True,
        groups: bool = True,
    ) -> Iterable[Tuple[str, Union[FileInfo, DatasetInfo, GroupInfo]]]:
        if datasets:
            yield from ((val.key, val) for val in self.datasets.values())
        if groups:
            yield from ((val.key, val) for val in self.groups.values())

    def dump_gen(
        self, attributes: bool = True
    ) -> Iterable[Union[FileInfoDumpDict, GroupInfoDumpDict, DatasetInfoDict]]:
        yield self.dump(attributes=attributes)
        for group in self.groups.values():
            yield from group.dump_gen(attributes=attributes)
        for dataset in self.datasets.values():
            yield dataset.dict(attributes=attributes)


def h5py_obj_info(
    obj: Union[h5py.Group, h5py.Dataset, h5py.File],
) -> Union[GroupInfo, DatasetInfo, FileInfo]:
    if isinstance(obj, h5py.Group):
        return GroupInfo.from_h5py_group(obj)
    elif isinstance(obj, h5py.Dataset):
        return DatasetInfo.from_h5py_dataset(obj)
    elif isinstance(obj, h5py.File):
        return FileInfo.from_h5py_file(obj.get("/"))
    else:
        raise TypeError(f"Unknown type: {type(obj)}")


def info(
    file: Union[str, Path, h5py.File, h5py.Group, h5py.Dataset],
) -> Union[GroupInfo, DatasetInfo, FileInfo]:
    if isinstance(file, (str, Path)):
        return FileInfo.from_fspath(str(file))
    return h5py_obj_info(file)
