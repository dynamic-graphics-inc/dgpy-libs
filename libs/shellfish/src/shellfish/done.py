"""Done ~ completed subprocess results"""

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
    """High resolution time as a typed-dict; see [HrTime][shellfish.done.HrTime]"""

    secs: int
    """Whole seconds"""
    nanos: int
    """Nanoseconds remainder (0 <= nanos < 1_000_000_000)"""


class HrTime(_ShellfishBaseModel):
    """High resolution time split into whole seconds and nanoseconds

    Examples:
        >>> HrTime.from_seconds(1.5)
        HrTime(secs=1, nanos=500000000)
        >>> HrTime.from_seconds(1.5).hrdt_dict()
        {'secs': 1, 'nanos': 500000000}

    """

    secs: int = Field(validation_alias=AliasChoices("sec", "secs", "s"))
    """Whole seconds"""
    nanos: int = Field(validation_alias=AliasChoices("ns", "nsecs", "nanos"))
    """Nanoseconds remainder (0 <= nanos < 1_000_000_000)"""

    @classmethod
    def from_seconds(cls, seconds: float) -> HrTime:
        """Return HrTime object from seconds

        Args:
            seconds: number of seconds

        Returns:
            HrTime object for the given number of seconds

        """
        _sec, _ns = divmod(int(seconds * 1_000_000_000), 1_000_000_000)
        return cls(secs=_sec, nanos=_ns)

    def hrdt_dict(self) -> HrTimeDict:
        """Return this HrTime as a typed-dict"""
        return {
            "secs": self.secs,
            "nanos": self.nanos,
        }

    @property
    def sec(self) -> int:  # deprecated alias
        """Deprecated alias for `secs`"""
        return self.secs

    @property
    def ns(self) -> int:  # deprecated alias
        """Deprecated alias for `nanos`"""
        return self.nanos


class DoneError(SubprocessError):
    r"""Error raised when a process returns a non-zero/not-ok exit status

    Raised by [Done.check][shellfish.done.Done.check].

    Examples:
        >>> done = Done(
        ...     args=["sh", "-c", "exit 1"],
        ...     returncode=1,
        ...     stdout="",
        ...     stderr="uh oh\n",
        ...     ti=0.0,
        ...     tf=0.1,
        ...     dt=0.1,
        ... )
        >>> try:
        ...     done.check()
        ... except DoneError as e:
        ...     (e.returncode, e.cmd, e.stderr)
        (1, ['sh', '-c', 'exit 1'], 'uh oh\n')

    """

    done: Done
    """The [Done][shellfish.done.Done] object that produced this error"""
    returncode: int
    """Exit status of the process"""
    stdout: str
    """Standard output (stdout) of the process"""
    stderr: str
    """Standard error (stderr) of the process"""
    cmd: list[str]
    """Command args the process was run with"""

    def __init__(self, done: Done) -> None:
        """Create a DoneError from a `Done` object

        Args:
            done: Done object with a non-zero/not-ok returncode

        """
        self.returncode = done.returncode
        self.cmd = done.args
        self.stderr = done.stderr
        self.stdout = done.stdout
        self.done = done

    def error_msg(self) -> str:
        """Return the error message string for this error's returncode"""
        if self.returncode and self.returncode < 0:
            try:
                return f"Command '{self.cmd}' died with {signal.Signals(-self.returncode)!r}."
            except ValueError:
                return f"Command '{self.cmd}' died with unknown signal {-self.returncode:d}."
        return (
            f"Command '{self.cmd}' returned non-zero exit status {self.returncode:d}."
        )

    def __str__(self) -> str:
        """Return the error message followed by the `Done` object

        Returns:
            str: Error message and the `Done` object for the subprocess

        """
        return f"{self.error_msg()}\n{self.done}"

    @property
    def output(self) -> str:
        """Alias for `stdout`; mirrors `subprocess.CalledProcessError.output`"""
        return self.stdout

    @output.setter
    def output(self, value: str) -> None:
        self.stdout = value


