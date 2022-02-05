# -*- coding: utf-8 -*-
import asyncio
import sys

from os import path
from pathlib import Path
from subprocess import TimeoutExpired

import pytest

from shellfish import fs, process, sh

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.asyncio
async def test_subproc_async() -> None:
    prun = await sh.do_async("ls")
    assert isinstance(prun, sh.Done)
    assert prun.async_proc



@pytest.mark.asyncio
@pytest.mark.aio
async def test_run_async_shell_false() -> None:
    res = await sh.do_async(["ls"], shell=False)
    assert res.async_proc


@pytest.mark.asyncio
@pytest.mark.aio
async def test_run_async_shell_true() -> None:
    res = await sh.do_async(["ls"], shell=True)
    assert res.async_proc


@pytest.mark.asyncio
@pytest.mark.timeout
async def test_timeout_subprocess_async(tmp_path: Path) -> None:
    sh.cd(str(tmp_path))
    script_2sec = (
        "from time import sleep\n"
        "print('About to sleep for 1 sec')\n"
        "sleep(1)\n"
        "print('slept for 1 sec')"
    )
    script_3sec = (
        "from time import sleep\n"
        "print('About to sleep for 3 sec')\n"
        "sleep(3)\n"
        "print('slept for 3 sec')"
    )
    script_1sec_filepath = "script_1sec.py"
    script_3sec_filepath = "script_3sec.py"
    fs.sstring(script_1sec_filepath, script_2sec)
    fs.sstring(script_3sec_filepath, script_3sec)
    proc = await sh.do_async(args=["python", script_1sec_filepath], timeout=2)
    assert proc.stdout == "About to sleep for 1 sec\nslept for 1 sec\n"

    if process.is_win() and sys.version_info < (3, 8):
        with pytest.raises(TimeoutExpired):
            proc = await sh.do_async(args=["python", script_3sec_filepath], timeout=2)
    else:
        with pytest.raises(asyncio.TimeoutError):
            proc = await sh.do_async(args=["python", script_3sec_filepath], timeout=2)
