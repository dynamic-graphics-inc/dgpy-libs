from __future__ import annotations

import json

from typing import TYPE_CHECKING

import pytest

from click.testing import CliRunner

from h5 import testing as h5testing
from h5.cli import cli

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_help() -> None:
    """Test help"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert all(
        el in result.output
        for el in (
            "dump",
            "keys",
            "is",
            "tree",
        )
    )


def test_is(tmp_path: Path, runner: CliRunner) -> None:
    """Test keys"""
    filepath = str(tmp_path / "test.h5")
    h5testing.make_test_hdf5_file(filepath)

    result = runner.invoke(cli, ["is", filepath])
    assert result.exit_code == 0


def test_is_not(tmp_path: Path, runner: CliRunner) -> None:
    filepath = str(tmp_path / "test.h5")
    with open(str(filepath), "w") as f:
        f.write("test")
    failing_result = runner.invoke(cli, ["is", filepath])
    assert failing_result.exit_code == 1


def test_keys(tmp_path: Path, runner: CliRunner) -> None:
    """Test keys"""
    filepath = str(tmp_path / "test.h5")

    h5testing.make_test_hdf5_file(filepath)
    result = runner.invoke(cli, ["keys", filepath])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list)
    expected_keys = sorted(
        [
            "/",
            "/a_subgroup",
            "/b_subgroup",
            "/chunked",
            "/filter-gzip",
            "/filter-lzf",
            "/root_dataset",
            "/vanilla",
            "/a_subgroup/a_dataset",
            "/a_subgroup/aa_subsubgroup",
            "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset",
            "/b_subgroup/b_dataset",
        ]
    )
    assert sorted(data) == expected_keys

    ls_result = runner.invoke(cli, ["ls", filepath])
    assert ls_result.exit_code == 0
    list_of_keys = ls_result.output.splitlines()

    assert sorted(list_of_keys) == expected_keys

    ls_json_result = runner.invoke(cli, ["ls", "-j", filepath])
    assert ls_json_result.exit_code == 0
    list_of_keys_json_array = json.loads(ls_json_result.output)

    assert sorted(list_of_keys_json_array) == expected_keys
