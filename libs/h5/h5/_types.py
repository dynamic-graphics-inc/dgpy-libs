"""h5._types"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union

import numpy.typing as npt

from h5py import File, Group

__all__ = (
    "FileOrGroup",
    "FsPath",
    "H5pyCompression",
    "H5pyDriver",
    "H5pyMode",
    "GroupLikeOrFsPath",
    "H5pyAttributesDict",
)

FsPath = Union[str, Path, PathLike[Any]]
FileOrGroup = Union[File, Group]
GroupLikeOrFsPath = Union[File, Group, FsPath]
H5pyCompression = Literal["gzip", "lzf", "szip"]

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
H5pyDriver = Optional[Literal["core", "sec2", "direct", "stdio", "mpio", "ros3"]]
H5pyAttributesDict = Dict[str, Union[str, int, float, bool, npt.NDArray[Any]]]
