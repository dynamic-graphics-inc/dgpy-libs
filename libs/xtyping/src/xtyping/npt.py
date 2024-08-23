# -*- coding: utf-8 -*-
"""import numpy.typing as npt"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    import numpy.typing as npt

    ArrayLike: TypeAlias = npt.ArrayLike
    DTypeLike: TypeAlias = npt.DTypeLike
    NBitBase: TypeAlias = npt.NBitBase
    NDArray: TypeAlias = npt.NDArray
else:
    ArrayLike = Any
    DTypeLike = np.dtype
    NBitBase = Any
    NDArray = np.ndarray

__all__ = ("ArrayLike", "DTypeLike", "NBitBase", "NDArray")
