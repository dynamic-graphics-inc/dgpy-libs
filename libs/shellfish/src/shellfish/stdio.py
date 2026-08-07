# -*- coding: utf-8 -*-
"""stdio utils"""

from __future__ import annotations

from enum import IntEnum

__all__ = ("Stdio",)


class Stdio(IntEnum):
    """Standard-io enum object; values are the standard file descriptors

    Examples:
        >>> from shellfish.stdio import Stdio
        >>> Stdio.stdout
        <Stdio.stdout: 1>
        >>> int(Stdio.stderr)
        2

    """

    stdin = 0
    """Standard input (fd 0)"""
    stdout = 1
    """Standard output (fd 1)"""
    stderr = 2
    """Standard error (fd 2)"""
