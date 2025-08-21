# -*- coding: utf-8 -*-
import json

from collections.abc import Callable

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
        dgpy_lib_pyproject_toml_string: Callable[[str], str],
    ) -> None:
        pyproject_toml_string = dgpy_lib_pyproject_toml_string(dgpy_lib_name)
        pyproject_toml = tomli.loads(pyproject_toml_string)
        assert "requires-python" in pyproject_toml["project"], (
            "requires-python not found in project section of pyproject.toml"
        )

    def test_run_module_json_output(
        self,
        dgpy_lib_name: str,
    ) -> None:
        from subprocess import run

        res = run(
            ["python", "-m", dgpy_lib_name],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 0

        # assert stdout is json
        output_json = json.loads(res.stdout)
        assert isinstance(output_json, dict)

        if dgpy_lib_name == "dgpylibs":  # dgpylibs is an arr
            assert "version" in output_json["dgpylibs"]
            # possibly fix and get in line?
            assert "title" in output_json["dgpylibs"]
            assert "pkgroot" in output_json["dgpylibs"]
        else:
            assert "version" in output_json
            assert "package" in output_json
            assert "pkgroot" in output_json

        assert res.stdout.endswith("}\n")
