# -*- coding: utf-8 -*-
import os

from os import path
from shutil import which

import nox


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os.name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

IS_GITLAB_CI = "GITLAB_CI" in os.environ
IS_GITHUB_CI = "CI" in os.environ and os.environ.get("CI") == "true"
PWD = path.abspath(path.dirname(__file__))
JSONBOURNE_PKG_DIRPATH = path.join(PWD, "jsonbourne")
TESTS_DIRPATH = path.join(PWD, "tests")

VENV_BACKEND = None if (is_win() or IS_GITHUB_CI or not which("conda")) else "conda"

REUSE_TEST_ENVS = True


#############
### UTILS ###
#############
def latest_wheel() -> str:
    wheels = sorted([el for el in os.listdir("dist") if el.endswith(".whl")])
    latest = wheels[-1]
    return latest


def _get_jsonbourne_version() -> str:
    _filepath = path.join(PWD, "pyproject.toml")
    version = (
        [line for line in open(_filepath).read().split("\n") if "version" in line][0]
        .replace("version = ", "")
        .strip('"')
    )
    return version


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session: nox.Session) -> None:
    session.install("flake8")
    session.install("flake8-print")
    session.install("flake8-eradicate")
    session.run("flake8", JSONBOURNE_PKG_DIRPATH)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake_tests(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8", TESTS_DIRPATH)


def install_common_test_deps(session: nox.Session) -> None:
    session.install("pytest", "pytest-cov", "coverage", "xtyping", "jsonc2json")


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pytest(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "not optdeps",
        TESTS_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pydantic_test(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.install("pydantic<2", "fastapi", "httpx", "orjson")
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "basic or pydantic",
        "--doctest-modules",
        TESTS_DIRPATH,
        JSONBOURNE_PKG_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def attrs_test(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.install("attrs")
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "basic or attrs",
        TESTS_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def jsonlibs_test(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.install("orjson")
    session.install("python-rapidjson")
    session.install("numpy")
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "jsonlibs",
        TESTS_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def orjson_test(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.install("orjson")
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "basic or orjson",
        TESTS_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def rapidjson_test(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.install("python-rapidjson")
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-m",
        "rapidjson or basic",
        TESTS_DIRPATH,
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def coverage_report(session: nox.Session) -> None:
    install_common_test_deps(session)
    session.run("coverage", "report")
