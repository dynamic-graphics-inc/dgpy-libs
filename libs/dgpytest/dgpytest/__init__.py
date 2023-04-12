# -*- coding: utf-8 -*-
# pyright: reportInvalidTypeVarUse=false
"""dgpytest = dgpy + pytest"""
import sys

from os import environ

import pytest

from dgpytest._meta import __version__

__all__ = ("__version__",)

skipif_windows = skipif_win32 = pytest.mark.skipif(
    sys.platform == "win32", reason="Test skipped on windows"
)

skipif_linux = pytest.mark.skipif(
    sys.platform == "linux", reason="Test skipped on linux"
)

skipif_macos = pytest.mark.skipif(
    sys.platform == "darwin", reason="Test skipped on macos"
)

only_windows = pytest.mark.skipif(
    sys.platform != "win32", reason="Test only runs on windows"
)

skipif_ci = pytest.mark.skipif(
    environ.get("CI", "false").lower() == "true", reason="Test skipped on CI"
)
