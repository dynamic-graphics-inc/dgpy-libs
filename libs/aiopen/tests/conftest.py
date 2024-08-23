# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from typing import Any

import pytest

_trio_backend = pytest.param(
    ("trio", {"restrict_keyboard_interrupt_to_checkpoints": True}), id="trio"
)
_is_windows = os.name == "nt"


anyio_pytest_fixture = (
    pytest.fixture(
        params=[
            pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
        ]
    )
    if _is_windows
    else pytest.fixture(
        params=[
            pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
            pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
        ]
    )
)


@anyio_pytest_fixture
def anyio_backend(request: Any) -> Any:
    return request.param
