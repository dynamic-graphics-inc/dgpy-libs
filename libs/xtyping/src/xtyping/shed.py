# -*- coding: utf-8 -*-
"""xtyping = typing | typing_extensions | misc"""

from __future__ import annotations

from enum import Enum
from os import PathLike
from pathlib import Path
from typing import __all__ as __all_typing

from annotated_types import (
    __all__ as __all_annotated_types,
    __version__ as __version_annotated_types__,
)
from typing_extensions import (
    IO,
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    ParamSpec,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    __all__ as __all_typing_extensions,
)

######################
## DEPRECATED TYPES ##
######################
__DEPRECATED_TYPES__: Tuple[str, ...] = ("ByteString",)

#############
## __all__ ##
#############
__all_typing__: Tuple[str, ...] = tuple(
    e for e in __all_typing if e not in __DEPRECATED_TYPES__
)
__all_typing_extensions__: Tuple[str, ...] = tuple(
    {*__all_typing_extensions, *__all_typing__}
)
__all_typing_extensions_future__: Tuple[str, ...] = ()
__all_annotated_types__: Tuple[str, ...] = tuple(
    e for e in __all_annotated_types if e != "__version__"
)

#############
## Aliases ##
#############
D = Dict
Lit = Literal
L = Literal
Ls = List
Opt = Optional
U = Union
Seq = Sequence

###############
## LITERALLY ##
###############
TRUE = Literal[True]
FALSE = Literal[False]
ZERO = Literal[0]
ONE = Literal[1]

##########
## NONE ##
##########
null = Null = None.__class__
NoneType = None.__class__
NoneStr = Optional[str]
NoneBytes = Optional[bytes]
StrBytes = Union[str, bytes]
NoneStrBytes = Optional[StrBytes]

############
## NUMBER ##
############
Number = Union[float, int]  # float or int
Flint = Union[float, int]  # float or int

##############
## TypeVars ##
##############
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

###############
## ParamSpec ##
###############
P = ParamSpec("P")
PT = ParamSpec("PT")
T_ParamSpec = ParamSpec("T_ParamSpec")


########################
## Covariant TypeVars ##
########################
KT_co = TypeVar("KT_co", covariant=True)
T_co = TypeVar("T_co", covariant=True)  # Any type covariant containers.
V_co = TypeVar("V_co", covariant=True)  # Any type covariant containers.
VT_co = TypeVar("VT_co", covariant=True)  # Value type covariant containers.

_KT_co = TypeVar("_KT_co", covariant=True)
_T_co = TypeVar("_T_co", covariant=True)
_V_co = TypeVar("_V_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

############################
## Contravariant TypeVars ##
############################
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


################
## Function-y ##
################
AnyCallable = Callable[..., Any]
AnyAsyncCallable = Callable[..., Awaitable[Any]]
FuncType = Callable[..., Any]
AsyncFuncType = Callable[..., Awaitable[Any]]
F = TypeVar("F", bound=AnyCallable)
FN = TypeVar("FN", bound=AnyCallable)
Fn = TypeVar("Fn", bound=AnyCallable)
AF = TypeVar("AF", bound=Awaitable[Any])
AFn = TypeVar("AFn", bound=Awaitable[Any])
AsyncFn = TypeVar("AsyncFn", bound=Awaitable[Any])

#################
## STDIO/STDIN ##
#################
STDIO = Union[None, int, bytes, IO[Any]]
STDIN = Union[bytes, str, None]

###########
## LISTS ##
###########
ListAny = List[Any]
ListT = List[T]
ListStr = List[str]
ListInt = List[int]
ListFloat = List[float]
ListNumber = List[Number]

############################
## LISTLESS AKA iterables ##
############################
IterableAny = Iterable[Any]
IterableT = Iterable[T]
IterableStr = Iterable[str]
IterableInt = Iterable[int]
IterableFloat = Iterable[float]
IterableNumber = Iterable[Number]

##########
## DICT ##
##########
DictAny = Dict[Any, Any]
DictStr = Dict[str, str]
DictInt = Dict[int, int]
DictFloat = Dict[float, float]
DictNumber = Dict[Number, Number]
DictAnyAny = Dict[Any, Any]
DictStrStr = Dict[str, str]
DictIntInt = Dict[int, int]
DictFloatFloat = Dict[float, float]
DictNumberNumber = Dict[Number, Number]
DictStrAny = Dict[str, Any]
DictStrInt = Dict[str, int]

#########
## SET ##
#########
SetAny = Set[Any]
SetT = Set[T]
SetStr = Set[str]
SetInt = Set[int]
SetFloat = Set[float]
SetNumber = Set[Number]

##########
## MISC ##
##########
IntStr = Union[int, str]
Bytes = Union[bytes, bytearray]
Txt = Union[bytes, str]
EnvMap = Union[Mapping[bytes, Txt], Mapping[str, Txt]]
AnyIterable = Union[Iterable[T], AsyncIterable[T]]
AnyIterator = Union[Iterator[T], AsyncIterator[T]]
AnyFunction = Union[Callable[..., R], Callable[..., Awaitable[R]]]
StrIntFloat = Union[str, float, int]
HrTime = Tuple[int, int]  # node/js hrtime type annotation

###############################
## Function type annotations ##
###############################
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
FsPathLike = "PathLike[Any]"
EnvType = Union[Mapping[bytes, Txt], Mapping[str, Txt]]
CmdArgs = CmdArgsType = Union[bytes, str, Sequence[str], Sequence[FsPath]]

##############
## LISTLESS ##
##############
ArrShape = Tuple[int, ...]
ArrayShape = Tuple[int, ...]
ShapeType = Tuple[int, ...]
TupleStrs = Tuple[str, ...]
ListListStr = List[List[str]]
TupleStrStr = Tuple[str, str]

#########
## OPT ##
#########
OptionalInt = Optional[int]
OptInt = Optional[int]
OptionalStr = Optional[str]
OptStr = Optional[str]
OptionalFloat = Optional[float]
OptFloat = Optional[float]

##########
## JSON ##
##########
JsonPrimitive = Union[None, bool, int, float, str]
Json = Union[Dict[str, "Json"], List["Json"], str, int, float, bool, None]
JsonT = Union[Dict[str, "JsonT"], List["JsonT"], str, int, float, bool, None]
JsonDictT = Dict[str, Any]
JsonListT = List[Any]
JsonObjT = Dict[str, Any]
JsonArrT = List[Any]

###################
## FROM TYPESHED ##
###################
StrPath = Union[str, "PathLike[str]"]  # stable
BytesPath = Union[bytes, "PathLike[bytes]"]  # stable
StrOrBytesPath = Union[str, bytes, "PathLike[Any]"]

OpenTextModeUpdating = Literal[
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
OpenTextModeWriting = Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"]
OpenTextModeReading = Literal[
    "r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"
]
OpenTextMode = Union[OpenTextModeUpdating, OpenTextModeWriting, OpenTextModeReading]
OpenBinaryModeUpdating = Literal[
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
OpenBinaryModeWriting = Literal["wb", "bw", "ab", "ba", "xb", "bx"]
OpenBinaryModeReading = Literal["rb", "br", "rbU", "rUb", "Urb", "brU", "bUr", "Ubr"]
OpenBinaryMode = Union[
    OpenBinaryModeUpdating, OpenBinaryModeReading, OpenBinaryModeWriting
]

#############
## __all__ ##
#############
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
