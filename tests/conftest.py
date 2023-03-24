from os import path
from typing import Callable

import pytest

PWD = path.split(path.abspath(__file__))[0]
REPO_ROOT = path.split(PWD)[0]


@pytest.fixture
def dgpy_libs_repo_root() -> str:
    return REPO_ROOT


@pytest.fixture
def dgpy_libs_dirpath() -> str:
    return path.join(REPO_ROOT, "libs")


@pytest.fixture
def dgpy_lib_dirpath(dgpy_libs_dirpath) -> Callable[[str], str]:
    return lambda libname: path.join(dgpy_libs_dirpath, libname)


@pytest.fixture
def dgpy_lib_pyproject_toml_string(dgpy_lib_dirpath) -> Callable[[str], str]:
    def _get_pyproject_toml_string(libname: str) -> str:
        pyproject_toml_filepath = path.join(dgpy_lib_dirpath(libname), "pyproject.toml")
        with open(pyproject_toml_filepath) as f:
            return f.read()

    return _get_pyproject_toml_string
