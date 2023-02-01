# -*- coding: utf-8 -*-
from os import path

from asyncify import __version__


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
    version = "UNKNOWN???"
    for _i in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            version = (
                [
                    line
                    for line in open(_filepath).read().split("\n")
                    if "version" in line
                ][0]
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    assert __version__ == _get_version()
