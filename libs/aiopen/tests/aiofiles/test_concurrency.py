# -*- coding: utf-8 -*-
"""Test concurrency properties of the implementation."""
from __future__ import annotations

import asyncio
import time

from os.path import dirname, join
from typing import Any

import pytest

from _pytest.monkeypatch import MonkeyPatch

import aiopen as aio


@pytest.mark.asyncio()
async def test_slow_file(monkeypatch: MonkeyPatch, unused_tcp_port: int) -> None:
    """Monkey patch open and file.read(), and assert the loop still works."""
    filename = join(dirname(__file__), "resources", "multiline_file.txt")

    with open(filename, mode="rb") as f:
        contents = f.read()

    def new_open(*args: Any, **kwargs: Any) -> Any:
        time.sleep(1)
        return open(*args, **kwargs)

    monkeypatch.setattr(aio.core, "_open", value=new_open)

    async def serve_file(_: Any, writer: Any) -> None:
        async with aio.aiopen(filename, mode="rb") as f:
            while True:
                data = await f.read(1)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
            await writer.drain()
        writer.close()

    async def return_one(_: Any, writer: Any) -> None:
        writer.write(b"1")
        await writer.drain()
        writer.close()

    counter = 0

    async def spam_client() -> None:
        nonlocal counter
        while True:
            r, w = await asyncio.open_connection("127.0.0.1", port=30001)
            assert (await r.read()) == b"1"
            counter += 1
            w.close()
            await asyncio.sleep(0.01)

    file_server = await asyncio.start_server(serve_file, port=unused_tcp_port)
    spam_server = await asyncio.start_server(return_one, port=30001)

    spam_task = asyncio.ensure_future(spam_client())

    reader, writer = await asyncio.open_connection("127.0.0.1", port=unused_tcp_port)

    actual_contents = await reader.read()
    writer.close()

    await asyncio.sleep(0)

    file_server.close()
    spam_server.close()

    await file_server.wait_closed()
    await spam_server.wait_closed()

    spam_task.cancel()

    assert actual_contents == contents
    assert counter > 30
