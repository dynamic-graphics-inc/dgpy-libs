# -*- coding: utf-8 -*-
from typing import Any

from jsonbourne import JSON


try:
    from starlette.responses import Response
except ModuleNotFoundError:
    Response = object


class JSONBOURNEResponse(Response):  # type: ignore
    """FastAPI/starlette json response to auto use jsonbourne"""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Return JSON string for content as bytes"""
        return JSON.binify(data=content)
