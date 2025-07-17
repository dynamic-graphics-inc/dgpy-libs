# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Protocol, Union

__all__ = (
    "Dumpable",
    "JsonInterface",
    "JsonInterfaceProperty",
    "JsonInterfaceProtocol",
)


class Dumpable(Protocol):
    def __dumpable__(self) -> Any: ...


class JsonInterface(Protocol):
    def __json_interface__(self) -> Any: ...


class JsonInterfaceProperty(Protocol):
    @property
    def __json_interface__(self) -> Any: ...


JsonInterfaceProtocol = Union[JsonInterface, JsonInterfaceProperty]
