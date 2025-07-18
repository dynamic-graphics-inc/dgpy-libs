from __future__ import annotations

import json

from collections.abc import AsyncIterable, Awaitable, Iterable
from pathlib import Path
from typing import Callable

import pytest

from shellfish import fs

_FILEPATH = Path(__file__).resolve()

_READ_BYTES_GEN_DEPRECATED_ALIASES = [
    fs.rbin_gen,
    fs.lbytes_gen,
    fs.rbytes_gen,
]
_READ_JSON_DEPRECATED_ALIASES = [
    fs.ljson,
    fs.rjson,
]
_READ_STRING_DEPRECATED_ALIASES = [
    fs.lstring,
    fs.lstr,
    fs.rstr,
    fs.rstring,
]
_WRITE_STRING_DEPRECATED_ALIASES = [
    fs.sstring,
    fs.sstr,
    fs.wstr,
    fs.wstring,
]
_WRITE_BYTES_DEPRECATED_ALIASES = [
    fs.sbytes,
    fs.wbin,
    fs.sbin,
    fs.wbytes,
]
_WRITE_JSON_DEPRECATED_ALIASES = [
    fs.sjson,
    fs.wjson,
]
# async deprecated aliases
_READ_BYTES_GEN_DEPRECATED_ALIASES_ASYNC = [
    fs.rbin_gen_async,
    fs.lbytes_gen_async,
    fs.rbytes_gen_async,
]
_READ_JSON_DEPRECATED_ALIASES_ASYNC = [
    fs.ljson_async,
    fs.rjson_async,
]
_READ_STRING_DEPRECATED_ALIASES_ASYNC = [
    fs.lstring_async,
    fs.rstring_async,
    fs.lstr_async,
    fs.rstr_async,
]

_WRITE_STRING_DEPRECATED_ALIASES_ASYNC = [
    fs.sstring_async,
    fs.wstring_async,
    fs.sstr_async,
    fs.wstr_async,
]
_WRITE_BYTES_DEPRECATED_ALIASES_ASYNC = [
    fs.wbytes_async,
    fs.sbytes_async,
    fs.wbin_async,
    fs.sbin_async,
]
_WRITE_JSON_DEPRECATED_ALIASES_ASYNC = [
    fs.sjson_async,
    fs.wjson_async,
]


class TestDeprecatedAliasesSync:
    @pytest.mark.parametrize("func", _WRITE_STRING_DEPRECATED_ALIASES)
    def test_deprecated_write_string_alias_sync(
        self,
        func: Callable[..., None],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            func(tmp_path / "test.txt", "This is a test string")

    @pytest.mark.parametrize("func", _WRITE_BYTES_DEPRECATED_ALIASES)
    def test_deprecated_read_write_bytes_alias_sync(
        self,
        func: Callable[..., None],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            func(tmp_path / "test.txt", b"This is a test bytes")

    @pytest.mark.parametrize("func", _READ_STRING_DEPRECATED_ALIASES)
    def test_deprecated_read_bytes_alias_sync(
        self,
        func: Callable[..., None],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            func(_FILEPATH)

    @pytest.mark.parametrize("func", _READ_BYTES_GEN_DEPRECATED_ALIASES)
    def test_deprecated_read_bytes_gen_alias_sync(
        self,
        func: Callable[[Path | str], Iterable[bytes]],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            for line in func(_FILEPATH):
                assert isinstance(line, bytes)

    @pytest.mark.parametrize("func", _WRITE_JSON_DEPRECATED_ALIASES)
    def test_deprecated_write_json_alias_sync(
        self,
        func: Callable[..., None],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            func(tmp_path / "test.json", {"key": "value"})
            assert (tmp_path / "test.json").exists()
            text = (tmp_path / "test.json").read_text()
            assert json.loads(text) == {"key": "value"}

    @pytest.mark.parametrize("func", _READ_JSON_DEPRECATED_ALIASES)
    def test_deprecated_read_json_alias_sync(
        self,
        func: Callable[[Path | str], dict],
        tmp_path: Path,
    ) -> None:
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value"}\n')
        with pytest.deprecated_call():
            data = func(json_file)
            assert data == {"key": "value"}
            assert isinstance(data, dict)


class TestDeprecatedAliasesAsync:
    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _WRITE_STRING_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_write_string_alias_async(
        self,
        func: Callable[..., Awaitable[None]],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            await func(tmp_path / "test.txt", "This is a test string")

    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _WRITE_BYTES_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_write_bytes_alias_async(
        self,
        func: Callable[..., Awaitable[None]],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            await func(tmp_path / "test.txt", b"This is a test bytes")

    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _READ_STRING_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_read_str_alias_async(
        self,
        func: Callable[[Path | str], Awaitable[str]],
    ) -> None:
        with pytest.deprecated_call():
            result = await func(_FILEPATH)
            assert isinstance(result, str)

    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _READ_BYTES_GEN_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_read_bytes_gen_alias_async(
        self,
        func: Callable[[Path | str], AsyncIterable[bytes]],
    ) -> None:
        with pytest.deprecated_call():
            async for line in func(_FILEPATH):
                assert isinstance(line, bytes)

    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _WRITE_JSON_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_write_json_alias_async(
        self,
        func: Callable[..., Awaitable[None]],
        tmp_path: Path,
    ) -> None:
        with pytest.deprecated_call():
            await func(tmp_path / "test.json", {"key": "value"})
            assert (tmp_path / "test.json").exists()
            text = (tmp_path / "test.json").read_text()
            assert json.loads(text) == {"key": "value"}

    @pytest.mark.anyio()
    @pytest.mark.parametrize("func", _READ_JSON_DEPRECATED_ALIASES_ASYNC)
    async def test_deprecated_read_json_alias_async(
        self,
        func: Callable[[Path | str], Awaitable[dict]],
        tmp_path: Path,
    ) -> None:
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value"}\n')
        with pytest.deprecated_call():
            data = await func(json_file)
            assert data == {"key": "value"}
            assert isinstance(data, dict)
