# -*- coding: utf-8 -*-
"""xtyping __all__ lists"""

from __future__ import annotations

import warnings

from xtyping.shed import (
    __all_annotated_types__,
    __all_typing__,
    __all_typing_extensions__,
    __all_typing_extensions_future__,
)

warnings.warn(
    "xtyping._all is deprecated, import from shed",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = (
    "__all_annotated_types__",
    "__all_typing__",
    "__all_typing_extensions__",
    "__all_typing_extensions_future__",
)
