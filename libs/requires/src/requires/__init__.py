# -*- coding: utf-8 -*-
"""`requires` ~ dependency utils"""

from __future__ import annotations

from requires.__about__ import __version__
from requires.core import (
    Requirement,
    RequirementAttributeError,
    RequirementDict,
    RequirementError,
    RequirementKwargs,
    RequirementProxy,
    RequirementsMeta,
    RequirementWarning,
    preflight_check,
    require,
    requires,
    requires_python,
    scope_requirements,
)

__all__ = (
    "Requirement",
    "RequirementAttributeError",
    "RequirementDict",
    "RequirementError",
    "RequirementKwargs",
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
