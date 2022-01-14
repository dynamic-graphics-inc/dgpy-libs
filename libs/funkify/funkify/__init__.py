# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
import sys

from types import ModuleType
from typing import Any, Callable, Optional, TypeVar

from funkify._meta import __version__

T = TypeVar("T")

__all__ = (
    "__version__",
    "default_export",
    "funkify",
)


def default_export(
    funk: Callable[..., T],
    *,
    key: Optional[str] = None,
) -> Callable[..., T]:
    """

    Args:
        funk: function to be made callable
        key (str): module name as it would appear in sys.modules

    Returns:

    """
    try:
        _module: str = key or funk.__module__
    except AttributeError:
        raise AttributeError(
            f"funk ({funk}) has no __module__ attribute; provide module key"
        )

    class ModuleCls(ModuleType):
        def __call__(self, *args: Any, **kwargs: Any) -> T:
            return funk(*args, **kwargs)

    try:
        sys.modules[_module].__class__ = ModuleCls
    except KeyError:
        raise ValueError(f"{_module} not found in sys.modules")
    return funk


@default_export
def funkify(funk: Callable[..., T], *, key: Optional[str] = None) -> Callable[..., T]:
    """Funkify a module"""
    return default_export(funk=funk, key=key)
