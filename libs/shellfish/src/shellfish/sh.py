# -*- coding: utf-8 -*-
"""shell utils"""

from __future__ import annotations

import sys

from functools import cache, lru_cache
from os import (
    chdir,
    environ,
    fspath as _fspath,
    getcwd,
    listdir,
    makedirs,
    path as path,
)
from pathlib import Path
from platform import system
from shlex import quote as _quote, split as _shplit
from shutil import which as _which
from subprocess import PIPE, CompletedProcess, TimeoutExpired, run
from time import time
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AnyStr,
    Callable,
    Optional,
    Union,
)

from asyncify import asyncify
from listless import flatten_strings as _flatten_strings
from shellfish import fs, sp
from shellfish.__about__ import __version__
from shellfish.dev import run_async as __run_async
from shellfish.done import (
    Done as Done,
    DoneDict as DoneDict,
    DoneError as DoneError,
    DoneObj as DoneObj,
    HrTime as HrTime,
    HrTimeDict as HrTimeDict,
    HrTimeObj as HrTimeObj,
)
from shellfish.echo import echo as echo
from shellfish.fs import (
    SymlinkType as SymlinkType,
    chmod as chmod,
    copy_file as copy_file,
    cp as cp,
    dir_exists as dir_exists,
    dir_exists_async as dir_exists_async,
    dirpath_gen as dirpath_gen,
    dirs_gen as dirs_gen,
    exists as exists,
    exists_async as exists_async,
    extension as extension,
    file_exists as file_exists,
    file_exists_async as file_exists_async,
    file_lines_gen as file_lines_gen,
    filecmp as filecmp,
    filepath_gen as filepath_gen,
    filepath_mtimedelta_sec as filepath_mtimedelta_sec,
    files_dirs_gen as files_dirs_gen,
    files_gen as files_gen,
    filesize as filesize,
    filesize_async as filesize_async,
    fspath as fspath,
    glob as glob,
    is_dir as is_dir,
    is_dir_async as is_dir_async,
    is_file as is_file,
    is_file_async as is_file_async,
    is_link as is_link,
    is_link_async as is_link_async,
    isdir as isdir,
    isdir_async as isdir_async,
    isfile as isfile,
    isfile_async as isfile_async,
    islink as islink,
    islink_async as islink_async,
    lbin as lbin,
    lbytes as lbytes,
    lbytes_async as lbytes_async,
    lbytes_gen as lbytes_gen,
    lbytes_gen_async as lbytes_gen_async,
    listdir_async as listdir_async,
    listdir_gen as listdir_gen,
    ljson as ljson,
    ljson_async as ljson_async,
    lstat_async as lstat_async,
    lstr as lstr,
    lstr_async as lstr_async,
    lstring as lstring,
    lstring_async as lstring_async,
    mkdir as mkdir,
    mkdirp as mkdirp,
    move as move,
    path_gen as path_gen,
    rbin as rbin,
    rbin_async as rbin_async,
    rbin_gen as rbin_gen,
    rbin_gen_async as rbin_gen_async,
    rbytes as rbytes,
    rbytes_async as rbytes_async,
    rbytes_gen as rbytes_gen,
    rbytes_gen_async as rbytes_gen_async,
    read_bytes as read_bytes,
    read_bytes_async as read_bytes_async,
    read_bytes_gen as read_bytes_gen,
    read_bytes_gen_async as read_bytes_gen_async,
    read_json as read_json,
    read_json_async as read_json_async,
    read_str as read_str,
    read_str_async as read_str_async,
    rename as rename,
    rjson as rjson,
    rjson_async as rjson_async,
    rm_gen as rm_gen,
    rmdir as rmdir,
    rmfile as rmfile,
    rstr as rstr,
    rstr_async as rstr_async,
    rstring as rstring,
    rstring_async as rstring_async,
    safepath as safepath,
    sbin as sbin,
    sbin_async as sbin_async,
    sbytes as sbytes,
    sbytes_async as sbytes_async,
    sbytes_gen as sbytes_gen,
    sbytes_gen_async as sbytes_gen_async,
    scandir as scandir,
    scandir_gen as scandir_gen,
    scandir_gen_filter as scandir_gen_filter,
    scandir_list as scandir_list,
    sep_join as sep_join,
    sep_lstrip as sep_lstrip,
    sep_rstrip as sep_rstrip,
    sep_split as sep_split,
    sep_strip as sep_strip,
    shebang as shebang,
    sjson as sjson,
    sjson_async as sjson_async,
    sstr as sstr,
    sstr_async as sstr_async,
    sstring as sstring,
    sstring_async as sstring_async,
    stat as stat,
    stat_async as stat_async,
    symlink as symlink,
    touch as touch,
    walk_gen as walk_gen,
    wbin as wbin,
    wbin_async as wbin_async,
    wbin_gen as wbin_gen,
    wbin_gen_async as wbin_gen_async,
    wbytes as wbytes,
    wbytes_async as wbytes_async,
    wbytes_gen as wbytes_gen,
    wbytes_gen_async as wbytes_gen_async,
    wjson as wjson,
    wjson_async as wjson_async,
    write_bytes as write_bytes,
    write_bytes_async as write_bytes_async,
    write_bytes_gen as write_bytes_gen,
    write_bytes_gen_async as write_bytes_gen_async,
    write_json as write_json,
    write_json_async as write_json_async,
    write_str as write_str,
    write_str_async as write_str_async,
    wstr as wstr,
    wstr_async as wstr_async,
    wstring as wstring,
    wstring_async as wstring_async,
)
from shellfish.libsh._dirtree import _DirTree
from shellfish.osfs import LIN as _LIN, WIN as _WIN
from shellfish.process import is_win
from shellfish.stdio import Stdio as Stdio

if TYPE_CHECKING:
    from collections.abc import Iterable

    from shellfish._types import (
        STDIN as STDIN,
        FsPath as FsPath,
        PopenArg as PopenArg,
        PopenArgs as PopenArgs,
    )

