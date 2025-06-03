# -*- coding: utf-8 -*-
"""jsonbourne jsonlib api"""

# pyright: reportOptionalMemberAccess=false
from __future__ import annotations

import dataclasses
import json as pyjson

from abc import ABC, abstractmethod
from datetime import date as dtdate, datetime, time as dttime, timedelta
from decimal import Decimal
from pathlib import Path
from sys import modules as _sys_modules
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Type, Union
from uuid import UUID

if TYPE_CHECKING:
    from jsonbourne.protocols import Dumpable, JsonInterfaceProtocol

try:
    from jsonc2json import jsonc2json
except ImportError:

    def jsonc2json(s: str) -> str:
        raise ImportError("jsonc2json not installed")


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
    orjson = None  # type: ignore[assignment]

try:
    import numpy as np
except ImportError:
    np = None

JSONLIB_DEFAULT_PREFERENCE = (
    "orjson",
    "rapidjson",
)


def _json_interface(obj: JsonInterfaceProtocol) -> Any:
    _json_interface = obj.__json_interface__
    if callable(_json_interface):
        _json_interface = _json_interface()
    return _json_interface


def _dumpable(obj: Dumpable) -> Any:
    return obj.__dumpable__()


def _json_encode_default(obj: Any) -> Any:
    if hasattr(obj, "__dumpable__"):
        return _dumpable(obj)
    if hasattr(obj, "__json_interface__"):
        return _json_interface(obj)
    if np:
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, (np.ndarray, np.generic)):
            return obj.tolist()
    if dataclasses.is_dataclass(obj) and callable(obj):
        obj_instance = obj()
        return dataclasses.asdict(obj_instance)
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, bytes):
        return str(obj, encoding="utf-8")
    if isinstance(obj, tuple):
        return tuple(obj)
    if isinstance(obj, (Path, UUID)):
        return str(obj)
    if isinstance(obj, (datetime, dttime, dtdate)):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    if isinstance(obj, Decimal):
        return float(obj)
    if hasattr(obj, "eject"):
        return obj.eject()
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "dict"):
        return obj.dict()

    raise TypeError(f"Cannot encode obj as JSON: {str(obj)}")


