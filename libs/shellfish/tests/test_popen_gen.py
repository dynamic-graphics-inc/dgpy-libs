from pathlib import Path

import pytest

from shellfish import sh
from shellfish.dev.popen_gen import popen_gen, popen_pipes_gen

python_script = r"""
import sys

for i in range(10):
    sys.stdout.write(f"{i} stdout\n")
    sys.stderr.write(f"{i} stderr\n")
"""


def test_popen_gen(tmp_path: Path) -> None:
    sh.cd(tmp_path)
    sh.wstring("test.py", python_script)

    stdout_lines = []
    stderr_lines = []

    for stdio_type, line in popen_gen(["python", "test.py"]):
        if stdio_type == 1:
            stdout_lines.append(line)

        elif stdio_type == 2:
            stderr_lines.append(line)

    expected_stdout_lines = [f"{i} stdout\n" for i in range(10)]
    expected_stderr_lines = [f"{i} stderr\n" for i in range(10)]

    assert stdout_lines == expected_stdout_lines
    assert stderr_lines == expected_stderr_lines


def test_popen_gen_not_popen_obj(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        list(popen_pipes_gen({"not": "a Popen object"}))  # type: ignore[arg-type]
