# -*- coding: utf-8 -*-
"""Funkify core"""
import sys
from types import ModuleType
from functools import partial


def _funkify(funk=None, *, name=None):
    try:
        _name = name or funk.__module__
    except AttributeError:
        raise ValueError(f"Bad args: funk={funk} name={name}")
    if funk is None:
        return partial(funk=_funkify, name=_name)

    class ModuleCls(ModuleType):
        def __call__(self, *args, **kwargs):
            return funk(*args, **kwargs)

    sys.modules[_name].__class__ = ModuleCls
    return funk


@_funkify
def funkify(funk=None, *, name=None):
    return _funkify(funk=funk, name=name)
