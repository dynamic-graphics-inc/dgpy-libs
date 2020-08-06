# -*- coding: utf-8 -*-
"""Json Bourne types"""
import sys

from typing import Any, Dict, List


if sys.version_info < (3, 7):
    from collections.abc import MutableMapping

    _JsonDictMutableMapping = MutableMapping
else:
    from typing import MutableMapping

    _JsonDictMutableMapping = MutableMapping[str, Any]

__all__ = [
    "JsonDictT",
    "JsonListT",
    "JsonArrT",
    "JsonObjT",
]

# Json friendly: Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
JsonDictT = Dict[str, Any]
JsonObjT = Dict[str, Any]
JsonListT = List[Any]
JsonArrT = List[Any]
