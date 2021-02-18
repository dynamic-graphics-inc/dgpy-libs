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

IS_GITLAB_CI = "GITLAB_CI" in os.environ
PWD = path.abspath(path.dirname(__file__))
PKG_DIRPATH = path.join(PWD, "xtyping")
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


def _get_package_site_packages_location(session):
    return path.join(_get_session_python_site_packages_dir(session), "funkify")


def _get_funkify_version() -> str:
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
    session.run("flake8", PKG_DIRPATH)


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
def gen(session):
    from xtyping import _xtyping

    session.install("black", "isort")

    import_from_xtyping = [*_xtyping.__typing__, *_xtyping.__xtyping__]

    xtyping_internal_imports = [
        f"from xtyping._xtyping import {el}" for el in sorted(import_from_xtyping)
    ]

    init_lines = [
        "# -*- coding: utf-8 -*-",
        '"""xtyping ~ extended typing"""\n',
        "from xtyping._meta import __version__",
        "from xtyping import _xtyping as xt",
        *xtyping_internal_imports,
        "",
        "__all__ = [",
        *[
            "    {}".format(el)
            for el in [
                "'__version__',",
                "'xt',",
                *["'{}',".format(el) for el in sorted(import_from_xtyping)],
            ]
        ],
        "]",
    ]
    init_filepath = path.join(PWD, "xtyping", "__init__.py")
    with open(path.join(PWD, "xtyping", "__init__.py"), "w") as f:
        f.write("\n".join(init_lines))

    session.run("isort", "--sp", "../../pyproject.toml", init_filepath)
    session.run("black", "-S", "--config", "../../pyproject.toml", "-S", "xtyping")
    # isort = isort --sp pyproject.toml libs


#     '''
#     isort = isort --sp pyproject.toml libs
# black = black -S --config pyproject.toml -l 88 libs
# '''
