"""Shared models for additional components/BOM entries."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Quantity(BaseModel):
    """Quantity value with optional unit."""

    number: int = Field(..., description="Quantity number for the component.")
    unit: Optional[str] = Field(default=None, description="Optional quantity unit.")

    model_config = ConfigDict(extra="forbid")


class BomEntry(BaseModel):
    """BOM-style entry for an additional component."""

    qty: Quantity
    description: str = Field(..., description="Description of the additional component.")
    id: Optional[str] = Field(default=None, description="Optional component identifier.")

    model_config = ConfigDict(extra="forbid")


class AdditionalComponent(BaseModel):
    """Wrapper for additional BOM entries."""

    bom_entry: BomEntry

    model_config = ConfigDict(extra="forbid")
