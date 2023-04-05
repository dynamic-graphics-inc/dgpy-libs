# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m h5`"""
import json
import sys

from h5._meta import __pkgroot__, __title__, __version__

try:
    from click import __version__ as __click_version__
except ImportError:
    __click_version__ = None


def _pkg_info() -> None:
    import numpy as np

    from h5py import __version__ as __h5py_version__

    sys.stdout.write(
        json.dumps(
            {
                "package": __title__,
                "version": __version__,
                "pkgroot": __pkgroot__,
                "h5py_version": __h5py_version__,
                "numpy_version": np.__version__,
                "click_version": __click_version__,
            }
        )
    )


def main() -> None:
    _pkg_info()


if __name__ == "__main__":
    main()
