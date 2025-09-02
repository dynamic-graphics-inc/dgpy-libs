# -*- coding: utf-8 -*-
"""xtyping = typing | typing_extensions | misc"""

from __future__ import annotations

from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Literal,
    Optional,
    TypeAlias,
    Union,
    __all__ as __all_typing,
)

from annotated_types import (
    __all__ as __all_annotated_types,
    __version__ as __version_annotated_types__,
)
from typing_extensions import (
    Any,
    ParamSpec,
    TypeVar,
    __all__ as __all_typing_extensions,
)

# =============================================================================
# DEPRECATED TYPES
# =============================================================================
__DEPRECATED_TYPES__: tuple[str, ...] = ("ByteString",)

# =============================================================================
# __all__
# =============================================================================
__all_typing__: tuple[str, ...] = tuple(
    e for e in __all_typing if e not in __DEPRECATED_TYPES__
)
__all_typing_extensions__: tuple[str, ...] = tuple({
    *__all_typing_extensions,
    *__all_typing__,
})
__all_typing_extensions_future__: tuple[str, ...] = ()
__all_annotated_types__: tuple[str, ...] = tuple(
    e for e in __all_annotated_types if e != "__version__"
)

# =============================================================================
# Aliases
# =============================================================================
D = dict
Lit = Literal
L = Literal
Ls = list
Opt = Optional
U = Union
Seq = Sequence

# =============================================================================
# LITERAL(LY)  # noqa: ERA001
# =============================================================================
TRUE = Literal[True]
FALSE = Literal[False]
ZERO = Literal[0]
ONE = Literal[1]

# =============================================================================
# NONE
# =============================================================================
null = Null = None.__class__
NoneType: TypeAlias = None.__class__
NoneStr: TypeAlias = str | None
NoneBytes: TypeAlias = bytes | None
StrBytes: TypeAlias = str | bytes
NoneStrBytes: TypeAlias = str | bytes | None

# =============================================================================
# NUMBER
# =============================================================================
Number: TypeAlias = Union[float, int]  # float or int
Flint: TypeAlias = Union[float, int]  # float or int

# =============================================================================
# TypeVars
# =============================================================================
T = TypeVar("T")  # Any type.
_T = TypeVar("_T")
KT = TypeVar("KT")  # Key type.
_KT = TypeVar("_KT")
VT = TypeVar("VT")  # Value type.
_VT = TypeVar("_VT")
KeyT = TypeVar("KeyT")  # Key type.
ValT = TypeVar("ValT")  # Value type.
KeyType = TypeVar("KeyType")  # Key type.
ValType = TypeVar("ValType")  # Value type.
El = TypeVar("El")
Element = TypeVar("Element")
R = TypeVar("R")
RT = TypeVar("RT")
_R = TypeVar("_R")
_RT = TypeVar("_RT")
ReturnT = TypeVar("ReturnT")
ReturnType = TypeVar("ReturnType")
N = TypeVar("N", float, int)
DT = TypeVar("DT")
_DT = TypeVar("_DT")
T_Retval = TypeVar("T_Retval")

# =============================================================================
# ParamSpec
# =============================================================================
P = ParamSpec("P")
PT = ParamSpec("PT")
T_ParamSpec = ParamSpec("T_ParamSpec")


# =============================================================================
# Covariant TypeVars
# =============================================================================
KT_co = TypeVar("KT_co", covariant=True)
T_co = TypeVar("T_co", covariant=True)  # Any type covariant containers.
V_co = TypeVar("V_co", covariant=True)  # Any type covariant containers.
VT_co = TypeVar("VT_co", covariant=True)  # Value type covariant containers.

