# -*- coding: utf-8 -*-
from __future__ import annotations

from concurrent.futures.thread import ThreadPoolExecutor
from queue import Empty, Queue
from subprocess import PIPE, Popen

from shellfish.fs import Stdio
from xtyping import IO, Any, AnyStr, Iterable, Tuple

__all__ = ("popen_gen",)


def _enqueue_output(fileio: IO[AnyStr], queue: Queue[AnyStr]) -> None:
    for line in iter(fileio.readline, ""):
        queue.put(line)
    fileio.close()


def _popen_pipes_gen(proc: Popen[AnyStr]) -> Iterable[Tuple[Stdio, str]]:
    """Yield stdout and stderr lines from a subprocess

    Args:
        proc (Popen): Popen process

    Yields:
        Tuple[Stdio, str]: Tuples with stdio enum marker followed by a string

    Raises:
        ValueError: if proc is not Popen or proc.stdout or proc.stderr is None

    """
    if not isinstance(proc, Popen):
        raise ValueError("proc must be a Popen object")
    if proc.stdout is not None and proc.stderr is not None:
        with ThreadPoolExecutor(2) as pool:
            q_stdout: Queue[AnyStr] = Queue()
            q_stderr: Queue[AnyStr] = Queue()
            pool.submit(_enqueue_output, proc.stdout, q_stdout)  # type: ignore[arg-type]
            pool.submit(_enqueue_output, proc.stderr, q_stderr)  # type: ignore[arg-type]
            while True:
                if proc.poll() is not None and q_stdout.empty() and q_stderr.empty():
                    break

                try:
                    yield Stdio.stdout, q_stdout.get_nowait()
                except Empty:
                    pass

                try:
                    yield Stdio.stderr, q_stderr.get_nowait()
                except Empty:
                    pass
    else:
        raise ValueError("proc.stdout and proc.stderr must be not None")


def popen_gen(*popenargs: Any, **popenkwargs: Any) -> Iterable[Tuple[Stdio, str]]:
    """Create and open a subprocess and yield tuples with stdout/stderr lines

    Args:
        *popenargs: Args to be passed to Popen
        **popenkwargs: Kwargs to be passed to Popen

    Yields:
        Tuple[str, str]: Tuples that are of the form ('stdout', stdout_line)
            or ('stderr', stderr_line) for the stdout and stderr lines for
            the subprocess created.

    """
    with Popen(
        *popenargs, **popenkwargs, stdout=PIPE, stderr=PIPE, text=True
    ) as proc:  # type: ignore[call-overload]
        yield from _popen_pipes_gen(proc)
