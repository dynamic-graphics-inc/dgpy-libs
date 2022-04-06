# -*- coding: utf-8 -*-
import os

from os import path
from shutil import which

import nox

LIBS = (
    "aiopen",
    "asyncify",
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
REUSE_TEST_ENVS = IS_GITLAB_CI or True
PWD = path.abspath(path.dirname(__file__))
LIBS_DIR = path.join(PWD, "libs")

VENV_BACKEND = None if is_win() or IS_GITHUB_CI or not which("conda") else "conda"
LIB_DIRS = {
    el: path.join(LIBS_DIR, el)
    for el in os.listdir(LIBS_DIR)
    if el[0] != "." and el in LIBS
}
SOURCE_DIRS = {el: path.join(LIBS_DIR, el, el) for el in LIBS}
TESTS_DIRS = {el: path.join(LIBS_DIR, el, "tests") for el in LIB_DIRS}


# #############
# ### UTILS ###
# #############


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


def _flake(session):
    # TODO add using the package "flake8-pytest-style"
    session.install(
        "flake8",
        "flake8-print",
        "flake8-eradicate",
        "flake8-comprehensions",
    )
    session.run("flake8", *[el for el in SOURCE_DIRS.values()])
    session.run("flake8", *[el for el in TESTS_DIRS.values()])


def _flake_w_pytest(session):
    # TODO add using the package "flake8-pytest-style"
    session.install(
        "flake8",
        "flake8-print",
        "flake8-eradicate",
        "flake8-comprehensions",
        "flake8-pytest-style",
    )
    session.run(
        "flake8",
        "--config",
        ".flake8",
        *[el for el in SOURCE_DIRS.values()],
    )
    session.run(
        "flake8",
        "--config",
        ".flake8",
        *[el for el in TESTS_DIRS.values()],
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session):
    _flake(session)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake_strict(session):
    _flake_w_pytest(session)


def _mypy(session):
    session.install("mypy", "typing-extensions", "pydantic", "anyio")
    session.install("orjson", "types-orjson", "fastapi")
    session.run('mypy', '--version')
    # session.run(
    #     'mypy',
    #     '--show-error-codes',
    #     '--config-file',
    #     './pyproject.toml',
    #     *[el for el in SOURCE_DIRS.values() if '.DS_Store' not in el],
    #     # *[el for el in TESTS_DIRS.values() if '.DS_Store' not in el],
    #     )

    # for lib in libs:
    #     session.run(
    #         'mypy',
    #         '--show-error-codes',
    #         '--config-file',
    #         './mypy.ini',
    #         *[el for el in SOURCE_DIRS.values() if '.DS_Store' not in el],
    #         path.join('libs', lib, 'tests')
    #         # *[el for el in TESTS_DIRS.values() if '.DS_Store' not in el],
    #         )

    session.run(
        "mypy",
        "--show-error-codes",
        "--config-file",
        # "./mypy.ini",
        "./pyproject.toml",
        *[el for el in SOURCE_DIRS.values()],
    )

    for lib in {
        el for el in LIBS if el not in {"aiopen", "shellfish", "jsonbourne", "requires"}
    }:

        session.run(
            "mypy",
            "--show-error-codes",
            "--config-file",
            "./pyproject.toml",
            *[el for el in SOURCE_DIRS.values() if ".DS_Store" not in el],
            path.join("libs", lib, "tests")
            # *[el for el in TESTS_DIRS.values() if '.DS_Store' not in el],
        )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mypy(session):
    _mypy(session)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def lint(session):
    _mypy(session)
    _flake(session)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def homepage(session):
    import toml

    # "# -*- coding: utf-8 -*-"
    for libname, dirpath in LIB_DIRS.items():
        print(libname, dirpath)
        pyproject_toml_fspath = path.join(dirpath, "pyproject.toml")
        with open(pyproject_toml_fspath) as f:
            pyproject_toml_str = f.read()
        data = toml.loads(pyproject_toml_str)
        print("____________________________")
        print("Package: {} ~ Dirpath: {}".format(libname, dirpath))
        poetry_metadata = data["tool"]["poetry"]
        lib_homepage = "https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/{}".format(
            libname
        )
        data["tool"]["poetry"] = poetry_metadata
        print(data)
        repository_line = (
            'repository = "https://github.com/dynamic-graphics-inc/dgpy-libs"'
        )
        edited = pyproject_toml_str.replace(
            repository_line, repository_line + '\nhomepage = "{}"'.format(lib_homepage)
        )
        print(edited)
        # with open(pyproject_toml_fspath, 'w') as f:
        #     f.write(edited)

        # with open(pyproject_toml_fspath, 'w') as f:
        #     f.write(toml.dumps(data))
        # # print(poetry_metadata)
        # assert "name" in poetry_metadata and poetry_metadata["name"] == libname
        # assert "version" in poetry_metadata
        # assert "description" in poetry_metadata and poetry_metadata["description"] != ""
        # metadata_file_lines = [
        #     "# -*- coding: utf-8 -*-",
        #     '"""Package metadata/info"""\n',
        #     "__title__ = '{}'".format(poetry_metadata["name"]),
        #     "__version__ = '{}'".format(poetry_metadata["version"]),
        #     "__description__ = '{}'".format(poetry_metadata["description"]),
        #     ]
        # metadata_file_string = "\n".join(metadata_file_lines).strip("\n") + "\n"
        #
        # # check that is valid python...
        # exec(metadata_file_string)
        # print('~~~')
        # print(metadata_file_string)
        # print('~~~')
        # metadata_filepath = path.join(dirpath, libname, '_meta.py')
        # with open(metadata_filepath, 'w') as f:
        #     f.write(metadata_file_string)


def _pkg_entry_point(pkg_name):
    return "\n".join(
        [
            "# -*- coding: utf-8 -*-",
            '"""pkg entry ~ `python -m {}`"""'.format(pkg_name),
            "import sys",
            "",
            "from {}._meta import __pkgroot__, __title__, __version__".format(pkg_name),
            "",
            "sys.stdout.write(",
            '    f"package: {__title__}\\nversion: {__version__}\\npkgroot: {__pkgroot__}\\n"',
            ")",
            "",
        ]
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def update_metadata(session):
    import toml

    # "# -*- coding: utf-8 -*-"
    for libname, dirpath in LIB_DIRS.items():
        print(libname, dirpath)
        with open(path.join(dirpath, "pyproject.toml")) as f:
            pyproject_toml_str = f.read()
        data = toml.loads(pyproject_toml_str)
        print("____________________________")
        poetry_metadata = data["tool"]["poetry"]
        # print(poetry_metadata)
        assert "name" in poetry_metadata and poetry_metadata["name"] == libname
        assert "version" in poetry_metadata
        assert "description" in poetry_metadata and poetry_metadata["description"] != ""
        metadata_file_lines = [
            "# -*- coding: utf-8 -*-",
            '"""Package metadata/info"""\n',
            '__title__ = "{}"'.format(poetry_metadata["name"]),
            '__description__ = "{}"'.format(poetry_metadata["description"]),
            '__pkgroot__ = __file__.replace("_meta.py", "").rstrip("/\\\\")',
            '__version__ = "{}"'.format(poetry_metadata["version"]),
        ]
        metadata_file_string = "\n".join(metadata_file_lines).strip("\n") + "\n"

        # check that is valid python...
        exec(metadata_file_string)
        print("~~~")
        print(metadata_file_string)
        print("~~~")
        metadata_filepath = path.join(dirpath, libname, "_meta.py")
        pkg_main_filepath = path.join(dirpath, libname, "__main__.py")
        with open(metadata_filepath, "w") as f:
            f.write(metadata_file_string)

        s = _pkg_entry_point(libname)
        if path.exists(pkg_main_filepath):
            with open(pkg_main_filepath, "r") as f:
                pkg_main_file_str = f.read()
            if pkg_main_file_str != s:
                print("updating __main__.py")
                with open(pkg_main_filepath, "w") as f:
                    f.write(s)
        else:
            print("creating __main__.py")
            with open(pkg_main_filepath, "w") as f:
                f.write(s)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs_serve(session):
    session.install("mkdocs")
    session.install("mkdocs-material")
    session.install("mkdocs-jupyter")
    session.install("mkdocstrings")
    session.run("mkdocs", "serve")


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs(session):
    session.install("mkdocs")
    session.install("mkdocs-material")
    session.install("mkdocs-jupyter")
    session.run("mkdocs", "build")


@nox.session(reuse_venv=True)
def freeze(session):
    for lib in LIBS:
        session.install(lib)
    _freeze = session.run("pip", "freeze", "--local", "-l")
