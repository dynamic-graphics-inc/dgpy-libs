# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from jsonbourne.dev.json_arr import JsonArr, n_args


def test_get_fn_args_count() -> None:
    assert n_args(lambda a, b: b % 4 == 0 and a % 2 == 0) == 2  # type: ignore

    def fn2() -> None:
        pass

    assert n_args(fn2) == 0

    def fn3(a: Any, b: Any, c: Any) -> None:
        pass

    assert n_args(fn3) == 3

    class OBJ:
        def __init__(self) -> None:
            pass

        def __call__(self, a: Any, b: Any, c: Any) -> None:
            pass

    assert n_args(OBJ()) == 3

    class OBJ_initializer:
        def __init__(self, a: Any, b: Any, c: Any) -> None:
            pass

        def __call__(self, a: Any, b: Any, c: Any) -> None:
            pass

    assert n_args(OBJ_initializer) == 3


def test_enumerate() -> None:
    alist = [0, 5, 10, 15, 20]
    assert alist == list(range(0, 25, 5))
    expected = list(enumerate(alist))
    expected_flip = [(el, ix) for ix, el in enumerate(alist)]
    assert list(JsonArr(alist).enumerate()) == expected
    assert list(JsonArr(alist).enumerate(flip=True)) == expected_flip


def test_filter_1() -> None:
    a = JsonArr(range(10))
    assert a.filter(lambda a: a % 2 == 0).eject() == [0, 2, 4, 6, 8]
    assert a.filter(lambda a: a % 2 == 1).eject() == [1, 3, 5, 7, 9]


def test_filter_2() -> None:
    a = JsonArr(range(10))
    assert a.filter(lambda a, b: b % 4 == 0 and a % 2 == 0).eject() == [0, 4, 8]
    assert a.filter(lambda a, b: b % 3 == 0 and a % 2 == 1).eject() == [3, 9]


def test_filter_3() -> None:
    a = JsonArr(range(10))
    assert a.filter(
        lambda a, b, c: b % 4 == 0 and a % 2 == 0 and len(c) > 0
    ).eject() == [0, 4, 8]
    assert a.filter(
        lambda a, b, c: b % 3 == 0 and a % 2 == 1 and len(c) > 0
    ).eject() == [3, 9]


def test_map_1() -> None:
    ja = JsonArr(range(10))
    assert ja.map(lambda a: a * 2).eject() == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


def test_map_2() -> None:
    ja = JsonArr(range(10))
    out = ja.map(lambda a, b: a * 2 * b).eject()
    enumerated = [
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
        (5, 10),
        (6, 12),
        (7, 14),
        (8, 16),
        (9, 18),
    ]
    expected = [el[0] * el[1] for el in enumerated]
    assert out == expected


def test_map_3() -> None:
    ja = JsonArr(range(10))
    enumerated = [
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
        (5, 10),
        (6, 12),
        (7, 14),
        (8, 16),
        (9, 18),
    ]
    expected = [el[0] * el[1] * len(ja) for el in enumerated]
    mapped_arr = ja.map(lambda a, b, c: a * 2 * b * len(c)).eject()
    assert mapped_arr == expected


def test_operators() -> None:
    ja = JsonArr(range(5))
    assert ja * 2 == JsonArr(list(range(5)) + list(range(5)))
    assert 2 * ja == JsonArr(list(range(5)) + list(range(5)))
    assert isinstance(2 * ja, JsonArr)
    assert isinstance(ja * 2, JsonArr)


def test_push() -> None:
    ja: JsonArr[int] = JsonArr()
    ja.push(0)
    assert ja.eject() == [0]
    ja.push(1, 2)
    assert ja.eject() == [0, 1, 2]
    ja.push(3, 4, 5, *[6, 7, 8])
    assert ja.eject() == [0, 1, 2, 3, 4, 5, 6, 7, 8]


if __name__ == "__main__":
    ...
