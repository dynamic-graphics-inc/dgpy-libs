# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from os import path
from shutil import which

import nox

LIBS = (
    "aiopen",
    "asyncify",
    "dgpylibs",
    "dgpytest",
    "fmts",
    "funkify",
    "h5",
    "jsonbourne",
    "lager",
    "listless",
    "requires",
    "shellfish",
    "xtyping",
)


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os.name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

IS_GITLAB_CI = "GITLAB_CI" in os.environ
IS_GITHUB_CI = "CI" in os.environ and os.environ["CI"] == "true"
REUSE_TEST_ENVS = True
PWD = path.abspath(path.dirname(__file__))
LIBS_DIR = path.join(PWD, "libs")

VENV_BACKEND = None if is_win() or IS_GITHUB_CI or not which("conda") else "conda"
LIB_DIRS = {
    el: path.join(LIBS_DIR, el)
    for el in os.listdir(LIBS_DIR)
    if el[0] != "." and el in LIBS
}
SOURCE_DIRS = {el: path.join(LIBS_DIR, el, "src", el) for el in LIBS}
TESTS_DIRS = {el: path.join(LIBS_DIR, el, "tests") for el in LIB_DIRS}


# #############
# ### UTILS ###
# #############


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def pipc(session: nox.Session) -> None:
    session.install("pip-tools")
    reqs_ini = (
        "dev.in",
        "docs.in",
    )
    for reqs_file in reqs_ini:
        output_filepath = path.join(
            PWD, "requirements", reqs_file.replace(".in", ".txt")
        )

        session.run(
            "uv",
            "pip",
            "compile",
            "-o",
            output_filepath,
            path.join(PWD, "requirements", reqs_file),
        )


def _mypy(session: nox.Session) -> None:
    session.install(
        "-U",
        "mypy",
        "typing-extensions",
        "pydantic",
        "pydantic_core",
        "anyio",
        "pytest",
        "nox",
    )
    session.install("orjson", "types-orjson", "fastapi", "click==8.1.3")
    session.run("mypy", "--version")
    session.run(
        "mypy",
        "--show-error-codes",
        "--config-file",
        "./pyproject.toml",
        *list(SOURCE_DIRS.values()),
    )

    for lib in LIBS:
        noxfile_path = path.join("libs", lib, "noxfile.py")
        args = [
            "mypy",
            "--show-error-codes",
            "--config-file",
            "./pyproject.toml",
            *list(SOURCE_DIRS.values()),
            path.join("libs", lib, "tests"),
        ]
        if path.exists(noxfile_path):
            args.append(noxfile_path)
        session.run(*args)


def _ruff(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "--version")
    session.run("ruff", "check", ".")


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mypy(session: nox.Session) -> None:
    _mypy(session)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def lint(session: nox.Session) -> None:
    _mypy(session)


ruffext = """

[tool.ruff]
extend = "../../pyproject.toml"
"""


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def dev(session: nox.Session) -> None:
    from pprint import pprint

    import tomllib

    for libname, dirpath in LIB_DIRS.items():
        echo(libname, dirpath)
        pyproject_toml_fspath = path.join(dirpath, "pyproject.toml")
        with open(pyproject_toml_fspath) as f:
            pyproject_toml_str = f.read().rstrip("\n")

        data = tomllib.loads(pyproject_toml_str)
        pprint(data)


def _pkg_entry_point(pkg_name: str) -> str:
    return "\n".join(
        [
            "# -*- coding: utf-8 -*-",
            f'"""pkg entry ~ `python -m {pkg_name}`"""',
            "import sys",
            "",
            f"from {pkg_name}._meta import __pkgroot__, __title__, __version__",
            "",
            "sys.stdout.write(",
            '    f"package: {__title__}\\nversion: {__version__}\\npkgroot: {__pkgroot__}\\n"',
            ")",
            "",
        ]
    )


echo = print


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def update_metadata(session: nox.Session) -> None:
    import tomllib

    libs2update = {k: v for k, v in LIB_DIRS.items() if k not in {"dgpylibs"}}
    for libname, dirpath in libs2update.items():
        echo(libname, dirpath)
        with open(path.join(dirpath, "pyproject.toml")) as f:
            pyproject_toml_str = f.read()
        data = tomllib.loads(pyproject_toml_str)
        echo("____________________________")
        poetry_metadata = data["tool"]["poetry"]
        assert "name" in poetry_metadata and poetry_metadata["name"] == libname
        assert "version" in poetry_metadata
        assert "description" in poetry_metadata and poetry_metadata["description"] != ""
        metadata_file_lines = [
            "# -*- coding: utf-8 -*-",
            '"""Package metadata/info"""\n',
            '__all__ = ("__title__", "__description__", "__pkgroot__", "__version__")',
            '__title__ = "{}"'.format(poetry_metadata["name"]),
            '__description__ = "{}"'.format(poetry_metadata["description"]),
            '__pkgroot__ = __file__.replace("_meta.py", "").rstrip("/\\\\")',
            '__version__ = "{}"'.format(poetry_metadata["version"]),
        ]
        metadata_file_string = "\n".join(metadata_file_lines).strip("\n") + "\n"

        deprecated_meta_file_lines = [
            "# -*- coding: utf-8 -*-",
            '"""Package metadata/info"""',
            "import warnings",
            "",
            f"from {libname}.__about__ import __description__, __pkgroot__, __title__, __version__",
            "",
            "warnings.warn(",
            f'    "{libname}._meta is deprecated, use {libname}.__about__ instead",',
            "    DeprecationWarning,",
            "    stacklevel=2,",
            ")",
            "",
            '__all__ = ("__title__", "__description__", "__pkgroot__", "__version__")',
            "",
        ]
        # check that is valid python...
        exec(metadata_file_string)
        echo("~~~")
        echo(metadata_file_string)
        echo("~~~")
        meta_filepath = path.join(dirpath, libname, "_meta.py")
        metadata_filepath = path.join(dirpath, libname, "__about__.py")
        with open(metadata_filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(metadata_file_string)

        with open(meta_filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(deprecated_meta_file_lines))


def _install_mkdocs_deps(session: nox.Session) -> None:
    session.install(
        "mkdocs",  # docs!
        "mkdocs-material",  # material theme
        "mkdocs-jupyter",  # rendering jupyter notebooks
        "mkdocstrings[python]",  # render docstrings 2 markdown
        "markdown-callouts",  # callouts
        "black",  # code formatting for mkdocstrings-signatures
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs_serve(session: nox.Session) -> None:
    _install_mkdocs_deps(session)
    session.run("mkdocs", "serve")


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs(session: nox.Session) -> None:
    _install_mkdocs_deps(session)
    session.run("mkdocs", "build")


@nox.session(reuse_venv=True)
def freeze(session: nox.Session) -> None:
    for lib in LIBS:
        session.install(lib)
    _freeze = session.run("pip", "freeze", "--local", "-l")
