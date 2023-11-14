# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

import pytest

_trio_backend = pytest.param(
    ("trio", {"restrict_keyboard_interrupt_to_checkpoints": True}), id="trio"
)


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
        pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
    ]
)
def anyio_backend(request: Any) -> Any:
    return request.param
