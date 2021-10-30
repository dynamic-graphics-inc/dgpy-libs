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

from typing_extensions import Literal

__all__ = (
    'AF',
    'AnyCallable',
    'AnyFunction',
    'AnyIterable',
    'AnyIterator',
    'ArrShape',
    'ArrayShape',
    'Bytes',
    'CmdArgsType',
    'DT',
    'DictAny',
    'DictAnyAny',
    'DictFloat',
    'DictFloatFloat',
    'DictInt',
    'DictIntInt',
    'DictNumber',
    'DictNumberNumber',
    'DictStr',
    'DictStrAny',
    'DictStrInt',
    'DictStrStr',
    'El',
    'Element',
    'EnvMap',
    'EnvType',
    'F',
    'FALSE',
    'FN',
    'Flint',
    'FsPath',
    'FsPathLike',
    'FuncType',
    'HrTime',
    'IO',
    'IntStr',
    'IterableAny',
    'IterableFloat',
    'IterableInt',
    'IterableNumber',
    'IterableStr',
    'IterableT',
    'JsonArrT',
    'JsonDictT',
    'JsonListT',
    'JsonObjT',
    'KT',
    'KeyT',
    'KeyType',
    'ListAny',
    'ListFloat',
    'ListInt',
    'ListListStr',
    'ListNumber',
    'ListStr',
    'ListT',
    'N',
    'NoneBytes',
    'NoneStr',
    'NoneStrBytes',
    'NoneType',
    'Null',
    'Number',
    'OptFloat',
    'OptInt',
    'OptStr',
    'OptionalFloat',
    'OptionalInt',
    'OptionalStr',
    'Path',
    'PathLike',
    'R',
    'RT',
    'ReturnT',
    'ReturnType',
    'STDIN',
    'STDIO',
    'SetAny',
    'SetFloat',
    'SetInt',
    'SetNumber',
    'SetStr',
    'SetT',
    'ShapeType',
    'StrBytes',
    'StrEnum',
    'StrIntFloat',
    'StringEnum',
    'T',
    'TRUE',
    'T_co',
    'T_contra',
    'TupleStrStr',
    'TupleStrs',
    'Txt',
    'VT',
    'VT_co',
    'V_co',
    'ValT',
    'ValType',
    '_DT',
    '_R',
    '_RT',
    '_T',
    '__all_shed__',
    'null',
)
__all_shed__ = __all__

#############
## Aliases ##
#############
Opt = Optional

###############
## LITERALLY ##
###############
TRUE = Literal[True]
FALSE = Literal[False]

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
Number = Union[int, float]  # float or int
Flint = Union[int, float]  # float or int

##############
## TypeVars ##
##############
T = TypeVar('T')  # Any type.
_T = TypeVar("_T")
KT = TypeVar('KT')  # Key type.
VT = TypeVar('VT')  # Value type.
KeyT = TypeVar('KeyT')  # Key type.
ValT = TypeVar('ValT')  # Value type.
KeyType = TypeVar('KeyType')  # Key type.
ValType = TypeVar('ValType')  # Value type.
El = TypeVar("El")
Element = TypeVar("Element")
R = TypeVar("R")
RT = TypeVar("RT")
_R = TypeVar("_R")
_RT = TypeVar("_RT")
ReturnT = TypeVar("ReturnT")
ReturnType = TypeVar("ReturnType")
N = TypeVar("N", int, float)
DT = TypeVar("DT")
_DT = TypeVar("_DT")

########################
## Covariant TypeVars ##
########################
T_co = TypeVar('T_co', covariant=True)  # Any type covariant containers.
V_co = TypeVar('V_co', covariant=True)  # Any type covariant containers.
VT_co = TypeVar('VT_co', covariant=True)  # Value type covariant containers.
T_contra = TypeVar('T_contra', contravariant=True)  # Ditto contravariant.


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
FN = TypeVar("FN", bound=AnyCallable)
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)
AF = TypeVar("AF", bound=Awaitable)

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
HrTime = Tuple[int, int]  # node/js hrtime type annotation

###############################
## Function type annotations ##
###############################
FsPath = Union[str, Path, PathLike]
FsPathLike = PathLike
EnvType = Union[Mapping[bytes, Txt], Mapping[str, Txt]]
CmdArgsType = Union[bytes, str, Sequence[str], Sequence[FsPath]]

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
