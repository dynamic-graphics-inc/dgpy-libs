# -*- coding: utf-8 -*-
from os import path

import dgpytest


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for _ in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            version = (
                [ln for ln in open(_filepath).read().split("\n") if "version" in ln][0]
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    assert dgpytest.__version__ == _get_version()