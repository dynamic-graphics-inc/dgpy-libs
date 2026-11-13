# -*- coding: utf-8 -*-
from __future__ import annotations

import inspect

from collections.abc import Callable, Iterable, Iterator, MutableSequence
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    Protocol,
    SupportsIndex,
    TypeAlias,
    TypeVar,
    cast,
    overload,
)

if TYPE_CHECKING:
    import builtins

    from types import CodeType

    from pydantic import GetCoreSchemaHandler

__all__ = (
    "JsonArr",
    "n_args",
)
_T = TypeVar("_T")
_R = TypeVar("_R")


class SupportsDunderLT(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


class SupportsDunderGT(Protocol):
    def __gt__(self, other: Any, /) -> bool: ...


SupportsRichComparison: TypeAlias = SupportsDunderLT | SupportsDunderGT
SupportsRichComparisonT = TypeVar(
    "SupportsRichComparisonT", bound=SupportsRichComparison
)


def n_args(fn: Callable[..., _R]) -> int:
    if not callable(fn):
        _emsg = f"{fn!r} is not callable"
        raise TypeError(_emsg)
    code: CodeType | None = getattr(fn, "__code__", None)
    if code is not None:
        return code.co_argcount - 1 if inspect.ismethod(fn) else code.co_argcount
    call: object = getattr(fn, "__call__", None)  # noqa: B004 (want the bound method)
    if inspect.ismethod(call):
        return n_args(call)
    try:
        params = inspect.signature(fn).parameters.values()
    except (TypeError, ValueError):
        params = None
    if params is not None:
        positional = [
            p for p in params if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
        ]
        if positional:
            return len(positional)
    _emsg = f"could not determine number of arguments for {fn!r}; pass `nargs=`"
    raise TypeError(_emsg)


class JsonArr(MutableSequence[_T], Generic[_T]):
    __arr: list[_T]

    def __init__(self, iterable: Iterable[_T] | None = None) -> None:
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

    def append(self, obj: _T, /) -> None:
        self.__arr.append(obj)

    def extend(self, iterable: Iterable[_T], /) -> None:
        self.__arr.extend(iterable)

    def push(self, *objects: _T) -> None:
        self.extend(objects)

    def pop(self, index: int = -1) -> _T:
        return self.__arr.pop(index)

    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    def index(
        self, value: _T, start: SupportsIndex = 0, stop: SupportsIndex = -1, /
    ) -> int:
        return self.__arr.index(value, start, stop)

    def count(self, value: _T, /) -> int:
        return self.__arr.count(value)

    def insert(self, index: SupportsIndex, obj: _T, /) -> None:
        return self.__arr.insert(index, obj)

    def remove(self, value: _T, /) -> None:
        return self.__arr.remove(value)

    @overload
    def sort(
        self: JsonArr[SupportsRichComparisonT], *, key: None = None, reverse: bool = ...
    ) -> None: ...
    @overload
    def sort(
        self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = ...
    ) -> None: ...
    def sort(
        self: JsonArr[Any],
        *,
        key: Callable[[Any], SupportsRichComparison] | None = None,
        reverse: bool = False,
    ) -> None:
        return self.__arr.sort(key=key, reverse=reverse)

    def __len__(self) -> int:
        return len(self.__arr)

    def __iter__(self) -> Iterator[_T]:
        return iter(self.__arr)

    __hash__: None  # type: ignore[assignment]

    @overload
    def __getitem__(self, i: SupportsIndex, /) -> _T: ...

    @overload
    def __getitem__(self, s: builtins.slice, /) -> JsonArr[_T]: ...

    def __getitem__(self, i: SupportsIndex | builtins.slice, /) -> _T | JsonArr[_T]:
        if isinstance(i, slice):
            return JsonArr(self.__arr[i])
        return self.__arr[i]

    @overload
    def __setitem__(self, i: SupportsIndex, o: _T, /) -> None: ...

    @overload
    def __setitem__(self, s: builtins.slice, o: Iterable[_T], /) -> None: ...

    def __setitem__(self, i: Any, o: Any, /) -> None:
        return self.__arr.__setitem__(i, o)

    def __delitem__(self, i: SupportsIndex | builtins.slice, /) -> None:
        self.__arr.__delitem__(i)

    def __add__(self, x: Iterable[_T] | JsonArr[_T], /) -> JsonArr[_T]:
        if isinstance(x, JsonArr):
            return JsonArr(self.__arr + x.__arr)
        return JsonArr(self.__arr + list(x))

    def __iadd__(self, x: Iterable[_T], /) -> JsonArr[_T]:
        self.__arr += x
        return self

    def __mul__(self, n: int, /) -> JsonArr[_T]:
        return JsonArr(self.__arr * n)

    def __rmul__(self, n: SupportsIndex, /) -> JsonArr[_T]:
        return JsonArr(self.__arr.__mul__(n))

    def __imul__(self, n: SupportsIndex, /) -> JsonArr[_T]:
        self.__arr.__mul__(n)
        return self

    def __contains__(self, o: object, /) -> bool:
        return self.__arr.__contains__(o)

    def __reversed__(self) -> Iterator[_T]:
        return reversed(self.__arr)

    def __gt__(self, x: list[_T], /) -> bool:
        return self.__arr > x

    def __ge__(self, x: list[_T], /) -> bool:
        return self.__arr >= x

    def __lt__(self, x: list[_T], /) -> bool:
        return self.__arr < x

    def __le__(self, x: list[_T], /) -> bool:
        return self.__arr <= x

    def as_list(self) -> list[_T]:
        return list(self.__arr)

    def as_tuple(self) -> tuple[_T, ...]:
        return tuple(self.__arr)

    @classmethod
    def validate_type(cls: type[JsonArr[_T]], val: Any) -> JsonArr[_T]:
        """Validate and convert a value to a JsonObj object"""
        return cls(val)

    @classmethod
    def __get_type_validator__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> Iterator[Callable[[Any], Any]]:
        """Return the JsonObj validator functions"""
        yield cls.validate_type  # ty: ignore[invalid-yield]

    def eject(self) -> list[_T]:
        return self.__arr

    @overload
    def enumerate(
        self, start: int = 0, *, flip: Literal[False] = False
    ) -> Iterator[tuple[int, _T]]: ...

    @overload
    def enumerate(
        self, start: int = 0, *, flip: Literal[True] = True
    ) -> Iterator[tuple[_T, int]]: ...

    @overload
    def enumerate(
        self, start: int = 0, *, flip: bool = False
    ) -> Iterator[tuple[int, _T]] | Iterator[tuple[_T, int]]: ...

    def enumerate(
        self, start: int = 0, *, flip: bool = False
    ) -> Iterator[tuple[int, _T]] | Iterator[tuple[_T, int]]:
        if flip:
            return zip(self.__arr, range(start, len(self.__arr) + start), strict=False)
        return enumerate(self.__arr, start=start)

    def _iter_el(self) -> Iterator[_T]:
        return iter(self.__arr)

    def _iter_el_ix(self) -> Iterator[tuple[_T, int]]:
        return self.enumerate(flip=True)

    def _iter_el_ix_arr(self) -> Iterator[tuple[_T, int, JsonArr[_T]]]:
        return ((el, ix, self) for el, ix in self.enumerate(flip=True))

    def _filter_el(self, func: Callable[[_T], bool]) -> JsonArr[_T]:
        return JsonArr(list(filter(func, self._iter_el())))

    def _filter_el_ix(self, func: Callable[[_T, int], bool]) -> JsonArr[_T]:
        return JsonArr([el for el, ix in self._iter_el_ix() if func(el, ix)])

    def _filter_el_ix_arr(
        self, func: Callable[[_T, int, JsonArr[_T]], bool]
    ) -> JsonArr[_T]:
        return JsonArr([
            el for el, ix, arr in self._iter_el_ix_arr() if func(el, ix, arr)
        ])

    def filter(
        self,
        func: Callable[[_T], bool]
        | Callable[[_T, int], bool]
        | Callable[[_T, int, JsonArr[_T]], bool],
        nargs: Literal[1, 2, 3] | None = None,
    ) -> JsonArr[_T]:
        _fn_args = nargs or n_args(func)
        if _fn_args == 3:
            _fn3 = cast("Callable[[_T, int, JsonArr[_T]], bool]", func)
            return self._filter_el_ix_arr(_fn3)
        if _fn_args == 2:
            _fn2 = cast("Callable[[_T, int], bool]", func)
            return self._filter_el_ix(_fn2)
        if _fn_args == 1:
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
        func: Callable[[_T], _R]
        | Callable[[_T, int], _R]
        | Callable[[_T, int, JsonArr[_T]], _R],
        nargs: Literal[1, 2, 3] | None = None,
    ) -> JsonArr[_R]:
        _fn_args = nargs or n_args(func)
        if _fn_args == 3:
            _fn3 = cast("Callable[[_T, int, JsonArr[_T]], _R]", func)
            return self._map_el_ix_arr(_fn3)
        if _fn_args == 2:
            _fn2 = cast("Callable[[_T, int], _R]", func)
            return self._map_el_ix(_fn2)
        if _fn_args == 1:
            _fn1 = cast("Callable[[_T], _R]", func)
            return self._map_el(_fn1)
        raise TypeError("Could not determine number of arguments for map function")

    def slice(self, start: int | None = None, end: int | None = None) -> JsonArr[_T]:
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
