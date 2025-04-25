# -*- coding: utf-8 -*-
from __future__ import annotations

from concurrent.futures.thread import ThreadPoolExecutor
from queue import Empty, Queue
from subprocess import PIPE, Popen, TimeoutExpired
from time import time
from typing import TYPE_CHECKING

from shellfish.fs import Stdio

if TYPE_CHECKING:
    from xtyping import IO, Any, AnyStr, Iterable, Optional, Tuple

__all__ = ("popen_gen", "popen_pipes_gen")


def _enqueue_output(
    fileio: IO[AnyStr],
    queue: Queue[AnyStr],
    block: bool = True,
) -> None:
    while True:
        line = fileio.readline()
        if line:
            queue.put(line, block=block)
        else:
            break


def _enqueue_output_iter_readline(
    fileio: IO[AnyStr], queue: Queue[AnyStr], block: bool = True
) -> None:
    for line in iter(fileio.readline, ""):
        queue.put(line, block=block)
    fileio.close()


def popen_pipes_gen(
    proc: Popen[AnyStr], timeout: Optional[float] = None
) -> Iterable[Tuple[Stdio, str]]:
    """Yield stdout and stderr lines from a subprocess

    Args:
        proc (Popen): Popen process
        timeout (Optional[float], optional): Timeout in seconds. Defaults to None.

    Yields:
        Tuple[Stdio, str]: Tuples with stdio enum marker followed by a string

    Raises:
        ValueError: if proc is not Popen or proc.stdout or proc.stderr is None

    """
    if not isinstance(proc, Popen):
        raise ValueError("proc must be a Popen object")
    _raise_err = False
    if proc.stdout is not None and proc.stderr is not None:
        ti = time()
        with ThreadPoolExecutor(2) as pool:
            q_stdout: Queue[AnyStr] = Queue()
            q_stderr: Queue[AnyStr] = Queue()
            _block = True
            stdout_future = pool.submit(
                _enqueue_output_iter_readline, proc.stdout, q_stdout, _block
            )
            stderr_future = pool.submit(
                _enqueue_output_iter_readline, proc.stderr, q_stderr, _block
            )
            while proc.poll() is None:
                try:
                    yield Stdio.stdout, q_stdout.get_nowait()
                except Empty:
                    pass
                try:
                    yield Stdio.stderr, q_stderr.get_nowait()
                except Empty:
                    pass
                if timeout is not None and time() - ti > timeout:
                    _raise_err = True
                    stdout_future.cancel()
                    stderr_future.cancel()
                    pool.shutdown(wait=False)
                    break
        if _raise_err and timeout is not None:
            proc.terminate()
            raise TimeoutExpired(proc.args, timeout, output=None, stderr=None)

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
    with Popen(*popenargs, **popenkwargs, stdout=PIPE, stderr=PIPE, text=True) as proc:  # type: ignore[call-overload]
        yield from popen_pipes_gen(proc)
