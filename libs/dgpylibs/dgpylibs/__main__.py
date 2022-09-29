# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m dgpylibs`"""
import sys

from dgpylibs._meta import __pkgroot__, __title__, __version__

sys.stdout.write(
    f"package: {__title__}\nversion: {__version__}\npkgroot: {__pkgroot__}\n"
)

from aiopen import __version__ as __aiopen_metadata__
from asyncify import __version__ as __asyncify_metadata__
from fmts import __version__ as __fmts_metadata__
from funkify import __version__ as __funkify_metadata__
from h5 import __version__ as __h5_metadata__
from jsonbourne import __version__ as __jsonbourne_metadata__
from lager import __version__ as __lager_metadata__
from listless import __version__ as __listless_metadata__
from requires import __version__ as __requires_metadata__
from shellfish import __version__ as __shellfish_metadata__
from xtyping import __version__ as __xtyping_metadata__
