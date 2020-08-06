from os import path

import pytest

from jsonbourne import __version__


pytestmark = [pytest.mark.basic]


def _get_version() -> str:
    _dirpath = path.split(path.realpath(__file__))[0]
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


def test_version():
    assert __version__ == _get_version()
