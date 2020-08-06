# -*- coding: utf-8 -*-
# =============================================================================
#  (c) Copyright 2020, Dynamic Graphics, Inc.
#  ALL RIGHTS RESERVED
#  Permission to use, copy, modify, or distribute this software for any
#  purpose is prohibited without specific, written prior permission from
#  Dynamic Graphics, Inc.
# =============================================================================
from os import path

from lager import __version__


PWD = path.split(path.realpath(__file__))[0]


def _get_version() -> str:
    _dirpath = PWD
    version = "UNKNOWN???"
    for i in range(3):
        _filepath = path.join(_dirpath, "pyproject.toml")
        if path.exists(_filepath):
            version = (
                [l for l in open(_filepath).read().split("\n") if "version" in l][0]
                .replace("version = ", "")
                .strip('"')
            )
            return version
        _dirpath = path.split(_dirpath)[0]
    return version


def test_version() -> None:
    pyproject_version: str = _get_version()
    assert __version__ == pyproject_version
