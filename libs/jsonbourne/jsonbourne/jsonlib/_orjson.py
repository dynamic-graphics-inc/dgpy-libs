# -*- coding: utf-8 -*-
from sys import modules as _sys_modules
from typing import Any, Callable, Optional

import orjson

from jsonbourne.jsonlib.base import JsonLibABC, _json_encode_default


class ORJSON(JsonLibABC):
    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return ORJSON.dumpb(
            data,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
        ).decode(encoding="utf-8")

    @staticmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        option = 0
        if pretty:
            option |= orjson.OPT_INDENT_2  # type: ignore
        if sort_keys:
            option |= orjson.OPT_SORT_KEYS
        if append_newline:
            option |= orjson.OPT_APPEND_NEWLINE
        if 'numpy' in _sys_modules:
            option |= orjson.OPT_SERIALIZE_NUMPY

        return orjson.dumps(
            data, option=option, default=default or _json_encode_default
        )

    @staticmethod
    def loads(string: str, **kwargs: Any) -> Any:
        return orjson.loads(string)
