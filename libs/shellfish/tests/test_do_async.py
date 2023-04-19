# -*- coding: utf-8 -*-
import asyncio
import sys

from os import path
from pathlib import Path
from subprocess import TimeoutExpired

import pytest

from shellfish import fs, process, sh

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.asyncio()
async def test_subproc_async() -> None:
    prun = await sh.do_async("ls")
    assert isinstance(prun, sh.Done)
    assert prun.async_proc


@pytest.mark.asyncio()
async def test_subproc_asyncify() -> None:
    prun = await sh.do_asyncify("pyton", "--version", shell=True)
    assert isinstance(prun, sh.Done)
    assert prun.async_proc


@pytest.mark.asyncio()
@pytest.mark.aio()
async def test_run_async_shell_false() -> None:
    res = await sh.do_async(["ls"], shell=False)
    assert res.async_proc


@pytest.mark.asyncio()
@pytest.mark.aio()
async def test_run_async_shell_true() -> None:
    res = await sh.do_async(["ls"], shell=True)
    assert res.async_proc


@pytest.mark.asyncio()
@pytest.mark.timeout()
async def test_timeout_subprocess_aio(tmp_path: Path) -> None:
    sh.cd(str(tmp_path))
    script_1sec = (
        "from time import sleep\n"
        "print('About to sleep for 1 sec')\n"
        "sleep(1)\n"
        "print('slept for 1 sec')"
    )

    script_2sec = (
        "from time import sleep\n"
        "print('About to sleep for 3 sec')\n"
        "sleep(2)\n"
        "print('slept for 3 sec')"
    )
    script_1sec_filepath = "script_1sec.py"
    script_2sec_filepath = "script_2sec.py"
    fs.sstring(script_1sec_filepath, script_1sec)
    fs.sstring(script_2sec_filepath, script_2sec)
    proc = await sh.do_async(args=["python", script_1sec_filepath], timeout=2)
    assert proc.stdout == "About to sleep for 1 sec\nslept for 1 sec\n"

    if process.is_win() and sys.version_info < (3, 8):
        with pytest.raises(TimeoutExpired):
            proc = await sh.do_async(args=["python", script_2sec_filepath], timeout=2)
    else:
        with pytest.raises(asyncio.TimeoutError):
            proc = await sh.do_async(args=["python", script_2sec_filepath], timeout=2)
