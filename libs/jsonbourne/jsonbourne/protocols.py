# -*- coding: utf-8 -*-
from xtyping import Any, Protocol, Union

__all__ = (
    "JsonInterface",
    "JsonInterfaceProperty",
    "JsonInterfaceProtocol",
    "Dumpable",
)


class Dumpable(Protocol):
    def __dumpable__(self) -> Any:
        ...


class JsonInterface(Protocol):
    def __json_interface__(self) -> Any:
        ...


class JsonInterfaceProperty(Protocol):
    @property
    def __json_interface__(self) -> Any:
        ...


JsonInterfaceProtocol = Union[JsonInterface, JsonInterfaceProperty]
