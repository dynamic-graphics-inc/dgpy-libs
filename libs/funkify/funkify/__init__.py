# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
import sys

from types import ModuleType
from typing import Any, Callable, Optional, TypeVar, cast

from funkify._meta import __version__

T = TypeVar("T")

__all__ = (
    "__version__",
    "default_export",
    "funkify",
)


def default_export(
    funk: T,
    *,
    key: Optional[str] = None,
) -> T:
    """Assign a function to a module's __call__ attr

    Args:
        funk: function to be made callable
        key (str): module name as it would appear in sys.modules

    Returns:
        Callable[..., T]: the function passed in

    Raises:
        AttributeError: if key is None and exported obj no __module__ attr
        ValueError: if key is not in sys.modules

    """
    try:
        _module: str = key or funk.__module__
    except AttributeError:
        raise AttributeError(
            f"funk ({funk}) has no __module__ attribute; plz provide module key"
        )

    class ModuleCls(ModuleType):
        def __call__(self, *args: Any, **kwargs: Any) -> T:
            return cast(T, funk(*args, **kwargs))  # type: ignore[operator]

    class ModuleClsStaticValue(ModuleCls):
        def __call__(self, *args: Any, **kwargs: Any) -> T:
            return funk

    mod_cls = ModuleCls if callable(funk) else ModuleClsStaticValue

    try:
        sys.modules[_module].__class__ = mod_cls
    except KeyError:
        raise ValueError(f"{_module} not found in sys.modules")
    return funk


@default_export
def funkify(funk: Callable[..., T], *, key: Optional[str] = None) -> Callable[..., T]:
    """Assign a function to a module's __call__ attr

    Args:
        funk: function to be made callable
        key (str): module name as it would appear in sys.modules

    Returns:
        Callable[..., T]: the function passed in

    """
    return default_export(funk=funk, key=key)
