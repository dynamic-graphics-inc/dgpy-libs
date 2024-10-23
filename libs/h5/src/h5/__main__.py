# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m h5`"""

from __future__ import annotations

import json
import sys

from typing import Optional

from h5.__about__ import __pkgroot__, __title__, __version__

__click_version__: Optional[str] = None
try:
    from click import __version__ as __click_version__
except ImportError:
    ...


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


def _h5_cli() -> None:
    from h5.cli import main as h5_cli

    h5_cli()


def main(h5cli: bool = True) -> None:
    if not h5cli or __click_version__ is None or sys.argv[-1].endswith("__main__.py"):
        _pkg_info()
    else:
        _h5_cli()


if __name__ == "__main__":
    main()
