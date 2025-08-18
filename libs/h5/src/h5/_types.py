"""h5._types"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeAlias

import numpy.typing as npt

from h5py import File, Group

__all__ = (
    "FileOrGroup",
    "FsPath",
    "GroupLikeOrFsPath",
    "H5pyAttributesDict",
    "H5pyCompression",
    "H5pyDriver",
    "H5pyMode",
)

if TYPE_CHECKING:
    PathLikeAny: TypeAlias = PathLike[Any]
    PathLikeStr: TypeAlias = PathLike[str]
    PathLikeBytes: TypeAlias = PathLike[bytes]
    PathLikeStrBytes: TypeAlias = PathLikeStr | PathLikeBytes
else:
    PathLikeAny = PathLike
    PathLikeStr = PathLike
    PathLikeBytes = PathLike
    PathLikeStrBytes = PathLike

FsPath: TypeAlias = str | Path | PathLikeAny
FileOrGroup: TypeAlias = File | Group
GroupLikeOrFsPath: TypeAlias = File | Group | FsPath
H5pyCompression: TypeAlias = Literal["gzip", "lzf", "szip"]

"""
h5py mode strings (taken from h5py docstrings)):
```
r        Readonly, file must exist (default)
r+       Read/write, file must exist
w        Create file, truncate if exists
w- or x  Create file, fail if exists
a        Read/write if exists, create otherwise
```
"""
H5pyMode = Literal["r", "r+", "w", "w-", "x", "a"]
H5pyDriver: TypeAlias = (
    Literal["core", "sec2", "direct", "stdio", "mpio", "ros3"] | None
)
H5pyAttributesDict: TypeAlias = dict[str, str | int | float | bool | npt.NDArray[Any]]
