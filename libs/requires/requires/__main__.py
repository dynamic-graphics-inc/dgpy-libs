# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m requires`"""
import sys

from requires._meta import __pkgroot__, __title__, __version__

sys.stdout.write(
    f"package: {__title__}\nversion: {__version__}\npkgroot: {__pkgroot__}\n"
)
