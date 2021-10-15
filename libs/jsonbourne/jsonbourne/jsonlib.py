# -*- coding: utf-8 -*-
import json as pyjson

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from sys import modules as _sys_modules
from typing import Any, Callable, List, Optional, Tuple, Type, Union


try:
    import dataclasses
except ImportError:
    dataclasses = None  # type: ignore

try:
    import rapidjson

    RapidJSONEncoder = rapidjson.Encoder
    RapidJSONDecoder = rapidjson.Decoder
    RapidJSONDecodeError = rapidjson.JSONDecodeError

except ImportError:
    rapidjson = None
    RapidJSONEncoder = None
    RapidJSONDecoder = None
    RapidJSONDecodeError = None

try:
    import orjson

except ImportError:
    orjson = None  # type: ignore

try:
    import numpy as np
except ImportError:
    np = None

JSONLIB_DEFAULT_PREFERENCE = ['orjson', 'rapidjson']


def _json_encode_default(obj: Any) -> Any:
    if np:
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, (np.ndarray, np.generic)):
            return obj.tolist()
    if dataclasses:
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
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
    lib = 'json'

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
    @abstractmethod
    def useable() -> bool:
        ...

    @staticmethod
    def default(obj: Any) -> Any:
        """Default encoder"""
        return _json_encode_default(obj)

    @staticmethod
    def has_rapidjson() -> bool:
        return rapidjson is not None

    @staticmethod
    def has_orjson() -> bool:
        return orjson is not None


class JSON_STDLIB(JsonLibABC):
    lib = 'json'
    JSONEncoder = pyjson.JSONEncoder
    JSONDecoder = pyjson.JSONDecoder
    JSONDecodeError = pyjson.JSONDecodeError

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
        dump_str = pyjson.dumps(
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
        return pyjson.loads(string, **kwargs)

    @staticmethod
    def useable() -> bool:
        return True


class ORJSON(JsonLibABC):
    lib = 'orjson'

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
            option |= orjson.OPT_INDENT_2
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

    @staticmethod
    def useable() -> bool:
        return JsonLibABC.has_orjson()


class RAPIDJSON(JsonLibABC):
    lib = 'rapidjson'

    JSONEncoder = RapidJSONEncoder
    JSONDecoder = RapidJSONDecoder
    JSONDecodeError = RapidJSONDecodeError

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

    @staticmethod
    def useable() -> bool:
        return JsonLibABC.has_rapidjson()


def pick_lib() -> "Type[JsonLibABC]":
    if ORJSON.useable():
        return ORJSON
    if RAPIDJSON.useable():
        return RAPIDJSON
    return JSON_STDLIB


def _import_rapidjson() -> "Type[RAPIDJSON]":
    if RAPIDJSON.useable():
        return RAPIDJSON
    raise ImportError('rapidjson (python-rapidjson) not installed')


def _import_orjson() -> "Type[ORJSON]":
    if ORJSON.useable():
        return ORJSON
    raise ImportError('orjson not installed')


def _import_json_stdlib() -> "Type[JSON_STDLIB]":
    return JSON_STDLIB


def import_json(
    jsonlibs: Optional[Union[Tuple[str], List[str]]] = None
) -> "Type[JsonLibABC]":
    lib2funk = {
        "rapidjson": _import_rapidjson,
        "orjson": _import_orjson,
        "json": _import_json_stdlib,
    }
    jsonlibs = jsonlibs or JSONLIB_DEFAULT_PREFERENCE

    for mod in jsonlibs:
        try:
            return lib2funk[mod]()
        except (ImportError, ModuleNotFoundError):
            pass

    return _import_json_stdlib()


JSONLIB: Type[JsonLibABC] = import_json()


def dumps(
    data: Any,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> str:
    return JSONLIB.dumps(
        data=data,
        pretty=pretty,
        sort_keys=sort_keys,
        append_newline=append_newline,
        default=default,
        **kwargs,
    )


def dumpb(
    data: Any,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> bytes:
    return JSONLIB.dumpb(
        data=data,
        pretty=pretty,
        sort_keys=sort_keys,
        append_newline=append_newline,
        default=default,
        **kwargs,
    )


def loads(string: str, **kwargs: Any) -> Any:
    return JSONLIB.loads(string, **kwargs)


def use_orjson() -> None:
    global JSONLIB
    JSONLIB = _import_orjson()


def use_rapidjson() -> None:
    global JSONLIB
    JSONLIB = _import_rapidjson()


def use_json_stdlib() -> None:
    global JSONLIB
    JSONLIB = _import_json_stdlib()


def use_json() -> None:
    use_json_stdlib()


def which() -> str:
    return JSONLIB.lib
