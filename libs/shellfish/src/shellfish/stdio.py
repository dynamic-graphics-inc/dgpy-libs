# -*- coding: utf-8 -*-
"""stdio utils"""

from __future__ import annotations

from enum import IntEnum

__all__ = ("Stdio",)


class Stdio(IntEnum):
    """Standard-io enum object"""

    stdin = 0
    stdout = 1
    stderr = 2
