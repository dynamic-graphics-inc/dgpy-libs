# -*- coding: utf-8 -*-
"""Jsonbourne wrapper around httpx clients -- lets you do response.JSON()"""

from typing import Any

from httpx import Response, __all__ as __httpx_all__

from jsonbourne import JSON


__all__ = [*__httpx_all__]


def _JSON(self, **kwargs: Any) -> Any:
    return JSON(self.json())


Response.JSON = _JSON
