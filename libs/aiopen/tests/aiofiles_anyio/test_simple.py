# -*- coding: utf-8 -*-
"""Simple tests verifying basic functionality."""

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING, Any

import pytest

import aiopen as aio

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.anyio()
async def test_serve_small_bin_file_sync(tmp_path: Path, unused_tcp_port: int) -> None:
    """Fire up a small simple file server, and fetch a file.

    The file is read into memory synchronously, so this test doesn't actually
    test anything except the general test concept.
    """
    # First we'll write a small file.
    filename = "test.bin"
    file_content = b"0123456789"
    file = tmp_path.joinpath(filename)
    file.write_bytes(file_content)

    async def serve_file(reader: Any, writer: Any) -> None:
        full_filename = str(file)
        with open(full_filename, "rb") as f:
            writer.write(f.read())
        writer.close()

    server = await asyncio.start_server(
        serve_file,
        port=unused_tcp_port,
    )

    reader, _ = await asyncio.open_connection(
        host="localhost",
        port=unused_tcp_port,
    )

    payload = await reader.read()

    assert payload == file_content

    server.close()
    await server.wait_closed()


@pytest.mark.anyio()
async def test_serve_small_bin_file(tmp_path: Path, unused_tcp_port: int) -> None:
    """Fire up a small simple file server, and fetch a file."""
    # First we'll write a small file.
    filename = "test.bin"
    file_content = b"0123456789"
    file = tmp_path.joinpath(filename)
    file.write_bytes(file_content)

    async def serve_file(reader: Any, writer: Any) -> None:
        full_filename = str(file)
        f = await aio.aiopen(full_filename, mode="rb")
        writer.write(await f.read())
        await f.close()
        writer.close()

    server = await asyncio.start_server(
        serve_file,
        port=unused_tcp_port,
    )

    reader, _ = await asyncio.open_connection(
        host="localhost",
        port=unused_tcp_port,
    )

    payload = await reader.read()

    assert payload == file_content

    server.close()
    await server.wait_closed()
