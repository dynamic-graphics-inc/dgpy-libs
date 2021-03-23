# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Callable, Optional


try:
    import numpy as np
except ImportError:
    np = None
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any


def _json_encode_default(obj: Any) -> Any:
    if np:
        if isinstance(obj, np.float):
            return float(obj)
        if isinstance(obj, np.int):
            return int(obj)
        if isinstance(obj, (np.ndarray, np.generic)):
            return obj.tolist()

    if isinstance(obj, bytes):
        return str(obj, encoding="utf-8")
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    if isinstance(obj, Decimal):
        return str(obj)
    if hasattr(obj, "eject"):
        return obj.eject()
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "dict"):
        return obj.dict()
    raise TypeError("Cannot encode obj as JSON: {}".format(str(obj)))


class JsonLibABC(ABC):
    @staticmethod
    @abstractmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        ...

    @staticmethod
    @abstractmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        ...

    @staticmethod
    @abstractmethod
    def loads(string: str, **kwargs: Any) -> Any:
        ...

    @staticmethod
    def default(obj: Any) -> Any:
        """Default encoder"""
        return _json_encode_default(obj)
