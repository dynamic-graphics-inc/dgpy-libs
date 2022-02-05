# -*- coding: utf-8 -*-
import sys

from os import path

import pytest

from shellfish import sh

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.skipif(sys.platform != "win32", reason="only runs on windows")
class TestWindowsSubproccess:
    windows_scripts_dirpath = path.join(PWD, "_windows_test_data")

    def test_cmd_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = sh.do("cmd_command")
        assert proc.stdout == "Hello\nCMD file\n"

    def test_bat_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = sh.do("bat_command")
        assert proc.stdout == "Hello\nBAT file\n"

    @pytest.mark.asyncio
    async def test_cmd_command_async(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = await sh.do_async("cmd_command")
        assert proc.stdout == "Hello\nCMD file\n"

    @pytest.mark.asyncio
    async def test_bat_command_async(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = await sh.do_async("bat_command")
        assert proc.stdout == "Hello\nBAT file\n"
