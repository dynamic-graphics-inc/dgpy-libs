# -*- coding: utf-8 -*-
"""shelfish._pydantic"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

__all__ = ("_ShellfishBaseModel", "shellfish_base_model_config")

shellfish_base_model_config: ConfigDict = {
    "extra": "forbid",
}


class _ShellfishBaseModel(BaseModel):
    """Pydantic shellfish base model"""

    model_config = shellfish_base_model_config

    def __json_interface__(self) -> dict[str, Any]:
        """Return the JSON interface for this model."""
        return self.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude_defaults=True,
        )
