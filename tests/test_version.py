# -*- coding: utf-8 -*-
from typing import Callable

import pytest
import tomli

from rich import print

import dgpylibs

from dgpydev import DGPY_LIBS
from lager import lager

pytestmark = [pytest.mark.basic]


@pytest.mark.parametrize("dgpy_lib_name", DGPY_LIBS)
class TestDgpyLib:
    def test_version(
        self,
        dgpy_lib_name: str,
        dgpy_lib_pyproject_toml_string: Callable[[str], str],
    ) -> None:
        if dgpy_lib_name == "dgpytest" and not hasattr(dgpylibs, "dgpytest"):
            pytest.skip("dgpytest not yet part of dgpylibs")
        lager.info(f"Testing version for {dgpy_lib_name}")
        dgpylibs_metadata = dgpylibs.dgpylibs_metadata
        lib_metadata: dgpylibs.DgpyLibMetadata = getattr(
            dgpylibs_metadata, dgpy_lib_name
        )

        pyproject_toml_string = dgpy_lib_pyproject_toml_string(dgpy_lib_name)
        lager.debug("pyproject.toml string", pyproject_toml_string)
        pyproject_toml = tomli.loads(pyproject_toml_string)
        lager.debug("pyproject.toml", pyproject_toml)

        assert "project" in pyproject_toml
        assert "tool" in pyproject_toml
        assert "version" in pyproject_toml["project"]
        assert pyproject_toml["project"]["version"] == lib_metadata.version

        lager.info("lib metadata", lib_metadata)

    def test_project_has_requires_python_version(
        self,
        dgpy_lib_name: str,
        dgpy_lib_dirpath: Callable[[str], str],
        dgpy_lib_pyproject_toml_string: Callable[[str], str],
    ) -> None:
        pyproject_toml_string = dgpy_lib_pyproject_toml_string(dgpy_lib_name)
        pyproject_toml = tomli.loads(pyproject_toml_string)
        assert "requires-python" in pyproject_toml["project"], (
            "requires-python not found in project section of pyproject.toml"
        )

        print(pyproject_toml["project"])
