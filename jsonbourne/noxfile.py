# -*- coding: utf-8 -*-
from os import path

import os
import nox


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os.name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

IS_GITLAB_CI = "GITLAB_CI" in os.environ
PWD = path.abspath(path.dirname(__file__))
JSONBOURNE_PKG_DIRPATH = path.join(PWD, "jsonbourne")
TESTS_DIRPATH = path.join(PWD, "tests")

VENV_BACKEND = None if is_win() else "conda"

REUSE_TEST_ENVS = IS_GITLAB_CI or True

#############
### UTILS ###
#############
def latest_wheel():
    wheels = sorted([el for el in os.listdir("dist") if el.endswith(".whl")])
    latest = wheels[-1]
    return latest


def _get_session_python_site_packages_dir(session):
    try:
        site_packages_dir = session._runner._site_packages_dir
    except AttributeError:
        old_install_only_value = session._runner.global_config.install_only
        try:
            # Force install only to be false for the following chunk of code
            # For additional information as to why see:
            #   https://github.com/theacodes/nox/pull/181
            session._runner.global_config.install_only = False
            site_packages_dir = session.run(
                "python",
                "-c"
                "import sys; "
                "from distutils.sysconfig import get_python_lib; "
                "sys.stdout.write(get_python_lib())",
                silent=True,
                log=False,
                )
            session._runner._site_packages_dir = site_packages_dir
        finally:
            session._runner.global_config.install_only = old_install_only_value
    return site_packages_dir


def _get_dgpy_site_packages_jsonbourne_location(session):
    return path.join(_get_session_python_site_packages_dir(session), "jsonbourne")


def _get_jsonbourne_version() -> str:
    _filepath = path.join(PWD, "pyproject.toml")
    version = (
        [l for l in open(_filepath).read().split("\n") if "version" in l][0]
            .replace("version = ", "")
            .strip('"')
    )
    return version


################
##### DGPY #####
################
@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session):
    session.install("flake8")
    session.install("flake8-print")
    session.install("flake8-eradicate")
    session.run("flake8", JSONBOURNE_PKG_DIRPATH)


# @nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
# def flake_tests(session):
#     session.install("flake8")
#     session.run("flake8", TESTS_DIRPATH)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def base_test(session):
    session.install("pytest")
    session.run(
        "pytest",
        "-m",
        "not optdeps",
        TESTS_DIRPATH,
        )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pydantic_test(session):
    session.install("pytest")
    session.install("pydantic")
    session.install("orjson")
    session.run(
        "pytest",
        "-m",
        "basic or pydantic",
        "--doctest-modules",
        TESTS_DIRPATH,
        JSONBOURNE_PKG_DIRPATH,
        )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def attrs_test(session):
    session.install("pytest")
    session.install("attrs")
    session.run(
        "pytest",
        "-m",
        "basic or attrs",
        TESTS_DIRPATH,
        )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def jsonlibs_test(session):
    session.install("pytest")
    session.install("orjson")
    session.install("python-rapidjson")
    session.run(
        "pytest",
        "-m",
        "jsonlibs",
        TESTS_DIRPATH,
        )

@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def orjson_test(session):
    session.install("pytest")
    session.install("orjson")
    session.run(
        "pytest",
        "-m",
        "basic or orjson",
        TESTS_DIRPATH,
        )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def rapidjson_test(session):
    session.install("pytest")
    session.install("python-rapidjson")
    session.run(
        "pytest",
        "-m",
        "rapidjson or basic",
        TESTS_DIRPATH,
        )

### TODO: add orjson (maybe)
# @nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
# def orjson_test(session):
#     session.install("pytest")
#     session.install("orjson")
#     session.run(
#         "pytest",
#         "-m",
#         "orjson or basic",
#         "--doctest-modules",
#         TESTS_DIRPATH,
#         JSONBOURNE_PKG_DIRPATH,
#         )
