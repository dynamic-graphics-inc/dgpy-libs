# -*- coding: utf-8 -*-
from __future__ import annotations

from collections.abc import Mapping, Sequence
from os import PathLike
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Literal, TypeAlias

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
PopenArg: TypeAlias = str | bytes | PathLikeStrBytes
PopenArgv: TypeAlias = Sequence[PopenArg]
PopenArgs: TypeAlias = bytes | str | PopenArgv
PopenEnv: TypeAlias = Mapping[str, str]
SymlinkType: TypeAlias = Literal["dir"] | Literal["file"] | Literal["junction"] | str
STDIN: TypeAlias = bytes | str | None
STDIO: TypeAlias = int | bytes | IO[Any] | None

__all__ = (
    "STDIN",
    "STDIO",
    "FsPath",
    "PathLikeAny",
    "PathLikeBytes",
    "PathLikeStr",
    "PathLikeStrBytes",
    "PopenArg",
    "PopenArgs",
    "PopenArgv",
    "PopenEnv",
    "SymlinkType",
)
