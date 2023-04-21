# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m listless`"""
import sys

from listless.__about__ import __pkgroot__, __title__, __version__


def main() -> None:
    import json

    sys.stdout.write(
        json.dumps(
            {"package": __title__, "version": __version__, "pkgroot": __pkgroot__},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
