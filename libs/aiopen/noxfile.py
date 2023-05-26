# -*- coding: utf-8 -*-
import os

from os import path

import nox


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os.name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

PWD = path.abspath(path.dirname(__file__))
PKG_DIRPATH = path.join(PWD, "aiopen")
TESTS_DIRPATH = path.join(PWD, "tests")

VENV_BACKEND = None if is_win() else "conda"

REUSE_TEST_ENVS = True


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session: nox.Session) -> None:
    session.install("flake8", "flake8-print", "flake8-eradicate")
    session.run("flake8", PKG_DIRPATH)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def base_test(session: nox.Session) -> None:
    session.install("pytest")
    session.run(
        "pytest",
        "-m",
        "not optdeps",
        TESTS_DIRPATH,
    )
