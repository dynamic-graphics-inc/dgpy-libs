from __future__ import annotations

import sys

from dataclasses import dataclass
from os import environ
from typing import TypedDict

import pytest

from _pytest.config import Config, PytestPluginManager
from _pytest.config.argparsing import Parser
from _pytest.python import Function

from dgpytest import hooks

_CI = environ.get("CI", "false").lower() == "true"


sys_platforms = {
    "win32": "windows",
    "linux": "linux",
    "darwin": "macos",
}


def pytest_addhooks(pluginmanager: PytestPluginManager) -> None:
    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("dgpytest")
    group.addoption(
        "--dgpy-off",
        action="store_true",
        help="Disables dgpytest",
        default=False,
    )


class DgpytestMarkerDict(TypedDict):
    name: str
    desc: str
    skip: bool


@dataclass
class DgpytestMarker:
    name: str
    desc: str
    skip: bool

    def asdict(self) -> DgpytestMarkerDict:
        return {
            "desc": self.desc,
            "name": self.name,
            "skip": self.skip,
        }


dgpytest_markers = {
    "skipci": DgpytestMarker(
        name="skipci",
        desc="mark test to skip if `CI` environment variable is set to `true`.",
        skip=_CI,
    ),
    "skip_darwin": DgpytestMarker(
        name="skip_darwin",
        desc="mark test to skip on macos.",
        skip=sys.platform == "darwin",
    ),
    "skip_linux": DgpytestMarker(
        name="skip_linux",
        desc="mark test to skip on linux.",
        skip=sys.platform == "linux",
    ),
    "skip_win32": DgpytestMarker(
        name="skip_win32",
        desc="mark test to skip on windows.",
        skip=sys.platform == "win32",
    ),
}


def pytest_runtest_setup(item: Function) -> None:
    dgpytest_item_markers = {
        marker.name: marker
        for marker in item.iter_markers()
        if marker.name in dgpytest_markers
    }
    if _CI and "skipci" in dgpytest_item_markers:
        pytest.skip("skipping test on CI")
    for marker_name in dgpytest_item_markers.keys():
        if marker_name.startswith("skip_") and dgpytest_markers[marker_name].skip:
            pytest.skip(f"skipping test on {sys_platforms[sys.platform]}")


def config_add_marker(config: Config, name: str, description: str) -> None:
    line = f"{name}: {description}"
    config.addinivalue_line("markers", line)


def pytest_configure(config: Config) -> None:
    for name, dgpytest_marker in dgpytest_markers.items():
        config_add_marker(config, name, dgpytest_marker.desc)
