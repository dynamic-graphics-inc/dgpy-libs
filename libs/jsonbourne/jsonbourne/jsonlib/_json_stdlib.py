# -*- coding: utf-8 -*-
import json

from typing import Any, Callable, Optional

from jsonbourne.jsonlib.base import JsonLibABC, _json_encode_default


class JSON_STDLIB(JsonLibABC):
    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        separators = (",", ": ") if pretty else (",", ":")
        dump_str = json.dumps(
            data,
            indent=2 if pretty else None,
            sort_keys=sort_keys,
            separators=separators,
            default=default or _json_encode_default,
            **kwargs,
        )
        if append_newline:
            return f"{dump_str}\n"
        return dump_str

    @staticmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return JSON_STDLIB.dumps(
            data,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
            **kwargs,
        ).encode()

    @staticmethod
    def loads(string: str, **kwargs: Any) -> Any:
        return json.loads(string, **kwargs)


JSONEncoder = json.JSONEncoder
JSONDecoder = json.JSONDecoder
JSONDecodeError = json.JSONDecodeError
