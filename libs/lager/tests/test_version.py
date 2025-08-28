# -*- coding: utf-8 -*-
from __future__ import annotations

from os import path

from lager import __version__

PWD = path.split(path.realpath(__file__))[0]


def _get_version() -> str:
    _dirpath = PWD
    version = "UNKNOWN???"
    for _i in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            version = (
                next(
                    line
                    for line in open(_filepath).read().split("\n")
                    if "version" in line
                )
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    pyproject_version: str = _get_version()
    assert __version__ == pyproject_version
