from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class LoopInterfaceModel(FilareInterfaceModel):
    """Loop definition tying two pins together."""

    first: Union[str, int] = Field(
        ..., description="First pin label or number participating in the loop."
    )
    second: Union[str, int] = Field(
        ..., description="Second pin label or number participating in the loop."
    )
    side: Optional[str] = Field(
        None,
        description="Side of the connector where the loop is drawn (LEFT or RIGHT).",
    )
    color: Optional[str] = Field(None, description="Loop color code.")
    show_label: bool = Field(
        default=True, description="Whether to render the loop label."
    )


class ConnectorInterfaceModel(FilareInterfaceModel):
    """Connector definition supplied by users."""

    designator: str = Field(..., description="Connector designator (e.g., J1).")
    type: Optional[str] = Field(
        None, description="Connector type (e.g., D-Sub, Molex)."
    )
    subtype: Optional[str] = Field(
        None, description="Connector subtype (e.g., female, male)."
    )
    pins: List[Union[str, int]] = Field(
        default_factory=list,
        description="Optional explicit pin numbers; if omitted, inferred from pinlabels.",
    )
    pinlabels: List[Union[str, int]] = Field(
        default_factory=list,
        description="Optional pin labels; if omitted, pins will render as numeric indices.",
    )
    pincolors: List[str] = Field(
        default_factory=list,
        description="Optional color codes per pin when rendering connectors.",
    )
    loops: List[LoopInterfaceModel] = Field(
        default_factory=list,
        description="Optional loops between pins for continuity or configuration.",
    )
    style: Optional[str] = Field(
        None, description="Rendering style override (e.g., simple)."
    )


class ConnectorConfigurationInterfaceModel(FilareInterfaceModel):
    """Configuration options controlling connector parsing/normalization."""

    # Placeholder for future parsing toggles; keeps a dedicated config object per connector type.
    pass
