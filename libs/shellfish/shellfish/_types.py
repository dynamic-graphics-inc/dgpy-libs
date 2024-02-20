# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from typing import TYPE_CHECKING, Mapping, Sequence, Union

from typing_extensions import Literal

from xtyping import FsPath as FsPath

if TYPE_CHECKING:
    PathLikeStr = os.PathLike[str]
    PathLikeBytes = os.PathLike[bytes]
    PathLikeStrBytes = Union[PathLikeStr, PathLikeBytes]
else:
    PathLikeStr = os.PathLike
    PathLikeBytes = os.PathLike
    PathLikeStrBytes = os.PathLike

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
