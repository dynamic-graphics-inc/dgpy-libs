from _pytest.config import Config
from _pytest.mark import Mark


def pytest_dgpy_set_mark(mark: Mark, config: Config) -> None:  # pragma: no cover
    """Called before set mark

    Args:
        mark: pytest mark
        config: Base pytest config

    """


def pytest_dgpy_item_mark(item: Mark, config: Config) -> None:  # pragma: no cover
    """Called after set mark

    Args:
        item: pytest item
        config: Base pytest config

    """
