# -*- coding: utf-8 -*-
"""Funkify core"""
import sys

from types import ModuleType
from typing import Any, Callable, Optional, TypeVar


T = TypeVar('T')


def _funkify(funk: Callable[..., T], *, name: Optional[str] = None) -> Callable[..., T]:
    try:
        _name = name or funk.__module__
    except AttributeError:
        raise ValueError(f"Bad args: funk={funk} name={name}")

    class ModuleCls(ModuleType):
        def __call__(self, *args: Any, **kwargs: Any) -> T:
            return funk(*args, **kwargs)

    sys.modules[_name].__class__ = ModuleCls
    return funk


@_funkify
def funkify(funk: Callable[..., T], *, name: Optional[str] = None) -> Callable[..., T]:
    """Funkify a module"""
    return _funkify(funk=funk, name=name)
