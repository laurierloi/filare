from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class ConnectionEndpointInterfaceModel(FilareInterfaceModel):
    """Endpoint of a connection referring to a connector pin."""

    parent: str = Field(..., description="Connector designator owning this endpoint.")
    pin: Union[str, int] = Field(
        ..., description="Pin identifier (label or number) on the connector."
    )


class ConnectionWireInterfaceModel(FilareInterfaceModel):
    """Reference to a wire within a cable."""

    parent: str = Field(..., description="Cable designator owning this wire.")
    wire: Union[str, int] = Field(
        ..., description="Wire identifier (index or label) within the cable."
    )


class ConnectionInterfaceModel(FilareInterfaceModel):
    """Connection triple tying two connector endpoints through a cable wire."""

    from_: Optional[ConnectionEndpointInterfaceModel] = Field(
        default=None, alias="from", description="Source connector endpoint."
    )
    via: ConnectionWireInterfaceModel = Field(
        ..., description="Cable wire reference carrying the connection."
    )
    to: Optional[ConnectionEndpointInterfaceModel] = Field(
        default=None, description="Target connector endpoint."
    )


class ConnectionConfigurationInterfaceModel(FilareInterfaceModel):
    """Configuration options controlling connection parsing/normalization."""

    # Placeholder for future parsing toggles; keeps a dedicated config object per connection.
    pass
