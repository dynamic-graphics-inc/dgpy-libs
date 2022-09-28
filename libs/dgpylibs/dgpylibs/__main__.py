# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m dgpylibs`"""
import sys

from dgpylibs._meta import __pkgroot__, __title__, __version__

sys.stdout.write(
    f"package: {__title__}\nversion: {__version__}\npkgroot: {__pkgroot__}\n"
)
