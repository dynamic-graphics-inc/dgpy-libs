# -*- coding: utf-8 -*-
# pyright: reportInvalidTypeVarUse=false
"""Listless generator utils"""
from collections import deque
from functools import reduce
from itertools import tee, zip_longest
from operator import iconcat, mul
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from listless._meta import __version__

__all__ = (
    "__version__",
    "aiterable",
    "chunks",
    "exhaust",
    "filter_is_none",
    "filter_none",
    "flatten",
    "it_product",
    "partition",
    "spliterable",
    "unique",
    "unique_gen",
)

_T = TypeVar("_T")
_K = TypeVar("_K")


def aiterable(it: Union[Iterable[_T], AsyncIterable[_T]]) -> AsyncIterator[_T]:
    """Convert any-iterable to an async iterator

    Examples:
        >>> from os import remove
        >>> from asyncio import run
        >>> plain_jane_list = list(range(10))
        >>> async def consume_aiterable(it):
        ...     stuff = []
        ...     async for el in aiterable(it):
        ...         stuff.append(el)
        ...     return stuff
        >>> run(consume_aiterable(plain_jane_list))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> async def async_gen():
        ...     for b in range(10):
        ...        yield b
        >>> run(consume_aiterable(async_gen()))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> class AsyncIterable:
        ...     def __aiter__(self):
        ...         return async_gen()
        >>> run(consume_aiterable(AsyncIterable()))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    """
    if isinstance(it, AsyncIterator):
        return it

    if isinstance(it, AsyncIterable):
        return it.__aiter__()

    async def gen() -> AsyncIterator[_T]:
        for item in cast(Iterable[_T], it):
            yield item

    return gen()


