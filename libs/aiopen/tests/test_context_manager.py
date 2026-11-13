# -*- coding: utf-8 -*-
from __future__ import annotations

from types import CodeType, FrameType
from typing import TYPE_CHECKING

from aiopen import aiopen

if TYPE_CHECKING:
    from pathlib import Path


def test_gi_properties_delegate_to_coroutine(tmp_path: Path) -> None:
    """`gi_*` used to raise AttributeError (native coroutines only have `cr_*`)"""
    fspath = tmp_path / "file.txt"
    fspath.write_text("x")
    cm = aiopen(fspath)
    try:
        assert isinstance(cm.gi_frame, FrameType)
        assert cm.gi_running is False
        assert isinstance(cm.gi_code, CodeType)
    finally:
        cm.close()