__all__ = (
    "LIN",
    "WIN",
    "Done",
    "DoneDict",
    "DoneError",
    "DoneObj",
    "Flag",
    "FlagMeta",
    "HrTime",
    "HrTimeDict",
    "HrTimeObj",
    # fs exports
    "Stdio",
    "SymlinkType",
    "TimeoutExpired",
    "__version__",
    "basename",
    "cd",
    "chmod",
    "copy_file",
    "cp",
    "decode_stdio_bytes",
    "dir_exists",
    "dir_exists_async",
    "dirname",
    "dirpath_gen",
    "dirs_gen",
    "do",
    "do_",
    "do_async",
    "do_asyncify",
    "doa",
    "echo",
    "exists",
    "exists_async",
    "export",
    "extension",
    "file_exists",
    "file_exists_async",
    "file_lines_gen",
    "filecmp",
    "filepath_gen",
    "filepath_mtimedelta_sec",
    "files_dirs_gen",
    "files_gen",
    "filesize",
    "filesize_async",
    "flatten_args",
    "fspath",
    "glob",
    "is_dir",
    "is_dir_async",
    "is_file",
    "is_file_async",
    "is_link",
    "is_link_async",
    "isdir",
    "isdir_async",
    "isfile",
    "isfile_async",
    "islink",
    "islink_async",
    "lbin",
    "lbytes",
    "lbytes_async",
    "lbytes_gen",
    "lbytes_gen_async",
    "link_dir",
    "link_dirs",
    "link_file",
    "link_files",
    "listdir_async",
    "listdir_gen",
    "ljson",
    "ljson_async",
    "ls",
    "ls_async",
    "ls_dirs",
    "ls_files",
    "ls_files_dirs",
    "lstat_async",
    "lstr",
    "lstr_async",
    "lstring",
    "lstring_async",
    "mkdir",
    "mkdirp",
    "mkenv",
    "move",
    "mv",
    "path",
    "path_gen",
    "popen_has_pipe_character",
    "pstderr",
    "pstdout",
    "pstdout_pstderr",
    "pwd",
    "q",
    "quote",
    "rbin",
    "rbin_async",
    "rbin_gen",
    "rbin_gen_async",
    "rbytes",
    "rbytes_async",
    "rbytes_gen",
    "rbytes_gen_async",
    "read_bytes",
    "read_bytes_async",
    "read_bytes_gen",
    "read_bytes_gen_async",
    "read_json",
    "read_json_async",
    "read_str",
    "read_str_async",
    "rename",
    "rjson",
    "rjson_async",
    "rm",
    "rm_gen",
    "rmdir",
    "rmfile",
    "rstr",
    "rstr_async",
    "rstring",
    "rstring_async",
    "run",
    "run_async",
    "safepath",
    "sbin",
    "sbin_async",
    "sbytes",
    "sbytes_async",
    "sbytes_gen",
    "sbytes_gen_async",
    "scandir",
    "scandir_gen",
    "scandir_gen_filter",
    "scandir_list",
    "sep_join",
    "sep_lstrip",
    "sep_rstrip",
    "sep_split",
    "sep_strip",
    "setenv",
    "shebang",
    "shell",
    "shplit",
    "shx",
    "sjson",
    "sjson_async",
    "source",
    "sstr",
    "sstr_async",
    "sstring",
    "sstring_async",
    "stat",
    "stat_async",
    "symlink",
    "sync",
    "touch",
    "tree",
    "unlink_dir",
    "unlink_dirs",
    "unlink_file",
    "unlink_files",
    "utf8_string",
    "validate_popen_args",
    "validate_popen_args_windows",
    "validate_stdin",
    "walk_gen",
    "wbin",
    "wbin_async",
    "wbin_gen",
    "wbin_gen_async",
    "wbytes",
    "wbytes_async",
    "wbytes_gen",
    "wbytes_gen_async",
    "where",
    "which",
    "which_lru",
    "wjson",
    "wjson_async",
    "write_bytes",
    "write_bytes_async",
    "write_bytes_gen",
    "write_bytes_gen_async",
    "write_json",
    "write_json_async",
    "write_str",
    "write_str_async",
    "wstr",
    "wstr_async",
    "wstring",
    "wstring_async",
)

IS_WIN: bool = is_win()


class FlagMeta(type):
    """Meta class"""

    @staticmethod
    @cache
    def attr2flag(string: str) -> str:
        """Convert and return attr to string"""
        return string.replace("_", "-")

    def __getattr__(self, name: str) -> str:
        return self.attr2flag(string=name)


class Flag(metaclass=FlagMeta):
    """Flag obj

    Examples:
        >>> Flag.__help
        '--help'
        >>> Flag._v
        '-v'

    """


def mkenv(env: dict[str, str], extenv: bool = True) -> dict[str, str]:
    if extenv:
        return {**dict(environ), **env}
    return env


def decode_stdio_bytes(stdio_bytes: Union[str, bytes], lf: bool = True) -> str:
    r"""Return Stdio bytes from stdout/stderr as a string

    Args:
        stdio_bytes (bytes): STDOUT/STDERR bytes
        lf (bool): Replace `\r\n` line endings with `\n`

    Returns:
        str: decoded stdio bytes

    """
    if isinstance(stdio_bytes, str):
        return stdio_bytes
    if lf:
        return decode_stdio_bytes(stdio_bytes, lf=False).replace("\r\n", "\n")
    try:
        return str(stdio_bytes.decode())
    except AttributeError:
        return ""
    except Exception:
        pass

    try:
        return str(stdio_bytes.decode("utf-8"))
    except UnicodeDecodeError:
        pass
    return str(stdio_bytes.decode("latin-1"))


def pstdout(proc: CompletedProcess[AnyStr]) -> str:
    """Get the STDOUT as a string from a subprocess

    Args:
        proc: python subprocess.process object with stdout

    Returns:
        STDOUT for the proc as string

    """
    if proc.stdout is None:
        return ""
    return decode_stdio_bytes(proc.stdout)


