import pytest

import requires

from .fixtures.frobulizer import frobulize, frobulize_multiple_requirements


def test_preflight_check_warns():
    with pytest.warns(requires.RequirementWarning):
        _res = requires.preflight_check(warn=True)


def test_preflight_check():
    reqsmeta = requires.preflight_check()
    assert isinstance(reqsmeta, requires.RequirementsMeta)


def test_frobulize_errs():
    with pytest.raises(requires.RequirementError):
        frobulize(["a", "b", "c"])
    with pytest.raises(requires.RequirementError):
        frobulize_multiple_requirements(["a", "b", "c"])
