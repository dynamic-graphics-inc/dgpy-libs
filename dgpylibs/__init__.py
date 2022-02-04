# -*- coding: utf-8 -*-
"""Dynamic Graphics Python libraries"""

from fmts import __version__ as __fmts_version__

from aiopen import __version__ as __aiopen_version__
from asyncify import __version__ as __asyncify_version__
from dgpylibs._meta import __version__
from funkify import __version__ as __funkify_version__
from h5 import __version__ as __h5_version__
from jsonbourne import __version__ as __jsonbourne_version__
from lager import __version__ as __lager_version__
from listless import __version__ as __listless_version__
from requires import __version__ as __requires_version__
from shellfish import __version__ as __shellfish_version__
from xtyping import __version__ as __xtyping_version__

try:
    from jsonbourne.trydantic import dataclass
except ImportError:
    from dataclasses import dataclass

__all__ = (
    "__version__",
    "__aiopen_version__",
    "__asyncify_version__",
    "__fmts_version__",
    "__funkify_version__",
    "__h5_version__",
    "__jsonbourne_version__",
    "__lager_version__",
    "__listless_version__",
    "__shellfish_version__",
    "__requires_version__",
    "__xtyping_version__",
)

LIBS = (
    "aiopen",
    "asyncify",
    "fmts",
    "funkify",
    "h5",
    "jsonbourne",
    "lager",
    "listless",
    "requires",
    "shellfish",
    "xtyping",
)


@dataclass(frozen=True)
class DgpyLibsVersions:
    """dgpy-libs env info"""

    aiopen: str = None
    asyncify: str = None
    fmts: str = None
    funkify: str = None
    h5: str = None
    jsonbourne: str = None
    lager: str = None
    listless: str = None
    requires: str = None
    shellfish: str = None
    xtyping: str = None


dgpylibs_info = DgpyLibsVersions(
    aiopen=__aiopen_version__,
    asyncify=__asyncify_version__,
    fmts=__fmts_version__,
    funkify=__funkify_version__,
    h5=__h5_version__,
    jsonbourne=__jsonbourne_version__,
    lager=__lager_version__,
    listless=__listless_version__,
    requires=__requires_version__,
    shellfish=__shellfish_version__,
    xtyping=__xtyping_version__,
)
