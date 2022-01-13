# -*- coding: utf-8 -*-
"""shellfish tests"""
from os import path

import shellfish


def _get_version() -> str:
    """get version from pyproject.toml"""
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for _ in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            with open(_filepath, encoding="utf8") as f:
                version = (
                    [ln for ln in f.read().split("\n") if "version" in ln][0]
                    .replace("version = ", "")
                    .strip('"')
                )
                return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    """test that package __version__ and pyproject.toml version match"""
    assert shellfish.__version__ == _get_version()
