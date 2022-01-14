# -*- coding: utf-8 -*-
"""dataclasses ~ `pydantic.dataclasses.dataclass` > `dataclasses.dataclass`"""
from dataclasses import (
    MISSING,
    Field,
    FrozenInstanceError,
    InitVar,
    asdict,
    astuple,
    field,
    fields,
    is_dataclass,
    make_dataclass,
    replace,
)

_PYDANTIC_AVAILABLE: bool = False

try:
    # use `pydantic.dataclasses.dataclass` if available
    from pydantic.dataclasses import dataclass as _dataclass

    _PYDANTIC_AVAILABLE = True
except ImportError:
    from dataclasses import dataclass as _dataclass  # type: ignore
    from functools import wraps

    dataclass = wraps(_dataclass)(
        lambda *args, **kwargs: _dataclass(
            *args, **{k: v for k, v in kwargs.items() if k != "config"}
        )
    )

__all__ = (
    "Field",
    "FrozenInstanceError",
    "InitVar",
    "MISSING",
    "asdict",
    "astuple",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
    "make_dataclass",
    "replace",
)
