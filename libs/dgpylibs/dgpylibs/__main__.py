# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m dgpylibs`"""
import sys

from dgpylibs import dgpylibs_metadata
from dgpylibs._meta import __pkgroot__, __title__, __version__

sys.stdout.write(
    f"package: {__title__}\nversion: {__version__}\npkgroot: {__pkgroot__}\n\n"
)


sys.stdout.write(
    "\n\n".join(
        (
            "\n".join(
                f"    {el}"
                for el in (
                    f"package: {v.__title__}",
                    f"version: {v.__version__}",
                    f"pkgroot: {v.__pkgroot__}",
                )
            )
            for v in dgpylibs_metadata.__dict__.values()
        )
    )
)
