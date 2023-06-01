# -*- coding: utf-8 -*-
from typing import Callable

import pytest
import tomli

from dgpydev import DGPY_LIBS
from lager import lager

pytestmark = [pytest.mark.basic]


@pytest.mark.parametrize("dgpy_lib_name", DGPY_LIBS)
class TestDgpyLib:
    def test_pypi_classifiers(
        self,
        dgpy_lib_name: str,
        dgpy_lib_pyproject_toml_string: Callable[[str], str],
    ) -> None:
        pyproject_toml_string = dgpy_lib_pyproject_toml_string(dgpy_lib_name)
        lager.debug("pyproject.toml string", pyproject_toml_string)
        pyproject_toml = tomli.loads(pyproject_toml_string)
        lager.debug("pyproject.toml", pyproject_toml)
        # check that classifiers match in 'tool.poetry.classifiers' and 'project.classifiers'

        poetry_classifiers = pyproject_toml["tool"]["poetry"]["classifiers"]
        project_classifiers = pyproject_toml["project"]["classifiers"]
        assert poetry_classifiers == project_classifiers

        pkg_classifiers = pyproject_toml["project"]["classifiers"]

        assert len(set(pkg_classifiers)) == len(
            pkg_classifiers
        ), "duplicate classifiers"
