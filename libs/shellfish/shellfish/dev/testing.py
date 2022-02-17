# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from xtyping import FsPath, Optional


def assert_symlink_exists(fspath: FsPath, *, target: Optional[FsPath] = None) -> bool:
    _path = Path(fspath)
    try:
        assert _path.exists()
        assert _path.is_symlink()
        if target is not None:
            assert _path.resolve() == Path(target)
        return True
    except AssertionError:
        ...
    return False
