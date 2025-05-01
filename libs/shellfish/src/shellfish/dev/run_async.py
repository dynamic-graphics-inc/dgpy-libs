# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import sys

from io import BytesIO
from os import getcwd, path
from subprocess import (
    DEVNULL as DEVNULL,
    CalledProcessError as CalledProcessError,
    CompletedProcess as CompletedProcess,
    TimeoutExpired,
)
from time import time
from typing import TYPE_CHECKING, Callable, Optional

from shellfish.libsh.args import args2cmd as _args2cmd, flatten_args as _flatten_args
from shellfish.sp import PopenArgs, ProcessDt

if TYPE_CHECKING:
    from xtyping import IO, Any, FsPath, List, Mapping, Set, Tuple, Union

__all__ = ("run_async",)


def utf8_string(val: Union[str, bytes, bytearray]) -> str:
    if not isinstance(val, str):
        return val.decode("utf-8")
    return val


async def _read_stream(
    stream: asyncio.StreamReader, callback: Callable[[bytes], None]
) -> None:
    while True:
        line = await stream.readline()
        if line:
            callback(line)
        else:
            break


async def run_dtee_async(
    *popenargs: PopenArgs,
    executable: Optional[str] = None,
    stdin: Optional[Union[IO[Any], int]] = None,
    text: bool = False,
    input: Optional[Union[str, bytes]] = None,
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
    universal_newlines: bool = False,
    **other_popen_kwargs: Any,
) -> Tuple[CompletedProcess[bytes], ProcessDt]:
    _args = list(_flatten_args(*popenargs))

    _stdin = DEVNULL if input is None else asyncio.subprocess.PIPE
    _input_bytes = input if not isinstance(input, str) else input.encode()

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
    _stdout = b""
    _stderr = b""

    def _tee_bytes(line: bytes, sink: BytesIO, pipe: IO[bytes]) -> None:
        sink.write(line)
        pipe.write(line)

    def _tee_string(line: bytes, sink: BytesIO, pipe: IO[str]) -> None:
        sink.write(line)
        pipe.write(line.decode())

    _bg = []
    if tee:
        if _input_bytes is not None and _proc.stdin is not None:
            _proc.stdin.write(_input_bytes)
            _proc.stdin.close()
        if _proc.stdout is not None:
            _bg.append(
                asyncio.create_task(
                    _read_stream(
                        _proc.stdout,
                        lambda line: _tee_string(line, _out_buf, sys.stdout),
                    )
                )
            )
        if _proc.stderr is not None:
            _bg.append(
                asyncio.create_task(
                    _read_stream(
                        _proc.stderr,
                        lambda line: _tee_string(line, _err_buf, sys.stderr),
                    )
                )
            )

        if timeout:
            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        *_bg,
                    ),
                    timeout=timeout,
                )
                tf = time()
            except ValueError as ve:
                for task in _bg:
                    task.cancel()
                _proc.terminate()
                raise TimeoutExpired(
                    cmd=_args,
                    timeout=timeout,
                    output=_out_buf.getvalue(),
                    stderr=_err_buf.getvalue(),
                ) from ve
            except TimeoutError as te:
                for task in _bg:
                    task.cancel()
                raise TimeoutExpired(
                    cmd=_args,
                    timeout=timeout,
                    output=_out_buf.getvalue(),
                    stderr=_err_buf.getvalue(),
                ) from te
            finally:
                await _proc.wait()
        else:
            await asyncio.gather(
                *_bg,
            )
            tf = time()
    else:
        if timeout:
            try:
                if _input_bytes is not None and _proc.stdin is not None:
                    (_stdout, _stderr) = await asyncio.wait_for(
                        _proc.communicate(
                            input=_input_bytes
                        ),  # wait for subprocess to finish
                        timeout=timeout,
                    )
                else:
                    (_stdout, _stderr) = await asyncio.wait_for(
                        _proc.communicate(),  # wait for subprocess to finish
                        timeout=timeout,
                    )
                tf = time()
            except (TimeoutError, asyncio.TimeoutError) as te:
                _proc.terminate()
                raise TimeoutExpired(
                    cmd=_args,
                    timeout=timeout,
                    output=_out_buf.getvalue(),
                    stderr=_err_buf.getvalue(),
                ) from te
            finally:
                await _proc.wait()
        else:
            (_stdout, _stderr) = await _proc.communicate(input=_input_bytes)
            tf = time()
    if tee:
        _stdout = _out_buf.getvalue()
        _stderr = _err_buf.getvalue()
    if universal_newlines:
        _stdout = _stdout.replace(b"\r\n", b"\n")
        _stderr = _stderr.replace(b"\r\n", b"\n")
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
        ProcessDt(
            ti=ti,
            tf=tf,
            dt=tf - ti,
        ),
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
    universal_newlines: bool = True,
    **other_popen_kwargs: Any,
) -> CompletedProcess[bytes]:
    completed_process, _pdt = await run_dtee_async(
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
