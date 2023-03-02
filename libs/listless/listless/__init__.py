# -*- coding: utf-8 -*-
# pyright: reportInvalidTypeVarUse=false
"""Listless generator utils"""
import asyncio

from collections import deque
from functools import reduce
from itertools import count, islice, tee, zip_longest
from operator import iconcat, mul
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Deque,
    Iterable,
    Iterator,
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
    "enumerate_async",
    "exhaust",
    "filter_is_none",
    "filter_none",
    "flatten",
    "flatten_strings",
    "it_product",
    "iter_async",
    "itlen",
    "list_async",
    "next_async",
    "partition",
    "set_async",
    "spliterable",
    "unique",
    "unique_gen",
    "xmap",
    "zip_async",
    "zip_longest",
)

_K = TypeVar("_K")
_T = TypeVar("_T")
_R = TypeVar("_R")
AnyIterable = Union[Iterable[_T], AsyncIterable[_T]]
AnyIterator = Union[Iterator[_T], AsyncIterator[_T]]


def aiterable(it: Union[Iterable[_T], AsyncIterable[_T]]) -> AsyncIterator[_T]:
    """Convert any-iterable to an async iterator

    Examples:
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


iter_async = aiterable


def pairs(it: Iterable[_T]) -> Iterable[Tuple[_T, _T]]:
    """Yield pairs of adjacent elements

    Examples:
        >>> list(pairs([1, 2, 3, 4]))
        [(1, 2), (2, 3), (3, 4)]
        >>> list(pairs(['a', 'b', 'c']))
        [('a', 'b'), ('b', 'c')]
        >>> list(pairs('abc'))
        [('a', 'b'), ('b', 'c')]

    """
    a, b = tee(it)
    next(b, None)
    return zip(a, b)


def partition(
    it: Sequence[_T],
    n: int,
    *,
    pad: bool = False,
    padval: Any = None,
    zip_strict: bool = False,
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


def nyield(it: Sequence[_T], n: int) -> Iterable[_T]:
    """Yield the first n items of an iterable"""
    return islice(it, n)


def is_sequence(seq: Any) -> bool:
    """Check if an object is a sequence

    Examples:
        >>> is_sequence([1, 2, 3])
        True
        >>> is_sequence('abc')
        False
        >>> is_sequence(1)
        False
        >>> is_sequence(None)
        False
        >>> is_sequence(True)
        False
        >>> is_sequence((1, 2, 3))
        True

    """

    if isinstance(seq, str):
        return False
    try:
        len(seq)
    except TypeError:
        return False
    return True


def chunkseq(it: Sequence[_T], n: int) -> Iterable[Sequence[_T]]:
    """Yield chunks of size n from a Sequence"""
    return (it[i : i + n] for i in range(0, len(it), n))


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

        >>> list(chunks((el for el in range(10)), 4))
        [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9)]

    """
    if isinstance(it, (str, list, tuple)) or is_sequence(it):
        yield from chunkseq(it, chunk_size)
    else:
        while True:
            _chunk = tuple(islice(it, chunk_size))
            if not _chunk:
                break
            yield _chunk


def chunk(it: Sequence[_T], n: int) -> Iterable[Sequence[_T]]:
    """Yield chunks of size n from a Sequence"""
    return chunks(it, n)


def exhaust(it: Iterable[_T], *, maxlen: Optional[int] = 0) -> Deque[_T]:
    """Exhaust an interable; useful for evaluating a map object.

    Args:
        it: Iterable to exhaust
        maxlen: Maximum length of the deque; if 0, deque is unbounded

    Examples:
        >>> a = [1, 2, 3, 4, 5, 6]
        >>> a_map = map(lambda x: x*2, a)
        >>> a_exhausted = exhaust(a_map)
        >>> a = [1, 2, 3, 4, 5, 6]
        >>> b = []
        >>> def square_and_append_to_b(n):
        ...     b.append(n**2)
        >>> a_map = map(square_and_append_to_b, a)
        >>> a_exhausted = exhaust(a_map)
        >>> a_exhausted
        deque([], maxlen=0)
        >>> b
        [1, 4, 9, 16, 25, 36]
        >>> another_map = map(lambda x: x*2, a)
        >>> another_exhausted = exhaust(another_map, maxlen=2)
        >>> another_exhausted
        deque([10, 12], maxlen=2)

    """
    return deque(it, maxlen=maxlen)


