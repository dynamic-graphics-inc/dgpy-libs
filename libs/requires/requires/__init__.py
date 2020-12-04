# -*- coding: utf-8 -*-
"""`requires` ~ make modules callable"""
from funkify import funkify
from requires._meta import __version__
from requires.core import Requirement, RequirementError, require, requires


funkify(requires, name="requires")

__all__ = [
    "__version__",
    "requires",
    "require",
    "RequirementError",
    "Requirement",
]
