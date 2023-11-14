# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from os import path

import pytest

from shellfish import batman, sh

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.skipif(sys.platform != "win32", reason="only runs on windows")
class TestBatman:
    windows_scripts_dirpath = path.join(PWD, "_windows_test_data")

    def test_cmd_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = batman.bat("cmd_command")
        assert proc.stdout == "Hello\nCMD file\n"

    def test_bat_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = batman.bat("bat_command")
        assert proc.stdout == "Hello\nBAT file\n"
