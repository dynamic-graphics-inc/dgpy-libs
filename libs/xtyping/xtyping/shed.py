# -*- coding: utf-8 -*-
"""xtyping = typing | typing_extensions | misc"""
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import (
    IO,
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from typing_extensions import Literal, ParamSpec

__all_typing__: Tuple[str, ...] = (
    "AbstractSet",
    "Any",
    "AnyStr",
    "AsyncContextManager",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "ByteString",
    "Callable",
    "ChainMap",
    "ClassVar",
    "Collection",
    "Container",
    "ContextManager",
    "Coroutine",
    "Counter",
    "DefaultDict",
    "Deque",
    "Dict",
    "FrozenSet",
    "Generator",
    "Generic",
    "Hashable",
    "IO",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "List",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "NamedTuple",
    "NewType",
    "Optional",
    "Reversible",
    "Sequence",
    "Set",
    "Sized",
    "SupportsAbs",
    "SupportsBytes",
    "SupportsComplex",
    "SupportsFloat",
    "SupportsInt",
    "SupportsRound",
    "TYPE_CHECKING",
    "Text",
    "Tuple",
    "Type",
    "TypeVar",
    "Union",
    "ValuesView",
    "cast",
    "get_type_hints",
    "no_type_check",
    "no_type_check_decorator",
    "overload",
)
__all_typing_extensions__: Tuple[str, ...] = (
    "Annotated",
    "AsyncContextManager",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "ChainMap",
    "ClassVar",
    "Concatenate",
    "ContextManager",
    "Coroutine",
    "Counter",
    "DefaultDict",
    "Deque",
    "Final",
    "IntVar",
    "Literal",
    "NewType",
    "NoReturn",
    "OrderedDict",
    "ParamSpec",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Protocol",
    "SupportsIndex",
    "TYPE_CHECKING",
    "Text",
    "Type",
    "TypeAlias",
    "TypeGuard",
    "TypedDict",
    "final",
    "get_args",
    "get_origin",
    "get_type_hints",
    "overload",
    "runtime",
    "runtime_checkable",
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

    ...


class StrEnum(StringEnum):
    """Alias for StringEnum"""

    ...


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
FsPath = Union[str, Path, PathLike]
FsPathLike = PathLike
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
# Json friendly: Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
JsonPrimitive = Union[None, bool, int, float, str]
Json = Union[Dict[str, "Json"], List["Json"], str, int, float, bool, None]  # type: ignore
JsonT = Union[Dict[str, "JsonT"], List["JsonT"], str, int, float, bool, None]  # type: ignore
JsonDictT = Dict[str, Any]
JsonListT = List[Any]
JsonObjT = Dict[str, Any]
JsonArrT = List[Any]

###################
## FROM TYPESHED ##
###################
Self = TypeVar("Self")
StrPath = Union[str, PathLike]  # stable
BytesPath = Union[bytes, PathLike]  # stable
StrOrBytesPath = Union[str, bytes, PathLike]

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
    "DT",
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
    "FALSE",
    "FN",
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
    "KT",
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
    "ONE",
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
    "PT",
    "Path",
    "PathLike",
    "R",
    "RT",
    "ReturnT",
    "ReturnType",
    "STDIN",
    "STDIO",
    "Self",
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
    "TRUE",
    "T_ParamSpec",
    "T_Retval",
    "T_co",
    "T_contra",
    "TupleStrStr",
    "TupleStrs",
    "Txt",
    "U",
    "VT",
    "VT_co",
    "VT_contra",
    "V_co",
    "ValT",
    "ValType",
    "ZERO",
    "_DT",
    "_KT",
    "_KT_co",
    "_KT_contra",
    "_R",
    "_RT",
    "_T",
    "_T_co",
    "_T_contra",
    "_VT",
    "_VT_co",
    "_VT_contra",
    "_V_co",
    "__all_shed__",
    "__all_typing__",
    "__all_typing_extensions__",
    "null",
)
__all_shed__ = __all__
