# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m h5`"""
import json
import sys

from h5._meta import __pkgroot__, __title__, __version__


def main() -> None:
    sys.stdout.write(
        json.dumps(
            {
                "package": __title__,
                "version": __version__,
                "pkgroot": __pkgroot__,
            }
        )
    )


if __name__ == "__main__":
    main()
