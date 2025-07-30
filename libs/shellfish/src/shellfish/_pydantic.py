# -*- coding: utf-8 -*-
"""shelfish._pydantic"""

from pydantic import BaseModel, ConfigDict

__all__ = ("_ShellfishBaseModel", "shellfish_base_model_config")

shellfish_base_model_config: ConfigDict = {
    "extra": "forbid",
    "arbitrary_types_allowed": True,
    "populate_by_name": True,
    "use_enum_values": True,
    "validate_default": True,
}


class _ShellfishBaseModel(BaseModel): ...