_KT_co = TypeVar("_KT_co", covariant=True)
_T_co = TypeVar("_T_co", covariant=True)
_V_co = TypeVar("_V_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

# =============================================================================
# Contravariant TypeVars
# =============================================================================
T_contra = TypeVar("T_contra", contravariant=True)  # Ditto contravariant.
_T_contra = TypeVar("_T_contra", contravariant=True)  # Ditto contravariant.
VT_contra = TypeVar("VT_contra", contravariant=True)
_VT_contra = TypeVar("_VT_contra", contravariant=True)
KT_contra = TypeVar("KT_contra", contravariant=True)
_KT_contra = TypeVar("_KT_contra", contravariant=True)


class StringEnum(str, Enum):
    """String enum base class -- based on usage with pydantic"""


class StrEnum(StringEnum):
    """Alias for StringEnum"""


# =============================================================================
# Function-y
# =============================================================================
AnyCallable = Callable[..., Any]
AnyAsyncCallable: TypeAlias = Callable[..., Awaitable[Any]]
FuncType: TypeAlias = Callable[..., Any]
AsyncFuncType: TypeAlias = Callable[..., Awaitable[Any]]
F = TypeVar("F", bound=AnyCallable)
FN = TypeVar("FN", bound=AnyCallable)
Fn = TypeVar("Fn", bound=AnyCallable)
AF = TypeVar("AF", bound=Awaitable[Any])
AFn = TypeVar("AFn", bound=Awaitable[Any])
AsyncFn = TypeVar("AsyncFn", bound=Awaitable[Any])

# =============================================================================
# STDIO/STDIN
# =============================================================================
STDIO: TypeAlias = Union[int, bytes, IO[Any], None]
STDIN: TypeAlias = Union[bytes, str, None]

# =============================================================================
# LISTS
# =============================================================================
ListAny: TypeAlias = list[Any]
ListT: TypeAlias = list[T]
ListStr: TypeAlias = list[str]
ListInt: TypeAlias = list[int]
ListFloat: TypeAlias = list[float]
ListNumber: TypeAlias = list[Number]

# =============================================================================
# LISTLESS AKA iterables
# =============================================================================
IterableAny: TypeAlias = Iterable[Any]
IterableT: TypeAlias = Iterable[T]
IterableStr: TypeAlias = Iterable[str]
IterableInt: TypeAlias = Iterable[int]
IterableFloat: TypeAlias = Iterable[float]
IterableNumber: TypeAlias = Iterable[Number]

# =============================================================================
# DICT
# =============================================================================
DictAny: TypeAlias = dict[Any, Any]
DictStr: TypeAlias = dict[str, str]
DictInt: TypeAlias = dict[int, int]
DictFloat: TypeAlias = dict[float, float]
DictNumber: TypeAlias = dict[Number, Number]
DictAnyAny: TypeAlias = dict[Any, Any]
DictStrStr: TypeAlias = dict[str, str]
DictIntInt: TypeAlias = dict[int, int]
DictFloatFloat: TypeAlias = dict[float, float]
DictNumberNumber: TypeAlias = dict[Number, Number]
DictStrAny: TypeAlias = dict[str, Any]
DictStrInt: TypeAlias = dict[str, int]

# =============================================================================
# SET
# =============================================================================
SetAny = set[Any]
SetT = set[T]
SetStr = set[str]
SetInt = set[int]
SetFloat = set[float]
SetNumber = set[Number]

# =============================================================================
# MISC
# =============================================================================
IntStr: TypeAlias = Union[int, str]
Bytes: TypeAlias = Union[bytes, bytearray]
Txt: TypeAlias = Union[bytes, str]
EnvMap: TypeAlias = Union[Mapping[bytes, Txt], Mapping[str, Txt]]
AnyIterable: TypeAlias = Union[Iterable[T], AsyncIterable[T]]
AnyIterator: TypeAlias = Union[Iterator[T], AsyncIterator[T]]
AnyFunction: TypeAlias = Union[Callable[..., R], Callable[..., Awaitable[R]]]
StrIntFloat: TypeAlias = Union[str, float, int]
HrTime: TypeAlias = tuple[int, int]  # node/js hrtime type annotation

# =============================================================================
# Function type annotations
# =============================================================================
if TYPE_CHECKING:
    PathLikeAny: TypeAlias = PathLike[Any]
    PathLikeStr: TypeAlias = PathLike[str]
    PathLikeBytes: TypeAlias = PathLike[bytes]
    PathLikeStrBytes: TypeAlias = Union[PathLikeStr, PathLikeBytes]
else:
    PathLikeAny: TypeAlias = PathLike
    PathLikeStr: TypeAlias = PathLike
    PathLikeBytes: TypeAlias = PathLike
    PathLikeStrBytes: TypeAlias = PathLike
FsPath: TypeAlias = Union[str, Path, PathLikeAny]
FsPathLike: TypeAlias = "PathLike[Any]"
EnvType: TypeAlias = Union[Mapping[bytes, Txt], Mapping[str, Txt]]
CmdArgs: TypeAlias = Union[bytes, str, Sequence[str], Sequence[FsPath]]
CmdArgsType: TypeAlias = Union[bytes, str, Sequence[str], Sequence[FsPath]]

# =============================================================================
# LISTLESS
# =============================================================================
ArrShape: TypeAlias = tuple[int, ...]
ArrayShape: TypeAlias = tuple[int, ...]
ShapeType: TypeAlias = tuple[int, ...]
TupleStrs: TypeAlias = tuple[str, ...]
ListListStr: TypeAlias = list[list[str]]
TupleStrStr: TypeAlias = tuple[str, str]

# =============================================================================
# OPT
# =============================================================================
OptionalInt: TypeAlias = int | None
OptInt: TypeAlias = int | None
OptionalStr: TypeAlias = str | None
OptStr: TypeAlias = str | None
OptionalFloat: TypeAlias = float | None
OptFloat: TypeAlias = float | None

# =============================================================================
# JSON
# =============================================================================
JsonPrimitive: TypeAlias = Union[bool, int, float, str, None]
Json: TypeAlias = Union[dict[str, "Json"], list["Json"], str, int, float, bool, None]
JsonT: TypeAlias = Union[dict[str, "JsonT"], list["JsonT"], str, int, float, bool, None]
JsonDictT: TypeAlias = dict[str, Any]
JsonListT: TypeAlias = list[Any]
JsonObjT: TypeAlias = dict[str, Any]
JsonArrT: TypeAlias = list[Any]

# =============================================================================
# FROM TYPESHED
# =============================================================================
StrPath: TypeAlias = Union[str, "PathLike[str]"]  # stable
BytesPath: TypeAlias = Union[bytes, "PathLike[bytes]"]  # stable
StrOrBytesPath: TypeAlias = Union[str, bytes, "PathLike[Any]"]

OpenTextModeUpdating: TypeAlias = Literal[
    "r+",
    "+r",
    "rt+",
    "r+t",
    "+rt",
    "tr+",
    "t+r",
    "+tr",
    "w+",
    "+w",
    "wt+",
    "w+t",
    "+wt",
    "tw+",
    "t+w",
    "+tw",
    "a+",
    "+a",
    "at+",
    "a+t",
    "+at",
    "ta+",
    "t+a",
    "+ta",
    "x+",
    "+x",
    "xt+",
    "x+t",
    "+xt",
    "tx+",
    "t+x",
    "+tx",
]
OpenTextModeWriting: TypeAlias = Literal[
    "w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"
]
OpenTextModeReading: TypeAlias = Literal[
    "r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"
]
OpenTextMode: TypeAlias = Union[
    OpenTextModeUpdating, OpenTextModeWriting, OpenTextModeReading
]
OpenBinaryModeUpdating: TypeAlias = Literal[
    "rb+",
    "r+b",
    "+rb",
    "br+",
    "b+r",
    "+br",
    "wb+",
    "w+b",
    "+wb",
    "bw+",
    "b+w",
    "+bw",
    "ab+",
    "a+b",
    "+ab",
    "ba+",
    "b+a",
    "+ba",
    "xb+",
    "x+b",
    "+xb",
    "bx+",
    "b+x",
    "+bx",
]
OpenBinaryModeWriting: TypeAlias = Literal["wb", "bw", "ab", "ba", "xb", "bx"]
OpenBinaryModeReading: TypeAlias = Literal[
    "rb", "br", "rbU", "rUb", "Urb", "brU", "bUr", "Ubr"
]
OpenBinaryMode: TypeAlias = Union[
    OpenBinaryModeUpdating, OpenBinaryModeReading, OpenBinaryModeWriting
]

# =============================================================================
# __all__
# =============================================================================
__all__ = (
    "AF",
    "DT",
    "FALSE",
    "FN",
    "KT",
    "ONE",
    "PT",
    "RT",
    "STDIN",
    "STDIO",
    "TRUE",
    "VT",
    "ZERO",
    "_DT",
    "_KT",
    "_R",
    "_RT",
    "_T",
    "_VT",
    "__DEPRECATED_TYPES__",
    "AFn",
    "AnyAsyncCallable",
    "AnyCallable",
    "AnyFunction",
    "AnyIterable",
    "AnyIterator",
    "ArrShape",
    "ArrayShape",
    "AsyncFn",
    "AsyncFuncType",
    "Bytes",
    "BytesPath",
    "CmdArgs",
    "CmdArgsType",
    "D",
    "DictAny",
    "DictAnyAny",
    "DictFloat",
    "DictFloatFloat",
    "DictInt",
    "DictIntInt",
    "DictNumber",
    "DictNumberNumber",
    "DictStr",
    "DictStrAny",
    "DictStrInt",
    "DictStrStr",
    "El",
    "Element",
    "Enum",
    "EnvMap",
    "EnvType",
    "F",
    "Flint",
    "Fn",
    "FsPath",
    "FsPathLike",
    "FuncType",
    "HrTime",
    "IntStr",
    "IterableAny",
    "IterableFloat",
    "IterableInt",
    "IterableNumber",
    "IterableStr",
    "IterableT",
    "Json",
    "JsonArrT",
    "JsonDictT",
    "JsonListT",
    "JsonObjT",
    "JsonPrimitive",
    "JsonT",
    "KT_co",
    "KT_contra",
    "KeyT",
    "KeyType",
    "L",
    "ListAny",
    "ListFloat",
    "ListInt",
    "ListListStr",
    "ListNumber",
    "ListStr",
    "ListT",
    "Lit",
    "Ls",
    "N",
    "NoneBytes",
    "NoneStr",
    "NoneStrBytes",
    "NoneType",
    "Null",
    "Number",
    "OpenBinaryMode",
    "OpenBinaryModeReading",
    "OpenBinaryModeUpdating",
    "OpenBinaryModeWriting",
    "OpenTextMode",
    "OpenTextModeReading",
    "OpenTextModeUpdating",
    "OpenTextModeWriting",
    "Opt",
    "OptFloat",
    "OptInt",
    "OptStr",
    "OptionalFloat",
    "OptionalInt",
    "OptionalStr",
    "P",
    "Path",
    "PathLike",
    "PathLikeAny",
    "PathLikeBytes",
    "PathLikeStr",
    "PathLikeStrBytes",
    "R",
    "ReturnT",
    "ReturnType",
    "Seq",
    "SetAny",
    "SetFloat",
    "SetInt",
    "SetNumber",
    "SetStr",
    "SetT",
    "ShapeType",
    "StrBytes",
    "StrEnum",
    "StrIntFloat",
    "StrOrBytesPath",
    "StrPath",
    "StringEnum",
    "T",
    "T_ParamSpec",
    "T_Retval",
    "T_co",
    "T_contra",
    "TupleStrStr",
    "TupleStrs",
    "Txt",
    "U",
    "VT_co",
    "VT_contra",
    "V_co",
    "ValT",
    "ValType",
    "_KT_co",
    "_KT_contra",
    "_T_co",
    "_T_contra",
    "_VT_co",
    "_VT_contra",
    "_V_co",
    "__all_annotated_types__",
    "__all_shed__",
    "__all_typing__",
    "__all_typing_extensions__",
    "__all_typing_extensions_future__",
    "__version_annotated_types__",
    "annotations",
    "null",
)
__all_shed__ = __all__
