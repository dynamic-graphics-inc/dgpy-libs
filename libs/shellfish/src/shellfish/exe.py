# -*- coding: utf-8 -*-
"""Exes/commands"""

from __future__ import annotations

from dataclasses import dataclass, field
from shlex import split as _shplit
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from shellfish import sh
from shellfish.sh import Done, flatten_args

if TYPE_CHECKING:
    from shellfish._types import STDIN, FsPath, PopenArgs, PopenArgv

__all__ = (
    "Exe",
    "ExeABC",
    "ExeAsync",
    "ExeConfig",
)

TExe = TypeVar("TExe", bound="ExeABC")


@dataclass
class ExeConfig:
    """Serializable configuration for an [ExeABC][shellfish.exe.ExeABC] subclass"""

    cmd: str
    """Name of (or path to) the executable"""
    subcmd: tuple[str, ...] | None = None
    """Sub-command args always prepended to the exe's args"""
    abspath: str | None = None
    """Resolved absolute path to the executable, if known/cached"""
    env: dict[str, str] | None = None
    """Environment variables to run the executable with"""
    cwd: str | None = None
    """Working directory to run the executable in"""
    shell: bool = False
    """Run the executable through the shell"""
    verbose: bool = False
    """Echo stdout/stderr of each run to the parent process"""
    timeout: float | int | None = None
    """Timeout in seconds for each run; None for no timeout"""
    ok_code: int | set[int] = field(default_factory=lambda: {0})
    """Return code(s) considered ok"""
    check: bool = False
    """Raise [DoneError][shellfish.done.DoneError] if the return code is not ok"""


