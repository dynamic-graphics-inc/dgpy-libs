# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import cast, overload

from xtyping import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    MutableSequence,
    Optional,
    Protocol,
    SupportsIndex,
    Tuple,
    Type,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler

__all__ = (
    "JsonArr",
    "n_args",
)
_T = TypeVar("_T")
_R = TypeVar("_R")


class SupportsDunderLT(Protocol):
    def __lt__(self, __other: Any) -> bool: ...


class SupportsDunderGT(Protocol):
    def __gt__(self, __other: Any) -> bool: ...


SupportsRichComparison = Union[SupportsDunderLT, SupportsDunderGT]
SupportsRichComparisonT = TypeVar(
    "SupportsRichComparisonT", bound=SupportsRichComparison
)


def n_args(fn: Callable[..., _R]) -> int:
    if not callable(fn):
        raise TypeError(f"{fn!r} is not callable")
    try:
        return fn.__code__.co_argcount
    except AttributeError:
        pass
    if hasattr(fn, "__call__"):  # noqa: B004
        _nargs = n_args(fn.__call__)
        co_varnames = fn.__call__.__code__.co_varnames
        if co_varnames[0] == "self":
            return len(co_varnames) - 1
        return _nargs
    raise TypeError(f"{fn!r} is not callable")


class JsonArr(MutableSequence[_T], Generic[_T]):
    __arr: List[_T]

    def __init__(self, iterable: Optional[Iterable[_T]] = None) -> None:
        self.__arr = list(iterable or [])

    def __post_init__(self) -> Any:
        """Function place holder that is called after object initialization"""
        # pylint: disable=unnecessary-pass

    def __repr__(self) -> str:
        return "JsonArr(" + repr(self.__arr) + ")"

    def __str__(self) -> str:
        return f"JsonArr({self.__arr.__str__()})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsonArr):
            return self.__arr == other.__arr
        if isinstance(other, list):
            return self.__arr == other
        if isinstance(other, tuple):
            return self.__arr == list(other)
        return False

    def copy(self) -> JsonArr[_T]:
        return JsonArr(self.__arr.copy())

    def append(self, __object: _T) -> None:
        self.__arr.append(__object)

    def extend(self, __iterable: Iterable[_T]) -> None:
        self.__arr.extend(__iterable)

    def push(self, *__object: _T) -> None:
        self.extend(__object)

    def pop(self, index: int = -1) -> _T:
        return self.__arr.pop(index)

    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    def index(
        self, __value: _T, __start: SupportsIndex = 0, __stop: SupportsIndex = -1
    ) -> int:
        return self.__arr.index(__value, __start, __stop)

    def count(self, __value: _T) -> int:
        return self.__arr.count(__value)

    def insert(self, __index: SupportsIndex, __object: _T) -> None:
        return self.__arr.insert(__index, __object)

    def remove(self, __value: _T) -> None:
        return self.__arr.remove(__value)

    @overload
    def sort(
        self: JsonArr[SupportsRichComparisonT], *, key: None = None, reverse: bool = ...
    ) -> None: ...

    @overload
    def sort(
        self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = ...
    ) -> None: ...

    def sort(
        self,
        *,
        key: Optional[Callable[[_T], SupportsRichComparison]] = None,
        reverse: bool = False,
    ) -> None:
        return self.__arr.sort(key=key, reverse=reverse)

    def __len__(self) -> int:
        return len(self.__arr)

    def __iter__(self) -> Iterator[_T]:
        return iter(self.__arr)

    __hash__: None  # type: ignore[assignment]

    @overload
    def __getitem__(self, __i: SupportsIndex) -> _T: ...

    @overload
    def __getitem__(self, __s: slice) -> JsonArr[_T]: ...

    def __getitem__(self, __i: Union[SupportsIndex, slice]) -> Union[_T, JsonArr[_T]]:
        if isinstance(__i, slice):
            return JsonArr(self.__arr[__i])
        return self.__arr[__i]

    @overload
    def __setitem__(self, __i: SupportsIndex, __o: _T) -> None: ...

    @overload
    def __setitem__(self, __s: slice, __o: Iterable[_T]) -> None: ...

    def __setitem__(self, __i: Any, __o: Any) -> None:
        return self.__arr.__setitem__(__i, __o)

    def __delitem__(self, __i: Union[SupportsIndex, slice]) -> None:
        self.__arr.__delitem__(__i)

    def __add__(self, __x: Union[Iterable[_T], JsonArr[_T]]) -> JsonArr[_T]:
        if isinstance(__x, JsonArr):
            return JsonArr(self.__arr + __x.__arr)
        return JsonArr(self.__arr + list(__x))

    def __iadd__(self, __x: Iterable[_T]) -> JsonArr[_T]:
        self.__arr += __x
        return self

    def __mul__(self, __n: int) -> JsonArr[_T]:
        return JsonArr(self.__arr * __n)

    def __rmul__(self, __n: SupportsIndex) -> JsonArr[_T]:
        return JsonArr(self.__arr.__mul__(__n))

    def __imul__(self, __n: SupportsIndex) -> JsonArr[_T]:
        self.__arr.__mul__(__n)
        return self

    def __contains__(self, __o: object) -> bool:
        return self.__arr.__contains__(__o)

    def __reversed__(self) -> Iterator[_T]:
        return reversed(self.__arr)

    def __gt__(self, __x: List[_T]) -> bool:
        return self.__arr > __x

    def __ge__(self, __x: List[_T]) -> bool:
        return self.__arr >= __x

    def __lt__(self, __x: List[_T]) -> bool:
        return self.__arr < __x

    def __le__(self, __x: List[_T]) -> bool:
        return self.__arr <= __x

    def as_list(self) -> List[_T]:
        return list(self.__arr)

    def as_tuple(self) -> Tuple[_T, ...]:
        return tuple(self.__arr)

    @classmethod
    def validate_type(cls: Type[JsonArr[_T]], val: Any) -> JsonArr[_T]:
        """Validate and convert a value to a JsonObj object"""
        return cls(val)

    @classmethod
    def __get_type_validator__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> Iterator[Callable[[Any], Any]]:
        """Return the JsonObj validator functions"""
        yield cls.validate_type

    def eject(self) -> List[_T]:
        return self.__arr

    @overload
    def enumerate(
        self, start: int = 0, flip: Literal[False] = False
    ) -> Iterator[Tuple[int, _T]]: ...

    @overload
    def enumerate(
        self, start: int = 0, flip: Literal[True] = True
    ) -> Iterator[Tuple[_T, int]]: ...

    @overload
    def enumerate(
        self, start: int = 0, flip: bool = False
    ) -> Union[Iterator[Tuple[int, _T]], Iterator[Tuple[_T, int]]]: ...

    def enumerate(
        self, start: int = 0, flip: bool = False
    ) -> Union[Iterator[Tuple[int, _T]], Iterator[Tuple[_T, int]]]:
        if flip:
            return zip(self.__arr, range(start, len(self.__arr) + start))
        return enumerate(self.__arr, start=start)

    def _iter_el(self) -> Iterator[_T]:
        return iter(self.__arr)

    def _iter_el_ix(self) -> Iterator[Tuple[_T, int]]:
        return self.enumerate(flip=True)

    def _iter_el_ix_arr(self) -> Iterator[Tuple[_T, int, JsonArr[_T]]]:
        return ((el, ix, self) for el, ix in self.enumerate(flip=True))

    def _filter_el(self, func: Callable[[_T], bool]) -> JsonArr[_T]:
        return JsonArr(list(filter(func, self._iter_el())))

    def _filter_el_ix(self, func: Callable[[_T, int], bool]) -> JsonArr[_T]:
        return JsonArr([el for el, ix in self._iter_el_ix() if func(el, ix)])

    def _filter_el_ix_arr(
        self, func: Callable[[_T, int, JsonArr[_T]], bool]
    ) -> JsonArr[_T]:
        return JsonArr(
            [el for el, ix, arr in self._iter_el_ix_arr() if func(el, ix, arr)]
        )

    def filter(
        self,
        func: Union[
            Callable[[_T], bool],
            Callable[[_T, int], bool],
            Callable[[_T, int, JsonArr[_T]], bool],
        ],
        nargs: Optional[Union[Literal[1], Literal[2], Literal[3]]] = None,
    ) -> JsonArr[_T]:
        _fn_args = nargs or n_args(func)
        if _fn_args == 3:
            _fn3 = cast("Callable[[_T, int, JsonArr[_T]], bool]", func)
            return self._filter_el_ix_arr(_fn3)
        elif _fn_args == 2:
            _fn2 = cast("Callable[[_T, int], bool]", func)
            return self._filter_el_ix(_fn2)
        elif _fn_args == 1:
            _fn1 = cast("Callable[[_T], bool]", func)
            return self._filter_el(_fn1)
        raise TypeError("Could not determine number of arguments for filter function")

    def _map_el(self, func: Callable[[_T], _R]) -> JsonArr[_R]:
        return JsonArr(list(map(func, self._iter_el())))

    def _map_el_ix(self, func: Callable[[_T, int], _R]) -> JsonArr[_R]:
        return JsonArr(list(map(lambda el_ix: func(*el_ix), self._iter_el_ix())))

    def _map_el_ix_arr(self, func: Callable[[_T, int, JsonArr[_T]], _R]) -> JsonArr[_R]:
        return JsonArr(
            list(map(lambda el_ix: func(el_ix[0], el_ix[1], self), self._iter_el_ix()))
        )

    def map(
        self,
        func: Union[
            Callable[[_T], _R],
            Callable[[_T, int], _R],
            Callable[[_T, int, JsonArr[_T]], _R],
        ],
        nargs: Optional[Union[Literal[1], Literal[2], Literal[3]]] = None,
    ) -> JsonArr[_R]:
        _fn_args = nargs or n_args(func)
        if _fn_args == 3:
            _fn3 = cast("Callable[[_T, int, JsonArr[_T]], _R]", func)
            return self._map_el_ix_arr(_fn3)
        elif _fn_args == 2:
            _fn2 = cast("Callable[[_T, int], _R]", func)
            return self._map_el_ix(_fn2)
        elif _fn_args == 1:
            _fn1 = cast("Callable[[_T], _R]", func)
            return self._map_el(_fn1)
        raise TypeError("Could not determine number of arguments for map function")

    def slice(
        self, start: Optional[int] = None, end: Optional[int] = None
    ) -> JsonArr[_T]:
        """Return a slice as new jsonarray

        Args:
            start (Optional[int], optional): start index. Defaults to None.
            end (Optional[int], optional): end index. Defaults to None.

        Returns:
            JsonArr[_T]: new JsonArr

        Examples:
            >>> arr = JsonArr([1, 2, 3, 4, 5])
            >>> arr.slice()
            JsonArr([1, 2, 3, 4, 5])
            >>> arr.slice(1, 3)
            JsonArr([2, 3])

        """
        if start is None and end is None:
            return JsonArr([*self.__arr])
        _start = 0 if start is None else start
        _end = len(self) if end is None else end
        return JsonArr(self.__arr[_start:_end])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