def pstderr(proc: CompletedProcess[AnyStr]) -> str:
    """Get the STDERR as a string from a subprocess

    Args:
        proc: python subprocess.process object with STDERR

    Returns:
        STDERR for the proc as string

    """
    if proc.stderr is None:
        return ""
    return decode_stdio_bytes(proc.stderr)


def pstdout_pstderr(proc: CompletedProcess[AnyStr]) -> tuple[str, str]:
    """Get the STDOUT and STDERR as strings from a subprocess

    Args:
        proc: Completed-subprocess

    Returns:
        Tuple of two strings: (stdout-string, stderr-string)

    """
    return pstdout(proc), pstderr(proc)


def validate_stdin(stdin: STDIN) -> STDIN:
    if stdin is None:
        return None
    if stdin and isinstance(stdin, str):
        return validate_stdin(str(stdin).encode())
    if isinstance(stdin, (bytes, bytearray)):
        return bytes(stdin)
    raise ValueError(f"Invalid stdin: (type={str(type(stdin))}) {str(stdin)}")


def utf8_string(val: Union[str, bytes, bytearray]) -> str:
    if not isinstance(val, str):
        return val.decode("utf-8")
    return val


def flatten_args(*args: Union[Any, list[Any]]) -> list[str]:
    """Flatten possibly nested iterables of sequences to a list of strings

    Examples:
        >>> list(flatten_args("cmd", ["uno", "dos", "tres"]))
        ['cmd', 'uno', 'dos', 'tres']
        >>> list(flatten_args("cmd", ["uno", "dos", "tres", ["4444", "five"]]))
        ['cmd', 'uno', 'dos', 'tres', '4444', 'five']

    """
    return list(_flatten_strings(*args))


def validate_popen_args(args: Union[PopenArgs, tuple[PopenArgs, ...]]) -> list[str]:
    if len(args) == 0:
        raise ValueError("args must be a non-empty sequence")
    if len(args) == 1:
        _args = args[0]
        if isinstance(_args, str):
            return shplit(_args)
        return flatten_args(_args)
    return flatten_args(args)


def popen_has_pipe_character(args: Union[list[PopenArg], tuple[PopenArg, ...]]) -> bool:
    return any(arg == "|" for arg in args)


def validate_popen_args_windows(
    args: PopenArgs, env: Optional[dict[str, str]] = None
) -> PopenArgs:
    args = validate_popen_args(args)
    _path = None
    if env and "PATH" in env:
        _path = env["PATH"]
    fspath = which_lru(args[0], path=_path)
    if fspath and fspath.lower() in {".cmd", ".bat"}:
        args[0] = str(Path(fspath).absolute())
    return args


def _do_tee(
    args: PopenArgs,
    input: Optional[STDIN],
    cwd: Optional[FsPath],
    env: Optional[dict[str, str]],
    timeout: Optional[float],
    shell: bool = False,
) -> Done:
    completed, pdt = sp.run_dtee(
        args, input=input, cwd=cwd, env=env, timeout=timeout, shell=shell
    )
    return Done(
        args=completed.args,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
        ti=pdt.ti,
        tf=pdt.tf,
        dt=pdt.dt,
    )


