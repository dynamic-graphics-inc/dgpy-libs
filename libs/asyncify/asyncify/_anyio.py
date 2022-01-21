# -*- coding: utf-8 -*-
from functools import partial, wraps

from anyio import (
    CapacityLimiter as CapacityLimiter,
    run as anyio_run,
    to_thread as to_thread,
)

from xtyping import Awaitable, Callable, Optional, ParamSpec, TypeVar

__all__ = (
    "anyio_run",
    "asyncify",
)

P = ParamSpec("P")
T = TypeVar("T")


def asyncify(
    funk: Callable[P, T],
    *,
    cancellable: bool = False,
    limiter: Optional[CapacityLimiter] = None,
) -> Callable[P, Awaitable[T]]:
    """asyncify decorator/wrapper that for use w/ anyio"""

    @wraps(funk)
    async def _async_fn(*args: P.args, **kwargs: P.kwargs) -> T:
        partial_f = partial(funk, *args, **kwargs)
        return await to_thread.run_sync(
            partial_f, cancellable=cancellable, limiter=limiter
        )

    return _async_fn
