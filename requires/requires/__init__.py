# -*- coding: utf-8 -*-
"""`requires` ~ make modules callable"""
from funkify import funkify
from requires.core import requires, RequirementError, Requirement
from requires._version import VERSION_INFO
from requires._version import VERSION_MAJOR
from requires._version import VERSION_MINOR
from requires._version import VERSION_PATCH
from requires._version import __version__

funkify(requires, name="requires")

__all__ = [
    "requires",
    "RequirementError",
    "Requirement",
    # Version et al
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "VERSION_INFO",
    "__version__",
]
