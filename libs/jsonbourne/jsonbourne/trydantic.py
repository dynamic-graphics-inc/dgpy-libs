# -*- coding: utf-8 -*-
"""trydantic = try + pydantic"""
from __future__ import annotations

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

PYDANTIC_AVAILABLE: bool = False

try:
    # use `pydantic.dataclasses.dataclass` if available
    from pydantic.dataclasses import dataclass as dataclass

    PYDANTIC_AVAILABLE = True
except ImportError:
    from dataclasses import dataclass as _dataclass
    from functools import wraps

    # TODO: remove type-ignore if possible
    dataclass = wraps(_dataclass)(  # type: ignore[assignment]
        lambda *args, **kwargs: _dataclass(
            *args, **{k: v for k, v in kwargs.items() if k != "config"}
        )
    )

__all__ = (
    "Field",
    "FrozenInstanceError",
    "InitVar",
    "MISSING",
    "PYDANTIC_AVAILABLE",
    "asdict",
    "astuple",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
    "make_dataclass",
    "replace",
)
