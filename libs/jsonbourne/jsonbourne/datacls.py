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

try:
    # use `pydantic.dataclasses.dataclass` if available
    from pydantic.dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


__all__ = (
    'Field',
    'FrozenInstanceError',
    'InitVar',
    'MISSING',
    'asdict',
    'astuple',
    'dataclass',
    'field',
    'fields',
    'is_dataclass',
    'make_dataclass',
    'replace',
)
