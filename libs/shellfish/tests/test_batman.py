# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from os import path
from subprocess import CompletedProcess
from typing import Any

import pytest

from shellfish import batman, sh

_PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.skipif(sys.platform != "win32", reason="only runs on windows")
class TestBatman:
    windows_scripts_dirpath = path.join(_PWD, "_windows_test_data")

    def test_cmd_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = batman.bat("cmd_command")
        assert proc.stdout == "Hello\nCMD file\n"

    def test_bat_command(self) -> None:
        sh.cd(self.windows_scripts_dirpath)
        proc = batman.bat("bat_command")
        assert proc.stdout == "Hello\nBAT file\n"

    def test_bat_uses_cmd_call_for_shell_false(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls: dict[str, Any] = {}

        def fake_run(**kwargs: Any) -> CompletedProcess[str]:
            calls.update(kwargs)
            return CompletedProcess(kwargs["args"], 0, stdout="", stderr="")

        monkeypatch.setattr(batman, "which", lambda _fspath: "script.bat")
        monkeypatch.setattr(batman, "run", fake_run)

        proc = batman.bat("script")

        assert proc.returncode == 0
        assert calls["args"] == ["cmd.exe", "/d", "/c", "call", "script.bat"]
        assert calls["shell"] is False
