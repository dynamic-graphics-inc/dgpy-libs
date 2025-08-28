from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from h5.testing import h5py_test_files

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(params=h5py_test_files())
def h5py_test_file(request: pytest.FixtureRequest) -> Path:
    return cast("Path", request.param)