def partition(
    it: Sequence[_T], n: int, *, pad: bool = False, padval: Any = None
) -> Iterable[Sequence[_T]]:
    """Partition an iterable into chunks of size n

    Args:
        it: Iterable to partition
        n (int): Size of the partition chunks
        pad (bool): Pad parts with padval if True, else do not pad
        padval (Any): Value to pad with

    Returns:
        Iterable of the partitioned chunks

    Examples:
        >>> list(partition([1, 2, 3, 4, 5, 6], 3))
        [(1, 2, 3), (4, 5, 6)]
        >>> list(partition([1, 2, 3, 4, 5, 6], 2))
        [(1, 2), (3, 4), (5, 6)]
        >>> for part in partition('abcdefghijklmnopqrstuvwxyz', 13):
        ...    print(part)
        ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm')
        ('n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
        >>> for part in partition('abcdefghijklmnopqrstuvwxyz', 4):
        ...    print(part)
        ('a', 'b', 'c', 'd')
        ('e', 'f', 'g', 'h')
        ('i', 'j', 'k', 'l')
        ('m', 'n', 'o', 'p')
        ('q', 'r', 's', 't')
        ('u', 'v', 'w', 'x')
        >>> for part in partition('abcdefghijklmnopqrstuvwxyz', 4, pad=True):
        ...    print(part)
        ('a', 'b', 'c', 'd')
        ('e', 'f', 'g', 'h')
        ('i', 'j', 'k', 'l')
        ('m', 'n', 'o', 'p')
        ('q', 'r', 's', 't')
        ('u', 'v', 'w', 'x')
        ('y', 'z', None, None)
        >>> for part in partition('abcdefghijklmnopqrstuvwxyz', 4, pad=True, padval=...):
        ...   print(part)
        ('a', 'b', 'c', 'd')
        ('e', 'f', 'g', 'h')
        ('i', 'j', 'k', 'l')
        ('m', 'n', 'o', 'p')
        ('q', 'r', 's', 't')
        ('u', 'v', 'w', 'x')
        ('y', 'z', Ellipsis, Ellipsis)

    Raises:
        TypeError: If `n` is not and int
        ValueError: if `n` is less than 1

    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")  # pragma: no cover
    if n < 1:
        raise ValueError("n must be >= 1")  # pragma: no cover
    args = [iter(it)] * n
    if pad:
        return zip_longest(*args, fillvalue=padval)
    else:
        return zip(*args)


@overload
def chunks(it: str, chunk_size: int) -> List[str]:
    ...


@overload
def chunks(it: List[_T], chunk_size: int) -> Iterable[List[_T]]:
    ...


@overload
def chunks(it: Sequence[_T], chunk_size: int) -> Iterable[Sequence[_T]]:
    ...


def chunks(it: Sequence[_T], chunk_size: int) -> Iterable[Sequence[_T]]:
    """Yield chunks of something slice-able with length <= chunk_size

    Args:
        it (Iterable[Any]): Iterable to chunk
        chunk_size (int): Size of the chunks

    Returns:
        Iterable of the chunks

    Examples:
        >>> list(chunks([1, 2, 3, 4, 5, 6], 3))
        [[1, 2, 3], [4, 5, 6]]
        >>> list(chunks([1, 2, 3, 4, 5, 6], 2))
        [[1, 2], [3, 4], [5, 6]]
        >>> list(chunks('abcdefghijklmnopqrstuvwxyz', 13))
        ['abcdefghijklm', 'nopqrstuvwxyz']

        Can chunk where it length is not divisible by chunk_size

        >>> list(chunks('abcdefghijklmnopqrstuvwxyz', 4))
        ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx', 'yz']

    """
    return (it[i : i + chunk_size] for i in range(0, len(it), chunk_size))


def exhaust(it: Iterable[Any]) -> None:
    """Exhaust an interable; useful for evaluating a map object.

    Args:
        it: Iterable to exhaust

    Examples:
        >>> a = [1, 2, 3, 4, 5, 6]
        >>> a_map = map(lambda x: x*2, a)
        >>> a_exhausted = exhaust(a_map)
        >>> a_exhausted is None # will be none after being exhausted
        True
        >>> a = [1, 2, 3, 4, 5, 6]
        >>> b = []
        >>> def square_and_append_to_b(n):
        ...     b.append(n**2)
        >>> a_map = map(square_and_append_to_b, a)
        >>> a_exhausted = exhaust(a_map)
        >>> a_exhausted is None # will be none after being exhausted
        True
        >>> b
        [1, 4, 9, 16, 25, 36]

    """
    deque(it, maxlen=0)


def filter_none(it: Iterable[Union[_T, None]]) -> Iterable[_T]:
    """Filter `None` values from an iterable

    Args:
        it: Iterable possibly containing None values

    Returns:
        filter object with None values excluded

    Examples:
        >>> list(filter_none([1, 2, None, 3, 4, None, 5, "a_string???"]))
        [1, 2, 3, 4, 5, 'a_string???']
        >>> list(filter_none([1, 2, '', 3, 4, None, 5, "a_string???", []]))
        [1, 2, 3, 4, 5, 'a_string???']
        >>> list(filter_none([-1, 0, 1, '', 's', None, [], ['s'], {}]))
        [-1, 1, 's', ['s']]

    This function is p simple and importing it and calling it might actually
    be more characters to type than just using `filter(None, ya_iterable)`
    but it is a fire thing to know and you can totally show off with this,
    also outperforms the list/gen comprehension equivalent, by quite a bit::

        import random
        res = [random.randrange(1, 300, 1) for i in range(1000)]

        lists = [
            res
        ]
        for i in range(40):
            random.shuffle(res)
            lists.append(res)

        def filter_one(it):
            return (i for i in it if i is not None)

        def filter_two(it):
            return filter(None, it)

    Timing the first function (generator comprehension)::

        %%timeit
        for i in range(100):
            for l in lists:
                a = list(filter_one(l))

        180 ms +/- 184 Ã‚Âµs/loop (mean +/- std. dev. of 7 runs, 10 loops each)


    Timing the second function (filter)::

        %%timeit
        for i in range(100):
            for l in lists:
                a = list(filter_two(l))

        42.5 ms +/- 112 Ã‚Âµs/loop (mean +/- std. dev. of 7 runs, 10 loops each)


    """
    return filter(None, it)


def filter_is_none(it: Iterable[Union[_T, None]]) -> Iterable[_T]:
    """Filter values that `is None`; checkout filter_none for false-y filtering

    Args:
        it: Iterable possibly containing None/False-y values

    Returns:
        filter object with None values excluded

    Examples:
        >>> list(filter_is_none([1, 2, None, 3, 4, None, 5, "a_string???"]))
        [1, 2, 3, 4, 5, 'a_string???']
        >>> list(filter_is_none([-1, 0, 1, '', 's', None, [], ['s'], {}]))
        [-1, 0, 1, '', 's', [], ['s'], {}]


    """
    return filter(None.__ne__, it)  # type: ignore


def flatten(*args: Union[_T, List[_T], Tuple[_T, ...]]) -> List[_T]:
    """Flatten possibly nested iterables of sequences to a flat list

    Examples:
        >>> list(flatten("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(flatten("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(
        reduce(
            iconcat,
            [
                flatten(*arg) if isinstance(arg, (list, tuple)) else (arg,)
                for arg in args
            ],
            [],
        )
    )


def it_product(it: Iterable[Union[int, float]]) -> Union[int, float]:
    """Product of all the elements in an iterable of numbers

    Args:
        it: Iterable of numbers

    Returns:
        The product of all the numbers in the iterable

    Examples:
        >>> it_product([1, 2, 3, 4])
        24
        >>> it_product(tuple([1, 2, 3, 4]))
        24
        >>> it_product([-1, -2, -3, 4])
        -24
        >>> it_product([-1, -2, 3, 4, 0.5])
        12.0

    """
    return reduce(mul, it)


def spliterable(
    it: Iterable[_T], fn: Callable[[_T], bool]
) -> Tuple[Iterable[_T], Iterable[_T]]:
    """1 generator + True/False-function => 2 generators (True-gen, False-gen)

    Args:
        it: iterable to split
        fn: Function to evaluate iterable elements and returns True or False

    Returns:
        tuple of generators. The first generator will yield elements of the
        original iterable where the conditional-function evaluates True, and
        the second generator where the conditional-function evaluates to False.

    Examples:
        >>> is_even = lambda n: n % 2 == 0
        >>> a, b = spliterable(range(10), is_even)
        >>> list(a)
        [0, 2, 4, 6, 8]
        >>> list(b)
        [1, 3, 5, 7, 9]

    """
    _true_gen, _false_gen = tee((fn(item), item) for item in it)
    return (i for p, i in _true_gen if p), (i for p, i in _false_gen if not p)


def unique_gen(
    it: Iterable[_T], key: Optional[Callable[[_T], _K]] = None
) -> Iterable[_T]:
    """Yield unique values (ordered) from an iterable

    Args:
        it: Iterable
        key: Optional callable to use to get the key to use for uniqueness

    Returns:
        Generator that yields unique values as they appear

    Examples:
        >>> l = [*range(10), *range(10)]
        >>> list(unique_gen(l))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> tuple(unique_gen(['cat', 'mouse', 'dog', 'hen'], key=len))
        ('cat', 'mouse')

    """
    if key is None:
        have: Set[_T] = set()
        have_add = have.add
        return (x for x in it if not (x in have or have_add(x)))
    else:
        havek: Set[_K] = set()
        havek_add = havek.add

        return (
            el
            for el, k_el in ((_el, key(_el)) for _el in it)
            if not (k_el in havek or havek_add(k_el))
        )


def unique(it: Iterable[_T], key: Optional[Callable[[_T], _K]] = None) -> Iterable[_T]:
    """Alias for unique_gen

    Examples:
        >>> l = [*range(10), *range(10)]
        >>> list(unique(l))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> tuple(unique(['cat', 'mouse', 'dog', 'hen'], key=len))
        ('cat', 'mouse')

    """
    return unique_gen(it=it, key=key)
