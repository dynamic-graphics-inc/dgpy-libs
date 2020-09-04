# -*- coding: utf-8 -*-
from typing import Any

from starlette.responses import JSONResponse

from jsonbourne import JSON


class JSONBOURNEResponse(JSONResponse):
    """FastAPI/starlette json response to auto use jsonbourne"""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Return JSON string for content as bytes"""
        return JSON.binify(data=content)
