# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m h5`"""
import sys

from h5._meta import __pkgroot__, __title__, __version__


def main() -> None:
    sys.stdout.write(
        f"package: {__title__}\nversion: {__version__}\npkgroot: {__pkgroot__}\n"
    )


if __name__ == "__main__":
    main()