class JsonLibABC(ABC):
    lib = "json"

    @staticmethod
    @abstractmethod
    def dumps(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str: ...

    @staticmethod
    @abstractmethod
    def dumpb(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes: ...

    @staticmethod
    @abstractmethod
    def loads(
        string: Union[bytes, str],
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
        **kwargs: Any,
    ) -> Any: ...

    @staticmethod
    @abstractmethod
    def usable() -> bool: ...

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

    @staticmethod
    @abstractmethod
    def jsoncp(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any: ...


class JSON_STDLIB(JsonLibABC):
    lib = "json"
    JSONEncoder = pyjson.JSONEncoder
    JSONDecoder = pyjson.JSONDecoder
    JSONDecodeError = pyjson.JSONDecodeError

    @staticmethod
    def dumps(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        _pretty = fmt or pretty
        separators = (",", ": ") if _pretty else (",", ":")
        dump_str = pyjson.dumps(
            data,
            indent=2 if _pretty else None,
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
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return JSON_STDLIB.dumps(
            data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
            **kwargs,
        ).encode()

    @staticmethod
    def loads(
        string: Union[bytes, str],
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
        **kwargs: Any,
    ) -> Any:
        if jsonc:
            string = jsonc2json(string)
        if ndjson or jsonl:
            return [
                pyjson.loads(line, **kwargs)
                for line in string.splitlines(keepends=False)
            ]
        return pyjson.loads(string, **kwargs)

    @staticmethod
    def usable() -> bool:
        return True

    @staticmethod
    @abstractmethod
    def jsoncp(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return JSON_STDLIB.loads(
            JSON_STDLIB.dumps(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default or _json_encode_default,
                **kwargs,
            )
        )


class ORJSON(JsonLibABC):
    lib = "orjson"

    @staticmethod
    def dumps(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return ORJSON.dumpb(
            data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
        ).decode(encoding="utf-8")

    @staticmethod
    def dumpb(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        option = 0
        if fmt or pretty:
            option |= orjson.OPT_INDENT_2
        if sort_keys:
            option |= orjson.OPT_SORT_KEYS
        if append_newline:
            option |= orjson.OPT_APPEND_NEWLINE
        if "numpy" in _sys_modules:
            option |= orjson.OPT_SERIALIZE_NUMPY

        return orjson.dumps(
            data, option=option, default=default or _json_encode_default
        )

    @staticmethod
    def loads(
        string: Union[bytes, str],
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
        **kwargs: Any,
    ) -> Any:
        if jsonc:
            string = jsonc2json(string)
        if ndjson or jsonl:
            return [orjson.loads(line) for line in string.splitlines(keepends=False)]
        return orjson.loads(string)

    @staticmethod
    def usable() -> bool:
        return JsonLibABC.has_orjson()

    @staticmethod
    @abstractmethod
    def jsoncp(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return ORJSON.loads(
            ORJSON.dumpb(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default or _json_encode_default,
                **kwargs,
            )
        )


class RAPIDJSON(JsonLibABC):
    lib = "rapidjson"

    JSONEncoder = RapidJSONEncoder
    JSONDecoder = RapidJSONDecoder
    JSONDecodeError = RapidJSONDecodeError

    @staticmethod
    def dumps(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        dump_str = str(
            rapidjson.dumps(
                data,
                indent=2 if (fmt or pretty) else None,
                sort_keys=sort_keys,
                default=default or _json_encode_default,
                datetime_mode=rapidjson.DM_ISO8601,
                number_mode=rapidjson.NM_NATIVE,
                uuid_mode=rapidjson.UM_CANONICAL,
                **kwargs,
            )
        )
        if append_newline:
            return f"{dump_str}\n"
        return dump_str

    @staticmethod
    def dumpb(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return RAPIDJSON.dumps(
            data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default or _json_encode_default,
            **kwargs,
        ).encode()

    @staticmethod
    def loads(
        string: Union[bytes, str],
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
        **kwargs: Any,
    ) -> Any:
        if jsonc and "parse_mode" not in kwargs:
            kwargs["parse_mode"] = rapidjson.PM_COMMENTS
        if ndjson or jsonl:
            return [
                rapidjson.loads(line, **kwargs)
                for line in string.splitlines(keepends=False)
            ]
        return rapidjson.loads(string, **kwargs)

    @staticmethod
    def usable() -> bool:
        return JsonLibABC.has_rapidjson()

    @staticmethod
    @abstractmethod
    def jsoncp(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return RAPIDJSON.loads(
            RAPIDJSON.dumps(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default or _json_encode_default,
                **kwargs,
            )
        )


def pick_lib() -> "Type[JsonLibABC]":
    if ORJSON.usable():
        return ORJSON
    if RAPIDJSON.usable():
        return RAPIDJSON
    return JSON_STDLIB


def _import_rapidjson() -> "Type[RAPIDJSON]":
    if RAPIDJSON.usable():
        return RAPIDJSON
    raise ImportError("rapidjson (python-rapidjson) not installed")


def _import_orjson() -> "Type[ORJSON]":
    if ORJSON.usable():
        return ORJSON
    raise ImportError("orjson not installed")


def _import_json_stdlib() -> "Type[JSON_STDLIB]":
    return JSON_STDLIB


def import_json(
    jsonlibs: Optional[Union[Tuple[str, ...], List[str]]] = None,
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


class JsonLib:
    _jsonlib: Type[JsonLibABC]
    _oj: Optional[Type[ORJSON]] = None
    _rj: Optional[Type[RAPIDJSON]] = None

    def __init__(self, jsonlib: Optional[Type[JsonLibABC]] = None):
        if jsonlib:
            self._jsonlib = jsonlib
        else:
            self._jsonlib = import_json()
        if ORJSON.usable():
            self._oj = ORJSON
        if RAPIDJSON.usable():
            self._rj = RAPIDJSON

    def dumps(
        self,
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return self._jsonlib.dumps(
            data=data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    def dumpb(
        self,
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return self._jsonlib.dumpb(
            data=data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    def loads(
        self, string: Union[bytes, str], jsonc: bool = False, **kwargs: Any
    ) -> Any:
        if jsonc and self._rj:
            return self._rj.loads(string, jsonc=jsonc, **kwargs)
        return self._jsonlib.loads(string, jsonc=jsonc, **kwargs)

    def orjson_usable(self) -> bool:
        return ORJSON.usable()

    def rapidjson_usable(self) -> bool:
        return RAPIDJSON.usable()

    def use_orjson(self) -> None:
        self._jsonlib = _import_orjson()

    def use_rapidjson(self) -> None:
        self._jsonlib = _import_rapidjson()

    def use_json_stdlib(self) -> None:
        self._jsonlib = _import_json_stdlib()

    def use_json(self) -> None:
        self.use_json_stdlib()

    def which(self) -> str:
        return self._jsonlib.lib

    def jsoncp(
        self,
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return self._jsonlib.jsoncp(
            data=data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )


_JSONLIB: Type[JsonLibABC] = import_json()
JSONLIB = JsonLib(_JSONLIB)


def dumps(
    data: Any,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> str:
    return JSONLIB.dumps(
        data=data,
        fmt=fmt,
        pretty=pretty,
        sort_keys=sort_keys,
        append_newline=append_newline,
        default=default,
        **kwargs,
    )


def dumpb(
    data: Any,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> bytes:
    return JSONLIB.dumpb(
        data=data,
        fmt=fmt,
        pretty=pretty,
        sort_keys=sort_keys,
        append_newline=append_newline,
        default=default,
        **kwargs,
    )


def loads(
    string: Union[bytes, str],
    jsonc: bool = False,
    jsonl: bool = False,
    ndjson: bool = False,
    **kwargs: Any,
) -> Any:
    if ndjson or jsonl:
        return [
            JSONLIB.loads(line, jsonc=jsonc, **kwargs)
            for line in string.splitlines(keepends=False)
        ]
    return JSONLIB.loads(string, jsonc=jsonc, **kwargs)


def parse(string: Union[bytes, str], jsonc: bool = False, **kwargs: Any) -> Any:
    return loads(string, jsonc=jsonc, **kwargs)


def wjson(
    fspath: Union[str, Path],
    data: Any,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> int:
    with open(fspath, "wb") as f:
        bytes_written = f.write(
            JSONLIB.dumpb(
                data, fmt, pretty, sort_keys, append_newline, default, **kwargs
            )
        )
    return bytes_written


def rjson(
    fspath: Union[str, Path],
    jsonc: bool = False,
    jsonl: bool = False,
    ndjson: bool = False,
    **kwargs: Any,
) -> Any:
    with open(fspath, "rb") as f:
        s = f.read()
    return loads(s, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson, **kwargs)


def jsoncp(
    data: Any,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    **kwargs: Any,
) -> Any:
    return JSONLIB.jsoncp(
        data=data,
        fmt=fmt,
        pretty=pretty,
        sort_keys=sort_keys,
        append_newline=append_newline,
        default=default,
        **kwargs,
    )


def orjson_usable() -> bool:
    return JSONLIB.orjson_usable()


def rapidjson_usable() -> bool:
    return JSONLIB.rapidjson_usable()


def use_orjson() -> None:
    JSONLIB.use_orjson()


def use_rapidjson() -> None:
    JSONLIB.use_rapidjson()


def use_json_stdlib() -> None:
    JSONLIB.use_json_stdlib()


def use_json() -> None:
    use_json_stdlib()


def which() -> str:
    return JSONLIB.which()
