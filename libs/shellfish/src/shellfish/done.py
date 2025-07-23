from __future__ import annotations

import signal
import sys

from pathlib import Path
from subprocess import CompletedProcess, SubprocessError
from typing import TYPE_CHECKING, Any, Optional, Union

from typing_extensions import TypedDict

from jsonbourne import JSON
from jsonbourne.pydantic import JsonBaseModel
from shellfish import fs

if TYPE_CHECKING:
    from shellfish._types import (
        STDIN as STDIN,
        FsPath as FsPath,
        PopenArg as PopenArg,
        PopenArgs as PopenArgs,
    )

__all__ = (
    "Done",
    "DoneDict",
    "DoneError",
    "DoneObj",
    "HrTime",
    "HrTimeDict",
    "HrTimeObj",
)


class HrTimeDict(TypedDict):
    """High resolution time"""

    sec: int
    ns: int


class HrTimeObj(TypedDict):
    """TODO: deprecate this in favor of HrTimeDict"""

    sec: int
    ns: int


class HrTime(JsonBaseModel):
    """High resolution time"""

    sec: int
    ns: int

    @classmethod
    def from_seconds(cls, seconds: float) -> HrTime:
        """Return HrTime object from seconds

        Args:
            seconds (float): number of seconds

        Returns:
            HrTime object

        """
        _sec, _ns = divmod(int(seconds * 1_000_000_000), 1_000_000_000)
        return cls(sec=_sec, ns=_ns)

    def hrdt_dict(self) -> HrTimeDict:
        return {
            "sec": self.sec,
            "ns": self.ns,
        }

    def hrdt_obj(self) -> HrTimeObj:
        return {
            "sec": self.sec,
            "ns": self.ns,
        }


class DoneError(SubprocessError):
    """Error raised when a process returns a non-zero/ok exit status

    Attributes:
        cmd (str): command that was run
        returncode (int): exit status of the process
        stdout (str): standard output (stdout) of the process
        stderr (str): standard error (stderr) of the process

    """

    done: Done
    returncode: int
    stdout: str
    stderr: str
    cmd: list[str]

    def __init__(self, done: Done) -> None:
        self.returncode = done.returncode
        self.cmd = done.args
        self.stderr = done.stderr
        self.stdout = done.stdout
        self.cmd = done.args
        self.done = done

    def error_msg(self) -> str:
        if self.returncode and self.returncode < 0:
            try:
                return f"Command '{self.cmd}' died with {signal.Signals(-self.returncode)!r}."
            except ValueError:
                return f"Command '{self.cmd}' died with unknown signal {-self.returncode:d}."
        return (
            f"Command '{self.cmd}' returned non-zero exit status {self.returncode:d}."
        )

    def __str__(self) -> str:
        return f"{self.error_msg()}\n{self.done}"

    @property
    def output(self) -> str:
        return self.stdout

    @output.setter
    def output(self, value: str) -> None:
        self.stdout = value


class DoneDict(TypedDict):
    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    ti: float
    tf: float
    dt: float
    hrdt: Optional[HrTimeDict]
    stdin: Optional[str]
    async_proc: bool
    verbose: bool


class DoneObj(TypedDict):
    """TODO: deprecate this in favor of DoneDict"""

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    ti: float
    tf: float
    dt: float
    hrdt: Optional[HrTimeObj]
    stdin: Optional[str]
    async_proc: bool
    verbose: bool


