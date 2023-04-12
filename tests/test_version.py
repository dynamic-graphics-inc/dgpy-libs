# -*- coding: utf-8 -*-
from typing import Callable

import pytest
import tomli

import dgpylibs

from dgpydev import DGPY_LIBS
from lager import lager

pytestmark = [pytest.mark.basic]


@pytest.mark.parametrize("dgpy_lib_name", DGPY_LIBS)
class TestDgpyLib:
    def test_version(
        self,
        dgpy_lib_name: str,
        dgpy_lib_dirpath: Callable[[str], str],
        dgpy_lib_pyproject_toml_string: Callable[[str], str],
    ) -> None:
        if dgpy_lib_name == "dgpytest" and not hasattr(dgpylibs, "dgpytest"):
            pytest.skip('not yet part of dgpylibs')
        lager.info(f"Testing version for {dgpy_lib_name}")
        dgpylibs_metadata = dgpylibs.dgpylibs_metadata
        lib_metadata: dgpylibs.DgpyLibMetadata = getattr(
            dgpylibs_metadata, dgpy_lib_name
        )

        pyproject_toml_string = dgpy_lib_pyproject_toml_string(dgpy_lib_name)
        lager.debug("pyproject.toml string", pyproject_toml_string)
        pyproject_toml = tomli.loads(pyproject_toml_string)
        lager.debug("pyproject.toml", pyproject_toml)

        assert "tool" in pyproject_toml
        assert "poetry" in pyproject_toml["tool"]
        assert "version" in pyproject_toml["tool"]["poetry"]

        assert pyproject_toml["tool"]["poetry"]["version"] == lib_metadata.version

        lager.info("lib metadata", lib_metadata)
