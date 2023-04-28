import requires.shed as requires_shed


def test_shed_exports():
    shed_requirements = [el for el in dir(requires_shed) if el.startswith("requires_")]
    requires_shed_all_set = set(requires_shed.__all__)
    missing_from_all = [
        el for el in shed_requirements if el not in requires_shed_all_set
    ]
    if missing_from_all:
        raise AssertionError(f"MISSING from __all__: {str(tuple(missing_from_all))}")


def test_all_sorted():
    expected = tuple(sorted(set(requires_shed.__all__)))
    assert requires_shed.__all__ == tuple(
        sorted(set(requires_shed.__all__))
    ), f"__all__ should be sorted -- __all__ = {expected}"