class Done(JsonBaseModel):
    """PRun => 'ProcessRun' for finished processes"""

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    ti: float
    tf: float
    dt: float
    hrdt: Optional[HrTime] = None
    stdin: Optional[str] = None
    async_proc: bool = False
    verbose: bool = False
    dryrun: bool = False

    def __post_init__(self) -> None:
        """Write the stdout/stdout to sys.stdout/sys.stderr post object init"""
        if self.verbose:
            self.sys_print()

    def hrdt_dict(self) -> HrTimeDict:
        if self.hrdt:
            return self.hrdt.hrdt_dict()
        return HrTime.from_seconds(seconds=self.dt).hrdt_dict()

    def hrdt_obj(self) -> HrTimeObj:
        if self.hrdt:
            return self.hrdt.hrdt_obj()
        return HrTime.from_seconds(seconds=self.dt).hrdt_obj()

    def stdout_lines(self, keepends: bool = False) -> list[str]:
        return self.stdout.splitlines(keepends=keepends)

    def stderr_lines(self, keepends: bool = False) -> list[str]:
        return self.stderr.splitlines(keepends=keepends)

    @property
    def lines(self) -> list[str]:
        return self.stdout_lines(keepends=False)

    def done_dict(self) -> DoneDict:
        """Return Done object as typed-dict"""
        return DoneDict(
            args=self.args,
            returncode=self.returncode,
            stdout=self.stdout,
            stderr=self.stderr,
            ti=self.ti,
            tf=self.tf,
            dt=self.dt,
            hrdt=self.hrdt_dict(),
            stdin=self.stdin,
            async_proc=self.async_proc,
            verbose=self.verbose,
        )

    def done_obj(self) -> DoneObj:
        """Return Done object typed dict"""
        return DoneObj(
            args=self.args,
            returncode=self.returncode,
            stdout=self.stdout,
            stderr=self.stderr,
            ti=self.ti,
            tf=self.tf,
            dt=self.dt,
            hrdt=self.hrdt_obj(),
            stdin=self.stdin,
            async_proc=self.async_proc,
            verbose=self.verbose,
        )

    def _error(self) -> DoneError:
        """Returns a CalledProcessError object"""
        return DoneError(done=self)

    def check(
        self,
        ok_code: Union[int, list[int], tuple[int, ...], set[int]] = 0,
    ) -> None:
        """Check returncode and stderr

        Raises:
            DoneError: If return code is non-zero and stderr is not None

        """
        if isinstance(ok_code, int):
            if self.returncode != ok_code and self.stderr:
                raise DoneError(done=self)
        else:
            if self.returncode not in ok_code:
                raise DoneError(done=self)

    def sys_print(self) -> None:
        """Write self.stdout to sys.stdout and self.stderr to sys.stderr"""
        sys.stdout.write(self.stdout)
        sys.stderr.write(self.stderr)

    def write_stdout(self, filepath: FsPath, *, append: bool = False) -> None:
        """Write stdout as a string to a fspath

        Args:
            filepath: Filepath to write stdout to
            append (bool): Flag to append to file or plain write to file

        """
        fs.write_str(Path(filepath), self.stdout, append=append)

    def completed_process(self) -> CompletedProcess[str]:
        """Return subprocess.CompletedProcess object"""
        return CompletedProcess(
            args=self.args,
            returncode=self.returncode,
            stdout=self.stdout,
            stderr=self.stderr,
        )

    def write_stderr(self, filepath: FsPath, *, append: bool = False) -> None:
        """Write stderr as a string to a fspath

        Args:
            filepath: Filepath of location to write stderr
            append (bool): Flag to append to file or plain write to file

        """
        fs.write_str(Path(filepath), self.stderr, append=append)

    def __gt__(self, filepath: FsPath) -> None:
        """Operator overload for writing a stdout to a fspath

        Args:
            filepath: Filepath to write stdout to

        """
        self.write_stdout(filepath)

    def __ge__(self, filepath: FsPath) -> Done:
        """Operator overload for writing stderr to fspath

        Args:
            filepath: Filepath of location to write stderr

        Returns:
            Done object; self

        """
        self.write_stderr(filepath)
        return self

    def __rshift__(self, filepath: FsPath) -> None:
        """Operator overload for appending stdout to fspath

        Args:
            filepath: Filepath to write stdout to

        """
        self.write_stdout(filepath, append=True)

    def __irshift__(self, filepath: FsPath) -> Done:
        """Operator overload for appending stderr to fspath

        Args:
            filepath: Filepath of location to write stderr

        Returns:
            Done object; self

        """
        self.write_stderr(filepath, append=True)
        return self

    def json_parse_stdout(
        self, jsonc: bool = False, jsonl: bool = False, ndjson: bool = False
    ) -> Any:
        """Return json parsed stdout"""
        return JSON.loads(self.stdout, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse_stderr(
        self, jsonc: bool = False, jsonl: bool = False, ndjson: bool = False
    ) -> Any:
        """Return json parsed stderr"""
        return JSON.loads(self.stderr, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse(
        self,
        stderr: bool = False,
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
    ) -> Any:
        """Return json parsed stdout"""
        return (
            self.json_parse_stdout(jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)
            if not stderr
            else self.json_parse_stderr(jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)
        )

    def parse_json(
        self,
        stderr: bool = False,
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
    ) -> Any:
        """Return json parsed stdout (alias bc I keep flip-flopping the fn name)"""
        return self.json_parse(stderr=stderr, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def grep(self, string: str) -> list[str]:
        """Return lines in stdout that have

        Args:
            string (str): String to search for

        Returns:
            list[str]: List of strings of stdout lines containing the given
                search string

        """
        return [
            line for line in self.stdout.splitlines(keepends=False) if string in line
        ]
