# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any

try:
    import httpx

    _SINKS = []

    class HttpxSink:
        def __init__(self, url: str, *args: Any, **kwargs: Any) -> None:
            self.url = url
            self.client = httpx.AsyncClient(*args, **kwargs)
            _SINKS.append(self)

        async def __call__(self, msg: Any) -> None:
            httpx.post(self.url, data={"msg": msg})

        async def handle(self, message: Any) -> None:
            await self.client.post(url=self.url, data={"msg": message})

        async def await_delete_channels(self) -> None:
            await self.client.aclose()

except ImportError:
    pass
