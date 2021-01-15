# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

from jsonbourne.jsonlib.base import JsonLibABC, _json_encode_default


try:
    import rapidjson

    JSONEncoder = rapidjson.Encoder
    JSONDecoder = rapidjson.Decoder
    JSONDecodeError = rapidjson.JSONDecodeError
except ImportError:
    rapidjson = None
JSONLIB = 'rapidjson'


class RAPIDJSON(JsonLibABC):
    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        dump_str = str(
            rapidjson.dumps(
                data,
                indent=2 if pretty else None,
                sort_keys=sort_keys,
                default=default or _json_encode_default,
                datetime_mode=rapidjson.DM_ISO8601,
                **kwargs,
            )
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
        return RAPIDJSON.dumps(
            data,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
            **kwargs,
        ).encode()

    @staticmethod
    def loads(string: str, **kwargs: Any) -> Any:
        return rapidjson.loads(string, **kwargs)
