# -*- coding: utf-8 -*-
from __future__ import annotations

from os import path
from pathlib import Path

import pytest

from aiopen import __version__

pytestmark = [pytest.mark.version]


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for _i in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            return (
                next(
                    line
                    for line in Path(_filepath).read_text(encoding="utf8").split("\n")
                    if "version" in line
                )
                .replace("version = ", "")
                .strip('"')
            )
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    assert __version__ == _get_version()
