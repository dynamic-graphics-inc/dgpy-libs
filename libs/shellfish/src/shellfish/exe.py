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
    "ExeAsync",
)

TExe = TypeVar("TExe", bound="ExeABC")


@dataclass
class ExeConfig:
    cmd: str
    subcmd: tuple[str, ...] | None = None
    abspath: str | None = None
    env: dict[str, str] | None = None
    cwd: str | None = None
    shell: bool = False
    verbose: bool = False
    timeout: float | int | None = None
    ok_code: int | set[int] = field(default_factory=lambda: {0})
    check: bool = False


class ExeABC:
    cmd: str
    subcmd: tuple[str, ...] | None = None

    abspath: str | None = None
    env: dict[str, str] | None = None
    cwd: FsPath | None = None
    shell: bool = False
    verbose: bool = False
    timeout: float | int | None = None
    ok_code: int | set[int] = 0
    check: bool = False

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
        """Post-initialization"""

    @classmethod
    def _from_exe_config(cls: type[TExe], config: ExeConfig) -> TExe:
        """Return a new instance from the config"""
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
        """Return the config"""
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
        """Return the path to the exe"""
        if self.abspath is not None:
            return self.abspath
        _abspath = sh.which(self.cmd)
        if _abspath is None:
            raise FileNotFoundError(f"{self.cmd} not found")
        self.abspath = _abspath
        return self.abspath

    def which(self) -> str:
        """Return the path to the exe"""
        return self._which()

    def _unredundify(
        self,
        popenargs: tuple[PopenArgs, ...],
        args: PopenArgs | None = None,
    ) -> tuple[str, ...]:
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
