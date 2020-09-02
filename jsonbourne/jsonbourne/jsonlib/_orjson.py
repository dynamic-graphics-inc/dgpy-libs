# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

import orjson

from jsonbourne.jsonlib.base import JsonLib, _json_encode_default


try:
    import numpy as np
except ImportError:
    np = None


class ORJSON(JsonLib):
    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return ORJSON.dumpb(
            data,
            pretty=pretty,
            sort_keys=sort_keys,
            default=default or _json_encode_default,
        ).decode(encoding="utf-8")

    @staticmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        option = 0
        if pretty:
            option |= orjson.OPT_INDENT_2  # type: ignore
        if sort_keys:
            option |= orjson.OPT_SORT_KEYS
        if np:
            option |= orjson.OPT_SERIALIZE_NUMPY

        return orjson.dumps(
            data, option=option, default=default or _json_encode_default
        )

    @staticmethod
    def loads(string: str, **kwargs: Any) -> Any:
        return orjson.loads(string)


if __name__ == "__main__":
    pass
