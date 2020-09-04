# -*- coding: utf-8 -*-
"""`requires` ~ make modules callable"""
from funkify import funkify
from requires._version import (
    VERSION_INFO,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    __version__,
)
from requires.core import Requirement, RequirementError, require, requires


funkify(requires, name="requires")

__all__ = [
    "requires",
    "require",
    "RequirementError",
    "Requirement",
    # Version et al
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
