from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class CableInterfaceModel(FilareInterfaceModel):
    """Cable definition supplied by users."""

    designator: str = Field(..., description="Cable designator (e.g., W1).")
    wirecount: int = Field(..., description="Number of wires contained in the cable.")
    colors: List[str] = Field(
        default_factory=list, description="Optional list of wire color codes."
    )
    length: Optional[str] = Field(
        None, description="Cable length with units (e.g., '1 m')."
    )
    gauge: Optional[str] = Field(
        None, description="Wire gauge with units (e.g., '0.25 mm2')."
    )
    shield: bool = Field(
        default=False, description="Whether the cable includes shielding."
    )
    type: Optional[str] = Field(None, description="Cable type or family (e.g., CAT5e).")


class CableConfigurationInterfaceModel(FilareInterfaceModel):
    """Configuration options controlling cable parsing/normalization."""

    # Placeholder for future parsing toggles; keeps a dedicated config object per cable type.
    pass
