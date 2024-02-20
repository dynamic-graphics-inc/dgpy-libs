# -*- coding: utf-8 -*-
"""`requires` ~ dependency utils"""
from __future__ import annotations

from funkify import funkify
from requires.__about__ import __version__
from requires.core import (
    Requirement,
    RequirementAttributeError,
    RequirementError,
    RequirementProxy,
    require,
    requires,
)

funkify(requires, key="requires")

__all__ = (
    "Requirement",
    "RequirementAttributeError",
    "RequirementError",
    "RequirementProxy",
    "__version__",
    "require",
    "requires",
)