class ExeABC:
    """Base class for command/executable wrapper objects

    Holds the defaults (env, cwd, timeout, ...) that each invocation of the
    wrapped executable is run with. Subclassed by [Exe][shellfish.exe.Exe] and
    [ExeAsync][shellfish.exe.ExeAsync], which make instances callable.
    """

    cmd: str
    """Name of (or path to) the executable"""
    subcmd: tuple[str, ...] | None = None
    """Sub-command args always prepended to the exe's args"""

    abspath: str | None = None
    """Resolved absolute path to the executable, if known/cached"""
    env: dict[str, str] | None = None
    """Environment variables to run the executable with"""
    cwd: FsPath | None = None
    """Working directory to run the executable in"""
    shell: bool = False
    """Run the executable through the shell"""
    verbose: bool = False
    """Echo stdout/stderr of each run to the parent process"""
    timeout: float | int | None = None
    """Timeout in seconds for each run; None for no timeout"""
    ok_code: int | set[int] = 0
    """Return code(s) considered ok"""
    check: bool = False
    """Raise [DoneError][shellfish.done.DoneError] if the return code is not ok"""

    def __init__(
        self,
        cmd: str,
        *,
        subcmd: tuple[str, ...] | list[str] | str | None = None,
        abspath: str | None = None,
        check: bool = False,
        cwd: FsPath | None = None,
        env: dict[str, str] | None = None,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
        shell: bool = False,
        timeout: float | int | None = None,
        verbose: bool = False,
    ) -> None:
        """Create an exe wrapper for `cmd`

        Args:
            cmd: Name of (or path to) the executable
            subcmd: Sub-command args always prepended to the exe's args
            abspath: Absolute path to the executable; skips the `which` lookup
            check: Raise `DoneError` if the return code is not ok
            cwd: Working directory to run the executable in
            env: Environment variables to run the executable with
            ok_code: Return code (or collection of return codes) considered ok
            shell: Run the executable through the shell
            timeout: Timeout in seconds for each run; None for no timeout
            verbose: Echo stdout/stderr of each run to the parent process

        """
        self.cmd = cmd
        if subcmd is not None:
            self.subcmd = (subcmd,) if isinstance(subcmd, str) else tuple(subcmd)
        self.abspath = abspath
        self.env = env
        self.cwd = cwd
        self.shell = shell
        self.verbose = verbose
        self.timeout = timeout
        self.ok_code = (
            {
                ok_code,
            }
            if isinstance(ok_code, int)
            else set(ok_code)
        )
        self.check = check
        self.__post_init__()

    def __post_init__(self) -> None:
        """Hook called at the end of `__init__`; a no-op subclasses may override"""

    @classmethod
    def _from_exe_config(cls: type[TExe], config: ExeConfig) -> TExe:
        """Return a new instance from an [ExeConfig][shellfish.exe.ExeConfig]"""
        return cls(
            cmd=config.cmd,
            subcmd=config.subcmd,
            abspath=config.abspath,
            check=config.check,
            cwd=config.cwd,
            env=config.env,
            ok_code=config.ok_code,
            shell=config.shell,
            timeout=config.timeout,
            verbose=config.verbose,
        )

    def _config(self) -> ExeConfig:
        """Return this exe's settings as an [ExeConfig][shellfish.exe.ExeConfig]"""
        return ExeConfig(
            cmd=self.cmd,
            subcmd=self.subcmd,
            abspath=self.abspath,
            env=self.env,
            cwd=str(self.cwd) if self.cwd is not None else None,
            shell=self.shell,
            verbose=self.verbose,
            timeout=self.timeout,
            ok_code=self.ok_code,
            check=self.check,
        )

    def _which(self) -> str:
        """Return (and cache) the absolute path to the exe

        Returns:
            Absolute path to the executable

        Raises:
            FileNotFoundError: If the executable is not found on the PATH

        """
        if self.abspath is not None:
            return self.abspath
        _abspath = sh.which(self.cmd)
        if _abspath is None:
            _emsg = f"{self.cmd} not found"
            raise FileNotFoundError(_emsg)
        self.abspath = _abspath
        return self.abspath

    def which(self) -> str:
        """Return the absolute path to the exe

        Returns:
            Absolute path to the executable

        Raises:
            FileNotFoundError: If the executable is not found on the PATH

        """
        return self._which()

    def _unredundify(
        self,
        popenargs: tuple[PopenArgs, ...],
        args: PopenArgs | None = None,
    ) -> tuple[str, ...]:
        """Flatten args, dropping a leading repeat of `self.cmd` if present"""
        _args = popenargs if args is None else args
        if len(_args) == 1 and isinstance(_args[0], str):
            _args_list = _shplit(_args[0])
        else:
            _args_list = flatten_args(*_args)
        if _args_list and _args_list[0] == self.cmd:
            _args_list = _args_list[1:]
        return tuple(_args_list)

    def _cmdargs(
        self,
        popenargs: tuple[PopenArgs, ...],
        args: PopenArgs | None = None,
    ) -> PopenArgv:
        """Return the full argv (`self.cmd` + flattened args) for a run"""
        argv = self._unredundify(popenargs, args)
        return (self.cmd, *argv)

    def _do(
        self,
        *popenargs: PopenArgs,
        args: PopenArgs | None = None,
        env: dict[str, str] | None = None,
        extenv: bool = True,
        cwd: FsPath | None = None,
        shell: bool = False,
        check: bool = False,
        verbose: bool = False,
        input: STDIN = None,
        timeout: float | int | None = None,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
        dryrun: bool = False,
    ) -> Done:
        """Run the exe with the given args, overriding this exe's defaults

        Args:
            *popenargs: Args to run the exe with
            args: Args to run the exe with (alternative to `*popenargs`)
            env: Environment variables; defaults to `self.env`
            extenv: Extend `os.environ` with `env` instead of replacing it
            cwd: Working directory; defaults to `self.cwd`
            shell: Run through the shell; or-ed with `self.shell`
            check: Raise `DoneError` if the return code is not ok
            verbose: Echo stdout/stderr; or-ed with `self.verbose`
            input: Stdin to write to the process
            timeout: Timeout in seconds; defaults to `self.timeout`
            ok_code: Return code(s) considered ok; defaults to `self.ok_code`
            dryrun: Do not actually run the process

        Returns:
            [Done][shellfish.done.Done] object for the finished process

        """
        _args = self._cmdargs(popenargs, args)
        return sh.do(
            args=_args,
            env=env or self.env,
            extenv=extenv,
            cwd=cwd or self.cwd,
            shell=shell or self.shell,
            check=check,
            verbose=verbose or self.verbose,
            input=input,
            timeout=timeout or self.timeout,
            ok_code=ok_code or self.ok_code,
            dryrun=dryrun,
        )

    async def _do_async(
        self,
        *popenargs: PopenArgs,
        args: PopenArgs | None = None,
        check: bool = False,
        cwd: str | None = None,
        dryrun: bool = False,
        env: dict[str, str] | None = None,
        extenv: bool = True,
        input: STDIN = None,
        loop: Any | None = None,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
        shell: bool = False,
        timeout: float | int | None = None,
        verbose: bool = False,
    ) -> Done:
        """Run the exe asynchronously, overriding this exe's defaults

        Args:
            *popenargs: Args to run the exe with
            args: Args to run the exe with (alternative to `*popenargs`)
            check: Raise `DoneError` if the return code is not ok
            cwd: Working directory; defaults to `self.cwd`
            dryrun: Do not actually run the process
            env: Environment variables; defaults to `self.env`
            extenv: Extend `os.environ` with `env` instead of replacing it
            input: Stdin to write to the process
            loop: Event loop to run in (unused; kept for signature compatibility)
            ok_code: Return code(s) considered ok; defaults to `self.ok_code`
            shell: Run through the shell; or-ed with `self.shell`
            timeout: Timeout in seconds; defaults to `self.timeout`
            verbose: Echo stdout/stderr; or-ed with `self.verbose`

        Returns:
            [Done][shellfish.done.Done] object for the finished process

        """
        _args = self._cmdargs(popenargs, args)
        return await sh.do_async(
            args=_args,
            check=check,
            cwd=cwd or str(self.cwd),
            dryrun=dryrun,
            env=env or self.env,
            extenv=extenv,
            input=input,
            ok_code=ok_code or self.ok_code,
            shell=shell or self.shell,
            timeout=timeout or self.timeout,
            verbose=verbose or self.verbose,
        )

    # aliases
    do = _do
    do_async = _do_async
    doa = _do_async


