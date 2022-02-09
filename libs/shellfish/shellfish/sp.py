# -*- coding: utf-8 -*-
from __future__ import annotations

from subprocess import (
    DEVNULL as DEVNULL,
    PIPE as PIPE,
    CompletedProcess as CompletedProcess,
    Popen as Popen,
    run as run,
)

from xtyping import TypedDict

__subprocess_all__ = (
    "CompletedProcess",
    "run",
    "Popen",
    "PIPE",
    "DEVNULL",
)
__all__ = (
    "CompletedProcessObj",
    "completed_process_obj",
    # from subprocess
    "CompletedProcess",
    "run",
    "Popen",
    "PIPE",
    "DEVNULL",
)


class CompletedProcessObj(TypedDict):
    args: list[str]
    stdout: str
    stderr: str
    returncode: int


def completed_process_obj(completed_process: CompletedProcess) -> CompletedProcessObj:
    """Convert CompletedProcess to CompletedProcessObj (typed dict)

    Args:
        completed_process: CompletedProcess object

    Returns:
        CompletedProcessObj typed dict

    Examples:
        >>> from subprocess import CompletedProcess
        >>> from shellfish.sp import completed_process_obj
        >>> cp = CompletedProcess(
        ...     args=['some', 'args'],
        ...     stdout="stdout string",
        ...     stderr="stderr string",
        ...     returncode=0
        ... )
        >>> from pprint import pprint
        >>> cp_typed_dict = completed_process_obj(completed_process=cp)
        >>> pprint(cp_typed_dict)
        {'args': ['some', 'args'],
         'returncode': 0,
         'stderr': 'stderr string',
         'stdout': 'stdout string'}

    """
    return CompletedProcessObj(
        args=completed_process.args,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        returncode=completed_process.returncode,
    )
