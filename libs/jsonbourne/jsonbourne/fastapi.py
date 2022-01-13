# -*- coding: utf-8 -*-
import os

from typing import Any

from jsonbourne import JSON

try:
    from starlette.responses import Response
except ModuleNotFoundError:
    if not ("CI" in os.environ and os.environ["CI"] == "true"):
        raise ModuleNotFoundError(
            "starlette not found/installed; `pip install starlette`"
        )
    else:
        Response = object  # type: ignore

__all__ = ("JSONBOURNEResponse",)


class JSONBOURNEResponse(Response):
    """FastAPI/starlette json response to auto use jsonbourne"""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Return JSON string for content as bytes"""
        return JSON.binify(data=content)
