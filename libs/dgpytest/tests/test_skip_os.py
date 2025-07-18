from __future__ import annotations

import sys

import pytest

from dgpytest import skipif_windows


@skipif_windows
def test_skip_if_windows() -> None:
    assert True


@pytest.mark.skip_darwin
def test_darwin_marker_skip() -> None:
    assert sys.platform != "darwin"


@pytest.mark.skip_linux
def test_linux_marker_skip() -> None:
    assert sys.platform != "linux"


@pytest.mark.skip_win32
def test_if_win32_crashes_skip() -> None:
    assert sys.platform != "win32"
