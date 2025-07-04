# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio

from os import path
from typing import TYPE_CHECKING

import pytest

from shellfish import fs, sh

if TYPE_CHECKING:
    from pathlib import Path

PWD = path.split(path.realpath(__file__))[0]


@pytest.mark.asyncio()
async def test_subproc_async() -> None:
    prun = await sh.do_async("ls")
    assert isinstance(prun, sh.Done)
    assert prun.async_proc


@pytest.mark.asyncio()
async def test_subproc_asyncify() -> None:
    prun = await sh.do_asyncify("python", "--version", shell=True)
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
    fs.write_str(script_1sec_filepath, script_1sec)
    fs.write_str(script_2sec_filepath, script_2sec)
    proc = await sh.do_async(args=["python", script_1sec_filepath], timeout=2)
    assert proc.stdout == "About to sleep for 1 sec\nslept for 1 sec\n"
    with pytest.raises(sh.TimeoutExpired):
        proc = await sh.do_async(args=["python", script_2sec_filepath], timeout=0.2)


async def _test_timeout_subprocess_aio_inner(tmp_path: Path) -> None:
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
    fs.write_str(script_1sec_filepath, script_1sec)
    fs.write_str(script_2sec_filepath, script_2sec)
    proc = await sh.do_async(args=["python", script_1sec_filepath], timeout=2)
    assert proc.stdout == "About to sleep for 1 sec\nslept for 1 sec\n"

    with pytest.raises(sh.TimeoutExpired):
        proc = await sh.do_async(args=["python", script_2sec_filepath], timeout=0.2)


@pytest.mark.timeout()
def test_timeout_subprocess_aio_sync(tmp_path: Path) -> None:
    asyncio.run(_test_timeout_subprocess_aio_inner(tmp_path))


async def _test_timeout_subprocess_aio_inner_shell_true(tmp_path: Path) -> None:
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
    fs.write_str(script_1sec_filepath, script_1sec)
    fs.write_str(script_2sec_filepath, script_2sec)
    proc = await sh.do_async(
        args=["python", script_1sec_filepath], timeout=2, shell=True
    )
    assert proc.stdout == "About to sleep for 1 sec\nslept for 1 sec\n"
    with pytest.raises(sh.TimeoutExpired):
        proc = await sh.do_async(
            args=["python", script_2sec_filepath], timeout=0.2, shell=True
        )


@pytest.mark.timeout()
def test_timeout_subprocess_aio_sync_shell_true(tmp_path: Path) -> None:
    asyncio.run(_test_timeout_subprocess_aio_inner_shell_true(tmp_path))
