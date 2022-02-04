# -*- coding: utf-8 -*-
from __future__ import annotations

from subprocess import CompletedProcess as CompletedProcess

from xtyping import TypedDict

__all__ = (
    "CompletedProcessObj",
    "completed_process_obj",
)


class CompletedProcessObj(TypedDict):
    args: list[str]
    stdout: str
    stderr: str
    returncode: int


def completed_process_obj(completed_process: CompletedProcess) -> CompletedProcessObj:
    return CompletedProcessObj(
        args=completed_process.args,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        returncode=completed_process.returncode,
    )
