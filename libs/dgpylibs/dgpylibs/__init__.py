# -*- coding: utf-8 -*-
"""Dynamic Graphics Python libraries"""
from dataclasses import dataclass

from dgpylibs._meta import __version__

import aiopen
import asyncify
import fmts
import funkify
import h5
import jsonbourne
import lager
import listless
import requires
import shellfish
import xtyping

from aiopen import __version__ as __aiopen_version__
from asyncify import __version__ as __asyncify_version__
from fmts import __version__ as __fmts_version__
from funkify import __version__ as __funkify_version__
from h5 import __version__ as __h5_version__
from jsonbourne import __version__ as __jsonbourne_version__
from lager import __version__ as __lager_version__
from listless import __version__ as __listless_version__
from requires import __version__ as __requires_version__
from shellfish import __version__ as __shellfish_version__
from xtyping import __version__ as __xtyping_version__

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
class DgpyLibMetadata:
    title: str
    description: str
    pkgroot: str
    version: str

    @property
    def __title__(self) -> str:
        return self.title

    @property
    def __description__(self) -> str:
        return self.description

    @property
    def __pkgroot__(self) -> str:
        return self.pkgroot

    @property
    def __version__(self) -> str:
        return self.version


@dataclass(frozen=True)
class DgpyLibsMetadata:
    """dgpy-libs env info"""

    aiopen: DgpyLibMetadata
    asyncify: DgpyLibMetadata
    fmts: DgpyLibMetadata
    funkify: DgpyLibMetadata
    h5: DgpyLibMetadata
    jsonbourne: DgpyLibMetadata
    lager: DgpyLibMetadata
    listless: DgpyLibMetadata
    requires: DgpyLibMetadata
    shellfish: DgpyLibMetadata
    xtyping: DgpyLibMetadata


@dataclass(frozen=True)
class DgpyLibsVersions:
    """dgpy-libs env info"""

    aiopen: str
    asyncify: str
    fmts: str
    funkify: str
    h5: str
    jsonbourne: str
    lager: str
    listless: str
    requires: str
    shellfish: str
    xtyping: str


dgpylibs_metadata = DgpyLibsMetadata(
    aiopen=DgpyLibMetadata(
        title=aiopen._meta.__title__,
        description=aiopen._meta.__description__,
        pkgroot=aiopen._meta.__pkgroot__,
        version=aiopen._meta.__version__,
    ),
    asyncify=DgpyLibMetadata(
        title=asyncify._meta.__title__,
        description=asyncify._meta.__description__,
        pkgroot=asyncify._meta.__pkgroot__,
        version=asyncify._meta.__version__,
    ),
    fmts=DgpyLibMetadata(
        title=fmts._meta.__title__,
        description=fmts._meta.__description__,
        pkgroot=fmts._meta.__pkgroot__,
        version=fmts._meta.__version__,
    ),
    funkify=DgpyLibMetadata(
        title=funkify._meta.__title__,
        description=funkify._meta.__description__,
        pkgroot=funkify._meta.__pkgroot__,
        version=funkify._meta.__version__,
    ),
    h5=DgpyLibMetadata(
        title=h5._meta.__title__,
        description=h5._meta.__description__,
        pkgroot=h5._meta.__pkgroot__,
        version=h5._meta.__version__,
    ),
    jsonbourne=DgpyLibMetadata(
        title=jsonbourne._meta.__title__,
        description=jsonbourne._meta.__description__,
        pkgroot=jsonbourne._meta.__pkgroot__,
        version=jsonbourne._meta.__version__,
    ),
    lager=DgpyLibMetadata(
        title=lager._meta.__title__,
        description=lager._meta.__description__,
        pkgroot=lager._meta.__pkgroot__,
        version=lager._meta.__version__,
    ),
    listless=DgpyLibMetadata(
        title=listless._meta.__title__,
        description=listless._meta.__description__,
        pkgroot=listless._meta.__pkgroot__,
        version=listless._meta.__version__,
    ),
    requires=DgpyLibMetadata(
        title=requires._meta.__title__,
        description=requires._meta.__description__,
        pkgroot=requires._meta.__pkgroot__,
        version=requires._meta.__version__,
    ),
    shellfish=DgpyLibMetadata(
        title=shellfish._meta.__title__,
        description=shellfish._meta.__description__,
        pkgroot=shellfish._meta.__pkgroot__,
        version=shellfish._meta.__version__,
    ),
    xtyping=DgpyLibMetadata(
        title=xtyping._meta.__title__,
        description=xtyping._meta.__description__,
        pkgroot=xtyping._meta.__pkgroot__,
        version=xtyping._meta.__version__,
    ),
)

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
