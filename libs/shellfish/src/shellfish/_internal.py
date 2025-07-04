from __future__ import annotations

from functools import wraps
from inspect import signature
from typing import Callable, TypeVar
from warnings import warn

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def deprecated_alias(
    target: Callable[P, R], *, msg: str | None = None
) -> Callable[P, R]:
    _warn_msg = f"use of deprecated alias which will be removed in a future release; use {target.__name__}() instead."

    @wraps(target)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        warn(
            _warn_msg if msg is None else msg,
            DeprecationWarning,
            stacklevel=2,
        )
        return target(*args, **kwargs)

    # forward `help()` signature etc...
    try:
        _wrapper.__signature__ = signature(target)  # type: ignore[attr-defined]
    except (ValueError, TypeError):
        ...

    return _wrapper
