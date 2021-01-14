# -*- coding: utf-8 -*-
"""Jsonbourne wrapper around httpx clients -- lets you do response.JSON()"""

from typing import Any

from httpx import AsyncClient, Client, Cookies, Response

from jsonbourne import JSON


__all__ = ['Response', 'AsyncClient', 'Client', 'Cookies']


def _JSON(self: Response, **kwargs: Any) -> Any:
    return JSON(self.json())  # type: ignore


Response.JSON = _JSON
