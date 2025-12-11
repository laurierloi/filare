from __future__ import annotations

import json
from typing import Any, Dict

import yaml
from pydantic import BaseModel, ConfigDict, Field


class FilareInterfaceModel(BaseModel):
    """Base class for all user-facing interface models."""

    schema_version: str = Field(
        default="1.0",
        description="Semantic version of the interface model schema this instance follows.",
    )

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        """Return the JSON Schema representation for this interface model."""
        return cls.model_json_schema()

    def to_yaml(self) -> str:
        """Serialize the model to YAML using its JSON-compatible representation."""
        return yaml.safe_dump(json.loads(self.model_dump_json()), sort_keys=False)
