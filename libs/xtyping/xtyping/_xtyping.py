# -*- coding: utf-8 -*-
"""xtyping => extended typing"""
import typing as __typing

from decimal import Decimal
from os import PathLike
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    AbstractSet,
    Any,
    AnyStr,
    AsyncContextManager,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    ByteString,
    Callable,
    ChainMap,
    ClassVar,
    Collection,
    Container,
    ContextManager,
    Coroutine,
    Counter,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Generator,
    Generic,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    NamedTuple,
    NewType,
    Optional,
    Reversible,
    Sequence,
    Set,
    Sized,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsInt,
    SupportsRound,
    Text,
    Tuple,
    Type,
    TypeVar,
    Union,
    ValuesView,
    cast,
    get_type_hints,
    no_type_check,
    no_type_check_decorator,
    overload,
)


# Based on pydantic
try:
    from typing import ForwardRef  # type: ignore

    def evaluate_forwardref(
        type_: ForwardRef, globalns: Any, localns: Any
    ) -> Type[Any]:  # type: ignore
        return type_._evaluate(globalns, localns)  # type: ignore

    def _get_base_generic(cls: Any) -> Any:
        # subclasses of Generic will have their _name set to None, but
        # their __origin__ will point to the base generic
        if cls._name is None:
            return cls.__origin__
        else:
            return getattr(__typing, cls._name)


except ImportError:
    # python 3.6
    from typing import _ForwardRef as ForwardRef  # type: ignore

    def evaluate_forwardref(
        type_: ForwardRef, globalns: Any, localns: Any
    ) -> Type[Any]:
        return type_._eval_type(globalns, localns)  # type: ignore

    def _get_base_generic(cls: Any) -> Any:
        try:
            return cls.__origin__
        except AttributeError:
            pass

        name = type(cls).__name__
        if not name.endswith("Meta"):
            raise NotImplementedError("Cannot determine base of {}".format(cls))

        name = name[:-4]
        try:
            return getattr(__typing, name)
        except AttributeError:
            raise NotImplementedError("Cannot determine base of {}".format(cls))


__typing__ = [
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
]
__xtyping__ = [
    "AnyCallable",
    "AnyFunction",
    "AnyIterable",
    "AnyIterator",
    "ArrShape",
    "Bytes",
    "DT",
    "Decimal",
    "DictAny",
    "DictFloat",
    "DictInt",
    "DictNumber",
    "DictStr",
    "El",
    "Element",
    "EnvMap",
    "FN",
    "Flint",
    "ForwardRef",
    "FsPath",
    "FsPathLike",
    "IO",
    "IntStr",
    "IterableAny",
    "IterableFloat",
    "IterableInt",
    "IterableNumber",
    "IterableStr",
    "IterableT",
    "JsonArrT",
    "JsonDictT",
    "JsonListT",
    "JsonObjT",
    "ListAny",
    "ListFloat",
    "ListInt",
    "ListNumber",
    "ListStr",
    "ListT",
    "N",
    "NoneBytes",
    "NoneStr",
    "NoneStrBytes",
    "NoneType",
    "Num",
    "Number",
    "OptInt",
    "OptIntFloat",
    "OptIntFloatDecimal",
    "OptionalInt",
    "OptionalIntFloat",
    "Path",
    "PathLike",
    "R",
    "RT",
    "ReturnType",
    "STDIN",
    "STDIO",
    "SetAny",
    "SetFloat",
    "SetInt",
    "SetNumber",
    "SetStr",
    "SetT",
    "StrBytes",
    "StrIntFloat",
    "T",
    "Txt",
    "_DT",
    "_R",
    "_RT",
    "_T",
    "_get_base_generic",
    "evaluate_forwardref",
]
__all__ = [
    # Typing
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
    # XTYPING
    *__xtyping__,
]

##########
## NONE ##
##########
NoneType = None.__class__
NoneStr = Optional[str]
NoneBytes = Optional[bytes]
StrBytes = Union[str, bytes]
NoneStrBytes = Optional[StrBytes]

#########
## OPT ##
#########
OptionalInt = Optional[int]
OptInt = Optional[int]
OptionalIntFloat = Union[OptionalInt, float]
OptIntFloat = Union[OptionalInt, float]
OptIntFloatDecimal = Union[OptionalIntFloat, Decimal]

############
## NUMBER ##
############
Number = Union[int, float]  # float or int
Num = Union[int, float]  # float or int
Flint = Union[int, float]  # float or int

######################
## File system path ##
######################
FsPath = Union[str, Path]
FsPathLike = Union[str, PathLike]

##############
## TypeVars ##
##############
T = TypeVar("T")
_T = TypeVar("_T")
El = TypeVar("El")
Element = TypeVar("Element")
R = TypeVar("R")
RT = TypeVar("RT")
_R = TypeVar("_R")
_RT = TypeVar("_RT")
ReturnType = TypeVar("ReturnType")
N = TypeVar("N", int, float)
DT = TypeVar("DT")
_DT = TypeVar("_DT")

################
## Function-y ##
################
AnyCallable = Callable[..., Any]
ArrShape = Tuple[int, ...]
FN = TypeVar("FN", bound=AnyCallable)

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
## JSON ##
##########
# Json friendly: Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
JsonDictT = Dict[str, Any]
JsonObjT = Dict[str, Any]
JsonListT = List[Any]
JsonArrT = List[Any]

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
StrIntFloat = Union[str, int, float]
