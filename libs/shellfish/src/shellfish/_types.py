# -*- coding: utf-8 -*-
from __future__ import annotations

from collections.abc import Mapping, Sequence
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from typing_extensions import Literal

if TYPE_CHECKING:
    PathLikeAny = PathLike[Any]
    PathLikeStr = PathLike[str]
    PathLikeBytes = PathLike[bytes]
    PathLikeStrBytes = Union[PathLikeStr, PathLikeBytes]
else:
    PathLikeAny = PathLike
    PathLikeStr = PathLike
    PathLikeBytes = PathLike
    PathLikeStrBytes = PathLike
FsPath = Union[str, Path, PathLikeAny]
PopenArg = Union[str, bytes, PathLikeStrBytes]
PopenArgv = Sequence[PopenArg]
PopenArgs = Union[bytes, str, PopenArgv]
PopenEnv = Mapping[str, str]
SymlinkType = Union[Literal["dir"], Literal["file"], Literal["junction"], str]

__all__ = (
    "FsPath",
    "PathLikeBytes",
    "PathLikeStr",
    "PathLikeStrBytes",
    "PopenArg",
    "PopenArgs",
    "PopenArgv",
    "PopenEnv",
    "SymlinkType",
)
