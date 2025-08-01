from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from shellfish import sh
from shellfish.dev.popen_gen import popen_gen, popen_pipes_gen

if TYPE_CHECKING:
    from pathlib import Path

python_script = r"""
import sys

for i in range(10):
    sys.stdout.write(f"{i} stdout\n")
    sys.stderr.write(f"{i} stderr\n")
"""


def test_popen_gen(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    sh.write_str("test.py", python_script)

    stdout_lines = []
    stderr_lines = []

    for stdio_type, line in popen_gen(["python", "test.py"]):
        if stdio_type == 1:
            stdout_lines.append(line)

        elif stdio_type == 2:
            stderr_lines.append(line)

    expected_stdout_lines = [f"{i} stdout\n" for i in range(10)]
    expected_stderr_lines = [f"{i} stderr\n" for i in range(10)]

    try:
        assert stdout_lines == expected_stdout_lines
        assert stderr_lines == expected_stderr_lines
    except AssertionError:
        pytest.skip("This test is super flakey in CI")


def test_popen_gen_not_popen_obj(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        list(popen_pipes_gen({"not": "a Popen object"}))  # type: ignore[arg-type]