def _do(
    args: PopenArgs,
    *,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[FsPath] = None,
    shell: bool = False,
    check: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    timeout: Optional[float] = None,
    text: bool = False,
    tee: bool = False,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess synchronously

    Args:
        args: Args as strings for the subprocess
        env: Environment variables as a dictionary (Default value = None)
        extenv: Extend the environment with current environment (Default value = True)
        cwd: Current working directory (Default value = None)
        shell: Run in shell or sub-shell
        check: Check the outputs (generally useless)
        input: Stdin to give to the subprocess
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        tee (bool): Flag to tee the subprocess stdout and stderr to sys.stdout/stderr
        text: Flag to decode the output as text
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code (Union[int, Sequence[int]]): Code(s) to consider as OK
        dryrun (bool): Flag to not run the subprocess and return faux Done

    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    Raises:
        ValueError: If args has pipe character (`|`)

    """
    _input = validate_stdin(input)
    _args = [*args]
    if IS_WIN:
        _syspath = None
        if env:
            _syspath = env.get("PATH", environ["PATH"])

        exe_path = which_lru(_args[0], path=_syspath)
        if exe_path:
            _args[0] = exe_path
    if not shell and popen_has_pipe_character(_args):
        raise ValueError(
            f"WARNING: has a pipe character, but shell=False; args: {_args}"
        )
    _env = None if env is None else mkenv(env, extenv=extenv)
    args_str = " ".join(_args)
    if dryrun:
        return Done(
            args=_args if IS_WIN or not shell else [args_str],
            returncode=0,
            stdout="",
            stderr="",
            ti=0,
            tf=0,
            dt=0,
            hrdt=HrTime(sec=0, ns=0),
            verbose=verbose,
            stdin=_input if not isinstance(_input, bytes) else _input.decode(),
            dryrun=True,
        )

    if tee:
        return _do_tee(
            args=args,
            input=_input,
            cwd=cwd,
            env=_env,
            timeout=timeout,
            shell=shell,
        )

    ti = time()
    proc = run(
        args=_args if IS_WIN or not shell else args_str,
        stdout=PIPE,
        stderr=PIPE,
        env=_env,
        cwd=cwd,
        shell=shell,
        input=validate_stdin(input),
        timeout=timeout,
        text=text,
    )
    tf = time()
    stdout_str = pstdout(proc)
    stderr_str = pstderr(proc)
    done = Done(
        args=proc.args if isinstance(proc.args, list) else [proc.args],
        returncode=proc.returncode,
        stdout=stdout_str,
        stderr=stderr_str,
        ti=ti,
        tf=tf,
        dt=tf - ti,
        hrdt=HrTime.from_seconds(tf - ti),
        verbose=verbose,
        stdin=_input if not isinstance(_input, bytes) else _input.decode(),
    )
    if check or ok_code != 0:
        done.check(ok_code=ok_code)
    return done


def do(
    *popenargs: PopenArgs,
    args: Optional[PopenArgs] = None,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[FsPath] = None,
    shell: bool = False,
    check: bool = False,
    tee: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    timeout: Optional[Union[float, int]] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess synchronously

    Args:
        *popenargs: Args given as `*args`; Cannot use both *popenargs and args
        args: Args as strings for the subprocess
        env: Environment variables as a dictionary (Default value = None)
        extenv: Extend the environment with the current environment (Default value = True)
        cwd: Current working directory (Default value = None)
        shell: Run in shell or sub-shell
        check: Check the outputs (generally useless)
        input: Stdin to give to the subprocess
        tee (bool): Flag to tee the subprocess stdout and stderr to sys.stdout/stderr
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code: Return code(s) to check against
        dryrun: Don't run the subprocess

    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    Raises:
        ValueError: if args and *popenargs are both given

    """
    if args and popenargs:
        raise ValueError("Cannot give *popenargs and `args` kwargs")
    args = validate_popen_args([*args]) if args else validate_popen_args(popenargs)
    if is_win():
        args = validate_popen_args_windows(args, env)
    _input = validate_stdin(input)
    return _do(
        args=args,
        env=env,
        extenv=extenv,
        cwd=cwd,
        shell=shell,
        check=check,
        verbose=verbose,
        input=_input,
        timeout=timeout,
        ok_code=ok_code,
        dryrun=dryrun,
        tee=tee,
    )


def shell(
    *popenargs: PopenArgs,
    args: Optional[PopenArgs] = None,
    env: Optional[dict[str, str]] = None,
    shell: bool = True,
    extenv: bool = True,
    cwd: Optional[FsPath] = None,
    check: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    timeout: Optional[Union[float, int]] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess synchronously in current shell

    Args:
        *popenargs: Args given as `*args`; Cannot use both *popenargs and args
        args: Args as strings for the subprocess
        env: Environment variables as a dictionary (Default value = None)
        shell: Run in shell or sub-shell; default is True for `shell`
        extenv: Extend the environment with the current environment (Default value = True)
        cwd: Current working directory (Default value = None)
        check: Check the outputs (generally useless)
        input: Stdin to give to the subprocess
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code: Return code(s) to check if ok
        dryrun: Don't run the subprocess


    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    """
    return do(
        *popenargs,
        args=args,
        shell=shell,
        env=env,
        extenv=extenv,
        cwd=cwd,
        check=check,
        verbose=verbose,
        input=input,
        timeout=timeout,
        ok_code=ok_code,
        dryrun=dryrun,
    )


shx = shell

_run_async = asyncify(run)
_do_asyncify = asyncify(do)


async def run_async(
    args: PopenArgs,
    *,
    stdin: Optional[Union[IO[AnyStr], int]] = None,
    input: Optional[str] = None,
    stdout: Optional[Union[IO[AnyStr], int]] = None,
    stderr: Optional[Union[IO[AnyStr], int]] = None,
    capture_output: bool = False,
    shell: bool = False,
    cwd: Optional[FsPath] = None,
    timeout: Optional[Union[float, int]] = None,
    check: bool = False,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    text: bool = False,
    env: Optional[dict[str, str]] = None,
    universal_newlines: bool = False,
    **other_popen_kwargs: Any,
) -> CompletedProcess[Any]:
    args = validate_popen_args(args)
    return await _run_async(
        args=args,
        input=input,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
        cwd=cwd,
        timeout=timeout,
        check=check,
        errors=errors,
        env=env,
        capture_output=capture_output,
        universal_newlines=universal_newlines | text,
        encoding=encoding,
        **other_popen_kwargs,
    )


async def do_asyncify(
    *popenargs: PopenArgs,
    args: Optional[PopenArgs] = None,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[str] = None,
    shell: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    check: bool = False,
    timeout: Optional[Union[float, int]] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess asynchronously using asyncified version of do"""
    done = await _do_asyncify(
        *popenargs,
        args=args,
        env=env,
        extenv=extenv,
        cwd=cwd,
        shell=shell,
        verbose=verbose,
        input=input,
        check=check,
        timeout=timeout,
        ok_code=ok_code,
        dryrun=dryrun,
    )
    done.async_proc = True
    return done


async def _do_async(
    args: PopenArgs,
    *,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[str] = None,
    shell: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    check: bool = False,
    timeout: Optional[Union[float, int]] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess and await completion

    Args:
        args: Args as strings for the subprocess
        check (bool): Check the result returncode
        env: Environment variables as a dictionary (Default value = None)
        extenv: Extend environment with the current environment (Default value = True)
        cwd: Current working directory (Default value = None)
        shell: Run in shell or sub-shell
        input: Stdin to give to the subprocess
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code: Return code(s) to check if ok
        dryrun: Don't run the subprocess

    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    Raises:
        CalledProcessError: If check is True and the returncode is not 0
        TimeoutError: If the process takes longer than timeout if given

    """
    # if is windows and python is below 3.7, use the asyncified-do func
    if is_win() and sys.version_info < (3, 8):
        done = await do_asyncify(
            args=args,
            env=env,
            cwd=cwd,
            shell=shell,
            verbose=verbose,
            input=input,
            check=check,
            timeout=timeout,
            ok_code=ok_code,
            dryrun=dryrun,
        )
        done.async_proc = True
        return done

    if input:
        input = validate_stdin(input)
    if isinstance(args, str):
        _args = [args]
    elif isinstance(args, bytes):
        _args = [utf8_string(args)]
    elif isinstance(args, (list, tuple)):
        _args = flatten_args(args)
    else:
        _args = list(map(str, args))

    # input is None or bytes
    _input = input if not isinstance(input, str) else input.encode()

    _env = None if env is None else mkenv(env, extenv=extenv)
    _cwd = pwd()
    if cwd and path.exists(cwd) and path.isdir(cwd):
        _cwd = cwd
    if is_win():
        _syspath = None
        if env:
            _syspath = env.get("PATH", environ["PATH"])

        exe_path = which_lru(_args[0], path=_syspath)
        if exe_path:
            _args[0] = exe_path

    if dryrun:
        return Done(
            args=_args,
            returncode=-1,
            stdout="",
            stderr="",
            ti=0,
            tf=0,
            dt=0,
            hrdt=HrTime(
                sec=0,
                ns=0,
            ),
            verbose=verbose,
            stdin=_input if not isinstance(_input, bytes) else _input.decode(),
            dryrun=True,
            async_proc=True,
        )
    _proc, _pdt = await __run_async.run_dtee_async(
        *_args,
        env=_env,
        cwd=_cwd,
        shell=shell,
        ok_code=ok_code if isinstance(ok_code, (list, tuple, set)) else {ok_code},
        check=check,
        capture_output=True,
        timeout=timeout,
        input=_input,
        universal_newlines=True,
    )
    _args_array = (
        list(map(str, args)) if isinstance(args, (list, tuple)) else [str(args)]
    )
    return Done(
        args=_args_array,
        returncode=_proc.returncode,
        stdout=decode_stdio_bytes(_proc.stdout),
        stderr=decode_stdio_bytes(_proc.stderr),
        stdin=input.decode(encoding="utf-8") if isinstance(input, bytes) else None,
        ti=_pdt.ti,
        tf=_pdt.tf,
        dt=_pdt.dt,
        hrdt=HrTime.from_seconds(
            _pdt.dt,
        ),
        verbose=verbose,
        async_proc=True,
    )


async def do_async(
    *popenargs: PopenArgs,
    args: Optional[PopenArgs] = None,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[str] = None,
    shell: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    check: bool = False,
    timeout: Optional[float] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess and await its completion

    Args:
        *popenargs: Args given as `*args`; Cannot use both *popenargs and args
        args: Args as strings for the subprocess
        check (bool): Check the result returncode
        env: Environment variables as a dictionary (Default value = None)
        extenv: Extend environment with the current environment (Default value = True)
        cwd: Current working directory (Default value = None)
        shell: Run in shell or sub-shell
        input: Stdin to give to the subprocess
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code: Return code(s) that are considered OK (Default value = 0)
        dryrun (bool): Flag to not run the subprocess but return a Done object

    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    Raises:
        ValueError: If both *popenargs and args are given

    """
    if args and popenargs:
        raise ValueError("Cannot give *args and args-keyword-argument")
    args = validate_popen_args([*args]) if args else validate_popen_args(popenargs)
    if is_win() and sys.version_info < (3, 8):
        done = await do_asyncify(
            args=args,
            env=env,
            extenv=extenv,
            cwd=cwd,
            shell=shell,
            verbose=verbose,
            input=input,
            check=check,
            timeout=timeout,
            ok_code=ok_code,
            dryrun=dryrun,
        )
        done.async_proc = True
        return done
    if not shell and is_win():
        args = validate_popen_args_windows(args, env)
    return await _do_async(
        args=args,
        env=env,
        extenv=extenv,
        cwd=cwd,
        shell=shell,
        verbose=verbose,
        input=input,
        check=check,
        timeout=timeout,
        ok_code=ok_code,
        dryrun=dryrun,
    )


do_ = do_async


async def doa(
    *popenargs: PopenArgs,
    args: Optional[PopenArgs] = None,
    env: Optional[dict[str, str]] = None,
    extenv: bool = True,
    cwd: Optional[str] = None,
    shell: bool = False,
    verbose: bool = False,
    input: STDIN = None,
    check: bool = False,
    timeout: Optional[float] = None,
    ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    dryrun: bool = False,
) -> Done:
    """Run a subprocess and await its completion

    Alias for sh.do_async

    Args:
        *popenargs: Args given as `*args`; Cannot use both *popenargs and args
        args: Args as strings for the subprocess
        check (bool): Check the result returncode
        env: Environment variables as a dictionary (Default value = None)
        cwd: Current working directory (Default value = None)
        shell: Run in shell or sub-shell
        input: Stdin to give to the subprocess
        verbose (bool): Flag to write the subprocess stdout and stderr to
            sys.stdout and sys.stderr
        timeout (Optional[int]): Timeout in seconds for the process if not None
        ok_code: Return code(s) that are considered OK (Default value = 0)
        dryrun (bool): Flag to not run the subprocess but return a Done object
        extenv: Extend environment with the current environment (Default value = True)

    Returns:
        Finished PRun object which is a dictionary, so a dictionary

    """
    return await do_async(
        *popenargs,
        args=args,
        env=env,
        extenv=extenv,
        cwd=cwd,
        shell=shell,
        verbose=verbose,
        input=input,
        check=check,
        timeout=timeout,
        ok_code=ok_code,
        dryrun=dryrun,
    )


# =============================================================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# =============================================================================
#  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\
# /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
# =============================================================================
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# =============================================================================


class LIN(_LIN):
    """Linux (and Mac) shell commands/methods container"""

    @staticmethod
    def rsync_args(
        src: str,
        dest: str,
        delete: bool = False,
        dry_run: bool = False,
        exclude: Optional[Iterable[str]] = None,
        include: Optional[Iterable[str]] = None,
    ) -> list[str]:
        """Return args for rsync command on linux/mac

        Args:
            src: path to remote (raid) tdir
            dest: path to local tdir
            delete: Flag that will do a 'hard sync'
            exclude: Strings/patterns to exclude
            include: Strings/patterns to include
            dry_run (bool): Perform operation as a dry run

        Returns:
            subprocess return code from rsync

        Rsync return codes::

            - 0 == Success
            - 1 == Syntax or usage error
            - 2 == Protocol incompatibility
            - 3 == Errors selecting input/output files, dirs
            - 4 == Requested  action not supported: an attempt was made to
              manipulate 64-bit files on a platform that cannot support them;
              or an option was specified that is supported by the client and
              not the server.
            - 5 == Error starting client-server protocol
            - 6 == Daemon unable to append to log-file
            - 10 == Error in socket I/O
            - 11 == Error in file I/O
            - 12 == Error in rsync protocol data stream
            - 13 == Errors with program diagnostics
            - 14 == Error in IPC code
            - 20 == Received SIGUSR1 or SIGINT
            - 21 == Some error returned by waitpid()
            - 22 == Error allocating core memory buffers
            - 23 == Partial transfer due to error
            - 24 == Partial transfer due to vanished source files
            - 25 == The --max-delete limit stopped deletions
            - 30 == Timeout in data send2viewserver/receive
            - 35 == Timeout waiting for daemon connection


        """
        if exclude is None:
            exclude = []
        if include is None:
            include = []

        if not dest.endswith("/"):
            dest = f"{dest}/"
        if not src.endswith("/"):
            src = f"{src}/"
        _args: list[Union[str, None]] = [
            "rsync",
            "-a",
            "-O",
            "--no-o",
            "--no-g",
            "--no-p",
            "--delete" if delete else None,
            *(f'--exclude="{pattern}"' for pattern in exclude),
            *(f'--include="{pattern}"' for pattern in include),
            *(("--dry-run", "-i") if dry_run else (None,)),
            src,
            dest,
        ]
        return list(filter(None, _args))

    @staticmethod
    def rsync(
        src: str,
        dest: str,
        delete: bool = False,
        mkdirs: bool = False,
        dry_run: bool = False,
        exclude: Optional[Iterable[str]] = None,
        include: Optional[Iterable[str]] = None,
    ) -> Done:
        """Run an `rsync` subprocess

        Args:
            mkdirs (bool): Make destination directories if they do not already
                exist; defaults to False.
            src (str): Source directory path
            dest (str): Destination directory path
            delete (bool): Delete files/directories in destination if they do
                exist in source
            exclude: Strings/patterns to exclude
            include: Strings/patterns to include
            dry_run (bool): Perform operation as a dry run

        Returns:
            Done: Done object containing the info for the rsync run

        Rsync return codes::

            - 0 == Success
            - 1 == Syntax or usage error
            - 2 == Protocol incompatibility
            - 3 == Errors selecting input/output files, dirs
            - 4 == Requested  action not supported: an attempt was made to
              manipulate 64-bit files on a platform that cannot support them;
              or an option was specified that is supported by the client and
              not the server.
            - 5 == Error starting client-server protocol
            - 6 == Daemon unable to append to log-file
            - 10 == Error in socket I/O
            - 11 == Error in file I/O
            - 12 == Error in rsync protocol data stream
            - 13 == Errors with program diagnostics
            - 14 == Error in IPC code
            - 20 == Received SIGUSR1 or SIGINT
            - 21 == Some error returned by waitpid()
            - 22 == Error allocating core memory buffers
            - 23 == Partial transfer due to error
            - 24 == Partial transfer due to vanished source files
            - 25 == The --max-delete limit stopped deletions
            - 30 == Timeout in data send2viewserver/receive
            - 35 == Timeout waiting for daemon connection

        """
        if exclude is None:
            exclude = []
        if include is None:
            include = []
        if mkdirs and not dry_run:
            makedirs(dest, exist_ok=True)
        rsync_args = LIN.rsync_args(
            src, dest, delete=delete, exclude=exclude, include=include, dry_run=dry_run
        )

        done = do(args=list(filter(None, rsync_args)))
        return done

    @staticmethod
    def sync(
        src: str,
        dest: str,
        delete: bool = False,
        mkdirs: bool = False,
        dry_run: bool = False,
        exclude: Optional[Iterable[str]] = None,
        include: Optional[Iterable[str]] = None,
    ) -> Done:
        return LIN.rsync(
            src,
            dest,
            delete=delete,
            mkdirs=mkdirs,
            dry_run=dry_run,
            exclude=exclude,
            include=include,
        )


# =============================================================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# =============================================================================
#  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\
# /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
# =============================================================================
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# =============================================================================


class WIN(_WIN):
    """Windows shell commands/methods container"""

    _MAX_CMD_LENGTH: int = 8192

    @staticmethod
    def robocopy_args(
        src: str,
        dest: str,
        *,
        delete: bool = False,
        exclude_files: Optional[list[str]] = None,
        exclude_dirs: Optional[list[str]] = None,
        dry_run: bool = False,
    ) -> list[str]:
        """Return list of robocopy command args

        Args:
            src (str): path to source directory
            dest (str): path to destination directory
            delete (bool): Delete files in the destination directory if they do
                not exist in the source directory
            exclude_files: Strings/patterns with which to exclude files
            exclude_dirs: Strings/patterns with which to exclude directories
            dry_run (bool): Do the operation as a dry run

        Returns:
            subprocess return code from robocopy

        Robocopy return codes::

            0. No files were copied. No failure was encountered. No files were
               mismatched. The files already exist in the destination
               directory; therefore, the copy operation was skipped.
            1. All files were copied successfully.
            2. There are some additional files in the destination directory
               that are not present in the source directory. No files were
               copied.
            3. Some files were copied. Additional files were present. No
               failure was encountered.
            5. Some files were copied. Some files were mismatched. No failure
               was encountered.
            6. Additional files and mismatched files exist. No files were
               copied and no failures were encountered. This means that the
               files already exist in the destination directory.
            7. Files were copied, a file mismatch was present, and additional
               files were present.
            8. Several files did not copy.

        """
        if exclude_files is None:
            exclude_files = []
        if exclude_dirs is None:
            exclude_dirs = []
        _args = [
            "robocopy",
            src,
            dest,
            "/MIR" if delete else "/E",
            "/mt",
            "/W:1",
            "/R:1",
        ]
        if exclude_dirs:
            _args.extend(["/XD", *exclude_dirs])
        if exclude_files:
            _args.extend(["/XF", *exclude_files])
        if dry_run:
            _args.append("/L")
        return list(filter(None, _args))

    @staticmethod
    def robocopy(
        src: str,
        dest: str,
        *,
        mkdirs: bool = True,
        delete: bool = False,
        exclude_files: Optional[Iterable[str]] = None,
        exclude_dirs: Optional[Iterable[str]] = None,
        dry_run: bool = False,
    ) -> Done:  # pragma: nocov
        """Robocopy wrapper function (crude in that it opens a subprocess)

        Args:
            src (str): path to source directory
            dest (str): path to destination directory
            delete (bool): Delete files in the destination directory if they do
                not exist in the source directory
            exclude_files: Strings/patterns with which to exclude files
            exclude_dirs: Strings/patterns with which to exclude directories
            dry_run (bool): Do the operation as a dry run
            mkdirs (bool): Flag to make destinaation directories if they do
                not already exist

        Returns:
            subprocess return code from robocopy

        Robocopy return codes::

            0. No files were copied. No failure was encountered. No files were
               mismatched. The files already exist in the destination
               directory; therefore, the copy operation was skipped.
            1. All files were copied successfully.
            2. There are some additional files in the destination directory
               that are not present in the source directory. No files were
               copied.
            3. Some files were copied. Additional files were present. No
               failure was encountered.
            5. Some files were copied. Some files were mismatched. No failure
               was encountered.
            6. Additional files and mismatched files exist. No files were
               copied and no failures were encountered. This means that the
               files already exist in the destination directory.
            7. Files were copied, a file mismatch was present, and additional
               files were present.
            8. Several files did not copy.

        """
        _exclude_files = [] if exclude_files is None else list(exclude_files)
        _exclude_dirs = [] if exclude_dirs is None else list(exclude_dirs)
        if mkdirs and not dry_run:
            makedirs(dest, exist_ok=True)
        _args = WIN.robocopy_args(
            src=src,
            dest=dest,
            delete=delete,
            exclude_files=_exclude_files,
            exclude_dirs=_exclude_dirs,
            dry_run=dry_run,
        )
        return do(args=_args)

    @staticmethod
    def sync(
        src: str,
        dest: str,
        *,
        delete: bool = False,
        mkdirs: bool = False,
        dry_run: bool = False,
        exclude: Optional[Iterable[str]] = None,
        include: Optional[Iterable[str]] = None,
    ) -> Done:  # pragma: nocov
        return WIN.robocopy(
            src=src,
            dest=dest,
            mkdirs=mkdirs,
            delete=delete,
            exclude_files=exclude,
            exclude_dirs=include,
            dry_run=dry_run,
        )


# =============================================================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# =============================================================================
#  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\
# /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
# =============================================================================
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# =============================================================================

# OS DEPENDENT
_OS: Union[type[LIN], type[WIN]] = (
    WIN if "windows" in system().lower() else LIN
)  # Use LIN/WIN as _OS
sync = _OS.sync
link_dir = _OS.link_dir
link_dirs = _OS.link_dirs
link_file = _OS.link_file
link_files = _OS.link_files
unlink_dir = _OS.unlink_dir
unlink_dirs = _OS.unlink_dirs
unlink_file = _OS.unlink_file
unlink_files = _OS.unlink_files


# =============================================================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# =============================================================================
#  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\
# /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
# =============================================================================
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# =============================================================================


def pwd() -> str:
    """Return present-working-directory path string; alias for os.getcwd

    Returns:
        str: present working directory as string

    Examples:
        >>> import os
        >>> pwd() == os.getcwd()
        True

    """
    return getcwd()


def dirname(fspath: FsPath) -> str:
    """Return dirname/parent-dir of given path; alias of os.path.dirname

    Args:
        fspath: File-system path

    Returns:
        str: basename of path

    """
    return path.dirname(_fspath(fspath))


def basename(fspath: FsPath) -> str:
    """Return the basename of given path; alias of os.path.dirname

    Args:
        fspath: File-system path

    Returns:
        str: basename of path

    """
    return path.basename(str(fspath))


def cd(dirpath: FsPath) -> None:
    """Change directory to given dirpath; alias for `os.chdir`

    Args:
        dirpath: Directory fspath

    """
    chdir(str(dirpath))


def export(key: str, val: Optional[str] = None) -> tuple[str, str]:
    """Export/Set an environment variable

    Args:
        key (str): environment variable name/key
        val (str): environment variable value

    Raises:
        ValueError: if unable to parse key/val

    """
    if val:
        environ[key] = val
        return (key, val)
    if "=" in key:
        _key = key.split("=")[0]
        return export(_key, key[len(_key) + 1 :])
    raise ValueError(
        f"Unable to parse env variable - key: {str(key)}, value: {str(val)}"
    )


def setenv(key: str, val: Optional[str] = None) -> tuple[str, str]:
    """Export/Set an environment variable

    Args:
        key (str): environment variable name/key
        val (str): environment variable value

    Returns:
        tuple[str, str]: environment variable key/value pair

    """
    return export(key=key, val=val)


def shplit(string: str, comments: bool = False, posix: bool = True) -> list[str]:
    """Typed alias for shlex.split"""
    return _shplit(string, comments=comments, posix=posix)


def quote(string: str) -> str:
    r"""Typed alias for shlex.quote

    Args:
        string (str): string to quote

    Returns:
        str: quoted string

    Examples:
        >>> quote("hello world")
        "'hello world'"
        >>> quote("hello 'world'")
        '\'hello \'"\'"\'world\'"\'"\'\''

    """
    return _quote(string)


def q(string: str) -> str:
    r"""Typed alias for shlex.quote

    Args:
        string (str): string to quote

    Returns:
        str: quoted string

    Examples:
        >>> q("hello world")
        "'hello world'"
        >>> q("hello 'world'")
        '\'hello \'"\'"\'world\'"\'"\'\''

    """
    return _quote(string)


def which(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which`

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return _which(cmd, path=path)


def where(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which`; alias of shellfish.sh.which

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return which(cmd, path=path)


@lru_cache(maxsize=128)
def which_lru(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which` and cache the results

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return which(cmd, path=path)


def tree(dirpath: FsPath, filterfn: Optional[Callable[[str], bool]] = None) -> str:
    """Create a directory tree string given a directory path

    Args:
        dirpath (FsPath): Directory string to make tree for
        filterfn: Function to filter sub-directories and sub-files with

    Returns:
        str: Directory-tree string

    Examples:
        >>> tmpdir = 'tree.doctest'
        >>> from os import makedirs; makedirs(tmpdir, exist_ok=True)
        >>> from pathlib import Path
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     makedirs(dirpath, exist_ok=True)
        ...     Path(fspath).touch()
        >>> print(tree(tmpdir))
        tree.doctest/
        └── dir/
            ├── dir2/
            │   ├── file1.txt
            │   ├── file2.txt
            │   └── file3.txt
            ├── dir2a/
            │   ├── file1.txt
            │   ├── file2.txt
            │   └── file3.txt
            ├── file1.txt
            ├── file2.txt
            └── file3.txt
        >>> print(tree(tmpdir, lambda s: _DirTree._default_filter(s) and not "file2" in s))
        tree.doctest/
        └── dir/
            ├── dir2/
            │   ├── file1.txt
            │   └── file3.txt
            ├── dir2a/
            │   ├── file1.txt
            │   └── file3.txt
            ├── file1.txt
            └── file3.txt
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    return "\n".join(
        p.displayable() for p in _DirTree.make_tree(Path(dirpath), filterfn=filterfn)
    )


def ls(dirpath: FsPath = ".", abspath: bool = False) -> list[str]:
    """List files and dirs given a dirpath (defaults to pwd)

    Args:
        dirpath (FsPath): path-string to directory to list
        abspath (bool): Give absolute paths

    Returns:
        List of the directory items

    """
    if abspath:
        return [el.path for el in scandir(str(dirpath))]
    return listdir(str(dirpath))


def ls_files(dirpath: FsPath = ".", *, abspath: bool = False) -> list[str]:
    """List the files in a given directory path

    Args:
        dirpath (FsPath): Directory path for which one might want to list files
        abspath (bool): Return absolute filepaths

    Returns:
        List of files as strings

    """
    files = (el for el in scandir(str(dirpath)) if el.is_file())
    if abspath:
        return list(map(lambda el: el.path, files))
    return list(map(lambda el: el.name, files))


def ls_dirs(dirpath: FsPath = ".", *, abspath: bool = False) -> list[str]:
    """List the directories in a given directory path

    Args:
        dirpath (FsPath): Directory path for which one might want list directories
        abspath (bool): Return absolute directory paths

    Returns:
        List of directories as strings

    """
    dirs = (el for el in scandir(str(dirpath)) if el.is_dir())
    if abspath:
        return list(map(lambda el: el.path, dirs))
    return list(map(lambda el: el.name, dirs))


def ls_files_dirs(
    dirpath: FsPath = ".", *, abspath: bool = False
) -> tuple[list[str], list[str]]:
    """List the files and directories given directory path

    Args:
        dirpath (FsPath): Directory path to execute on
        abspath (bool): Return absolute file/directory paths

    Returns:
        Two lists of strings; the first is a list of the files and the second
            is a list of the directories

    """
    dir_items = list(fs.scandir_gen(dirpath, files=True, dirs=True))
    dir_dir_entries = (el for el in dir_items if el.is_dir())
    file_dir_entries = (el for el in dir_items if el.is_file())
    if not abspath:
        return [el.name for el in file_dir_entries], [el.name for el in dir_dir_entries]
    return [el.path for el in file_dir_entries], [el.path for el in dir_dir_entries]


async def ls_async(dirpath: FsPath = ".", abspath: bool = False) -> list[str]:
    """List files and dirs given a dirpath (defaults to pwd)

    Args:
        dirpath (FsPath): path-string to directory to list
        abspath (bool): Give absolute paths

    Returns:
        List of the directory items

    """
    items = await listdir_async(dirpath)
    if abspath:
        return [path.join(dirpath, el) for el in items]
    return items


def rm(
    fspath: FsPath,
    *,
    force: bool = False,
    recursive: bool = False,
    verbose: bool = False,
    f: bool = False,
    r: bool = False,
    v: bool = False,
    dryrun: bool = False,
) -> None:
    """Remove files & directories in the style of the shell

    Args:
        fspath (FsPath): Path to file or directory to remove
        force (bool): Flag to force removal; ignore missing
        recursive (bool): Flag to remove recursively (like the `-r` in `rm -r dir`)
        verbose (bool): Flag to be verbose
        f (bool): alias for force kwarg
        v (bool): alias for verbose
        r (bool): alias for recursive kwarg
        dryrun (bool): Flag to not actually remove anything

    Raises:
        ValueError: If recursive and r are `False` and fspath is a directory

    """
    if verbose or v:
        echo(f"Removing {fspath}")
    fs.rm(
        fspath,
        force=force or f,
        recursive=recursive or r,
        dryrun=dryrun,
    )


def mv(src: FsPath, dest: FsPath) -> None:
    """Move file(s) like on the command line

    Args:
        src (FsPath): source file(s)
        dest (FsPath): destination path

    """
    fs.move(src, dest)


def source(filepath: FsPath, _globals: bool = True) -> None:  # pragma: nocov
    """Execute/run a python file given a fspath and put globals in globasl

    Args:
        filepath (FsPath): Path to python file
        _globals (bool): Exec using globals

    """
    string = fs.lstring(str(filepath))
    if _globals:
        exec(string, globals())
    else:
        exec(string)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
