# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

from jsonbourne.jsonlib.base import JsonLib, _json_encode_default


try:
    import rapidjson

    JSONEncoder = rapidjson.Encoder
    JSONDecoder = rapidjson.Decoder
    JSONDecodeError = rapidjson.JSONDecodeError
except ImportError:
    rapidjson = None
JSONLIB = 'rapidjson'


class RAPIDJSON(JsonLib):
    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return str(
            rapidjson.dumps(
                data,
                indent=2 if pretty else None,
                sort_keys=sort_keys,
                default=default or _json_encode_default,
                datetime_mode=rapidjson.DM_ISO8601,
                **kwargs,
            )
        )

    @staticmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return RAPIDJSON.dumps(
            data,
            pretty=pretty,
            sort_keys=sort_keys,
            default=default or _json_encode_default,
            **kwargs,
        ).encode()

    @staticmethod
    def loads(string: str, **kwargs: Any) -> Any:
        return rapidjson.loads(string, **kwargs)


if __name__ == "__main__":
    pass
