# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from dataclasses import dataclass
from io import StringIO
from subprocess import (
    DEVNULL as DEVNULL,
    PIPE as PIPE,
    CalledProcessError as CalledProcessError,
    CompletedProcess as CompletedProcess,
    Popen as Popen,
    TimeoutExpired as TimeoutExpired,
    run as run,
)
from time import time

from shellfish._types import PopenArgs as PopenArgs  # noqa: TC001
from shellfish.dev.popen_gen import popen_pipes_gen
from shellfish.libsh.args import args2cmd
from shellfish.process import is_win
from xtyping import (
    IO,
    STDIN,
    Any,
    Dict,
    FsPath,
    List,
    Mapping,
    Optional,
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
    "DEVNULL",
    "PIPE",
    # from subprocess
    "CompletedProcess",
    "CompletedProcessDict",
    "Popen",
    "completed_process_dict",
    "run",
    "runb",
    "runs",
)


@dataclass(frozen=True)
class ProcessDt:
    """Process time delta dataclass

    Examples:
        >>> from shellfish.sp import ProcessDt
        >>> ti = 0
        >>> tf = 1
        >>> dt = ProcessDt.from_titf(ti=ti, tf=tf)
        >>> dt
        ProcessDt(ti=0, tf=1, dt=1)

    """

    ti: float
    tf: float
    dt: float
    __slots__ = ("ti", "tf", "dt")

    @classmethod
    def from_titf(cls, ti: float, tf: float) -> ProcessDt:
        return cls(ti=ti, tf=tf, dt=tf - ti)


class CompletedProcessDict(TypedDict):
    args: List[str]
    stdout: str
    stderr: str
    returncode: int


def completed_process_dict(
    completed_process: CompletedProcess[str],
) -> CompletedProcessDict:
    """Convert CompletedProcess to CompletedProcessObj (typed dict)

    Args:
        completed_process: CompletedProcess object

    Returns:
        CompletedProcessObj typed dict

    Examples:
        >>> from subprocess import CompletedProcess
        >>> from shellfish.sp import completed_process_dict
        >>> cp = CompletedProcess(
        ...     args=['some', 'args'],
        ...     stdout="stdout string",
        ...     stderr="stderr string",
        ...     returncode=0
        ... )
        >>> from pprint import pprint
        >>> cp_typed_dict = completed_process_dict(completed_process=cp)
        >>> pprint(cp_typed_dict)
        {'args': ['some', 'args'],
         'returncode': 0,
         'stderr': 'stderr string',
         'stdout': 'stdout string'}

    """
    if not isinstance(completed_process, CompletedProcess):  # pragma: nocov
        raise TypeError(
            f"completed_process must be CompletedProcess object, not {type(completed_process)}"
        )
    return CompletedProcessDict(
        args=completed_process.args,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
        returncode=completed_process.returncode,
    )


def pcheck(
    process: CompletedProcess[Any],
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
) -> None:
    """Check process return code

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
        text=True,
        **other_popen_kwargs,
    )
    if check:
        pcheck(process=process, ok_code=ok_code)
    return process


def run_dtee(
    args: PopenArgs,
    cwd: Optional[FsPath] = None,
    env: Optional[Dict[str, str]] = None,
    input: Optional[STDIN] = None,
    shell: bool = False,
    timeout: Optional[float] = None,
) -> Tuple[CompletedProcess[str], ProcessDt]:
    stdout_sio = StringIO()
    stderr_sio = StringIO()
    args_str = args2cmd(args)
    with Popen(
        args=args if is_win() or not shell else args_str,
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE if input else None,
        env=env,
        cwd=str(cwd) if cwd else None,
        shell=shell,
        text=True,
        universal_newlines=True,
    ) as proc:
        try:
            if input is not None and proc.stdin:
                proc.stdin.write(input if isinstance(input, str) else input.decode())
                proc.stdin.flush()
                proc.stdin.close()
            ti = time()
            for io_type, line in popen_pipes_gen(proc, timeout=timeout):
                if io_type == 1:  # stdout is 1
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    stdout_sio.write(line)
                elif io_type == 2:  # stderr is 2
                    sys.stderr.write(line)
                    sys.stderr.flush()
                    stderr_sio.write(line)
            tf = time()
            stdout_str = stdout_sio.getvalue()
            stderr_str = stderr_sio.getvalue()
        except TimeoutExpired as e:
            tf = time()
            proc.kill()
            raise e
        except KeyboardInterrupt as e:
            tf = time()
            proc.kill()
            raise e
        except Exception as e:
            tf = time()
            proc.kill()
            raise e

    return (
        CompletedProcess(
            args=args,
            returncode=proc.returncode,
            stdout=stdout_str,
            stderr=stderr_str,
        ),
        ProcessDt(
            ti=ti,
            tf=tf,
            dt=tf - ti,
        ),
    )


def run_tee(
    args: PopenArgs,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    input: Optional[STDIN] = None,
    shell: bool = False,
    timeout: Optional[float] = None,
) -> CompletedProcess[str]:
    completed_process, _pdt = run_dtee(
        args=args,
        input=input,
        cwd=cwd,
        env=env,
        timeout=timeout,
        shell=shell,
    )
    return completed_process
