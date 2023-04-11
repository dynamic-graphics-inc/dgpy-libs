# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import sys

from functools import reduce
from io import BytesIO
from operator import iconcat
from os import getcwd, path
from subprocess import (
    DEVNULL as DEVNULL,
    CalledProcessError as CalledProcessError,
    CompletedProcess as CompletedProcess,
)
from time import time
from typing import Callable, Optional

from shellfish.sp import PopenArgs
from xtyping import IO, Any, FsPath, List, Mapping, Set, Tuple, Union

__all__ = ("run_async",)


def utf8_string(val: Union[str, bytes, bytearray]) -> str:
    if not isinstance(val, str):
        return val.decode("utf-8")
    return val


def _flatten_args(*args: Union[Any, List[Any]]) -> List[str]:
    """Flatten possibly nested iterables of sequences to a list of strings

    Examples:
        >>> list(_flatten_args("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(_flatten_args("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(
        map(
            utf8_string,
            reduce(
                iconcat,
                [
                    _flatten_args(*arg) if isinstance(arg, (list, tuple)) else (arg,)
                    for arg in args
                ],
                [],
            ),
        )
    )


def _args2cmd(args: PopenArgs) -> Union[str, bytes]:
    """Return single command string from given popenargs"""
    if isinstance(args, (str, bytes)):
        return args
    return " ".join(map(str, args))


async def _read_stream(
    stream: asyncio.StreamReader, callback: Callable[[bytes], None]
) -> None:
    while True:
        line = await stream.readline()
        if line:
            callback(line)
        else:
            break


async def run_async_dt(
    *popenargs: PopenArgs,
    executable: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    text: bool = False,
    input: Optional[str] = None,
    stdout: Optional[Union[IO[Any], int]] = None,
    stderr: Optional[Union[IO[Any], int]] = None,
    shell: bool = False,
    cwd: Optional[FsPath] = None,
    timeout: Optional[float] = None,
    capture_output: bool = False,
    check: bool = False,
    env: Optional[Mapping[str, str]] = None,
    tee: bool = False,
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
    **other_popen_kwargs: Any,
) -> Tuple[CompletedProcess[bytes], float, float]:
    _args = list(_flatten_args(popenargs))

    _stdin = DEVNULL if input is None else asyncio.subprocess.PIPE
    _input = input if not isinstance(input, str) else input.encode()

    _cwd = getcwd()
    if cwd and path.exists(cwd) and path.isdir(cwd):
        _cwd = str(cwd)
    if shell:
        _cmd = _args2cmd(_args)
        ti = time()
        _proc = await asyncio.create_subprocess_shell(
            cmd=_cmd,
            stdin=_stdin,
            stdout=asyncio.subprocess.PIPE if capture_output else stdout,
            stderr=asyncio.subprocess.PIPE if capture_output else stderr,
            env=env,
            shell=True,
            limit=2**23,
            cwd=_cwd,
        )
    else:
        ti = time()
        _proc = await asyncio.create_subprocess_exec(
            *_args,
            stdin=_stdin,
            stdout=asyncio.subprocess.PIPE if capture_output else stdout,
            stderr=asyncio.subprocess.PIPE if capture_output else stderr,
            env=env,
            limit=2**23,
            cwd=_cwd,
        )

    _out_buf = BytesIO()
    _err_buf = BytesIO()

    def _tee_bytes(line: bytes, sink: BytesIO, pipe: IO[bytes]) -> None:
        sink.write(line)
        pipe.write(line)

    def _tee_string(line: bytes, sink: BytesIO, pipe: IO[str]) -> None:
        sink.write(line)
        pipe.write(line.decode())

    if tee:
        if _input is not None and _proc.stdin is not None:
            _proc.stdin.write(_input)
            _proc.stdin.close()
        _bg = []
        if _proc.stdout is not None:
            _bg.append(
                _read_stream(
                    _proc.stdout, lambda line: _tee_string(line, _out_buf, sys.stdout)
                )
            )
        if _proc.stderr is not None:
            _bg.append(
                _read_stream(
                    _proc.stderr, lambda line: _tee_string(line, _err_buf, sys.stderr)
                )
            )
        if _bg:
            await asyncio.gather(
                *_bg,
            )
    if timeout:
        try:
            if _input:
                (_stdout, _stderr) = await asyncio.wait_for(
                    _proc.communicate(input=_input),  # wait for subprocess to finish
                    timeout=timeout,
                )
            else:
                (_stdout, _stderr) = await asyncio.wait_for(
                    _proc.communicate(),  # wait for subprocess to finish
                    timeout=timeout,
                )

            tf = time()
        except TimeoutError as te:
            _proc.terminate()
            raise TimeoutError(
                str(
                    {
                        "args": _args,
                        "input": input,
                        "env": env,
                        "cwd": cwd,
                        "shell": shell,
                        "asyncio.TimeoutError": str(te),
                    }
                )
            )
    else:
        (_stdout, _stderr) = await _proc.communicate(input=_input)  # wait fo
        tf = time()

    if tee:
        _stdout = _out_buf.getvalue()
        _stderr = _err_buf.getvalue()
    if check or ok_code != 0:
        _ok_codes = {ok_code} if isinstance(ok_code, int) else set(ok_code)
        if _proc.returncode and _proc.returncode not in _ok_codes:
            raise CalledProcessError(
                returncode=_proc.returncode,
                output=_stdout,
                stderr=_stderr,
                cmd=str(_args),
            )
    return (
        CompletedProcess(
            args=_args,
            returncode=_proc.returncode or 0,
            stdout=_stdout or b"",
            stderr=_stderr or b"",
        ),
        ti,
        tf,
    )


async def run_async(
    *popenargs: PopenArgs,
    executable: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    text: bool = False,
    input: Optional[str] = None,
    stdout: Optional[Union[IO[Any], int]] = None,
    stderr: Optional[Union[IO[Any], int]] = None,
    shell: bool = False,
    cwd: Optional[FsPath] = None,
    timeout: Optional[float] = None,
    capture_output: bool = True,
    check: bool = False,
    env: Optional[Mapping[str, str]] = None,
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = 0,
    tee: bool = False,
    **other_popen_kwargs: Any,
) -> CompletedProcess[bytes]:
    completed_process, _ti, _tf = await run_async_dt(
        *popenargs,
        executable=executable,
        stdin=stdin,
        text=text,
        input=input,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
        cwd=cwd,
        timeout=timeout,
        capture_output=capture_output,
        check=check,
        env=env,
        ok_code=ok_code,
        tee=tee,
        **other_popen_kwargs,
    )
    return completed_process
