# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from subprocess import (
    DEVNULL as DEVNULL,
    PIPE as PIPE,
    CalledProcessError as CalledProcessError,
    CompletedProcess as CompletedProcess,
    Popen as Popen,
    run as run,
)

from xtyping import (
    IO,
    TYPE_CHECKING,
    Any,
    FsPath,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypedDict,
    Union,
)

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
    "PopenArg",
    "PopenArgs",
    "PopenArgv",
    "PopenEnv",
    "runb",
    "runs",
    # from subprocess
    "CompletedProcess",
    "run",
    "Popen",
    "PIPE",
    "DEVNULL",
)

if TYPE_CHECKING:
    PathLikeStr = os.PathLike[str]
    PathLikeBytes = os.PathLike[bytes]
    PathLikeStrBytes = Union[PathLikeStr, PathLikeBytes]
else:
    PathLikeStr = os.PathLike
    PathLikeBytes = os.PathLike
    PathLikeStrBytes = os.PathLike


PopenArg = Union[str, bytes, PathLikeStrBytes]
PopenArgv = Sequence[PopenArg]
PopenArgs = Union[bytes, str, PopenArgv]
PopenEnv = Mapping[str, str]


class CompletedProcessObj(TypedDict):
    args: list[str]
    stdout: str
    stderr: str
    returncode: int


def completed_process_obj(
    completed_process: CompletedProcess[str],
) -> CompletedProcessObj:
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
    if not isinstance(completed_process, CompletedProcess):
        raise TypeError(
            f"completed_process must be CompletedProcess object, not {type(completed_process)}"
        )
    return CompletedProcessObj(
        args=completed_process.args,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        returncode=completed_process.returncode,
    )


def pcheck(
    process: CompletedProcess[Any],
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
) -> None:
    """

    Args:
        process: CompletedProcess object
        ok_code: OK code or sequence of codes, default is 0

    Returns:
        None

    Raises:
        CompletedProcessError: if process.returncode not in ok_code

    """
    if isinstance(ok_code, int):
        if process.returncode != ok_code:
            raise CalledProcessError(
                process.returncode,
                process.args,
                output=process.stdout,
                stderr=process.stderr,
            )
    else:
        if process.returncode not in ok_code:
            raise CalledProcessError(
                process.returncode,
                process.args,
                output=process.stdout,
                stderr=process.stderr,
            )


def runb(
    args: PopenArgs,
    *,
    executable: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    input: Optional[str] = None,
    stdout: Optional[Union[IO[Any], int]] = None,
    stderr: Optional[Union[IO[Any], int]] = None,
    shell: bool = False,
    cwd: Optional[FsPath] = None,
    timeout: Optional[float] = None,
    capture_output: bool = False,
    check: bool = False,
    env: Optional[Mapping[str, str]] = None,
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
    **other_popen_kwargs: Any,
) -> CompletedProcess[bytes]:
    process = run(
        args=args,
        input=input,
        executable=executable,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
        cwd=cwd,
        timeout=timeout,
        env=env,
        capture_output=capture_output,
        **other_popen_kwargs,
    )
    if check:
        pcheck(process=process, ok_code=ok_code)
    return process


def runs(
    args: PopenArgs,
    *,
    executable: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    input: Optional[str] = None,
    stdout: Optional[Union[IO[Any], int]] = None,
    stderr: Optional[Union[IO[Any], int]] = None,
    shell: bool = False,
    cwd: Optional[FsPath] = None,
    timeout: Optional[float] = None,
    capture_output: bool = False,
    check: bool = False,
    env: Optional[Mapping[str, str]] = None,
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
    **other_popen_kwargs: Any,
) -> CompletedProcess[str]:
    """Run command with txt output"""
    process = run(
        args=args,
        input=input,
        executable=executable,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
        cwd=cwd,
        timeout=timeout,
        env=env,
        capture_output=capture_output,
        universal_newlines=True,
        **other_popen_kwargs,
    )
    if check:
        pcheck(process=process, ok_code=ok_code)
    return process
