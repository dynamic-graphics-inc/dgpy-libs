# -*- coding: utf-8 -*-

from __future__ import annotations

from os import name as os_name, path

import nox

from nox import Session


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os_name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

PWD = path.abspath(path.dirname(__file__))
PKG_DIRPATH = path.join(PWD, "dgpytest")
TESTS_DIRPATH = path.join(PWD, "tests")

VENV_BACKEND = None if is_win() else "conda"

REUSE_TEST_ENVS = True


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session: Session) -> None:
    session.install("flake8")
    session.install("flake8-print")
    session.install("flake8-eradicate")
    session.run("flake8", PKG_DIRPATH)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pytest(session: Session) -> None:
    session.install("pytest")
    session.run(
        "pytest",
        "-m",
        "not optdeps",
        TESTS_DIRPATH,
    )
