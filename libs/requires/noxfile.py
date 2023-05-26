# -*- coding: utf-8 -*-
from os import environ, name, path

import nox


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

IS_GITLAB_CI = "GITLAB_CI" in environ
PWD = path.abspath(path.dirname(__file__))
PKG_DIRPATH = path.join(PWD, "requires")
TESTS_DIRPATH = path.join(PWD, "tests")

VENV_BACKEND = None if is_win() else "conda"

REUSE_TEST_ENVS = True


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session: nox.Session) -> None:
    session.install("flake8")
    session.install("flake8-print")
    session.install("flake8-eradicate")
    session.run("flake8", PKG_DIRPATH)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pytest(session: nox.Session) -> None:
    session.install("pytest")
    session.install("funkify")
    session.run(
        "pytest",
        "-m",
        "not optdeps",
        TESTS_DIRPATH,
    )
