# -*- coding: utf-8 -*-
"""Dynamic Graphics Python libraries"""
from dataclasses import dataclass
from typing import TypedDict, TypeVar

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
from dgpylibs.__about__ import __version__, __version__ as __dgpylibs_version__
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
    "__dgpylibs_version__",
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

T = TypeVar("T")


class DgpyLibMetadataDict(TypedDict):
    title: str
    description: str
    pkgroot: str
    version: str


class DgpyLibsMetadataDict(TypedDict):
    dgpylibs: DgpyLibMetadataDict
    aiopen: DgpyLibMetadataDict
    asyncify: DgpyLibMetadataDict
    fmts: DgpyLibMetadataDict
    funkify: DgpyLibMetadataDict
    h5: DgpyLibMetadataDict
    jsonbourne: DgpyLibMetadataDict
    lager: DgpyLibMetadataDict
    listless: DgpyLibMetadataDict
    requires: DgpyLibMetadataDict
    shellfish: DgpyLibMetadataDict
    xtyping: DgpyLibMetadataDict


@dataclass(frozen=True)
class DgpyLibMetadata:
    __slots__ = ("title", "description", "pkgroot", "version")
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

    def asdict(self) -> DgpyLibMetadataDict:
        return {
            "title": self.title,
            "description": self.description,
            "pkgroot": self.pkgroot,
            "version": self.version,
        }


@dataclass(frozen=True)
class DgpyLibsMetadata:
    """dgpy-libs env info"""

    __slots__ = (
        "dgpylibs",
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

    dgpylibs: DgpyLibMetadata
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

    def asdict(self) -> DgpyLibsMetadataDict:
        return {
            "dgpylibs": self.dgpylibs.asdict(),
            "aiopen": self.aiopen.asdict(),
            "asyncify": self.asyncify.asdict(),
            "fmts": self.fmts.asdict(),
            "funkify": self.funkify.asdict(),
            "h5": self.h5.asdict(),
            "jsonbourne": self.jsonbourne.asdict(),
            "lager": self.lager.asdict(),
            "listless": self.listless.asdict(),
            "requires": self.requires.asdict(),
            "shellfish": self.shellfish.asdict(),
            "xtyping": self.xtyping.asdict(),
        }


class DgpyLibsVersionsDict(TypedDict):
    dgpylibs: str
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


@dataclass(frozen=True)
class DgpyLibsVersions:
    """dgpy-libs env info"""

    __slots__ = (
        "dgpylibs",
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

    dgpylibs: str
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

    def asdict(self) -> DgpyLibsVersionsDict:
        return {
            "dgpylibs": self.dgpylibs,
            "aiopen": self.aiopen,
            "asyncify": self.asyncify,
            "fmts": self.fmts,
            "funkify": self.funkify,
            "h5": self.h5,
            "jsonbourne": self.jsonbourne,
            "lager": self.lager,
            "listless": self.listless,
            "requires": self.requires,
            "shellfish": self.shellfish,
            "xtyping": self.xtyping,
        }


dgpylibs__about__data = DgpyLibsMetadata(
    dgpylibs=DgpyLibMetadata(
        title=__about__.__title__,
        description=__about__.__description__,
        pkgroot=__about__.__pkgroot__,
        version=__about__.__version__,
    ),
    aiopen=DgpyLibMetadata(
        title=aiopen.__about__.__title__,
        description=aiopen.__about__.__description__,
        pkgroot=aiopen.__about__.__pkgroot__,
        version=aiopen.__about__.__version__,
    ),
    asyncify=DgpyLibMetadata(
        title=asyncify.__about__.__title__,
        description=asyncify.__about__.__description__,
        pkgroot=asyncify.__about__.__pkgroot__,
        version=asyncify.__about__.__version__,
    ),
    fmts=DgpyLibMetadata(
        title=fmts.__about__.__title__,
        description=fmts.__about__.__description__,
        pkgroot=fmts.__about__.__pkgroot__,
        version=fmts.__about__.__version__,
    ),
    funkify=DgpyLibMetadata(
        title=funkify.__about__.__title__,
        description=funkify.__about__.__description__,
        pkgroot=funkify.__about__.__pkgroot__,
        version=funkify.__about__.__version__,
    ),
    h5=DgpyLibMetadata(
        title=h5.__about__.__title__,
        description=h5.__about__.__description__,
        pkgroot=h5.__about__.__pkgroot__,
        version=h5.__about__.__version__,
    ),
    jsonbourne=DgpyLibMetadata(
        title=jsonbourne.__about__.__title__,
        description=jsonbourne.__about__.__description__,
        pkgroot=jsonbourne.__about__.__pkgroot__,
        version=jsonbourne.__about__.__version__,
    ),
    lager=DgpyLibMetadata(
        title=lager.__about__.__title__,
        description=lager.__about__.__description__,
        pkgroot=lager.__about__.__pkgroot__,
        version=lager.__about__.__version__,
    ),
    listless=DgpyLibMetadata(
        title=listless.__about__.__title__,
        description=listless.__about__.__description__,
        pkgroot=listless.__about__.__pkgroot__,
        version=listless.__about__.__version__,
    ),
    requires=DgpyLibMetadata(
        title=requires.__about__.__title__,
        description=requires.__about__.__description__,
        pkgroot=requires.__about__.__pkgroot__,
        version=requires.__about__.__version__,
    ),
    shellfish=DgpyLibMetadata(
        title=shellfish.__about__.__title__,
        description=shellfish.__about__.__description__,
        pkgroot=shellfish.__about__.__pkgroot__,
        version=shellfish.__about__.__version__,
    ),
    xtyping=DgpyLibMetadata(
        title=xtyping.__about__.__title__,
        description=xtyping.__about__.__description__,
        pkgroot=xtyping.__about__.__pkgroot__,
        version=xtyping.__about__.__version__,
    ),
)

dgpylibs_info = DgpyLibsVersions(
    dgpylibs=__version__,
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
