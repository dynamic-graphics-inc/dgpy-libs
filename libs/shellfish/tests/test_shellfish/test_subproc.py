# -*- coding: utf-8 -*-
# =============================================================================
#  (c) Copyright 2022, Dynamic Graphics, Inc.
#  ALL RIGHTS RESERVED
#  Permission to use, copy, modify, or distribute this software for any
#  purpose is prohibited without specific, written prior permission from
#  Dynamic Graphics, Inc.
# =============================================================================
import asyncio
import sys

from os import path
from pathlib import Path
from subprocess import TimeoutExpired

import pytest

from shellfish import fs, process, sh

PWD = path.split(path.realpath(__file__))[0]


def test_subproc() -> None:
    prun = sh.do("ls")
    assert isinstance(prun, sh.Done)


@pytest.mark.asyncio
async def test_subproc_async() -> None:
    prun = await sh.do_async("ls")
    assert isinstance(prun, sh.Done)
    assert prun.async_proc


def test_pipe_in_command(tmp_path: Path) -> None:
    grep_location = sh.which("grep")
    if grep_location is not None:
        sh.cd(tmp_path)
        fizzbuzz = 'for i in range(1, 101): print("Fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0) or str(i))'
        _fizzbuzz = fizzbuzz if process.is_win() else sh.quote(fizzbuzz)
        proc = sh.do(
            [
                "python",
                "-c",
                _fizzbuzz,
                "|",
                "grep",
                "Fizz",
                "|",
                "grep",
                "-v",
                "Buzz",
            ],
            shell=True,
        )
        lines = proc.stdout.strip("\n").split("\n")
        assert all(line == "Fizz" for line in lines)
        assert len(lines) == 27


def test_pipe_in_command_shell_is_false(tmp_path: Path) -> None:
    fizzbuzz = 'for i in range(1, 101): print("Fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0) or str(i))'
    args = ["python", "-c", fizzbuzz, "|", "grep", "Fizz", "|", "grep", "-v", "Buzz"]
    with pytest.raises(ValueError):
        sh.do(args, shell=False)


def test_pipe_stdout(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    proc = sh.do(["echo", "hello"])
    proc > "stdout.txt"
    stdout = fs.lstring("stdout.txt")
    assert stdout == proc.stdout

    proc >> "stdout.txt"
    stdout = fs.lstring("stdout.txt")
    assert stdout == proc.stdout * 2


def test_pipe_stderr(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    proc = sh.do(["echo", "hello"])
    proc.stderr = "STDERR IS THIS"
    proc >= "stderr.txt"
    stderr = fs.lstring("stderr.txt")
    assert stderr == proc.stderr

    proc >>= "stderr.txt"
    stdout = fs.lstring("stderr.txt")
    assert stdout == proc.stderr * 2


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


@pytest.mark.timeout
def test_timeout_subprocess(tmp_path: Path) -> None:
    sh.cd(str(tmp_path))
    script_2sec = (
        "from time import sleep\n"
        "print('About to sleep for 2 sec')\n"
        "sleep(2)\n"
        "print('slept for 2 seconds')"
    )
    script_4sec = (
        "from time import sleep\n"
        "print('About to sleep for 4 sec')\n"
        "sleep(4)\n"
        "print('slept for 4 seconds')"
    )
    script_2sec_filepath = "script_2sec.py"
    script_4sec_filepath = "script_4sec.py"
    fs.sstring(script_2sec_filepath, script_2sec)
    fs.sstring(script_4sec_filepath, script_4sec)
    proc = sh.do(args=["python", script_2sec_filepath], timeout=3)
    assert proc.stdout == "About to sleep for 2 sec\nslept for 2 seconds\n"
    with pytest.raises(TimeoutExpired):
        sh.do(args=["python", script_4sec_filepath], timeout=3)


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
