# -*- coding: utf-8 -*-
import os

from os import path
from shutil import which

import nox


libs = [
    'aiopen',
    'asyncify',
    'funkify',
    'h5',
    'jsonbourne',
    'lager',
    'requires',
    'shellfish',
    'xtyping',
]


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return os.name == "nt"


nox.options.envdir = ".nox_win" if is_win() else ".nox"

IS_GITLAB_CI = "GITLAB_CI" in os.environ
REUSE_TEST_ENVS = IS_GITLAB_CI or True
PWD = path.abspath(path.dirname(__file__))
LIBS_DIR = path.join(PWD, "libs")

VENV_BACKEND = None if is_win() or not which("conda") else "conda"
LIB_DIRS = {el: path.join(LIBS_DIR, el) for el in os.listdir(LIBS_DIR) if el[0] != '.' and el in libs}
SOURCE_DIRS = {el: path.join(LIBS_DIR, el, el) for el in libs}
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
    session.install("flake8")
    session.install("flake8-print")
    session.install("flake8-eradicate")
    session.run("flake8", *[el for el in SOURCE_DIRS.values() if '.DS_Store' not in el])
    session.run("flake8", *[el for el in TESTS_DIRS.values() if '.DS_Store' not in el])


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def flake(session):
    _flake(session)


def _mypy(session):
    session.install('mypy')
    session.install('typing-extensions')
    session.install('pydantic')
    session.install('orjson', 'types-orjson')
    session.run(
        'mypy',
        '--show-error-codes',
        '--config-file',
        './mypy.ini',
        # './pyproject.toml',
        *[el for el in SOURCE_DIRS.values() if '.DS_Store' not in el],
        # *[el for el in TESTS_DIRS.values() if '.DS_Store' not in el],
    )


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mypy(session):
    _mypy(session)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def update_metadata(session):
    import toml

    # "# -*- coding: utf-8 -*-"
    for libname, dirpath in LIB_DIRS.items():
        print(libname, dirpath)
        with open(path.join(dirpath, "pyproject.toml")) as f:
            pyproject_toml_str = f.read()
        data = toml.loads(pyproject_toml_str)
        print('____________________________')
        poetry_metadata = data["tool"]["poetry"]
        print(poetry_metadata)
        assert "name" in poetry_metadata and poetry_metadata["name"] == libname
        assert "version" in poetry_metadata
        assert "description" in poetry_metadata and poetry_metadata["description"] != ""
        assert "license" in poetry_metadata and poetry_metadata["license"] == "MIT"
        metadata_file_lines = [
            "# -*- coding: utf-8 -*-",
            '"""Package metadata/info"""\n',
            "__title__ = '{}'".format(poetry_metadata["name"]),
            "__version__ = '{}'".format(poetry_metadata["version"]),
            "__license__ = '{}'".format(poetry_metadata["license"]),
            "__description__ = '{}'".format(poetry_metadata["description"]),
        ]
        metadata_file_string = "\n".join(metadata_file_lines).strip("\n") + "\n"

        # check that is valid python...
        exec(metadata_file_string)
        print('~~~')
        print(metadata_file_string)
        print('~~~')
        metadata_filepath = path.join(dirpath, libname, '_meta.py')
        with open(metadata_filepath, 'w') as f:
            f.write(metadata_file_string)


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs_serve(session):
    session.install('mkdocs')
    session.install('mkdocs-material')
    session.install('mkdocs-jupyter')
    session.run('mkdocs', 'serve')


@nox.session(venv_backend=VENV_BACKEND, reuse_venv=True)
def mkdocs(session):
    session.install('mkdocs')
    session.install('mkdocs-material')
    session.install('mkdocs-jupyter')
    session.run('mkdocs', 'build')