class Exe(ExeABC):
    """Callable wrapper around an executable

    Examples:
        >>> from shellfish.exe import Exe
        >>> git = Exe("git", subcmd="status", verbose=False)
        >>> git.cmd
        'git'
        >>> git.subcmd
        ('status',)
        >>> git.ok_code
        {0}

        Calling the instance runs the executable and returns a
        [Done][shellfish.done.Done] object:

        ```python
        done = git("--porcelain")
        done.check()
        print(done.stdout)
        ```

    """

    def __call__(
        self,
        *popenargs: PopenArgs,
        args: PopenArgs | None = None,
        env: dict[str, str] | None = None,
        extenv: bool = True,
        cwd: FsPath | None = None,
        shell: bool = False,
        check: bool = False,
        verbose: bool = False,
        input: STDIN = None,
        timeout: float | int | None = None,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
        dryrun: bool = False,
    ) -> Done:
        """Run the exe with the given args; see [do][shellfish.exe.ExeABC.do]

        Returns:
            [Done][shellfish.done.Done] object for the finished process

        """
        return self._do(
            *popenargs,
            args=args,
            check=check,
            cwd=cwd,
            dryrun=dryrun,
            env=env,
            extenv=extenv,
            input=input,
            ok_code=ok_code,
            shell=shell,
            timeout=timeout,
            verbose=verbose,
        )


class ExeAsync(ExeABC):
    """Awaitable wrapper around an executable

    Same configuration as [Exe][shellfish.exe.Exe], but calling an instance
    returns a coroutine:

    ```python
    git = ExeAsync("git")
    done = await git("status", "--porcelain")
    ```
    """

    async def __call__(
        self,
        *popenargs: PopenArgs,
        args: PopenArgs | None = None,
        check: bool = False,
        cwd: str | None = None,
        dryrun: bool = False,
        env: dict[str, str] | None = None,
        extenv: bool = True,
        input: STDIN = None,
        loop: Any | None = None,
        shell: bool = False,
        timeout: float | int | None = None,
        verbose: bool = False,
    ) -> Done:
        """Run the exe asynchronously; see [do_async][shellfish.exe.ExeABC.do_async]

        Returns:
            [Done][shellfish.done.Done] object for the finished process

        """
        return await self._do_async(
            *popenargs,
            args=args,
            check=check,
            cwd=cwd,
            dryrun=dryrun,
            env=env,
            extenv=extenv,
            input=input,
            loop=loop,
            shell=shell,
            timeout=timeout,
            verbose=verbose,
        )
