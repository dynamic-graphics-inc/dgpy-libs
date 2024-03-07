# -*- coding: utf-8 -*-
"""Jsonbourne wrapper around httpx clients -- lets you do response.JSON()"""

from __future__ import annotations

from typing import Any

from httpx import AsyncClient, Client, Cookies, Response

from jsonbourne import JSON

__all__ = (
    "AsyncClient",
    "Client",
    "Cookies",
    "Response",
)


def _JSON(self: Response, **kwargs: Any) -> Any:
    json_data = self.json()
    return JSON.jsonify(json_data)


Response.JSON = _JSON
