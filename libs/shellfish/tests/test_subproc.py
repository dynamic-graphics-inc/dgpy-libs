# -*- coding: utf-8 -*-

from __future__ import annotations

from os import path
from subprocess import TimeoutExpired
from typing import TYPE_CHECKING

import pytest

from shellfish import fs, process, sh

if TYPE_CHECKING:
    from pathlib import Path

PWD = path.split(path.realpath(__file__))[0]


def test_subproc() -> None:
    prun = sh.do("ls")
    assert isinstance(prun, sh.Done)


@pytest.mark.asyncio()
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
    proc > "stdout.txt"  # noqa: B015
    stdout = fs.read_str("stdout.txt")
    assert stdout == proc.stdout

    proc >> "stdout.txt"
    stdout = fs.read_str("stdout.txt")
    assert stdout == proc.stdout * 2


def test_pipe_stderr(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    proc = sh.do(["echo", "hello"])
    proc.stderr = "STDERR IS THIS"
    proc >= "stderr.txt"  # noqa: B015
    stderr = fs.read_str("stderr.txt")
    assert stderr == proc.stderr

    proc >>= "stderr.txt"
    stdout = fs.read_str("stderr.txt")
    assert stdout == proc.stderr * 2


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


@pytest.mark.timeout()
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
    fs.write_str(script_2sec_filepath, script_2sec)
    fs.write_str(script_4sec_filepath, script_4sec)
    proc = sh.do(args=["python", script_2sec_filepath], timeout=3)
    assert proc.stdout == "About to sleep for 2 sec\nslept for 2 seconds\n"
    with pytest.raises(TimeoutExpired):
        sh.do(args=["python", script_4sec_filepath], timeout=3)