class DoneDict(TypedDict):
    """Completed subprocess as a typed-dict; see [Done][shellfish.done.Done]"""

    args: list[str]
    """Command args the process was run with"""
    returncode: int
    """Exit status of the process"""
    stdout: str
    """Standard output (stdout) of the process"""
    stderr: str
    """Standard error (stderr) of the process"""
    ti: float
    """Time the process started (seconds since epoch)"""
    tf: float
    """Time the process finished (seconds since epoch)"""
    dt: float
    """Time the process took to run (seconds; `tf - ti`)"""
    hrdt: HrTimeDict | None
    """High resolution `dt`, if the runner provided one"""
    stdin: str | None
    """Standard input (stdin) written to the process, if any"""
    async_proc: bool
    """True if the process was run asynchronously"""
    verbose: bool
    """True if stdout/stderr were echoed to the parent process' stdout/stderr"""


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
    r"""Completed subprocess

    Returned by [shellfish.sh.do][] (and friends) once a process has finished.

    Examples:
        >>> done = Done(
        ...     args=["echo", "hello"],
        ...     returncode=0,
        ...     stdout="hello\nworld\n",
        ...     stderr="",
        ...     ti=0.0,
        ...     tf=0.5,
        ...     dt=0.5,
        ... )
        >>> done.returncode
        0
        >>> done.lines
        ['hello', 'world']
        >>> done.grep("world")
        ['world']
        >>> done.check()  # does not raise; returncode is 0

    """

    args: list[str]
    """Command args the process was run with"""
    returncode: int
    """Exit status of the process"""
    stdout: str
    """Standard output (stdout) of the process"""
    stderr: str
    """Standard error (stderr) of the process"""
    ti: float
    """Time the process started (seconds since epoch)"""
    tf: float
    """Time the process finished (seconds since epoch)"""
    dt: float
    """Time the process took to run (seconds; `tf - ti`)"""
    hrdt: HrTime | None = None
    """High resolution `dt`, if the runner provided one"""
    stdin: str | None = None
    """Standard input (stdin) written to the process, if any"""
    async_proc: bool = False
    """True if the process was run asynchronously"""
    dryrun: bool = Field(False)
    """True if the process was not actually run (dryrun)"""
    verbose: bool = Field(False, exclude=True)
    """Echo stdout/stderr to the parent process on init; excluded from dumps"""

    def __post_init__(self) -> None:
        """Write stdout/stderr to sys.stdout/sys.stderr post object init"""
        if self.verbose:
            self.sys_print()

    def model_post_init(self, _context: Any) -> None:
        """Pydantic post-init hook; defers to `__post_init__`"""
        self.__post_init__()

    def __str__(self) -> str:
        """Return a multi-line string representation of this Done object"""
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
        """Return a single-line string representation of this Done object"""
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
        """Return the high resolution run-time as a typed-dict

        Falls back to converting `dt` to [HrTime][shellfish.done.HrTime] when the
        runner did not provide an `hrdt`.
        """
        if self.hrdt:
            return self.hrdt.hrdt_dict()
        return HrTime.from_seconds(seconds=self.dt).hrdt_dict()

    def stdout_lines(self, *, keepends: bool = False) -> list[str]:
        """Return stdout split into lines

        Args:
            keepends: Keep the line-ending characters on each line

        Returns:
            List of stdout lines

        """
        return self.stdout.splitlines(keepends=keepends)

    def stderr_lines(self, *, keepends: bool = False) -> list[str]:
        """Return stderr split into lines

        Args:
            keepends: Keep the line-ending characters on each line

        Returns:
            List of stderr lines

        """
        return self.stderr.splitlines(keepends=keepends)

    @property
    def lines(self) -> list[str]:
        """Stdout split into lines without line-endings"""
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
        """Return a DoneError object for this Done object"""
        return DoneError(done=self)

    def check(
        self,
        ok_code: int | list[int] | tuple[int, ...] | set[int] = 0,
    ) -> None:
        """Check returncode and stderr

        Args:
            ok_code: Return code (or collection of return codes) considered ok

        Raises:
            DoneError: If the return code is not ok

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
            append: Append to the file instead of overwriting it

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
            append: Append to the file instead of overwriting it

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
        """Return json parsed stdout

        Args:
            jsonc: Parse stdout as jsonc (json with comments)
            jsonl: Parse stdout as jsonl (json-lines)
            ndjson: Parse stdout as ndjson (newline delimited json)

        Returns:
            The parsed stdout

        """
        return JSON.loads(self.stdout, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse_stderr(
        self, *, jsonc: bool = False, jsonl: bool = False, ndjson: bool = False
    ) -> Any:
        """Return json parsed stderr

        Args:
            jsonc: Parse stderr as jsonc (json with comments)
            jsonl: Parse stderr as jsonl (json-lines)
            ndjson: Parse stderr as ndjson (newline delimited json)

        Returns:
            The parsed stderr

        """
        return JSON.loads(self.stderr, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def json_parse(
        self,
        *,
        stderr: bool = False,
        jsonc: bool = False,
        jsonl: bool = False,
        ndjson: bool = False,
    ) -> Any:
        """Return json parsed stdout (or stderr)

        Args:
            stderr: Parse stderr instead of stdout
            jsonc: Parse as jsonc (json with comments)
            jsonl: Parse as jsonl (json-lines)
            ndjson: Parse as ndjson (newline delimited json)

        Returns:
            The parsed stdout, or the parsed stderr if `stderr` is True

        """
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
        """Alias for [json_parse][shellfish.done.Done.json_parse]

        (bc I keep flip-flopping the fn name)

        Args:
            stderr: Parse stderr instead of stdout
            jsonc: Parse as jsonc (json with comments)
            jsonl: Parse as jsonl (json-lines)
            ndjson: Parse as ndjson (newline delimited json)

        Returns:
            The parsed stdout, or the parsed stderr if `stderr` is True

        """
        return self.json_parse(stderr=stderr, jsonc=jsonc, jsonl=jsonl, ndjson=ndjson)

    def grep(self, string: str) -> list[str]:
        """Return lines in stdout that contain the given string

        Args:
            string: String to search for

        Returns:
            list[str]: List of strings of stdout lines containing the given
                search string

        """
        return [
            line for line in self.stdout.splitlines(keepends=False) if string in line
        ]
