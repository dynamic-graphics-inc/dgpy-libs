# -*- coding: utf-8 -*-
"""`funkify` ~ make modules callable"""
import sys

from types import ModuleType
from typing import Any, Callable, Optional

from xtyping import T

from funkify._meta import __version__


def default_export(
    funk: Callable[..., T],
    *,
    module: Optional[str] = None,
) -> Callable[..., T]:
    """

    Args:
        funk: function to be made callable
        module (str): module name as it would appear in sys.modules

    Returns:

    """
    try:
        _module: str = module or funk.__module__
    except AttributeError:
        raise AttributeError(
            f"funk ({funk}) has no __module__ attribute; provide module name"
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
def funkify(
    funk: Callable[..., T], *, module: Optional[str] = None
) -> Callable[..., T]:
    """Funkify a module"""
    return default_export(funk=funk, module=module)


__all__ = (
    "__version__",
    "default_export",
    "funkify",
)
