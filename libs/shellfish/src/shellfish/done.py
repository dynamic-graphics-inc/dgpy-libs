from __future__ import annotations

import signal
import sys

from functools import lru_cache
from pathlib import Path
from subprocess import CompletedProcess, SubprocessError
from typing import TYPE_CHECKING, Any, AnyStr, TypedDict

from pydantic import AliasChoices, Field

from jsonbourne import JSON
from shellfish import fs
from shellfish._pydantic import _ShellfishBaseModel

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
    "HrTime",
    "HrTimeDict",
)


class HrTimeDict(TypedDict):
    """High resolution time"""

    secs: int
    nanos: int


class HrTime(_ShellfishBaseModel):
    """High resolution time"""

    secs: int = Field(validation_alias=AliasChoices("sec", "secs", "s"))
    nanos: int = Field(validation_alias=AliasChoices("ns", "nsecs", "nanos"))

    @classmethod
    def from_seconds(cls, seconds: float) -> HrTime:
        """Return HrTime object from seconds

        Args:
            seconds (float): number of seconds

        Returns:
            HrTime object

        """
        _sec, _ns = divmod(int(seconds * 1_000_000_000), 1_000_000_000)
        return cls(secs=_sec, nanos=_ns)

    def hrdt_dict(self) -> HrTimeDict:
        return {
            "secs": self.secs,
            "nanos": self.nanos,
        }

    @property
    def sec(self) -> int:  # deprecated alias
        return self.secs

    @property
    def ns(self) -> int:  # deprecated alias
        return self.nanos


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
    hrdt: HrTimeDict | None
    stdin: str | None
    async_proc: bool
    verbose: bool


@lru_cache(maxsize=32)
def _pfmt_stdio(s: AnyStr) -> AnyStr:
    """Pretty format stdout/stderr strings"""
    # BYTES
    if isinstance(s, bytes):
        if not s:
            return b"b''"

        lines = s.splitlines(keepends=True)
        return (
            b"(\n"
            + b"\n".join(f"        {line!r},".encode() for line in lines)
            + b"\n    )"
        )
    # STR
    if not s:
        return "''"
    lines = s.splitlines(keepends=True)
    return "(\n" + "\n".join(f"        {line!r}," for line in lines) + "\n    )"


class Done(_ShellfishBaseModel):
    """Completed subprocess"""

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    ti: float
    tf: float
    dt: float
    hrdt: HrTime | None = None
    stdin: str | None = None
    async_proc: bool = False
    dryrun: bool = Field(False)
    verbose: bool = Field(False, exclude=True)

    def __post_init__(self) -> None:
        """Write the stdout/stdout to sys.stdout/sys.stderr post object init"""
        if self.verbose:
            self.sys_print()

    def model_post_init(self, _context: Any) -> None:
        self.__post_init__()

    def __str__(self) -> str:
        return "\n".join((
            "Done(",
            f"    args={self.args},",
            f"    returncode={self.returncode},",
            f"    stdout={self.stdout!r},",
            f"    stderr={self.stderr!r},",
            f"    ti={self.ti},",
            f"    tf={self.tf},",
            f"    dt={self.dt},",
            f"    hrdt={self.hrdt_dict() if self.hrdt else HrTime.from_seconds(seconds=self.dt).hrdt_dict()},",
            f"    stdin={self.stdin!r},",
            f"    async_proc={self.async_proc},",
            f"    verbose={self.verbose},",
            f"    dryrun={self.dryrun},",
            ")",
        ))

    def __repr__(self) -> str:
        return " ".join((
            f"Done(args={self.args},",
            f"returncode={self.returncode},",
            f"stdout={self.stdout!r},",
            f"stderr={self.stderr!r},",
            f"ti={self.ti},",
            f"tf={self.tf},",
            f"dt={self.dt},",
            f"hrdt={self.hrdt_dict() if self.hrdt else HrTime.from_seconds(seconds=self.dt).hrdt_dict()},",
            f"stdin={self.stdin!r},",
            f"async_proc={self.async_proc},",
            f"verbose={self.verbose},",
            f"dryrun={self.dryrun})",
        ))

    def hrdt_dict(self) -> HrTimeDict:
        if self.hrdt:
            return self.hrdt.hrdt_dict()
        return HrTime.from_seconds(seconds=self.dt).hrdt_dict()

    def stdout_lines(self, *, keepends: bool = False) -> list[str]:
        return self.stdout.splitlines(keepends=keepends)

    def stderr_lines(self, *, keepends: bool = False) -> list[str]:
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

    def _error(self) -> DoneError:
        """Returns a CalledProcessError object"""
        return DoneError(done=self)

    def check(
        self,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
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
        fs.write_bytes(Path(filepath), self.stdout.encode("utf-8"), append=append)

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
        fs.write_bytes(Path(filepath), self.stderr.encode("utf-8"), append=append)

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
        self, *, jsonc: bool = False, jsonl: bool = False, ndjson: bool = False
    ) -> Any:
        """Return json parsed stdout"""
        return JSON.loads(self.stdout, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse_stderr(
        self, *, jsonc: bool = False, jsonl: bool = False, ndjson: bool = False
    ) -> Any:
        """Return json parsed stderr"""
        return JSON.loads(self.stderr, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse(
        self,
        *,
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
        *,
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
