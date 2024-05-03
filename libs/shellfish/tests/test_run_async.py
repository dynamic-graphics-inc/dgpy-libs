from __future__ import annotations

from os import chdir
from subprocess import CompletedProcess
from typing import TYPE_CHECKING

import pytest

from shellfish.dev.run_async import run_async

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.asyncio
async def test_subprocess_run_async() -> None:
    proc = await run_async(["echo", "hello"])
    assert isinstance(proc, CompletedProcess)
    assert proc.stdout.strip(b"\n") == b"hello"


@pytest.mark.asyncio
async def test_subprocess_run_async_shell() -> None:
    proc = await run_async(["echo", "hello"], shell=True)
    assert isinstance(proc, CompletedProcess)
    assert proc.stdout.replace(b"\r\n", b"\n").strip(b"\n") == b"hello"


python_script_string = r"""
import sys
from time import sleep

# read all of stdin
stdin_data = sys.stdin.read()
print(f"stdin: {stdin_data}")

for i in range(10):
    sys.stdout.write(f"{i} stdout\n")
    sys.stderr.write(f"{i} stderr\n")
    sleep(0.1)
"""


@pytest.mark.asyncio
async def test_subprocess_run_async_tee(
    capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    chdir(tmp_path)
    with open("file.py", "w") as f:
        f.write(python_script_string)

    proc = await run_async(
        ["python", "file.py"],
        capture_output=True,
        input="this is stdin\n",
        shell=False,
        tee=True,
    )
    proc = await run_async(
        ["python", "file.py"], capture_output=True, shell=True, tee=True
    )
    assert isinstance(proc, CompletedProcess)
    captured = capsys.readouterr()
    assert "this is stdin" in captured.out
    assert "stdout" in captured.out
    assert "stderr" in captured.err


async def main() -> None:
    await test_subprocess_run_async_tee()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
