# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m dgpytest`"""

from __future__ import annotations

import sys

from dgpytest.__about__ import __pkgroot__, __title__, __version__


def main() -> None:
    """Print package metadata"""
    import json

    sys.stdout.write(
        json.dumps(
            {
                "package": __title__,
                "version": __version__,
                "pkgroot": __pkgroot__,
            },
            indent=2,
        )
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
