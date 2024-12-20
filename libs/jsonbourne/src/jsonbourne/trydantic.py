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
from typing import Union

__pydantic__: bool = False
__pydantic_version__: Union[str, bool] = False

try:
    import pydantic

    # use `pydantic.dataclasses.dataclass` if available
    from pydantic.dataclasses import dataclass as dataclass

    __pydantic__ = True
    __pydantic_version__ = pydantic.__version__
except ImportError:
    from dataclasses import dataclass as _dataclass
    from functools import wraps

    # TODO: remove type-ignore if possible
    dataclass = wraps(_dataclass)(
        lambda *args, **kwargs: _dataclass(
            *args, **{k: v for k, v in kwargs.items() if k != "config"}
        )
    )

__all__ = (
    "MISSING",
    "Field",
    "FrozenInstanceError",
    "InitVar",
    "__pydantic__",
    "__pydantic_version__",
    "asdict",
    "astuple",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
    "make_dataclass",
    "replace",
)
