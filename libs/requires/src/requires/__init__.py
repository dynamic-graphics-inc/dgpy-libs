# -*- coding: utf-8 -*-
"""`requires` ~ dependency utils"""

from __future__ import annotations

from funkify import funkify
from requires.__about__ import __version__
from requires.core import (
    Requirement,
    RequirementAttributeError,
    RequirementDict,
    RequirementError,
    RequirementProxy,
    RequirementsMeta,
    RequirementWarning,
    preflight_check,
    require,
    requires,
    requires_python,
    scope_requirements,
)

funkify(requires, key="requires")

__all__ = (
    "Requirement",
    "RequirementAttributeError",
    "RequirementDict",
    "RequirementError",
    "RequirementProxy",
    "RequirementWarning",
    "RequirementsMeta",
    "__version__",
    "preflight_check",
    "require",
    "requires",
    "requires_python",
    "scope_requirements",
)
