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

__all__ = (
    'AF',
    'AFn',
    'AnyAsyncCallable',
    'AnyCallable',
    'AnyFunction',
    'AnyIterable',
    'AnyIterator',
    'ArrShape',
    'ArrayShape',
    'AsyncFn',
    'AsyncFuncType',
    'Bytes',
    'CmdArgs',
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
    'Enum',
    'EnvMap',
    'EnvType',
    'F',
    'FALSE',
    'FN',
    'Flint',
    'Fn',
    'FsPath',
    'FsPathLike',
    'FuncType',
    'HrTime',
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
    'KT_co',
    'KT_contra',
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
    'ONE',
    'Opt',
    'OptFloat',
    'OptInt',
    'OptStr',
    'OptionalFloat',
    'OptionalInt',
    'OptionalStr',
    'P',
    'PT',
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
    'T_ParamSpec',
    'T_Retval',
    'T_co',
    'T_contra',
    'TupleStrStr',
    'TupleStrs',
    'Txt',
    'VT',
    'VT_co',
    'VT_contra',
    'V_co',
    'ValT',
    'ValType',
    'ZERO',
    '_DT',
    '_KT',
    '_KT_co',
    '_KT_contra',
    '_R',
    '_RT',
    '_T',
    '_T_co',
    '_T_contra',
    '_VT',
    '_VT_co',
    '_VT_contra',
    '_V_co',
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
Number = Union[int, float]  # float or int
Flint = Union[int, float]  # float or int

##############
## TypeVars ##
##############
T = TypeVar('T')  # Any type.
_T = TypeVar('_T')
KT = TypeVar('KT')  # Key type.
_KT = TypeVar('_KT')
VT = TypeVar('VT')  # Value type.
_VT = TypeVar('_VT')
KeyT = TypeVar('KeyT')  # Key type.
ValT = TypeVar('ValT')  # Value type.
KeyType = TypeVar('KeyType')  # Key type.
ValType = TypeVar('ValType')  # Value type.
El = TypeVar('El')
Element = TypeVar('Element')
R = TypeVar('R')
RT = TypeVar('RT')
_R = TypeVar('_R')
_RT = TypeVar('_RT')
ReturnT = TypeVar('ReturnT')
ReturnType = TypeVar('ReturnType')
N = TypeVar('N', int, float)
DT = TypeVar('DT')
_DT = TypeVar('_DT')
T_Retval = TypeVar('T_Retval')

###############
## ParamSpec ##
###############
P = ParamSpec('P')
PT = ParamSpec('PT')
T_ParamSpec = ParamSpec('T_ParamSpec')


########################
## Covariant TypeVars ##
########################
KT_co = TypeVar('KT_co', covariant=True)
T_co = TypeVar('T_co', covariant=True)  # Any type covariant containers.
V_co = TypeVar('V_co', covariant=True)  # Any type covariant containers.
VT_co = TypeVar('VT_co', covariant=True)  # Value type covariant containers.

_KT_co = TypeVar('_KT_co', covariant=True)
_T_co = TypeVar('_T_co', covariant=True)
_V_co = TypeVar('_V_co', covariant=True)
_VT_co = TypeVar('_VT_co', covariant=True)

############################
## Contravariant TypeVars ##
############################
T_contra = TypeVar('T_contra', contravariant=True)  # Ditto contravariant.
_T_contra = TypeVar('_T_contra', contravariant=True)  # Ditto contravariant.
VT_contra = TypeVar('VT_contra', contravariant=True)
_VT_contra = TypeVar('_VT_contra', contravariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)
_KT_contra = TypeVar('_KT_contra', contravariant=True)


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
F = TypeVar('F', bound=AnyCallable)
FN = TypeVar('FN', bound=AnyCallable)
Fn = TypeVar('Fn', bound=AnyCallable)
AF = TypeVar('AF', bound=Awaitable)
AFn = TypeVar('AFn', bound=Awaitable)
AsyncFn = TypeVar('AsyncFn', bound=Awaitable)

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
