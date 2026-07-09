# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from os import path

import pytest

from shellfish import sh

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.skipif(sys.platform != "win32", reason="only runs on windows")
class TestWindowsSubprocessValidatePopenArgs:
    def test_validate_popen_args_platform_rewrites_batch_file(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            sh, "which_lru", lambda *_args, **_kwargs: r"C:\bin\script.bat"
        )

        args = sh._validate_popen_args_platform(["script", "one", "two"])

        assert args == [
            "cmd.exe",
            "/d",
            "/c",
            "call",
            r"C:\bin\script.bat",
            "one",
            "two",
        ]

    def test_validate_popen_args_platform_rewrites_cmd_file(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            sh, "which_lru", lambda *_args, **_kwargs: r"C:\bin\script.cmd"
        )

        args = sh._validate_popen_args_platform(["script"])

        assert args == ["cmd.exe", "/d", "/c", "call", r"C:\bin\script.cmd"]

    def test_validate_popen_args_platform_resolves_non_batch_exe(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            sh, "which_lru", lambda *_args, **_kwargs: r"C:\bin\python.exe"
        )

        args = sh._validate_popen_args_platform(["python", "-V"])

        assert args == [r"C:\bin\python.exe", "-V"]


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