def xmap(
    func: Callable[[_T], _R], it: Iterable[_T], *, maxlen: Optional[int] = 0
) -> Deque[_R]:
    """Apply a function to each element of an iterable immediately

    Args:
        func: Function to apply to each element
        it: iterable to apply func to

    Returns:
        Deque of the possible results if maxlen is greater than 0

    Examples:
        >>> xmap(lambda x: x*2, list(range(1, 7)))
        deque([], maxlen=0)
        >>> xmap(lambda x: x*2, list(range(1, 7)), maxlen=2)
        deque([10, 12], maxlen=2)
        >>> xmap(lambda x: x*2, list(range(1, 7)), maxlen=None)
        deque([2, 4, 6, 8, 10, 12])

    """
    return exhaust(map(func, it), maxlen=maxlen)


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
    return filter(None.__ne__, it)  # type: ignore[arg-type]


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


def flatten_strings(
    *args: Union[
        Sequence[Union[str, int, float]],
        str,
        int,
        float,
    ]
) -> List[str]:
    """Flatten possibly nested iterables of sequences to a list of strings

    Examples:
        >>> from listless import flatten_strings
        >>> list(flatten_strings("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(flatten_strings("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(
        reduce(
            iconcat,
            [
                flatten_strings(*arg)
                if isinstance(arg, (list, tuple))
                else (str(arg),)
                if isinstance(arg, (int, float))
                else (arg,)
                for arg in args
            ],
            [],
        )
    )


def itlen(iterable: Iterable[Any], unique: bool = False) -> int:
    """Return the length/num-items in an iterable

    This consumes the iterable.

    Args:
        iterable: Iterable
        unique: Count unique values

    Returns:
        Length of an iterable

    Examples:
        >>> itlen(range(10))
        10
        >>> itlen(x for x in range(1000000) if x % 3 == 0)
        333334
        >>> l = [x for x in range(1000000) if x % 3 == 0]
        >>> itlen(l + l, unique=True)
        333334

    """
    if unique:
        return len(set(iterable))
    counter = count()
    deque(zip(iterable, counter), maxlen=0)
    return next(counter)


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


#########################
# ASYNC ~ ASYNC ~ ASYNC #
#########################


async def next_async(it: AnyIterator[_T]) -> _T:
    """Return the next item of any iterator/iterable (sync or async

    Examples:
        >>> from asyncio import run as aiorun
        >>> async def async_gen():
        ...     for b in range(10):
        ...        yield b
        >>> gen = async_gen()
        >>> async def fn(gen):
        ...     first = await next_async(gen)
        ...     second = await next_async(gen)
        ...     return first, second
        >>> aiorun(fn(gen))
        (0, 1)
        >>> aiorun(fn(iter(range(2))))
        (0, 1)

    """
    if isinstance(it, AsyncIterator):
        return await it.__anext__()

    try:
        return next(it)
    except StopIteration:  # pragma: no cover
        raise StopAsyncIteration


async def list_async(itr: AnyIterable[_T]) -> List[_T]:
    """Consume any iterable (async/sync) and return as a list

    Examples:
        >>> async def t():
        ...     return await list_async(range(5))
        >>> from asyncio import run as aiorun
        >>> aiorun(t())
        [0, 1, 2, 3, 4]

    """
    return [item async for item in aiterable(itr)]


async def set_async(itr: AnyIterable[_T]) -> Set[_T]:
    """Consume any iterable (async/sync) and return as a list

    Examples:
        >>> async def t():
        ...     return await set_async(range(5))
        >>> from asyncio import run as aiorun
        >>> aiorun(t())
        {0, 1, 2, 3, 4}

    """
    return {item async for item in aiterable(itr)}


async def enumerate_async(
    it: AnyIterable[_T], start: int = 0
) -> AsyncIterator[Tuple[int, _T]]:
    """Enumerate (async) over any iterable

    Examples:
        >>> async def t():
        ...     return [item async for item in enumerate_async('abcde')]
        >>> from asyncio import run as aiorun
        >>> aiorun(t())
        [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e')]

    """
    index = start
    async for item in aiterable(it):  # pragma: no cover
        yield index, item
        index += 1


async def zip_async(*iterables: AnyIterable[Any]) -> AsyncIterator[Tuple[Any, ...]]:
    """Async verstion of builtin zip function

    Example:
        >>> from asyncio import run as aiorun
        >>> from listless import zip_async
        >>> from listless import list_async, iter_async  # for fake async iters
        >>> a, b, c = iter_async(range(4)), iter_async(range(6)), iter_async(range(5))
        >>> aiorun(list_async(zip_async(a, b, c)))
        [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]]

    """
    its: List[AsyncIterator[Any]] = [aiterable(it) for it in iterables]

    while True:
        try:
            values = await asyncio.gather(*[it.__anext__() for it in its])
            yield values
        except (StopIteration, StopAsyncIteration):
            break


if __name__ == "__main__":
    import doctest

    doctest.testmod()
